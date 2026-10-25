import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1", "").strip()
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2", "").strip()
BOT_TOKEN_3 = os.getenv("BOT_TOKEN_3", "").strip()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

