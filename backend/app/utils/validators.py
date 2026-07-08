from fastapi import HTTPException, UploadFile

from app.core.config import settings


def validate_image(image: UploadFile) -> None:
    if image.content_type not in settings.supported_image_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {', '.join(settings.supported_image_types)}",
        )

    if image.size and image.size > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_upload_size_mb}MB",
        )
