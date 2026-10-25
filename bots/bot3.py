"""
Bot 3: ស្វែងរកស្នេហ៍😘 (@LoveFinderKh_bot)
Features:
- Daily Couple Matchmaking (/match, /couple)
- Love Compatibility Calculator (/love)
- Sweet Pick-up Lines (/flirt)
- Daily Love Horoscope & Fortune (/fortune)
- Anonymous Crush Confession (/crush)
- Romantic Truth or Dare (/truth, /dare)
- Anti-Link Spam Protection
- Warm Romantic Welcome for New Members
"""
import logging
import re
import asyncio
import random
import html
from typing import Dict, Set, Tuple
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ApplicationHandlerStop,
)
from telegram.request import HTTPXRequest

from utils.love_data import (
    get_random_flirt,
    get_random_fortune,
    get_random_truth,
    get_random_dare,
    calculate_love_score,
)

logger = logging.getLogger("Bot3_LoveFinder")

# Regex to detect links in chat messages
LINK_REGEX = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+|bit\.ly/\S+)",
    re.IGNORECASE,
)

# In-memory storage of active users in groups for matchmaking: chat_id -> dict of {user_id: user_name}
chat_active_members: Dict[int, Dict[int, str]] = {}

def get_user_name(update: Update) -> str:
    """Extract a friendly user display name."""
    user = update.effective_user
    if user and user.first_name:
        first = user.first_name.strip()
        if first.lower() not in ["group", "channel", "telegram", "group anonymous bot"]:
            return html.escape(first)
    return "គ្នាយើង"

async def delete_after_delay(msg, delay_seconds: int = 7):
    """Delete message after delay."""
    await asyncio.sleep(delay_seconds)
    try:
        await msg.delete()
    except Exception:
        pass

