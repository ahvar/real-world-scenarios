"""
boto3 RWC Skeleton: GitHub -> Transform -> S3 (mocked) -> Summary report

Why this is interview-friendly:
- Uses boto3 in a realistic ETL flow (list/upload/download)
- Does NOT require AWS credentials (moto mocks S3 locally)
- Leaves room for you to extend: pagination, retries, concurrency, richer transforms

How to run (local):
1) pip install boto3 moto requests
2) python rwc_boto3_s3_pipeline.py

Optional extensions:
- Add asyncio/thread pool for GitHub fetch step
- Add structured logging + metrics counters
- Add unit tests (pytest) around transform & S3 IO

How to extend this into Apex-relevant practice (quick ideas)

Add a queue step (simulated SQS):
put “repo keys” into an in-memory queue; worker consumes and processes → mirrors event-driven ETL.

Add concurrency to fetch:
fetch multiple orgs/users in parallel using ThreadPoolExecutor (I/O-bound) and compare timings.

Add reliability hooks:
retries with exponential backoff around GitHub calls; idempotency
(don’t re-upload if already present); DLQ simulation.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import boto3
import requests
from botocore.exceptions import ClientError
from moto import mock_s3


# -------------------------
# Config / Data Models
# -------------------------


@dataclass(frozen=True)
class PipelineConfig:
    bucket_name: str = "rwc-boto3-bucket"
    raw_prefix: str = "raw/github"
    processed_prefix: str = "processed"
    region: str = "us-east-1"
    github_timeout_s: float = 10.0
    user_agent: str = "rwc-boto3-skeleton/1.0"


@dataclass(frozen=True)
class RepoRecord:
    full_name: str
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    language: Optional[str]


# -------------------------
# GitHub Fetch (sync)
# -------------------------


def fetch_github_repos(org: str, cfg: PipelineConfig) -> List[Dict[str, Any]]:
    """
    Fetch repos for an org using GitHub's REST API.
    Keep it simple for interview settings; later you can add pagination.
    """
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {"User-Agent": cfg.user_agent}
    resp = requests.get(url, headers=headers, timeout=cfg.github_timeout_s)
    resp.raise_for_status()
    data = resp.json()

    if not isinstance(data, list):
        raise ValueError("Unexpected GitHub response shape (expected list).")

    return data


# -------------------------
# Transform
# -------------------------


def transform_repos(raw_repos: List[Dict[str, Any]]) -> List[RepoRecord]:
    """
    Extract a small, stable subset of fields and produce typed records.
    This is where you'd do validation, normalization, filtering, etc.
    """
    records: List[RepoRecord] = []
    for repo in raw_repos:
        # Defensive access - interviews love this kind of robustness
        full_name = str(repo.get("full_name", ""))
        if not full_name:
            continue

        records.append(
            RepoRecord(
                full_name=full_name,
                stargazers_count=int(repo.get("stargazers_count") or 0),
                forks_count=int(repo.get("forks_count") or 0),
                open_issues_count=int(repo.get("open_issues_count") or 0),
                language=repo.get("language"),
            )
        )
    return records


def summarize(records: List[RepoRecord]) -> Dict[str, Any]:
    """
    Produce a compact summary artifact (good interview deliverable).
    """
    by_language: Dict[str, int] = {}
    for r in records:
        lang = r.language or "Unknown"
        by_language[lang] = by_language.get(lang, 0) + 1

    top_by_stars = sorted(records, key=lambda r: r.stargazers_count, reverse=True)[:10]

    return {
        "repo_count": len(records),
        "languages": dict(
            sorted(by_language.items(), key=lambda kv: kv[1], reverse=True)
        ),
        "top_10_by_stars": [
            {"repo": r.full_name, "stars": r.stargazers_count, "forks": r.forks_count}
            for r in top_by_stars
        ],
        "generated_at_epoch": int(time.time()),
    }


# -------------------------
# S3 Helpers (boto3)
# -------------------------


def create_s3_client(cfg: PipelineConfig):
    return boto3.client("s3", region_name=cfg.region)


def ensure_bucket(s3, bucket_name: str, region: str) -> None:
    """
    Create bucket if missing. Region rules differ in real AWS.
    moto is forgiving, but we keep the structure realistic.
    """
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        # In real AWS, us-east-1 creation has special behavior; keep simple here.
        s3.create_bucket(Bucket=bucket_name)


def s3_put_json(s3, bucket: str, key: str, payload: Any) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")


def s3_get_json(s3, bucket: str, key: str) -> Any:
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw = obj["Body"].read().decode("utf-8")
    return json.loads(raw)


def s3_list_keys(s3, bucket: str, prefix: str) -> List[str]:
    """
    Demonstrates listing + pagination pattern.
    moto supports it; real S3 requires handling continuation tokens.
    """
    keys: List[str] = []
    continuation_token: Optional[str] = None

    while True:
        kwargs = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": 1000}
        if continuation_token:
            kwargs["ContinuationToken"] = continuation_token

        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get("Contents", [])
        keys.extend([c["Key"] for c in contents])

        if resp.get("IsTruncated"):
            continuation_token = resp.get("NextContinuationToken")
        else:
            break

    return keys


# -------------------------
# Pipeline Orchestration
# -------------------------


def build_s3_keys(org: str, cfg: PipelineConfig) -> Tuple[str, str]:
    raw_key = f"{cfg.raw_prefix}/{org}/repos.json"
    processed_key = f"{cfg.processed_prefix}/{org}/summary.json"
    return raw_key, processed_key


def run_pipeline(org: str, cfg: PipelineConfig) -> Dict[str, Any]:
    """
    End-to-end:
    - fetch GitHub repos (extract)
    - store raw in S3
    - transform to typed records
    - summarize + store summary in S3
    - return summary (handy for interview)
    """
    s3 = create_s3_client(cfg)
    ensure_bucket(s3, cfg.bucket_name, cfg.region)

    raw_key, processed_key = build_s3_keys(org, cfg)

    raw_repos = fetch_github_repos(org, cfg)
    s3_put_json(s3, cfg.bucket_name, raw_key, raw_repos)

    records = transform_repos(raw_repos)
    summary = summarize(records)
    s3_put_json(s3, cfg.bucket_name, processed_key, summary)

    # Example of reading back (verifies correctness)
    roundtrip_summary = s3_get_json(s3, cfg.bucket_name, processed_key)
    return roundtrip_summary


# -------------------------
# Demo Runner (mocked AWS)
# -------------------------


@mock_s3
def main() -> None:
    cfg = PipelineConfig()

    # Pick any org; keep in mind GitHub rate limits for unauthenticated requests.
    org = "pallets"  # e.g., Flask org. Replace with "ahvar" for user repos via different endpoint.
    summary = run_pipeline(org, cfg)

    # Show what got written
    s3 = create_s3_client(cfg)
    print("\nS3 Keys Written:")
    for k in s3_list_keys(s3, cfg.bucket_name, prefix=""):
        print(" -", k)

    print("\nSummary Artifact:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
