import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Bot 1: ក្រុមនិយាយគ្នាលេង (@funnychatkh_bot)
BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1", "").strip() or "8924846395:AAFOGLG4LywUd2I6BqN0WsAaXFJdijSEtYo"

# Bot 2: ក្រុមចែករំលែកចំណេះដឹង (@sharelearningkh_bot)
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2", "").strip() or "8838422638:AAFEe_Fj5S7aICM1XyegK8BB4wRnG-bmqg4"

# Bot 3: ស្វែងរកស្នេហ៍ (@LoveFinderKh_bot)
BOT_TOKEN_3 = os.getenv("BOT_TOKEN_3", "").strip() or "8908269933:AAFW-89grzLEhU4N_QNemZr0rIA3uhAsfG8"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