async def anti_link_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detect and delete spam link messages in groups."""
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if not message or not chat or not user or chat.type == "private":
        return

    raw_text = message.text or message.caption or ""
    if not LINK_REGEX.search(raw_text):
        return

    try:
        member = await chat.get_member(user.id)
        if member.status in ["creator", "administrator"]:
            return
    except Exception:
        pass

    try:
        await message.delete()
        name = get_user_name(update)
        warn = await chat.send_message(
            f"⚠️ ជម្រាបសួរ {name}! គ្រុប <b>ស្វែងរកស្នេហ៍😘</b> មិនអនុញ្ញាតឱ្យផ្ញើ Link ឬផ្សាយពាណិជ្ជកម្មទេបាទ/ចាស! 🚫",
            parse_mode="HTML"
        )
        asyncio.create_task(delete_after_delay(warn, 7))
        raise ApplicationHandlerStop
    except ApplicationHandlerStop:
        raise
    except Exception as e:
        logger.warning(f"Cannot delete link in Bot 3: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    welcome_text = (
        "សួស្តីបាទ/ចាស! ស្វាគមន៍មកកាន់ <b>ស្វែងរកស្នេហ៍😘</b> (@LoveFinderKh_bot) 💘\n\n"
        "ខ្ញុំជា Bot មេអណ្តើកប្រចាំគ្រុប ដែលជួយផ្គូផ្គងគូស្នេហ៍ វាស់កម្រិតចិត្តស្រឡាញ់ និងបង្កើតបរិយាកាសរីករាយក្នុងគ្រុប!\n\n"
        "<b>ពាក្យបញ្ជាឡូយៗក្នុងគ្រុប៖</b>\n"
        "👉 /match ឬ /couple - ផ្គូផ្គងគូស្នេហ៍ចៃដន្យប្រចាំថ្ងៃក្នុងគ្រុប 💘\n"
        "👉 /love [ឈ្មោះ១] [ឈ្មោះ២] - វាស់ភាគរយស្នេហា និងភាពស៊ីសង្វាក់គ្នា ❤️\n"
        "👉 /flirt - ពាក្យញ៉ែផ្អែមល្ហែមរំជួលចិត្ត 🌹\n"
        "👉 /fortune - ទស្សន៍ទាយរាសីស្នេហាប្រចាំថ្ងៃ 🔮\n"
        "👉 /crush [@user] [សារ] - សារភាពស្នេហាសម្ងាត់ទៅកាន់ Crush (លាក់ឈ្មោះ) 💌\n"
        "👉 /truth - សំណួរសច្ចៈស្នេហា 🤫\n"
        "👉 /dare - ការប្រឈមហ៊ានស្នេហា 🔥\n"
        "👉 /help - មើលរបៀបប្រើប្រាស់\n\n"
        "<i>សូមជូនពរឱ្យអ្នកទាំងអស់គ្នាឆាប់មានសង្សារ និង Crush ស្រឡាញ់វិញណា៎!</i> 🥰✨"
    )
    try:
        await update.message.reply_text(welcome_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(welcome_text.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    help_text = (
        "<b>📖 របៀបប្រើប្រាស់ Bot «ស្វែងរកស្នេហ៍😘»៖</b>\n\n"
        "1. <b>/match ឬ /couple ៖</b> ឱ្យ Bot ដើរតួជាមេអណ្តើក ចាប់គូសមាជិក ២ នាក់ក្នុងគ្រុបជាគូស្នេហ៍ប្រចាំថ្ងៃ 💘\n"
        "2. <b>/love [ឈ្មោះ១] [ឈ្មោះ២] ៖</b> គណនាភាគរយស្នេហា (ឬ Reply លើសាររបស់ Crush រួចវាយ /love) ❤️\n"
        "3. <b>/flirt ៖</b> ចែករំលែកពាក្យញ៉ែផ្អែមល្ហែម និងកំប្លែងៗ 🌹\n"
        "4. <b>/fortune ៖</b> ទស្សន៍ទាយរាសីស្នេហា និងឱកាសជួបមនុស្សពិសេសថ្ងៃនេះ 🔮\n"
        "5. <b>/crush [@user] [សារ] ៖</b> សារភាពស្នេហាសម្ងាត់! Bot នឹងប្រកាសក្នុងគ្រុបដោយមិនប្រាប់ឈ្មោះអ្នកផ្ញើឡើយ 💌\n"
        "6. <b>/truth & /dare ៖</b> ល្បែងសច្ចៈ ឬហ៊ានបែបស្នេហាសម្រាប់លេងកម្សាន្តក្នុងគ្រុប 🔥\n"
        "7. <b>ការពារគ្រុប៖</b> ប្រព័ន្ធ Anti-Link លុប Link Spam ផ្សាយពាណិជ្ជកម្មដោយស្វ័យប្រវត្តិ!"
    )
    try:
        await update.message.reply_text(help_text, parse_mode="HTML")
    except Exception:
        await update.message.reply_text(help_text.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""))

async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pair two members as the group's Couple of the Day!"""
    chat = update.effective_chat
    sender_name = get_user_name(update)

    members = chat_active_members.get(chat.id, {})
    
    # Need at least 2 distinct members recorded
    if len(members) >= 2:
        user_list = list(members.values())
        sampled = random.sample(user_list, 2)
        person1, person2 = sampled[0], sampled[1]
    elif len(members) == 1:
        person1 = sender_name
        person2 = "Crush អាថ៌កំបាំងក្នុងគ្រុប"
    else:
        person1 = sender_name
        person2 = "Crush ក្នុងគ្រុប"

    score, bar, commentary = calculate_love_score(person1, person2)

    response = (
        "💘 <b>គូស្នេហ៍ប្រចាំថ្ងៃក្នុងគ្រុប (Couple of the Day)៖</b>\n\n"
        f"🙋‍♂️ <b>{person1}</b>  ❤️  🙋‍♀️ <b>{person2}</b>\n\n"
        f"📊 <b>កម្រិតភាពស៊ីសង្វាក់គ្នា៖</b> <b>{score}%</b>\n"
        f"<code>{bar}</code>\n\n"
        f"{commentary}\n\n"
        "🎉 <i>អបអរសាទរគូស្នេហ៍ថ្មីក្នុងគ្រុប! កុំភ្លេចប៉ាវគ្នាយើងញ៉ាំតែគុជ ឬកាហ្វេផងណា៎!</i> 🧋☕🥰"
    )
    try:
        await update.message.reply_text(response, parse_mode="HTML")
    except Exception:
        await update.message.reply_text(response.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace("<code>", "").replace("</code>", ""))

