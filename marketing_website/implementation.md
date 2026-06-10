# Marketing Lead Intake + CRM Sync Service

## Purpose

Build a Flask backend service that simulates the kind of backend integration work expected in a marketing operations / SaaS web-platform role.

The service receives customer-facing marketing form submissions, normalizes and validates the payload, stores the submission, queues background sync work, and syncs the lead to mock Marketo and Salesforce APIs.

Start with a simple in-memory implementation suitable for a 45-minute live-coding interview. Then extend it toward more production-like patterns: idempotency, retries, dead-letter handling, HTTP integrations, Redis Queue, SQLAlchemy/PostgreSQL, S3 metadata storage, SQS, and an optional React dashboard.

---

## Why this challenge is relevant

This challenge is designed around backend work commonly associated with marketing operations platforms:

- Customer-facing website APIs
- Marketing form submission handling
- Data normalization and validation
- CRM / marketing automation integrations
- Marketo- and Salesforce-style sync behavior
- Reliable asynchronous workflows
- Idempotency and duplicate prevention
- Third-party API retry and error handling
- SQL querying and database schema evolution
- AWS-flavored backend services such as S3, SQS, Lambda, IAM, and Secrets Manager

It also mirrors likely interview signals from the assessment:

- SQL query writing
- Python string parsing / camelCase conversion
- JavaScript or AWS SDK-style S3 metadata retrieval
- Web security basics
- Lambda scaling concepts
- Git rebase/history concepts
- Backend API design
- Possible LRU cache or small practical coding exercise

---

## Target implementation path

Implement the project in stages.

| Stage | Goal | Interview relevance |
|---|---|---|
| 1 | Flask API with in-memory store and queue | Highest |
| 2 | Validation and normalization | Highest |
| 3 | Process queued sync jobs | Highest |
| 4 | Mock Marketo/Salesforce HTTP APIs | High |
| 5 | Idempotency and LRU cache | High |
| 6 | Retry and dead-letter behavior | High |
| 7 | SQLAlchemy/PostgreSQL | High |
| 8 | Redis Queue | Medium-high |
| 9 | S3 raw payload + metadata | Medium-high |
| 10 | SQS/Lambda worker | Medium-high |
| 11 | React dashboard | Optional |

The first 6 stages are the most useful for a 45-minute technical interview.

---

## Core prompt

Build a Flask backend service for a marketing website.

The website receives `request a demo` form submissions. Your service should validate and normalize each submission, enrich it with campaign metadata, store it, and queue a background sync to two external systems: a fake Marketo API and a fake Salesforce API.

Start with in-memory storage and an in-memory queue. Add more realistic persistence and cloud services only after the local version works.

---

## Example input

```json
{
  "First Name": " Ana ",
  "last-name": "Velasquez",
  "Email": "ANA.VELASQUEZ+demo@Example.com",
  "Company": "Acme Law Group",
  "form_id": "demo_request",
  "utm_source": "google",
  "utm_medium": "paid_search",
  "utm_campaign": "lawpay-demo-2026",
  "consent": true
}
```

## Example normalized output

```json
{
  "firstName": "Ana",
  "lastName": "Velasquez",
  "email": "ana.velasquez+demo@example.com",
  "company": "Acme Law Group",
  "formId": "demo_request",
  "utmSource": "google",
  "utmMedium": "paid_search",
  "utmCampaign": "lawpay-demo-2026",
  "consent": true
}
```

---

# Milestone 1: Live-coding essentials

This is the version to practice first.

## Requirements

Implement a Flask API with these endpoints:

### `POST /api/submissions`

Accept a marketing form submission.

Required behavior:

1. Validate required fields:
   - first name
   - last name
   - email
   - company
   - form ID
   - consent must be `true`

2. Normalize:
   - trim whitespace
   - convert field names to camelCase
   - lowercase email
   - preserve UTM fields

3. Generate:
   - `submissionId`
   - `createdAt`
   - initial `status = "queued"`

