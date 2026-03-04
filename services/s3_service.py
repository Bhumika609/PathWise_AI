# services/s3_service.py
import os
import uuid
import boto3
import logging

logger = logging.getLogger("s3_service")
logger.setLevel(logging.INFO)

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET")  # REQUIRED

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_bytes_to_s3(data: bytes, filename: str, content_type: str) -> str:
    if not S3_BUCKET:
        raise ValueError("S3_BUCKET env var is not set")

    key = f"uploads/{uuid.uuid4().hex}-{filename}"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type
    )

    s3_uri = f"s3://{S3_BUCKET}/{key}"
    logger.info(f"Uploaded audio to {s3_uri}")
    return s3_uri
