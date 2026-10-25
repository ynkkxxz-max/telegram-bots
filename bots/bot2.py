import logging
import re
import asyncio
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
from utils.general_knowledge import get_random_fact, get_random_quiz
from utils.knowledge_ai import generate_knowledge_reply, get_random_tip
from utils.chinese_lessons import (
    get_chinese_menu,
    get_chinese_level,
    handle_chinese_query,
    get_random_chinese_card,
)
from utils.english_lessons import (
    get_english_menu,
    get_english_level,
    handle_english_query,
    get_random_english_card,
)

logger = logging.getLogger("Bot2_Knowledge")

# Regex to detect links in chat messages
LINK_REGEX = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+|bit\.ly/\S+)",
    re.IGNORECASE,
)

# Trigger keywords for educational queries in groups
KNOWLEDGE_KEYWORDS = [
    "តើ", "អ្វីទៅជា", "ហេតុអ្វី", "ចំណេះដឹង", "ប្រវត្តិ", "ពន្យល់",
    "របៀប", "វិទ្យាសាស្ត្រ", "បច្ចេកវិទ្យា", "ai", "មេរៀន", "រៀន",
    "អង្គរវត្ត", "ខ្មែរ", "ផែនដី", "ភព", "ព្រះអាទិត្យ", "ខួរក្បាល", "បេះដូង",
    "fact", "quiz", "tips", "ចំណេះដឹងទូទៅ",
    "ជួសជុល", "ជុសជុស", "កុំព្យូទ័រ", "computer", "pc", "laptop", "ram", "ssd", "ខូច",
    "រូបវិទ្យា", "ជីវវិទ្យា", "សេដ្ឋកិច្ច", "លុយ", "សន្សំ", "វិនិយោគ", "អាជីវកម្ម", "ទីផ្សារ",
    "កូដ", "coding", "programming", "python", "cyber", "cybersecurity", "hacker", "virus",
    "ចិត្តវិទ្យា", "ដឹកនាំ", "leadership", "អង់គ្លេស", "english", "អវកាស", "ភ្នំ", "everest", "សមុទ្រ",
    "ចិន", "ភាសាចិន", "រៀនចិន", "chinese", "hsk", "pinyin", "hanzi",
    "រៀនអង់គ្លេស", "ភាសាអង់គ្លេស", "grammar", "vocabulary", "idiom", "idioms",
]

def get_user_name(update: Update) -> str:
    user = update.effective_user
    if user and user.first_name:
        first = user.first_name.strip()
        if first.lower() not in ["group", "channel", "telegram", "group anonymous bot"]:
            return first
    return "គ្នាយើង"

async def delete_after_delay(msg, delay_seconds: int = 7):
    """Delete warning message after delay to keep chat clean."""
    await asyncio.sleep(delay_seconds)
    try:
        await msg.delete()
    except Exception:
        pass