async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate love compatibility score."""
    message = update.message
    sender_name = get_user_name(update)
    args = context.args

    # Scenario 1: User replied to someone's message with /love
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.first_name or "Crush"
        p1, p2 = sender_name, target
    # Scenario 2: User provided arguments
    elif args and len(args) >= 2:
        p1, p2 = args[0], args[1]
    elif args and len(args) == 1:
        p1, p2 = sender_name, args[0]
    else:
        hint = (
            "❤️ <b>របៀបវាស់ភាគរយស្នេហា៖</b>\n\n"
            "👉 <b>វិធីទី ១៖</b> Reply លើសាររបស់ Crush ក្នុងគ្រុប រួចវាយ <code>/love</code>\n"
            "👉 <b>វិធីទី ២៖</b> វាយ <code>/love ឈ្មោះអ្នក ឈ្មោះCrush</code>\n"
            "👉 <b>វិធីទី ៣៖</b> វាយ <code>/love @Username</code>\n\n"
            "<i>សាកល្បងឥឡូវនេះដើម្បីដឹងពីភាពស៊ីសង្វាក់គ្នានៃបេះដូងអ្នកទាំងពីរ!</i> 💘✨"
        )
        try:
            await message.reply_text(hint, parse_mode="HTML")
        except Exception:
            await message.reply_text(hint.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "").replace("<i>", "").replace("</i>", ""))
        return

    score, bar, commentary = calculate_love_score(p1, p2)
    safe_p1 = html.escape(p1)
    safe_p2 = html.escape(p2)
    res = (
        f"❤️ <b>ការវាស់ស្ទង់កម្រិតស្នេហា & ភាពស៊ីសង្វាក់គ្នា៖</b>\n\n"
        f"💘 <b>{safe_p1}</b>  +  <b>{safe_p2}</b>\n\n"
        f"📊 <b>ពិន្ទុភាពចុះសម្រុង៖</b> <b>{score}%</b>\n"
        f"<code>{bar}</code>\n\n"
        f"{commentary}"
    )
    try:
        await message.reply_text(res, parse_mode="HTML")
    except Exception:
        await message.reply_text(res.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "").replace("<i>", "").replace("</i>", ""))

async def flirt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send sweet Khmer pickup line."""
    line = get_random_flirt()
    await update.message.reply_text(f"🌹 <b>ពាក្យញ៉ែផ្អែមល្ហែម៖</b>\n\n{line}", parse_mode="HTML")

async def fortune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send daily love horoscope."""
    user_name = get_user_name(update)
    fortune = get_random_fortune(user_name)
    await update.message.reply_text(fortune, parse_mode="HTML")

async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Truth question for romance/dating."""
    t = get_random_truth()
    await update.message.reply_text(t, parse_mode="HTML")

