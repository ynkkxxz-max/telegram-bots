import logging
import random
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
from utils.khmer_jokes import (
    get_random_joke,
    get_random_riddle,
    get_random_encouragement,
    get_random_greeting,
)
from utils.general_knowledge import (
    get_random_fact,
    get_random_quiz,
)
from utils.ai_helper import generate_bot_reply
from utils.sticker_manager import (
    get_random_sticker,
    add_sticker,
)

logger = logging.getLogger("Bot1_Funny")

# Regex to detect links in chat messages
LINK_REGEX = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+|bit\.ly/\S+)",
    re.IGNORECASE,
)

# List of keywords that trigger automatic response/teasing in groups
TRIGGER_KEYWORDS = [
    "single", "crush", "សង្សារ", "ស្រឡាញ់", "នៅលីវ", "ការ",
    "លុយ", "ប្រាក់ខែ", "អស់លុយ", "លុយខែ",
    "កាហ្វេ", "តែគុជ", "cafe", "coffee",
    "ហត់", "នឿយ", "ធុញ", "ស្ត្រេស", "stress", "ឈឺក្បាល", "ខូចចិត្ត",
    "ឃ្លាន", "បាយ", "ញ៉ាំ", "food",
    "គេង", "ងងុយ", "sleep", "good night", "រាត្រីសួស្តី",
    "ស្ទះផ្លូវ", "traffic",
    "កំប្លែង", "សើច", "funny", "joke",
    "sticker", "ស្ទីកឃ័រ", "ស្ទីគ័រ",
    "ចំណេះដឹង", "fact", "quiz", "ដឹងអត់", "សំណួរ", "សួរ",
    "សួស្តី", "hello", "hi", "hey", "ហាយ",
    "កំពង់ធំ", "សៀមរាប", "ភ្នំពេញ", "បាត់ដំបង", "កំពត", "ព្រះសីហនុ", "កំពង់សោម", "ខេត្ត", "ចម្ងាយ", "ប៉ុន្មានម៉ោង",
    "+", "-", "*", "/", "=", "គុណ", "បូក", "ដក", "ចែក", "ស្មើប៉ុន្មាន", "ប៉ុន្មាន",
]

