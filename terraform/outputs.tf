output "s3_bucket_name" {
  description = "Name des S3-Buckets für Bild-Uploads"
  value       = aws_s3_bucket.aiogram_uploads.bucket
}

output "s3_bucket_arn" {
  description = "ARN des S3-Buckets"
  value       = aws_s3_bucket.aiogram_uploads.arn
}