async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Dare challenge for romance/dating."""
    d = get_random_dare()
    await update.message.reply_text(d, parse_mode="HTML")

async def crush_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Secret love confession in group without revealing sender identity."""
    message = update.message
    args = context.args
    chat = update.effective_chat

    if not args or len(args) < 2:
        usage = (
            "💌 <b>របៀបផ្ញើសារសារភាពស្នេហាសម្ងាត់ (Secret Crush Confession)៖</b>\n\n"
            "វាយ៖ <code>/crush @Username សាររបស់អ្នក</code>\n\n"
            "💡 <i>ឧទាហរណ៍៖</i> <code>/crush @sreypov ខ្ញុំលួចស្រឡាញ់អូនយូរហើយ តែមិនហ៊ានប្រាប់!</code>\n\n"
            "🔒 <b>Bot នឹងលុបសាររបស់អ្នកភ្លាមៗ ហើយប្រកាសក្នុងគ្រុបដោយលាក់ឈ្មោះអ្នក ១០០%!</b> 🤫💘"
        )
        await message.reply_text(usage, parse_mode="HTML")
        return

    target = html.escape(args[0])
    secret_text = html.escape(" ".join(args[1:]))

    # Delete original message to keep sender anonymous
    try:
        await message.delete()
    except Exception:
        pass

    announcement = (
        f"💌 <b>មានសារសារភាពស្នេហាសម្ងាត់មួយផ្ញើជូន {target}!</b>\n\n"
        f"«<i>{secret_text}</i>»\n\n"
        "💘 <b>ពី៖</b> <i>មនុស្សសម្ងាត់ម្នាក់ក្នុងគ្រុបនេះ! (Bot រក្សាការសម្ងាត់ជូន ១០០%)</i> 🤫🌹✨"
    )
    try:
        await chat.send_message(announcement, parse_mode="HTML")
    except Exception:
        await chat.send_message(announcement.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""))

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Warm and romantic welcome message for new group members."""
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        name = html.escape(member.first_name or "គ្នាយើង")
        welcome_msg = (
            f"👋 ស្វាគមន៍ {name} ចូលមកកាន់គ្រុប <b>ស្វែងរកស្នេហ៍😘</b>! 🌹\n\n"
            "សូមជូនពរឱ្យអ្នកឆាប់បាន Crush ឬរកបានសង្សារក្នុងគ្រុបនេះណា៎! 💖\n\n"
            "👉 វាយ <b>/match</b> ដើម្បីផ្គូផ្គងគូស្នេហ៍ចៃដន្យ 💘\n"
            "👉 វាយ <b>/flirt</b> ដើម្បីមើលពាក្យញ៉ែផ្អែមល្ហែម 🍯\n"
            "👉 វាយ <b>/fortune</b> ដើម្បីទស្សន៍ទាយរាសីស្នេហាថ្ងៃនេះ! 🔮"
        )
        try:
            await update.message.reply_text(welcome_msg, parse_mode="HTML")
        except Exception:
            await update.message.reply_text(welcome_msg.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process incoming messages, track active members, and reply to romance keywords."""
    message = update.message
    if not message or not message.text:
        return

    chat = update.effective_chat
    user = update.effective_user
    user_name = get_user_name(update)
    text = message.text.lower()

    # Track active users in group for matchmaking
    if chat.type in ["group", "supergroup"] and user and not user.is_bot:
        if chat.id not in chat_active_members:
            chat_active_members[chat.id] = {}
        chat_active_members[chat.id][user.id] = user_name

    bot = context.bot
    is_private = chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == bot.id
    )
    is_mentioned = bot.username and f"@{bot.username.lower()}" in text

    # Keywords for automatic fun responses
    if any(k in text for k in ["ផ្គូផ្គង", "គូស្នេហ៍", "match"]):
        await match_command(update, context)
        return

    if any(k in text for k in ["ញ៉ែ", "flirt", "ពាក្យញ៉ែ"]):
        await flirt_command(update, context)
        return

    if any(k in text for k in ["រាសីស្នេហ៍", "fortune", "គូព្រេង"]):
        await fortune_command(update, context)
        return

    # If mentioned or private or reply to bot
    if is_private or is_reply_to_bot or is_mentioned:
        if any(k in text for k in ["single", "នៅលីវ", "គ្មានសង្សារ"]):
            reply = (
                f"នៅលីវមែនទេ {user_name}? កុំបារម្ភអី! ចូលគ្រុប <b>ស្វែងរកស្នេហ៍😘</b> ធានាថាមិនខ្វះគូទេ! "
                "សាកវាយ <b>/match</b> មើលគូស្នេហ៍ថ្ងៃនេះ ឬវាយ <b>/flirt</b> យកពាក្យញ៉ែទៅញ៉ែ Crush មើលទៅ! 💘😉"
            )
        elif any(k in text for k in ["ស្រឡាញ់", "crush", "លួចស្រឡាញ់"]):
            reply = (
                f"បើលួចស្រឡាញ់គេ កុំទុកយូរប្រយ័ត្នគេឆក់បាត់ណា៎ {user_name}! 🫣 "
                "អាចប្រើពាក្យបញ្ជា <code>/crush @Username សារ</code> ដើម្បីផ្ញើសារសារភាពស្នេហ៍សម្ងាត់ដោយលាក់ឈ្មោះបានណា៎! 💌🌹"
            )
        elif any(k in text for k in ["ខូចចិត្ត", "sad", "ឈឺចាប់"]):
            reply = (
                f"កុំពិបាកចិត្តអី {user_name}! មនុស្សម្នាក់ចាកចេញ គឺដើម្បីទុកកន្លែងឱ្យមនុស្សល្អពិតប្រាកដម្នាក់ទៀតចូលមក! "
                "ញញឹមឡើង មនុស្សល្អរបស់អ្នកកំពុងរង់ចាំអ្នកនៅខាងមុខនេះហើយ! 💖🌻"
            )
        else:
            reply = (
                f"សួស្តី {user_name}! ស្វាគមន៍មកកាន់ <b>ស្វែងរកស្នេហ៍😘</b> 💘\n\n"
                "តើថ្ងៃនេះអ្នកចង់៖\n"
                "• ផ្គូផ្គងគូស្នេហ៍? វាយ <b>/match</b>\n"
                "• វាស់ភាគរយស្នេហា? វាយ <b>/love [ឈ្មោះ]</b>\n"
                "• អានពាក្យញ៉ែផ្អែមល្ហែម? វាយ <b>/flirt</b>\n"
                "• ទស្សន៍ទាយរាសីស្នេហ៍? វាយ <b>/fortune</b>\n"
                "• សារភាពស្នេហាសម្ងាត់? វាយ <b>/crush</b>\n\n"
                "<i>សូមរីករាយជាមួយពេលវេលាដ៏ផ្អែមល្ហែមក្នុងគ្រុប!</i> 🌹✨"
            )
        try:
            await message.reply_text(reply, parse_mode="HTML")
        except Exception:
            await message.reply_text(reply.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace("<code>", "").replace("</code>", ""))

