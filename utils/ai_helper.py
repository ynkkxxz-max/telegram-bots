import logging
from utils.khmer_jokes import get_smart_reply

logger = logging.getLogger(__name__)

async def generate_bot_reply(user_message: str, user_name: str = "") -> str:
    """Generate high-speed, instant local response in Khmer (Fast & No Lag)."""
    # Runs 100% locally for zero-latency instant responses
    return get_smart_reply(user_message, user_name)
