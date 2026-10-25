import os
import socket
from aiohttp import web

# Force IPv4 to prevent IPv6 DNS timeout issues on Windows
_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4

import asyncio
import logging
from telegram import Update
import config
from bots.bot1_funny import build_bot1_app
from bots.bot2 import build_bot2_app
from bots.bot3 import build_bot3_app

# Configure logging
logging.basicConfig(
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("MultiBotRunner")

async def _health_handler(request):
    return web.Response(text="OK", content_type="text/plain", charset="utf-8")

async def start_health_server():
    """Lightweight HTTP server so Render Web Service detects the open port and doesn't timeout."""
    port = int(os.environ.get("PORT", "8080"))
    try:
        app = web.Application()
        app.router.add_get("/", _health_handler)
        app.router.add_get("/health", _health_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"🌐 Health-check HTTP server listening on port {port}")
    except Exception as e:
        logger.warning(f"Could not bind HTTP server to port {port}: {e}")

async def run_single_bot(bot_builder, token: str, bot_name: str, stop_event: asyncio.Event):
    """Run an individual bot application concurrently with auto-reconnect."""
    while not stop_event.is_set():
        try:
            app = bot_builder(token)
            async with app:
                await app.start()
                await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
                bot_info = await app.bot.get_me()
                logger.info(f"✅ {bot_name} (@{bot_info.username}) is ACTIVE and POLLING.")
                
                # Wait until cancellation or stop event
                await stop_event.wait()
                
                logger.info(f"Stopping {bot_name}...")
                await app.updater.stop()
                await app.stop()
        except asyncio.CancelledError:
            logger.info(f"{bot_name} task was cancelled.")
            break
        except Exception as e:
            if stop_event.is_set():
                break
            logger.error(f"❌ Error in {bot_name}: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

async def main():
    stop_event = asyncio.Event()
    tasks = []
    
    # Start web health server for Render/Cloud keep-alive
    await start_health_server()
    
    # 1. Bot 1 (Funny Group Friend Bot)
    if config.BOT_TOKEN_1:
        logger.info("Initializing Bot 1 (Funny Group Friend Bot)...")
        tasks.append(asyncio.create_task(run_single_bot(build_bot1_app, config.BOT_TOKEN_1, "Bot 1 (Funny Friend)", stop_event)))
    else:
        logger.warning("BOT_TOKEN_1 is not set in .env")

    # 2. Bot 2 (ក្រុមចែករំលែកចំណេះដឹង)
    if config.BOT_TOKEN_2:
        logger.info("Initializing Bot 2 (ក្រុមចែករំលែកចំណេះដឹង @sharelearningkh_bot)...")
        tasks.append(asyncio.create_task(run_single_bot(build_bot2_app, config.BOT_TOKEN_2, "Bot 2 (Knowledge Share)", stop_event)))
    else:
        logger.info("BOT_TOKEN_2 is empty (not running).")

    # 3. Bot 3 (ស្វែងរកស្នេហ៍ @LoveFinderKh_bot)
    if config.BOT_TOKEN_3:
        logger.info("Initializing Bot 3 (ស្វែងរកស្នេហ៍ @LoveFinderKh_bot)...")
        tasks.append(asyncio.create_task(run_single_bot(build_bot3_app, config.BOT_TOKEN_3, "Bot 3 (Love Finder)", stop_event)))
    else:
        logger.info("BOT_TOKEN_3 is empty (not running).")

    if not tasks:
        logger.error("No bots were configured! Please add at least one bot token in .env")
        return

    logger.info(f"🚀 Running {len(tasks)} bot(s) concurrently...")

    # Wait for all bots
    try:
        await asyncio.gather(*tasks)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutdown signal received. Stopping all bots...")
        stop_event.set()
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBots stopped gracefully by user.")