4. Store the submission in memory.
5. Add a job to an in-memory queue.
6. Return `201 Created`.

Example response:

```json
{
  "submissionId": "sub_123",
  "status": "queued",
  "message": "Submission accepted"
}
```

---

### `GET /api/submissions/<submission_id>`

Return the stored submission and current sync status.

Example response:

```json
{
  "submissionId": "sub_123",
  "status": "queued",
  "submission": {
    "firstName": "Ana",
    "lastName": "Velasquez",
    "email": "ana.velasquez+demo@example.com",
    "company": "Acme Law Group",
    "formId": "demo_request",
    "utmCampaign": "lawpay-demo-2026",
    "consent": true
  }
}
```

---

### `GET /api/submissions`

Return all submissions.

Support optional status filtering:

```http
GET /api/submissions?status=failed
```

Example response:

```json
{
  "count": 1,
  "submissions": [
    {
      "submissionId": "sub_123",
      "email": "ana.velasquez+demo@example.com",
      "status": "failed"
    }
  ]
}
```

---

### `POST /api/jobs/process-next`

Process the next queued sync job.

For the first version, this can call local mock functions instead of real APIs:

```python
def sync_to_marketo(submission: dict) -> dict:
    ...


def sync_to_salesforce(submission: dict) -> dict:
    ...
```

If both succeed, mark the submission as:

```json
{
  "status": "synced"
}
```

If either fails, mark the submission as:

```json
{
  "status": "failed"
}
```

Example response:

```json
{
  "jobId": "job_123",
  "submissionId": "sub_123",
  "status": "synced"
}
```

---

## Recommended functions

Keep route logic thin. Implement core behavior in plain Python functions.

```python
def camel_case_key(raw_key: str) -> str:
    """Convert keys like 'First Name', 'last-name', and 'form_id' to camelCase."""
    ...


def normalize_submission(payload: dict) -> dict:
    """Normalize keys and values from a raw form payload."""
    ...


def validate_submission(submission: dict) -> list[str]:
    """Return a list of validation errors. Empty list means valid."""
    ...


def create_submission(payload: dict) -> dict:
    """Validate, normalize, store, and queue a submission."""
    ...


def enqueue_sync_job(submission_id: str) -> dict:
    """Create a sync job and push it to the queue."""
    ...


def process_next_job() -> dict:
    """Process the next queued job and update submission status."""
    ...


def sync_to_marketo(submission: dict) -> dict:
    """Mock Marketo sync."""
    ...


def sync_to_salesforce(submission: dict) -> dict:
    """Mock Salesforce sync."""
    ...
```

---

## Suggested in-memory data structures

```python
from collections import deque

submissions = {}
jobs = {}
job_queue = deque()
idempotency_keys = {}
```

Example stored submission:

```python
submissions[submission_id] = {
    "submissionId": submission_id,
    "status": "queued",
    "createdAt": "2026-06-07T14:10:00Z",
    "updatedAt": "2026-06-07T14:10:00Z",
    "data": normalized_submission,
    "syncResults": {}
}
```

Example job:

```python
jobs[job_id] = {
    "jobId": job_id,
    "submissionId": submission_id,
    "status": "queued",
    "attempts": 0,
    "lastError": None
}
```

---

## Validation rules

Use these exact rules for practice.

| Field | Rule |
|---|---|
| `firstName` | required, non-empty string |
| `lastName` | required, non-empty string |
| `email` | required, must look like an email |
| `company` | required, non-empty string |
| `formId` | required, non-empty string |
| `consent` | required and must be `true` |

Simple email validation is enough:

```python
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
```

---

## Status values

Use these status values consistently:

```python
RECEIVED = "received"
QUEUED = "queued"
SYNCING = "syncing"
SYNCED = "synced"
FAILED = "failed"
RETRYING = "retrying"
DEAD_LETTER = "dead_letter"
```

---

## Acceptance criteria for Milestone 1

### 1. Valid submission

Input:

