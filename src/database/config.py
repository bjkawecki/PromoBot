import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",  # Lokaler DynamoDB Endpoint
    region_name="us-west-2",  # Dummy Region für Local
    aws_access_key_id="fake",  # Dummy Keys für Local
    aws_secret_access_key="fake",
)

# Beispiel: Table-Objekte laden
seller_table = dynamodb.Table("seller")
buyer_table = dynamodb.Table("buyer")