def get_friendly_name(update: Update) -> str:
    """Return a natural friendly name, avoiding 'Group', 'Channel', or anonymous bot names."""
    user = update.effective_user
    msg = update.effective_message

    # If sent anonymously or as channel/group
    if msg and msg.sender_chat:
        return random.choice(["មេគ្រុប", "គ្នាយើង", "bro/sis", "ពួកម៉ាក"])

    if user and user.first_name:
        first = user.first_name.strip()
        if first.lower() in ["group", "channel", "group anonymous bot", "telegram"]:
            return random.choice(["មេគ្រុប", "គ្នាយើង", "bro/sis", "ពួកម៉ាក"])
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
    """Detect and delete link messages in groups from non-admin members."""
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if not message or not chat or not user:
        return

    # Anti-link only operates in groups/supergroups
    if chat.type == "private":
        return

    # Check text or caption
    raw_text = message.text or message.caption or ""

    # Check Telegram entities
    has_link_entity = False
    entities = message.entities or message.caption_entities or []
    for ent in entities:
        if ent.type in ["url", "text_link"]:
            has_link_entity = True
            break

    contains_link = has_link_entity or bool(LINK_REGEX.search(raw_text))
    if not contains_link:
        return

    # Check if sender is admin or creator
    try:
        member = await chat.get_member(user.id)
        if member.status in ["creator", "administrator"]:
            return  # Allow admin to post links
    except Exception as e:
        logger.warning(f"Could not verify admin status: {e}")

    # Delete the message if sent by a regular member
    try:
        await message.delete()
        name = get_friendly_name(update)
        warn = await chat.send_message(
            f"⚠️ នែ {name}! គ្រុបនេះមិនអនុញ្ញាតឱ្យផ្ញើ Link ឬផ្សាយពាណិជ្ជកម្មទេណា bro/sis! សុំលុបចោលហើយ! 😜🚫"
        )
        asyncio.create_task(delete_after_delay(warn, 7))
        raise ApplicationHandlerStop
    except ApplicationHandlerStop:
        raise
    except Exception as e:
        logger.warning(f"Cannot delete link (Make sure bot is group Admin with Delete Messages permission): {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    name = get_friendly_name(update)
    msg = (
        f"សួស្តី {name}! ខ្ញុំជា <b>Bot មិត្តភក្តិប្រចាំគ្រុប</b> (@funnychatkh_bot) 😎🎉\n\n"
        "ខ្ញុំនៅទីនេះដើម្បីកំដរជជែក ចំអន់លេង ការពារគ្រុបពី Link Spam ចែករំលែកចំណេះដឹងទូទៅ និងធ្វើឱ្យគ្រុបកក្រើកដោយសំណើច! 😂🔥\n\n"
        "<b>ពាក្យបញ្ជាកម្សាន្ត និងចំណេះដឹង៖</b>\n"
        "👉 /fact - ចំណេះដឹងទូទៅប្លែកៗគួរឱ្យចាប់អារម្មណ៍ 💡\n"
        "👉 /quiz - ល្បងប្រាជ្ញាចំណេះដឹងទូទៅ (Poll Quiz) 🎯\n"
        "👉 /joke - ស្តាប់រឿងកំប្លែង\n"
        "👉 /riddle - លេងពាក្យបណ្តៅ (មានលាក់ចម្លើយ)\n"
        "👉 /encourage - លើកទឹកចិត្តពេលហត់ ឬស្ត្រេស\n"
        "👉 /tease - ឱ្យ Bot ចំអន់លេងមួយកំប្លែង 😜\n"
        "👉 /single - ចំអន់អ្នកនៅលីវ (Single) 🤣💔\n"
        "👉 /sticker - លេង Sticker កំប្លែងៗ 🎭\n"
        "👉 /game - លេងបោះគ្រាប់ឡុកឡាក់ 🎲\n"
        "👉 /help - មើលរបៀបលេង\n\n"
        "🛡️ <i>ប្រព័ន្ធ Anti-Link៖ បើកដំណើរការលុប Link ស្វ័យប្រវត្តិ!</i>"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    msg = (
        "<b>របៀបលេងជាមួយខ្ញុំគ្នាយើង៖</b> 😜\n"
        "1. ហៅខ្ញុំក្នុងគ្រុប៖ @funnychatkh_bot ឬ Reply លើសារ/Sticker ខ្ញុំ\n"
        "2. ចំណេះដឹងទូទៅ៖ /fact (ចំណេះដឹង), /quiz (សំណួរល្បងប្រាជ្ញា)\n"
        "3. កម្សាន្ត៖ /joke, /riddle, /encourage, /tease, /single, /sticker, /game\n"
        "4. និយាយពាក្យគន្លឹះដូចជា៖ single, crush, លុយ, ហត់, កាហ្វេ, ចំណេះដឹង... ខ្ញុំនឹងឆ្លើយតបភ្លាម! 😂🔥\n"
        "5. 🛡️ ហាមផ្ញើ Link ផ្សាយពាណិជ្ជកម្មក្នុងគ្រុប បើមិនមែនជា Admin ទេ ខ្ញុំលុបភ្លាម! 😜🚫"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /fact command: share a fascinating knowledge fact."""
    fact = get_random_fact()
    await update.message.reply_text(
        f"💡 <b>ចំណេះដឹងទូទៅគួរដឹង៖</b>\n\n{fact}",
        parse_mode="HTML"
    )

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

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /joke command."""
    joke = get_random_joke()
    await update.message.reply_text(joke)

async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /riddle command."""
    riddle = get_random_riddle()
    text = (
        f"{riddle['question']}\n\n"
        f"<i>(ចុចលើប្រអប់ខ្មៅខាងក្រោមដើម្បីមើលចម្លើយ)</i>\n"
        f"👉 <tg-spoiler>{riddle['answer']}</tg-spoiler>"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def encourage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /encourage command."""
    enc = get_random_encouragement()
    await update.message.reply_text(enc)

async def tease_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /tease command."""
    name = get_friendly_name(update)
    teases = [
        f"អីយ៉ា {name}! មុខស្អាតបាតចឹង ម៉េចក៏នៅស្ងាត់ម្ល៉េះ? ប្រយ័ត្ន Crush គេឆក់យកបាត់ណា! 😜🔥",
        f"នែ {name}! ថ្ងៃនេះញ៉ាំបាយប៉ុន្មានចានហើយ? ឃើញស្ងាត់ៗម៉េចដឹង ដល់ពេលឃ្លានស៊ីដូចព្យុះ! 🤣🍚",
        f"ឃើញមុខស្ងប់ស្ងាត់ចឹង តាមពិតកំពុងលួចស្រឡាញ់សមាជិកក្នុងគ្រុបនេះមែនទេ {name}? 🤫❤️👰",
        f"កុំធ្វើមុខស្អុយពេក {name}! ញញឹមមួយមក ស្អាតដូចតារាហុងកុងហើយ! 😜💅",
        f"នែ {name}! ឃើញដើរញញឹមម្នាក់ឯង... ប្រយ័ត្នគេគិតថាវិកលចរិតណា bro! 🤣🤪",
        f"អីយ៉ា {name} ថ្ងៃនេះតែងខ្លួនឡើង Cute! ចង់ទៅណាត់ជួបអ្នកណាប្រាប់គ្នាយើងត្រង់ៗមក! 💄👗✨",
        f"ដឹងខ្លួនអត់ {name}? សំឡេងសើចរបស់ឯងឮដល់ភពព្រះអង្គារហើយ! 🤣🚀",
        f"នែ {name}! កុំលេងទូរស័ព្ទច្រើនពេក ប្រយ័ត្នទូរស័ព្ទធ្លាក់ត្រូវច្រមុះកំពិតណា! 📱👃😂",
    ]
    await update.message.reply_text(random.choice(teases))

async def single_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /single command."""
    name = get_friendly_name(update)
    single_jokes = [
        f"នៅ Single មែនទេ {name}? 🤣 មិនអីទេ ជីវិត Single ឡូយណាស់ ចង់ញ៉ាំអីញ៉ាំហ្នឹង គ្មានអ្នកណាទារ Password Facebook ទេ! 😎🔥",
        f"គេថា 'មនុស្សស្អាតៗច្រើនតែនៅ Single'... {name} អានហើយញញឹមបិទមាត់មិនជិតទេ! 😜💅✨",
        f"Crush គេមិនចាប់អារម្មណ៍មែនទេ {name}? មិនអីទេ មកចាប់អារម្មណ៍ Bot វិញ ឆ្លើយតប ២៤ ម៉ោង មិនដែលទុកឱ្យខូចចិត្តទេ! ❤️🤖",
        f"កុំពិបាកចិត្តរឿងនៅ Single ណា {name}! យ៉ាងហោចណាស់ក៏យើងសន្សំលុយបានច្រើន... យកទៅទិញតែគុជ និងបាយមាន់ស៊ីឱ្យឆ្អែតទៅ! 🧋🍗😋",
        f"នៅ Single យូរពេក ឥឡូវសូម្បីតែស្រមោលខ្លួនឯងក៏មើលទៅដូចគូដណ្តឹងដែរ {name}! 🤣👤💍",
        f"ស្ថានភាព {name} ពេលនេះ៖ គេស្រឡាញ់យើង យើងមិនស្រឡាញ់គេ... ដល់ពេលយើងស្រឡាញ់គេ គេទៅការចោលបាត់! 😭💔🥀",
        f"នែ {name}! គេចូលរោងការអស់ហើយ នៅឡើយតែយើងអង្គុយចាំចងដៃគេ! 💌👰🤵😂",
        f"នៅ Single មិនមែនគ្មានជម្រើសទេ គឺគ្មានអ្នកណាគេរើសសោះហ្មង! 😜🤣✌️",
    ]
    await update.message.reply_text(random.choice(single_jokes))
    try:
        await update.message.reply_sticker(sticker=get_random_sticker())
    except Exception:
        pass

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /game command (animated dice)."""
    msg = await update.message.reply_dice(emoji="🎲")
    value = msg.dice.value

    if value == 6:
        comment = "🔥 វ៉ោវ! គ្រាប់ ៦ ហ្មង bro! ហេងកប់ក្ដោង ត្រូវរង្វាន់ធំហើយ! 🥳🎉"
    elif value >= 4:
        comment = f"😎 បានគ្រាប់ {value}! ពិន្ទុមិនធម្មតាទេ sis/bro ឡូយណាស់! 👏"
    elif value >= 2:
        comment = f"😜 បានគ្រាប់ {value}! ស្ទើរតែឈ្នះហើយ សាកល្បងម្ដងទៀតមើល! 🎲"
    else:
        comment = "🤣 បានតែគ្រាប់ ១ ទេពួកម៉ាក? មិនអីទេ សំណាងស្នេហាវិញហ្នឹង! ❤️😂"

    await update.message.reply_text(comment)

async def sticker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /sticker command: send a random funny sticker."""
    sticker_id = get_random_sticker()
    try:
        await update.message.reply_sticker(sticker=sticker_id)
    except Exception as e:
        logger.error(f"Failed to send sticker: {e}")
        await update.message.reply_text("🎭 ផ្ញើ Sticker មកលេងមួយមក bro ខ្ញុំចាំរៀនទុកលេងវិញ! 😜")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming stickers: learn them and reply back with fun stickers/comments."""
    message = update.message
    if not message or not message.sticker:
        return

    chat = update.effective_chat
    name = get_friendly_name(update)
    bot = context.bot

    file_id = message.sticker.file_id
    add_sticker(file_id)

    is_private = chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == bot.id
    )

    if is_private or is_reply_to_bot:
        comments = [
            f"Sticker នេះឡូយម៉េះ {name}! 😂 ខ្ញុំសុំ Save ទុកលេងដែរហើយ! 🔥",
            f"មុខដូច Sticker ហ្នឹងបេះបិទ bro/sis! 🤣😜",
            f"Sticker ត្រូវចិត្តហ្មងពួកម៉ាក! តោះតបមួយវិញ! 😎",
            f"ហាហា Sticker អីក៏គួរឱ្យស្រឡាញ់ម្ល៉េះ! 😜❤️",
        ]
        await message.reply_text(random.choice(comments))

        try:
            counter_sticker = get_random_sticker()
            await message.reply_sticker(sticker=counter_sticker)
        except Exception as e:
            logger.error(f"Failed to reply sticker: {e}")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members joined group with funny greeting."""
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        name = member.first_name
        welcomes = [
            f"🎉 ស្វាគមន៍គ្នាយើង {name} ចូលមកកាន់គ្រុប! ចូលមកហើយកុំភ្លេចប៉ាវកាហ្វេផងណា bro/sis! ☕️😜",
            f"👋 Hello {name}! ស្វាគមន៍មកកាន់គ្រុបនិយាយគ្នាលេង! ចូលមកឱ្យតែសប្បាយ កុំប្រកាន់ច្រើនណាពួកម៉ាក! 😂🔥",
            f"✨ អីយ៉ា! សមាជិកថ្មី {name} មកដល់ហើយ! សូមស្វាគមន៍យ៉ាងកក់ក្តៅពី Bot មិត្តភក្តិប្រចាំគ្រុប! 😎🙌",
        ]
        await update.message.reply_text(random.choice(welcomes))
        try:
            await update.message.reply_sticker(sticker=get_random_sticker())
        except Exception:
            pass

async def process_chat_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Internal processor for text and unknown command messages."""
    chat = update.effective_chat
    bot = context.bot
    user_name = get_friendly_name(update)
    message = update.message

    is_private = chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == bot.id
    )
    is_mentioned = bot.username and f"@{bot.username.lower()}" in text.lower()

    text_lower = text.lower()
    has_keyword = any(k in text_lower for k in TRIGGER_KEYWORDS)

    # In groups: respond if private, replied to bot, mentioned, OR message has keywords!
    should_respond = is_private or is_reply_to_bot or is_mentioned or has_keyword

    if should_respond:
        if any(k in text_lower for k in ["fact", "ចំណេះដឹង", "ដឹងអត់"]):
            fact = get_random_fact()
            await message.reply_text(f"💡 <b>ចំណេះដឹងទូទៅ៖</b>\n\n{fact}", parse_mode="HTML")
            return

        wants_sticker = any(k in text_lower for k in ["sticker", "ស្ទីកឃ័រ", "ស្ទីគ័រ", "ស្ទីកគឺ", "ស្ទិកគ័រ"])

        cleaned_text = text
        if bot.username:
            cleaned_text = cleaned_text.replace(f"@{bot.username}", "").replace(f"@{bot.username.lower()}", "").strip()

        await context.bot.send_chat_action(chat_id=chat.id, action="typing")

        reply = await generate_bot_reply(cleaned_text if cleaned_text else text, user_name)
        try:
            await message.reply_text(reply, parse_mode="HTML")
        except Exception as e:
            if "Message to be replied not found" in str(e):
                await context.bot.send_message(chat_id=chat.id, text=reply, parse_mode="HTML")
            else:
                logger.error(f"Failed to send text reply: {e}")

        if wants_sticker or random.random() < 0.25:
            try:
                await message.reply_sticker(sticker=get_random_sticker())
            except Exception as e:
                logger.error(f"Failed to send random sticker: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle chat messages in private and groups."""
    message = update.message
    if not message or not message.text:
        return
    await process_chat_text(update, context, message.text)

async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands like /single, /crush, etc."""
    message = update.message
    if not message or not message.text:
        return
    raw_text = message.text.lstrip("/")
    await process_chat_text(update, context, raw_text)

from telegram.request import HTTPXRequest

def build_bot1_app(token: str) -> Application:
    """Build and configure Bot 1 Application."""
    request = HTTPXRequest(connect_timeout=60.0, read_timeout=60.0, write_timeout=60.0, pool_timeout=60.0)
    app = ApplicationBuilder().token(token).request(request).build()

    # 1. Anti-Link Filter (Runs with high priority in group -1 on all messages with links)
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
    app.add_handler(CommandHandler("fact", fact_command))
    app.add_handler(CommandHandler("know", fact_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("riddle", riddle_command))
    app.add_handler(CommandHandler("encourage", encourage_command))
    app.add_handler(CommandHandler("tease", tease_command))
    app.add_handler(CommandHandler("single", single_command))
    app.add_handler(CommandHandler("sticker", sticker_command))
    app.add_handler(CommandHandler("game", game_command))

    # 3. Service messages: new members
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # 4. Sticker messages
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    # 5. Regular text messages (and unknown commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown_command))

    # Global error handler
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.error and "Message to be replied not found" in str(context.error):
            logger.info(f"Handled deleted message gracefully: {context.error}")
            return
        logger.error(f"Telegram error: {context.error}")

    app.add_error_handler(error_handler)

    return app