```json
{
  "First Name": " Ana ",
  "last-name": "Velasquez",
  "Email": "ANA@Example.com",
  "Company": "Acme Law",
  "form_id": "demo_request",
  "utm_campaign": "lawpay-demo-2026",
  "consent": true
}
```

Expected response:

```json
{
  "status": "queued"
}
```

Expected HTTP status: `201`.

---

### 2. Invalid email

Input:

```json
{
  "First Name": "Ana",
  "last-name": "Velasquez",
  "Email": "not-an-email",
  "Company": "Acme Law",
  "form_id": "demo_request",
  "consent": true
}
```

Expected response:

```json
{
  "errors": ["email is invalid"]
}
```

Expected HTTP status: `400`.

---

### 3. Missing consent

Expected response:

```json
{
  "errors": ["consent must be true"]
}
```

Expected HTTP status: `400`.

---

### 4. Process next job

Request:

```http
POST /api/jobs/process-next
```

Expected response:

```json
{
  "status": "synced"
}
```

---

# Milestone 2: Add mock HTTP integrations

After the core local implementation works, replace local mock sync functions with HTTP calls.

You can create mock endpoints inside the same Flask app.

## Mock campaign metadata endpoint

### `GET /mock/campaigns/<campaign_id>`

Example response:

```json
{
  "campaignId": "lawpay-demo-2026",
  "marketoProgramId": 4567,
  "salesforceCampaignId": "701ABC123",
  "owner": "demand-generation",
  "active": true
}
```

## Mock Marketo endpoint

### `POST /mock/marketo/leads`

Example request:

```json
{
  "email": "ana.velasquez+demo@example.com",
  "firstName": "Ana",
  "lastName": "Velasquez",
  "company": "Acme Law Group",
  "programId": 4567,
  "consent": true
}
```

Example response:

```json
{
  "marketoLeadId": 98765,
  "status": "created"
}
```

## Mock Salesforce endpoint

### `POST /mock/salesforce/leads`

Example request:

```json
{
  "email": "ana.velasquez+demo@example.com",
  "firstName": "Ana",
  "lastName": "Velasquez",
  "company": "Acme Law Group",
  "campaignId": "701ABC123"
}
```

Example response:

```json
{
  "salesforceLeadId": "00QABC123",
  "status": "upserted"
}
```

## HTTP client requirements

Use `requests`:

```python
import requests

response = requests.post(url, json=payload, timeout=5)
response.raise_for_status()
return response.json()
```

Production-minded talking points:

- Always set a timeout.
- Use `raise_for_status()` or explicit status handling.
- Retry transient failures.
- Do not retry invalid payloads.
- Store credentials outside code.
- Log enough context to debug failures.
- Do not log sensitive PII unnecessarily.

---

# Milestone 3: Add idempotency

Duplicate form submissions are common in marketing workflows. Users double-click forms, browsers retry requests, and third-party systems may re-send events.

## Requirement

Support an `Idempotency-Key` header.

Example request:

```http
POST /api/submissions
Idempotency-Key: demo-form-ana-001
```

First response:

```json
{
  "submissionId": "sub_123",
  "status": "queued",
  "duplicate": false
}
```

Second response with the same header:

```json
{
  "submissionId": "sub_123",
  "status": "queued",
  "duplicate": true
}
```

## Implementation idea

Use an in-memory dictionary first:

```python
idempotency_keys = {
    "demo-form-ana-001": "sub_123"
}
```

Then optionally replace this with:

- SQL table
- Redis key/value entry
- DynamoDB conditional write
- LRU cache for local exercise purposes

---

# Milestone 4: Implement an LRU cache

Public candidate reports for engineering roles have mentioned LRU Cache-style questions. Use LRU in a role-relevant way instead of practicing it in isolation.

## Use cases

Use an LRU cache for one or both of these:

1. Idempotency key lookup
2. Campaign metadata lookup

Example:

```python
campaign_cache.get("lawpay-demo-2026")
campaign_cache.put("lawpay-demo-2026", campaign_metadata)
```