async def anti_link_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detect and delete spam link messages in groups from non-admin members."""
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if not message or not chat or not user or chat.type == "private":
        return

    raw_text = message.text or message.caption or ""
    has_link_entity = False
    entities = message.entities or message.caption_entities or []
    for ent in entities:
        if ent.type in ["url", "text_link"]:
            has_link_entity = True
            break

    contains_link = has_link_entity or bool(LINK_REGEX.search(raw_text))
    if not contains_link:
        return

    # Check admin status
    try:
        member = await chat.get_member(user.id)
        if member.status in ["creator", "administrator"]:
            return
    except Exception as e:
        logger.warning(f"Could not verify admin status: {e}")

    try:
        await message.delete()
        name = get_user_name(update)
        warn = await chat.send_message(
            f"⚠️ ជម្រាបសួរ {name}! <b>ក្រុមចែករំលែកចំណេះដឹង ♻️💯</b> មិនអនុញ្ញាតឱ្យផ្ញើ Link ឬផ្សាយពាណិជ្ជកម្មទេបាទ/ចាស! 🚫",
            parse_mode="HTML"
        )
        asyncio.create_task(delete_after_delay(warn, 7))
        raise ApplicationHandlerStop
    except ApplicationHandlerStop:
        raise
    except Exception as e:
        logger.warning(f"Cannot delete link: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    welcome_text = (
        "សួស្តីបាទ/ចាស! ស្វាគមន៍មកកាន់ <b>ក្រុមចែករំលែកចំណេះដឹង ♻️💯</b> (@sharelearningkh_bot)\n\n"
        "ខ្ញុំគឺជា Bot ឆ្លាតវៃដែលត្រៀមខ្លួនជួយចែករំលែក និងឆ្លើយនូវរាល់ចម្ងល់ទាក់ទងនឹង៖\n"
        "• វិទ្យាសាស្ត្រ និងបច្ចេកវិទ្យា 🔬💻\n"
        "• ប្រវត្តិសាស្ត្រ និងវប្បធម៌ 🏛️🇰🇭\n"
        "• ការអភិវឌ្ឍខ្លួន និងការសិក្សា 📚💡\n"
        "• រៀនភាសាអង់គ្លេសបកប្រែខ្មែរ (A1-C2) 🇬🇧✨\n"
        "• រៀនភាសាចិនបកប្រែខ្មែរ (HSK 1-6) 🇨🇳✨\n"
        "• ចំណេះដឹងទូទៅជុំវិញពិភពលោក 🌍✨\n\n"
        "<b>ពាក្យបញ្ជាសំខាន់ៗ៖</b>\n"
        "👉 /english - រៀនភាសាអង់គ្លេសបកប្រែខ្មែរ (កម្រិត ១ ដល់ ៥) 🇬🇧\n"
        "👉 /chinese - រៀនភាសាចិនបកប្រែខ្មែរ (កម្រិត ១ ដល់ ៥) 🇨🇳\n"
        "👉 /fact - ចំណេះដឹងទូទៅប្លែកៗគួរឱ្យចាប់អារម្មណ៍ 💡\n"
        "👉 /quiz - ល្បងប្រាជ្ញាចំណេះដឹងទូទៅ (Poll Quiz) 🎯\n"
        "👉 /tips - គន្លឹះអភិវឌ្ឍខ្លួន និងបច្ចេកទេសរៀនសូត្រ 🧠\n"
        "👉 /help - មើលរបៀបប្រើប្រាស់\n\n"
        "តើអ្នកមានសំណួរអ្វីដែរថ្ងៃនេះ? សូមសរសេរសំណួររបស់អ្នកនៅទីនេះបានភ្លាមៗ! 📖✨"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    help_text = (
        "<b>📖 របៀបប្រើប្រាស់ Bot «ក្រុមចែករំលែកចំណេះដឹង»៖</b>\n\n"
        "1. <b>សួរសំណួរដោយផ្ទាល់៖</b> សរសេរសំណួររបស់អ្នកផ្ញើមកកាន់ Bot ក្នុងឆាតឯកជន ឬ Tag @sharelearningkh_bot ក្នុងគ្រុប\n"
        "2. <b>/english [1-5] ៖</b> រៀនភាសាអង់គ្លេសបកប្រែខ្មែរពីកម្រិតដំបូងដល់កម្រិតខ្ពស់ (A1 - C2)\n"
        "3. <b>/chinese [1-5] ៖</b> រៀនភាសាចិនបកប្រែខ្មែរពីកម្រិតដំបូងដល់កម្រិតខ្ពស់ (HSK 1 - HSK 6)\n"
        "4. <b>/fact ៖</b> អានចំណេះដឹងទូទៅប្លែកៗអំពីវិទ្យាសាស្ត្រ ប្រវត្តិសាស្ត្រ និងកម្ពុជា\n"
        "5. <b>/quiz ៖</b> ចូលរួមលេងសំណួរល្បងប្រាជ្ញាចំណេះដឹងទូទៅ\n"
        "6. <b>/tips ៖</b> ទទួលគន្លឹះអភិវឌ្ឍខ្លួន បច្ចេកទេសគ្រប់គ្រងពេលវេលា និងវិធីរៀនពូកែ\n"
        "7. <b>ការពារគ្រុប៖</b> ប្រព័ន្ធ Anti-Link លុប Link Spam ដោយស្វ័យប្រវត្តិ!"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def english_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /english command: learning English with Khmer translations from level 1 to 5."""
    args = context.args
    if args and args[0].isdigit():
        lvl = int(args[0])
        response_text = get_english_level(lvl)
    else:
        response_text = get_english_menu()
    await update.message.reply_text(response_text, parse_mode="HTML")

