import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    config=Config(signature_version="s3v4"),
)

REQUIRED_BUCKETS = ["original-images", "cropped-lips", "brushed-lips"]


def ensure_buckets():
    for bucket in REQUIRED_BUCKETS:
        try:
            s3_client.head_bucket(Bucket=bucket)
        except ClientError:
            s3_client.create_bucket(Bucket=bucket)


async def upload_file(bucket: str, path: str, data: bytes, content_type: str = "image/jpeg") -> str:
    s3_client.put_object(
        Bucket=bucket,
        Key=path,
        Body=data,
        ContentType=content_type,
    )
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": path},
        ExpiresIn=86400,
    )


async def delete_file(bucket: str, path: str) -> None:
    s3_client.delete_object(Bucket=bucket, Key=path)