## Required interface

```python
class LRUCache:
    def __init__(self, capacity: int):
        ...

    def get(self, key: str):
        ...

    def put(self, key: str, value):
        ...
```

## Recommended Python implementation

Use `collections.OrderedDict` first:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

Be ready to explain the more manual version:

- Hash map for O(1) lookup
- Doubly linked list for O(1) recency updates
- Evict least-recently-used node when capacity is exceeded

---

# Milestone 5: Retry and dead-letter behavior

Real integrations fail. Build failure handling into the queue processor.

## Retry rules

| Error | Retry? | Example |
|---|---:|---|
| HTTP 400 | No | Invalid payload |
| HTTP 401/403 | No, alert/config issue | Bad credentials |
| HTTP 409 | Usually no or special handling | Duplicate external record |
| HTTP 429 | Yes | Rate limit |
| HTTP 500/502/503 | Yes | Temporary provider failure |
| Timeout | Yes | Slow third-party API |

## Job fields

Each job should track:

```json
{
  "jobId": "job_123",
  "submissionId": "sub_123",
  "attempts": 2,
  "status": "retrying",
  "lastError": "Salesforce returned 429"
}
```

## Constants

```python
MAX_ATTEMPTS = 3
```

## Required behavior

1. When a job starts, mark it `syncing`.
2. If sync succeeds, mark job and submission `synced`.
3. If sync fails with a retryable error and attempts remain, mark job `retrying` and requeue it.
4. If sync fails permanently, mark job and submission `failed`.
5. If attempts exceed `MAX_ATTEMPTS`, mark job and submission `dead_letter`.

---

# Milestone 6: Add SQLAlchemy and PostgreSQL or SQLite

Move from in-memory dictionaries to a relational database.

Start with SQLite if speed matters. Use PostgreSQL if you want more realistic practice.

## Suggested tables

### `lead_submissions`

| Column | Type | Notes |
|---|---|---|
| `id` | string / UUID | submission ID |
| `first_name` | string | required |
| `last_name` | string | required |
| `email` | string | indexed |
| `company` | string | required |
| `form_id` | string | required |
| `utm_source` | string | optional |
| `utm_medium` | string | optional |
| `utm_campaign` | string | optional, indexed |
| `consent` | boolean | required |
| `status` | string | queued/synced/failed/etc. |
| `created_at` | timestamp | UTC |
| `updated_at` | timestamp | UTC |

### `sync_jobs`

| Column | Type | Notes |
|---|---|---|
| `id` | string / UUID | job ID |
| `submission_id` | foreign key | references lead submission |
| `status` | string | queued/syncing/retrying/synced/etc. |
| `attempt_count` | integer | starts at 0 |
| `last_error` | text | nullable |
| `created_at` | timestamp | UTC |
| `updated_at` | timestamp | UTC |

### `sync_attempts`

| Column | Type | Notes |
|---|---|---|
| `id` | string / UUID | attempt ID |
| `job_id` | foreign key | references sync job |
| `target_system` | string | `marketo` or `salesforce` |
| `status` | string | success/failure |
| `http_status_code` | integer | nullable |
| `error_message` | text | nullable |
| `created_at` | timestamp | UTC |

### `idempotency_keys`

| Column | Type | Notes |
|---|---|---|
| `idempotency_key` | string | unique |
| `submission_id` | foreign key | references lead submission |
| `created_at` | timestamp | UTC |

---

## SQL practice queries

Find duplicate leads by email:

```sql
SELECT email, COUNT(*) AS lead_count
FROM lead_submissions
GROUP BY email
HAVING COUNT(*) > 1;
```

Count submissions by campaign:

```sql
SELECT utm_campaign, COUNT(*) AS submissions
FROM lead_submissions
GROUP BY utm_campaign
ORDER BY submissions DESC;
```

Find failed sync jobs:

