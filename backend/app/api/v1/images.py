from fastapi import APIRouter, HTTPException, Response
from botocore.exceptions import ClientError

from app.services.storage_service import s3_client

router = APIRouter()


@router.get("/images/{bucket}/{key:path}")
async def serve_image(bucket: str, key: str):
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read()
        content_type = obj.get("ContentType", "image/jpeg")
        return Response(content=body, media_type=content_type)
    except ClientError:
        raise HTTPException(status_code=404, detail="Image not found")
