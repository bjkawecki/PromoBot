import os

import boto3
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
verkaeufer_kanal_id = os.environ.get("SELLER_CHANNEL_ID")
ADMIN_USER_NAME = os.environ.get("ADMIN_USER_NAME")
DB_URL = os.environ.get("DB_URL")
TEST_SELLER_ID = os.environ.get("TEST_SELLER_ID")


dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",  # Lokaler DynamoDB Endpoint
    region_name="us-west-2",  # Dummy Region für Local
    aws_access_key_id="fake",  # Dummy Keys für Local
    aws_secret_access_key="fake",
)


seller_table = dynamodb.Table("seller")