```sql
SELECT ls.email, sj.status, sj.last_error, sj.attempt_count
FROM sync_jobs sj
JOIN lead_submissions ls
  ON sj.submission_id = ls.id
WHERE sj.status = 'failed';
```

Find submissions that have not synced:

```sql
SELECT ls.id, ls.email, ls.created_at
FROM lead_submissions ls
LEFT JOIN sync_jobs sj
  ON ls.id = sj.submission_id
WHERE sj.id IS NULL;
```

Coderbyte-style query, PostgreSQL version:

```sql
SELECT COUNT(*)
FROM lead_submissions
WHERE first_name ILIKE '%e%'
  AND LENGTH(last_name) > 5;
```

Schema evolution:

```sql
ALTER TABLE lead_submissions
ADD COLUMN lead_score INTEGER DEFAULT 0;
```

---

# Milestone 7: Replace in-memory queue with Redis Queue

This is a strong extension if Redis Queue is on your resume.

## Architecture

```text
POST /api/submissions
        |
        v
Validate + normalize
        |
        v
Store submission
        |
        v
Enqueue job in Redis Queue
        |
        v
Worker processes Marketo/Salesforce sync
```

## Goal

Keep queue behavior behind an interface so the route code does not care whether the queue is in memory, Redis, or SQS.

Example interface:

```python
class QueueClient:
    def enqueue(self, message: dict) -> str:
        ...

    def dequeue(self) -> dict | None:
        ...
```

Production-minded explanation:

> I started with an in-memory queue for the coding exercise, but I separated queue behavior from route logic so the queue can be replaced with Redis Queue or AWS SQS without rewriting the API layer.

---

# Milestone 8: Add AWS SQS

Replace or supplement Redis Queue with AWS SQS.

## Requirements

1. Create an SQS queue.
2. Create a dead-letter queue.
3. On form submission, send a message:

```json
{
  "submissionId": "sub_123",
  "eventType": "lead.submitted"
}
```

4. Create a worker script that polls SQS and processes jobs.
5. Delete messages only after successful processing.
6. Allow repeated failures to go to the DLQ.

## Worker behavior

```text
Poll SQS
  -> receive message
  -> load submission
  -> sync to Marketo
  -> sync to Salesforce
  -> update status
  -> delete message from queue
```

If a retryable failure occurs:

```text
Do not delete message
  -> message becomes visible again after visibility timeout
  -> SQS redrive policy eventually moves it to DLQ
```

---

# Milestone 9: Add S3 raw payload storage and metadata lookup

This extension directly reinforces the S3-style assessment task.

## Requirement

When a submission is accepted, write the raw payload to S3:

```text
s3://your-bucket/raw-submissions/sub_123.json
```

Add metadata:

```json
{
  "submission-id": "sub_123",
  "form-id": "demo_request",
  "utm-campaign": "lawpay-demo-2026",
  "status": "queued"
}
```

Then implement:

```python
def get_submission_object_metadata(submission_id: str) -> dict:
    ...
```

Use a HEAD-style object metadata request rather than downloading the whole object.

## Python boto3 sketch

```python
import boto3

s3 = boto3.client("s3")


def put_raw_submission(bucket: str, key: str, payload: bytes, metadata: dict) -> None:
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=payload,
        Metadata=metadata,
        ContentType="application/json",
    )


def get_submission_metadata(bucket: str, key: str) -> dict:
    response = s3.head_object(Bucket=bucket, Key=key)
    return response.get("Metadata", {})
```

Production-minded details:

- Use IAM roles, not hardcoded credentials.
- Use least privilege S3 permissions.
- Consider encryption at rest.
- Avoid logging full PII payloads.
- Use predictable prefixes such as `raw-submissions/yyyy/mm/dd/submission_id.json`.

---

# Milestone 10: Add Lambda-style processing

Use this only after the local and SQS versions are clear.

## Goal

Practice explaining how this would run serverlessly.

Architecture:

