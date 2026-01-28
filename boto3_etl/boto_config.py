import boto3
from botocore.config import Config

cfg = Config(retries={"mode": "adaptive", "max_attempts": 10})
session = boto3.Session(profile_name="default", region_name="us-east-1")

s3 = session.client("s3", config=cfg)
p = s3.get_paginator("list_objects_v2")
pages = p.paginate(Bucket="genomics-data-repository", Prefix="OPTIONAL/PREFIX/")

count = 0

for page in pages:
    for obj in page.get("Contents", []):
        count += 1
        if count <= 10:
            head = s3.head_object(
                Bucket="genomics-data-repository",
                Key=obj["annotations/gene_annotation.tsv"],
            )
            print(
                obj["annotations/gene_annotation.tsv"],
                head.get("ContentType"),
                head.get("ServerSideEncryption"),
            )

print("Total objects scanned:", count)
