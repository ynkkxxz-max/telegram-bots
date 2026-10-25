import os
import json
import random
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STICKERS_FILE = os.path.join(DATA_DIR, "stickers.json")

# Official Telegram dog sticker pack only (No foreign/other stickers)
DEFAULT_STICKERS = [
    "CAACAgIAAxUAAWrcsGN26zdf786nWTPb1mmTZLUPAALeAAP0exkAAb2F7273xc49PQQ",
    "CAACAgIAAxUAAWrcsGPH5c9-Hy-vXA9U645Jpkw4AAIEAQAC9HsZAAGAEeRAK8ac-z0E",
    "CAACAgIAAxUAAWrcsGNhSn_Wu0zVfFtXSCWBaxbVAAILAQAC9HsZAAG4Cs7MocWO6z0E",
    "CAACAgIAAxUAAWrcsGNGHt51nTSMxmJaymIqf3_BAAL-AAP0exkAAaAWf7umYeLZPQQ",
    "CAACAgIAAxUAAWrcsGMRCkXWIuovA3RwLwAB0DNGeAACDwEAAvR7GQABZvQ5FANUzPQ9BA",
]

def load_stickers() -> list[str]:
    """Load stickers, strictly enforcing ONLY approved official stickers."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(STICKERS_FILE):
        try:
            with open(STICKERS_FILE, "r", encoding="utf-8") as f:
                stickers = json.load(f)
                if isinstance(stickers, list):
                    # Filter strictly to only default dog stickers
                    approved = [s for s in stickers if s in DEFAULT_STICKERS]
                    if approved:
                        return approved
        except Exception as e:
            logger.warning(f"Could not load stickers.json: {e}")

    # Fallback and reset to approved default stickers
    save_stickers(DEFAULT_STICKERS)
    return list(DEFAULT_STICKERS)

def save_stickers(stickers: list[str]):
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        approved = [s for s in stickers if s in DEFAULT_STICKERS]
        with open(STICKERS_FILE, "w", encoding="utf-8") as f:
            json.dump(approved if approved else DEFAULT_STICKERS, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving stickers: {e}")

def add_sticker(file_id: str):
    """Do NOT learn or add other/external stickers."""
    pass

def get_random_sticker() -> str:
    """Return a random approved dog sticker."""
    return random.choice(DEFAULT_STICKERS)