```text
Website / frontend
        |
        v
API Gateway
        |
        v
Lambda: create submission
        |
        v
Database + S3 raw payload
        |
        v
SQS queue
        |
        v
Lambda: sync worker
        |
        v
Marketo + Salesforce
```

## Lambda talking points

- Lambda scales concurrent execution environments automatically.
- Use reserved concurrency to protect downstream systems.
- Use provisioned concurrency only if cold starts are a real concern.
- Use environment variables for configuration.
- Use Secrets Manager or Parameter Store for credentials.
- Use CloudWatch logs and metrics.
- Use DLQ or SQS redrive policy for failures.

---

# Milestone 11: Add observability

Marketing integrations need operational visibility.

## Metrics to track

| Metric | Why it matters |
|---|---|
| `submissions_received` | Website form volume |
| `submissions_queued` | Queue intake health |
| `sync_success_count` | Integration success |
| `sync_failure_count` | Integration failure trend |
| `sync_latency_ms` | Third-party API slowness |
| `queue_depth` | Backlog / worker health |
| `dead_letter_count` | Unrecoverable failures |
| `marketo_error_rate` | Marketo integration health |
| `salesforce_error_rate` | Salesforce integration health |

## Logs should include

- `submissionId`
- `jobId`
- target system
- status
- attempt count
- error type
- HTTP status code

Avoid logging full PII unless necessary and approved.

---

# Milestone 12: Optional React dashboard

This is optional. Do it only after the backend is strong.

## Component

Build a simple `LeadSyncDashboard` component that:

1. Fetches `/api/submissions`
2. Shows loading state
3. Shows error state
4. Renders submissions grouped by status
5. Has a `Process next job` button that calls `POST /api/jobs/process-next`

## Minimal React sketch

```jsx
import { useEffect, useState } from "react";

function LeadSyncDashboard() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadSubmissions() {
    try {
      setLoading(true);
      const response = await fetch("/api/submissions");
      if (!response.ok) throw new Error("Failed to load submissions");
      const data = await response.json();
      setSubmissions(data.submissions);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function processNextJob() {
    const response = await fetch("/api/jobs/process-next", {
      method: "POST",
    });
    if (!response.ok) throw new Error("Failed to process job");
    await loadSubmissions();
  }

  useEffect(() => {
    loadSubmissions();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <section>
      <h1>Lead Sync Dashboard</h1>
      <button onClick={processNextJob}>Process next job</button>
      <ul>
        {submissions.map((submission) => (
          <li key={submission.submissionId}>
            {submission.email} — {submission.status}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default LeadSyncDashboard;
```

---

# Suggested repo structure

```text
marketing-lead-sync/
  README.md
  implementation.md
  requirements.txt
  app.py
  config.py
  services/
    __init__.py
    normalization.py
    validation.py
    storage.py
    queue.py
    idempotency.py
    lru_cache.py
    crm_clients.py
    retry.py
  models/
    __init__.py
    submission.py
    job.py
  tests/
    test_normalization.py
    test_validation.py
    test_lru_cache.py
    test_api.py
    test_jobs.py
  scripts/
    seed.py
    worker.py
```

---

# Recommended first-pass files

For the first implementation, keep it simple:

```text
marketing-lead-sync/
  app.py
  requirements.txt
  tests/
    test_app.py
```

Only split into the larger structure after the simple version works.

---

# Suggested `requirements.txt`

First pass:

```text
Flask==3.*
pytest==8.*
requests==2.*
```

Later extensions:

```text
SQLAlchemy==2.*
Flask-SQLAlchemy==3.*
psycopg2-binary==2.*
redis==5.*
rq==1.*
boto3==1.*
python-dotenv==1.*
```

---

# Curl test commands

## Create valid submission

```bash
curl -X POST http://localhost:5000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-form-ana-001" \
  -d '{
    "First Name": " Ana ",
    "last-name": "Velasquez",
    "Email": "ANA.VELASQUEZ+demo@Example.com",
    "Company": "Acme Law Group",
    "form_id": "demo_request",
    "utm_source": "google",
    "utm_medium": "paid_search",
    "utm_campaign": "lawpay-demo-2026",
    "consent": true
  }'
```