def build_bot3_app(token: str) -> Application:
    """Build and configure Bot 3 Application (ស្វែងរកស្នេហ៍😘 @LoveFinderKh_bot)."""
    request = HTTPXRequest(connect_timeout=60.0, read_timeout=60.0, write_timeout=60.0, pool_timeout=60.0)
    app = ApplicationBuilder().token(token).request(request).build()

    # 1. Anti-link filter (High priority in group -1)
    app.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS & (
                filters.Entity("url")
                | filters.Entity("text_link")
                | filters.CaptionEntity("url")
                | filters.CaptionEntity("text_link")
                | filters.Regex(LINK_REGEX)
            ),
            anti_link_filter,
        ),
        group=-1,
    )

    # 2. Commands (group 0)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("match", match_command))
    app.add_handler(CommandHandler("couple", match_command))
    app.add_handler(CommandHandler("love", love_command))
    app.add_handler(CommandHandler("flirt", flirt_command))
    app.add_handler(CommandHandler("pickup", flirt_command))
    app.add_handler(CommandHandler("fortune", fortune_command))
    app.add_handler(CommandHandler("destiny", fortune_command))
    app.add_handler(CommandHandler("crush", crush_command))
    app.add_handler(CommandHandler("truth", truth_command))
    app.add_handler(CommandHandler("dare", dare_command))

    # 3. New member service messages
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # 4. Text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.error and "Message to be replied not found" in str(context.error):
            logger.info(f"Handled deleted message gracefully: {context.error}")
            return
        logger.error(f"Telegram error in Bot 3: {context.error}")

    app.add_error_handler(error_handler)

    return app
