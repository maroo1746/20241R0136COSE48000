import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PRODUCTION = os.getenv("VER") == "prod"

DB_URL = os.getenv("DB_URL")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW"))

FRONT_URL = os.getenv("FRONT_URL")