## Submit duplicate idempotency key

```bash
curl -X POST http://localhost:5000/api/submissions \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-form-ana-001" \
  -d '{
    "First Name": " Ana ",
    "last-name": "Velasquez",
    "Email": "ANA.VELASQUEZ+demo@Example.com",
    "Company": "Acme Law Group",
    "form_id": "demo_request",
    "utm_campaign": "lawpay-demo-2026",
    "consent": true
  }'
```

## Get all submissions

```bash
curl http://localhost:5000/api/submissions
```

## Process next job

```bash
curl -X POST http://localhost:5000/api/jobs/process-next
```

## Get failed submissions

```bash
curl http://localhost:5000/api/submissions?status=failed
```

---

# Test plan

## Unit tests

Test `camel_case_key`:

| Input | Expected |
|---|---|
| `First Name` | `firstName` |
| `last-name` | `lastName` |
| `form_id` | `formId` |
| `utm_campaign` | `utmCampaign` |
| `Email` | `email` |

Test `normalize_submission`:

- Trims string values
- Lowercases email
- Converts all keys to camelCase
- Preserves boolean consent

Test `validate_submission`:

- Accepts valid submission
- Rejects missing first name
- Rejects missing last name
- Rejects invalid email
- Rejects missing company
- Rejects missing form ID
- Rejects false/missing consent

Test `LRUCache`:

- Returns `None` for missing keys
- Returns stored values
- Moves accessed keys to most recently used
- Evicts least recently used key when capacity is exceeded

## API tests

- `POST /api/submissions` returns `201` for valid input
- `POST /api/submissions` returns `400` for invalid input
- Duplicate idempotency key returns original submission
- `GET /api/submissions/<id>` returns stored submission
- `POST /api/jobs/process-next` updates status to `synced`
- Failed sync updates status to `retrying`, `failed`, or `dead_letter`

---

# Interview explanation script

Use this language while implementing or discussing your solution:

> I’ll keep the first version simple and correct: validate, normalize, store, enqueue, and expose sync status. I’m using in-memory storage for the exercise, but I’ll keep storage and queue behavior behind function boundaries so they can be replaced with SQLAlchemy/PostgreSQL, Redis Queue, or SQS.

Then explain productionization:

> For real Marketo/Salesforce integrations, I would make the sync idempotent, use retries for transient failures, respect API rate limits, store credentials in Secrets Manager, and add metrics around success rate, failure rate, latency, and dead-letter queue depth.

And for frontend limitations:

> My strongest area is backend Python, SQL, AWS, and integration work. I have working JavaScript/React knowledge, so I can read components, make focused changes, and build a small dashboard, but I would treat the backend/API/data-flow work as my main contribution.

---

# What not to overbuild first

Do not start with:

- Terraform
- full AWS deployment
- real Salesforce OAuth
- real Marketo API setup
- full React frontend
- complex CSS
- Kubernetes
- ECS deployment
- Elasticsearch
- multi-tenant auth
- full admin dashboard
- elaborate database migrations before the basic API works

These may be useful later, but they are not the best first move for a 45-minute technical interview.

---

# Final recommended build sequence

1. Core Flask API with in-memory store
2. Validation and normalization
3. In-memory queue and `process-next` endpoint
4. Idempotency key support
5. LRU cache implementation
6. Mock HTTP calls to fake Marketo/Salesforce
7. Retry and dead-letter behavior
8. SQLAlchemy/PostgreSQL
9. Redis Queue
10. S3 raw payload and metadata
11. SQS/Lambda architecture
12. React dashboard

The most interview-useful version is complete by step 7.

---

# North-star challenge statement

Build a Flask backend that receives marketing form submissions, normalizes and validates them, prevents duplicates, queues CRM sync work, calls mock Marketo/Salesforce APIs, tracks status, and handles failures.