async def chinese_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /chinese command: learning Chinese with Khmer translations from level 1 to 5."""
    args = context.args
    if args and args[0].isdigit():
        lvl = int(args[0])
        response_text = get_chinese_level(lvl)
    else:
        response_text = get_chinese_menu()
    await update.message.reply_text(response_text, parse_mode="HTML")

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /fact command."""
    fact = get_random_fact()
    await update.message.reply_text(f"💡 <b>ចំណេះដឹងទូទៅគួរដឹង៖</b>\n\n{fact}", parse_mode="HTML")

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /quiz command: interactive trivia quiz poll."""
    quiz = get_random_quiz()
    await update.message.reply_poll(
        question=quiz["question"],
        options=quiz["options"],
        type="quiz",
        correct_option_id=quiz["correct_id"],
        explanation=quiz["explanation"],
        is_anonymous=False,
    )

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /tips command."""
    tip = get_random_tip()
    await update.message.reply_text(tip, parse_mode="HTML")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new group members warmly."""
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        name = member.first_name or "គ្នាយើង"
        welcome_msg = (
            f"👋 ស្វាគមន៍ {name} ចូលមកកាន់ <b>ក្រុមចែករំលែកចំណេះដឹង ♻️💯</b>!\n\n"
            "សូមរីករាយជាមួយការចែករំលែក និងសាកសួរចំណេះដឹងផ្សេងៗ! បើមានសំណួរ សូម Tag @sharelearningkh_bot បានភ្លាមៗ! 📚💡✨"
        )
        await update.message.reply_text(welcome_msg, parse_mode="HTML")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process incoming educational messages and queries."""
    message = update.message
    if not message or not message.text:
        return

    chat = update.effective_chat
    bot = context.bot
    user_name = get_user_name(update)
    text = message.text

    is_private = chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == bot.id
    )
    is_mentioned = bot.username and f"@{bot.username.lower()}" in text.lower()

    text_lower = text.lower()
    has_keyword = any(k in text_lower for k in KNOWLEDGE_KEYWORDS)

    should_respond = is_private or is_reply_to_bot or is_mentioned or has_keyword

    if should_respond:
        cleaned_text = text
        if bot.username:
            cleaned_text = cleaned_text.replace(f"@{bot.username}", "").replace(f"@{bot.username.lower()}", "").strip()

        await context.bot.send_chat_action(chat_id=chat.id, action="typing")
        query_text = cleaned_text if cleaned_text else text

        chinese_reply = handle_chinese_query(query_text)
        english_reply = handle_english_query(query_text)

        if chinese_reply:
            reply = chinese_reply
        elif english_reply:
            reply = english_reply
        else:
            reply = await generate_knowledge_reply(query_text, user_name)

        try:
            await message.reply_text(reply, parse_mode="HTML")
        except Exception as e:
            if "Message to be replied not found" in str(e):
                await context.bot.send_message(chat_id=chat.id, text=reply, parse_mode="HTML")
            else:
                logger.error(f"Failed to send knowledge reply: {e}")

def build_bot2_app(token: str) -> Application:
    """Build and configure Bot 2 Application (ក្រុមចែករំលែកចំណេះដឹង)."""
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
    app.add_handler(CommandHandler("english", english_command))
    app.add_handler(CommandHandler("en", english_command))
    app.add_handler(CommandHandler("chinese", chinese_command))
    app.add_handler(CommandHandler("cn", chinese_command))
    app.add_handler(CommandHandler("fact", fact_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("tips", tips_command))
    app.add_handler(CommandHandler("ask", handle_message))

    # 3. New member service messages
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # 4. Text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.error and "Message to be replied not found" in str(context.error):
            logger.info(f"Handled deleted message gracefully: {context.error}")
            return
        logger.error(f"Telegram error in Bot 2: {context.error}")

    app.add_error_handler(error_handler)

    return app
