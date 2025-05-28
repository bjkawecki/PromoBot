provider "aws" {
  region = "eu-central-1" # z. B. Frankfurt
}

resource "aws_s3_bucket" "aiogram_uploads" {
  bucket = "promobot-seller-promo-images" # muss global einzigartig sein

  tags = {
    Name        = "PromoBot Seller Image Upload Bucket"
    Environment = "dev"
  }

  force_destroy = true # löscht auch alle Objekte beim `terraform destroy`
}

# Verhindert öffentlichen Zugriff explizit
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket                  = aws_s3_bucket.aiogram_uploads.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

