import io

import boto3
from PIL import Image

from config import AWS_BUCKET_NAME

s3 = boto3.client("s3", region_name="eu-central-1")


def validate_and_resize_image(
    file_bytes: bytes, max_width=1280, max_height=720
) -> bytes:
    with Image.open(io.BytesIO(file_bytes)) as img:
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height))
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return buf.getvalue()


def upload_image_to_s3(
    file_bytes: bytes, seller_id: str, promo_id: str, extension: str
) -> str:
    key = f"{seller_id}/promo-{promo_id}-image.{extension}"
    s3.put_object(
        Bucket=AWS_BUCKET_NAME,
        Key=key,
        Body=file_bytes,
        ContentType=f"image/{extension}",
    )
    return key
