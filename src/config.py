import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
verkaeufer_kanal_id = os.environ.get("SELLER_CHANNEL_ID")
ADMIN_USER_NAME = os.environ.get("ADMIN_USER_NAME")
DB_URL = os.environ.get("DB_URL")
TEST_SELLER_ID = os.environ.get("TEST_SELLER_ID")
