import boto3

from config import AWS_BUCKET_NAME

s3 = boto3.client("s3", region_name="eu-central-1")


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
