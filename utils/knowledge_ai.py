import logging
import random
import httpx
import config
from utils.general_knowledge import get_random_fact, get_random_quiz

logger = logging.getLogger("KnowledgeAI")

SYSTEM_PROMPT = """You are the AI Assistant for "ក្រុមចែករំលែកចំណេះដឹង" (Telegram Bot: @sharelearningkh_bot). 
Your mission is to serve as a knowledgeable, smart, encouraging, and friendly educational guide for Cambodian users.

### CORE OBJECTIVES & DOMAINS:
1. Provide accurate, clear, and easy-to-understand explanations on general knowledge topics, including:
   - Science, Technology, and Digital Literacy
   - World and Cambodian History, Culture, and Geography
   - Personal Development, Study Habits, and Productivity Tips
   - Health basics, Environmental awareness, and Daily Life hacks
   - Business, Financial literacy, and Entrepreneurship basics

### LANGUAGE & TONE:
- Primary Language: Natural, polite, grammatically correct Khmer (ភាសាខ្មែរ).
- If the user asks in English or another language, reply in that language, but maintain the same warm and informative persona.
- Tone: Friendly, respectful, intellectually curious, encouraging, and structured (ដូចជាមិត្តភក្តិដែលចេះដឹង និងចូលចិត្តចែករំលែក).
- Address users politely (e.g., "សួស្តីបាទ/ចាស", "បងប្អូន", "មិត្តអ្នកអាន").

### FORMATTING GUIDELINES:
- Use bullet points, bold text, and numbered lists to make explanations easy to scan on mobile devices (Telegram).
- Avoid long, unbroken blocks of text.
- If a question is complex, break down the answer into:
  1. សេចក្ដីសង្ខេបខ្លី (Short Summary)
  2. ចំណុចសំខាន់ៗ (Key Explanations/Points)
  3. ការអនុវត្ត ឬគន្លឹះបន្ថែម (Actionable Tips or Takeaways)

### STRICT RULES & ETHICS:
- Accuracy: State verified facts. If unsure or if information is outdated, honestly acknowledge the limitation.
- Safety: Do not provide dangerous medical prescriptions, illegal instructions, or harmful financial gambling advice.
- Group Chat Behavior: Keep answers concise yet comprehensive so it doesn't flood the chat, but offer to expand if members want more details.
"""

STUDY_TIPS = [
    (
        "🧠 <b>បច្ចេកទេសរៀន Pomodoro (២៥/៥)៖</b>\n\n"
        "1. <b>កំណត់គោលដៅ៖</b> ជ្រើសរើសមេរៀន ឬការងារ ១ មុខដែលត្រូវធ្វើ\n"
        "2. <b>កំណត់ម៉ោង៖</b> រៀនផ្ដោតអារម្មណ៍រយៈពេល ២៥ នាទី (មិនប៉ះទូរស័ព្ទ)\n"
        "3. <b>សម្រាកខ្លី៖</b> សម្រាក ៥ នាទី (ញ៉ាំទឹក ដើរលំហែ)\n"
        "4. <b>ធ្វើ ៤ ជុំ៖</b> សម្រាកវែងពី ១៥ ទៅ ៣០ នាទី!\n\n"
        "💡 <i>ជួយបង្កើនការចងចាំ និងមិនងាយនឿយហត់ខួរក្បាល!</i>"
    ),
    (
        "📚 <b>បច្ចេកទេស Feynman Technique (រៀនដោយការពន្យល់)៖</b>\n\n"
        "1. <b>ជ្រើសរើសប្រធានបទ៖</b> សរសេរចំណងជើងលើក្រដាស\n"
        "2. <b>ពន្យល់ដូចបង្រៀនក្មេងអាយុ ៨ ឆ្នាំ៖</b> ប្រើពាក្យសាមញ្ញបំផុត គ្មានពាក្យបច្ចេកទេសស្មុគស្មាញ\n"
        "3. <b>រកចំណុចដែលទាល់៖</b> ត្រឡប់ទៅបើកសៀវភៅមើលឡើងវិញ\n"
        "4. <b>សម្រួលឱ្យកាន់តែសាមញ្ញ៖</b> ប្រើឧទាហរណ៍ជាក់ស្តែងប្រចាំថ្ងៃ!\n\n"
        "💡 <i>បើអ្នកមិនអាចពន្យល់ឱ្យក្មេងយល់បានទេ មានន័យថាអ្នកមិនទាន់យល់ច្បាស់ឡើយ!</i>"
    ),
    (
        "⏰ <b>វិធីគ្រប់គ្រងពេលវេលា Time Blocking៖</b>\n\n"
        "• បែងចែកម៉ោងក្នុងមួយថ្ងៃជាប្លុកៗ (Block)\n"
        "• ពេលព្រឹក (ខួរក្បាលស្រឡះ)៖ ធ្វើការងារដែលពិបាកបំផុត (Deep Work)\n"
        "• ពេលរសៀល៖ ធ្វើការងារទូទៅ ឆ្លើយសារ អានសៀវភៅ\n"
        "• យប់៖ រៀបចំផែនការសម្រាប់ថ្ងៃស្អែក ៣ ចំណុចសំខាន់ៗ!"
    ),
    (
        "💧 <b>ទម្លាប់សុខភាពខួរក្បាលល្អ៖</b>\n\n"
        "• <b>ផឹកទឹក៖</b> ខួរក្បាលមានជាតិទឹករហូតដល់ ៧៥% ខ្វះទឹកធ្វើឱ្យថយចុះការផ្តោតអារម្មណ៍\n"
        "• <b>គេងឱ្យគ្រប់ ៧-៨ ម៉ោង៖</b> អំឡុងពេលគេង ខួរក្បាលរៀបចំការចងចាំឱ្យមានរបៀប\n"
        "• <b>ហាត់ប្រាណស្រាលៗ៖</b> បង្កើនអុកស៊ីសែនទៅកាន់ខួរក្បាល និងកាត់បន្ថយស្ត្រេស!"
    ),
]

def get_random_tip() -> str:
    return random.choice(STUDY_TIPS)

async def _call_gemini_api(prompt: str) -> str:
    """Call Google Gemini API if key is provided."""
    api_key = config.GEMINI_API_KEY
    if not api_key:
        return ""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
            else:
                logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")

    return ""

async def _call_openai_api(prompt: str) -> str:
    """Call OpenAI API if key is provided."""
    api_key = config.OPENAI_API_KEY
    if not api_key:
        return ""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                return text.strip()
            else:
                logger.warning(f"OpenAI API returned status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")

    return ""

def _smart_offline_reply(user_query: str, user_name: str = "") -> str:
    """Intelligent structured Khmer educational answer when no API key is set."""
    t = user_query.lower()
    name = f" {user_name}" if user_name else ""

    # 1. សួស្តី / Greeting
    if any(k in t for k in ["សួស្តី", "hello", "hi", "ជម្រាបសួរ"]):
        return (
            f"សួស្តីបាទ/ចាស{name}! ស្វាគមន៍មកកាន់ <b>ក្រុមចែករំលែកចំណេះដឹង ♻️💯</b>\n\n"
            "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចក្នុងការជួយឆ្លើយសំណួរទាក់ទងនឹង វិទ្យាសាស្ត្រ បច្ចេកវិទ្យា ប្រវត្តិសាស្ត្រ "
            "ការអភិវឌ្ឍខ្លួន និងចំណេះដឹងទូទៅ។\n\n"
            "👉 តើអ្នកមានចម្ងល់ ឬប្រធានបទអ្វីចង់ពិភាក្សាថ្ងៃនេះដែរ?"
        )

    # 2. បច្ចេកវិទ្យា / AI / បញ្ញាសិប្បនិម្មិត
    if any(k in t for k in ["ai", "បញ្ញាសិប្បនិម្មិត", "artificial intelligence", "កុំព្យូទ័រ", "បច្ចេកវិទ្យា", "tech"]):
        return (
            "🤖 <b>អ្វីទៅជាបញ្ញាសិប្បនិម្មិត (Artificial Intelligence - AI)?</b>\n\n"
            "<b>១. សេចក្ដីសង្ខេប៖</b>\n"
            "AI គឺជាបច្ចេកវិទ្យាដែលធ្វើឱ្យម៉ាស៊ីន ឬកុំព្យូទ័រអាចគិត រៀនសូត្រ និងដោះស្រាយបញ្ហាដូចខួរក្បាលមនុស្ស។\n\n"
            "<b>២. ចំណុចសំខាន់ៗ៖</b>\n"
            "• <b>Machine Learning (ML)៖</b> កុំព្យូទ័ររៀនតាមរយៈទិន្នន័យ (Data) ដោយមិនបាច់សរសេរកូដប្រាប់គ្រប់ជំហាន\n"
            "• <b>Natural Language Processing (NLP)៖</b> ជួយឱ្យកុំព្យូទ័រយល់ និងឆ្លើយតបភាសាមនុស្ស (ដូចជា ChatGPT/Gemini)\n"
            "• <b>Computer Vision៖</b> ជួយឱ្យកុំព្យូទ័រមើលឃើញ និងស្គាល់រូបភាព/វីដេអូ\n\n"
            "<b>៣. ការអនុវត្តក្នុងជីវិតប្រចាំថ្ងៃ៖</b>\n"
            "• ប្រព័ន្ធ Face Unlock លើទូរស័ព្ទ\n"
            "• ការណែនាំវីដេអូលើ YouTube / TikTok\n"
            "• ការបកប្រែភាសាស្វ័យប្រវត្តិ ដូចជា Google Translate!"
        )

    # 3. ប្រាសាទអង្គរវត្ត / ប្រវត្តិសាស្ត្រខ្មែរ
    if any(k in t for k in ["អង្គរវត្ត", "ប្រាសាទ", "ប្រវត្តិសាស្ត្រ", "ជ័យវរ្ម័ន", "សូរ្យវរ្ម័ន", "ខ្មែរ"]):
        return (
            "🇰🇭 <b>ប្រវត្តិសង្ខេបនៃប្រាសាទអង្គរវត្ត</b>\n\n"
            "<b>១. សេចក្ដីសង្ខេប៖</b>\n"
            "ប្រាសាទអង្គរវត្ត ជាស្នាដៃស្ថាបត្យកម្មកំពូលនៃអាណាចក្រខ្មែរ និងជាសំណង់សាសនាដ៏ធំបំផុតលើពិភពលោក។\n\n"
            "<b>២. ចំណុចសំខាន់ៗគួរដឹង៖</b>\n"
            "• <b>អ្នកកសាង៖</b> ព្រះបាទសូរ្យវរ្ម័នទី២ នៅដើមសតវត្សរ៍ទី១២ (គ.ស ១១១៣-១១៥០)\n"
            "• <b>សាសនាដើម៖</b> ឧទ្ទិសថ្វាយព្រះវិស្ណុ ក្នុងព្រហ្មញ្ញសាសនា ក្រោយមកក្លាយជាពុទ្ធសាសនា\n"
            "• <b>ផ្ទៃដី៖</b> ប្រមាណ ១៦២.៦ ហិកតា ព័ទ្ធជុំវិញដោយកសិន្ធុទឹកដ៏ធំល្វឹងល្វើយ\n\n"
            "<b>៣. តម្លៃបេតិកភណ្ឌ៖</b>\n"
            "ត្រូវបានអង្គការ UNESCO ចុះបញ្ជីជាសម្បត្តិបេតិកភណ្ឌពិភពលោកនៅឆ្នាំ ១៩៩២!"
        )

    # 4. ការសិក្សា / បច្ចេកទេសរៀន
    if any(k in t for k in ["រៀន", "ការសិក្សា", "study", "ប្រឡង", "ចងចាំ", "គន្លឹះ"]):
        return (
            "📚 <b>គន្លឹះ ៣ យ៉ាងជួយឱ្យការរៀនកាន់តែមានប្រសិទ្ធភាព៖</b>\n\n"
            "<b>១. កុំរៀនទន្ទេញតែមួយមុខ ត្រូវរៀនឱ្យយល់ (Active Recall)៖</b>\n"
            "ក្រោយពេលអានមេរៀនចប់ សូមបិទសៀវភៅ ហើយសរសេរ ឬសូត្រឡើងវិញនូវអ្វីដែលអ្នកចាំ។ វិធីនេះជួយឱ្យខួរក្បាលចងចាំបានយូរជាងការអានដដែលៗ។\n\n"
            "<b>២. ប្រើបច្ចេកទេស Pomodoro (២៥/៥)៖</b>\n"
            "រៀនផ្តោតអារម្មណ៍ ២៥ នាទី រួចសម្រាក ៥ នាទី។ ធ្វើបែបនេះ ៤ ដង រួចសម្រាកវែង ១៥-៣០ នាទី។\n\n"
            "<b>៣. បង្រៀន ឬពន្យល់អ្នកដទៃ (Feynman Technique)៖</b>\n"
            "សាកល្បងពន្យល់មេរៀនដែលទើបតែរៀនចប់ ទៅកាន់មិត្តភក្តិ។ បើអ្នកអាចពន្យល់បានច្បាស់ មានន័យថាអ្នកយល់មេរៀននោះ ១០០%!"
        )

    # 5. សុខភាព / ផឹកទឹក / ការគេង
    if any(k in t for k in ["សុខភាព", "ទឹក", "គេង", "health", "ចំណីអាហារ", "ហាត់ប្រាណ"]):
        return (
            "🌿 <b>គន្លឹះសុខភាពទូទៅគួរដឹងសម្រាប់រាងកាយរឹងមាំ៖</b>\n\n"
            "<b>១. ជាតិទឹកគ្រប់គ្រាន់៖</b>\n"
            "មនុស្សពេញវ័យគួរទទួលទានទឹកពី ២ ទៅ ៣ លីត្រជារៀងរាល់ថ្ងៃ ដើម្បីជួយដល់ការរំលាយអាហារ និងសុខភាពស្បែក។\n\n"
            "<b>២. ដំណេកគ្រប់គ្រាន់៖</b>\n"
            "ការគេងពី ៧ ទៅ ៨ ម៉ោងក្នុងមួយយប់ ជួយឱ្យខួរក្បាលជួសជុលកោសិកា និងពង្រឹងប្រព័ន្ធការពាររាងកាយ។\n\n"
            "<b>៣. ចលនារាងកាយ៖</b>\n"
            "ដើរ ឬហាត់ប្រាណស្រាលៗយ៉ាងហោចណាស់ ៣០ នាទីក្នុងមួយថ្ងៃ កាត់បន្ថយហានិភ័យនៃជំងឺបេះដូង និងកាត់បន្ថយភាពតានតឹង!"
        )

    # 6. Default response: structured and encouraging
    return (
        f"💡 <b>សូមអរគុណសម្រាប់សំណួរ{name}!</b>\n\n"
        f"ទាក់ទងនឹងប្រធានបទនេះ ខ្ញុំសូមចែករំលែកសង្ខេបដូចខាងក្រោម៖\n\n"
        f"• <b>ចំណុចគោល៖</b> {user_query} គឺជាប្រធានបទដ៏គួរឱ្យចាប់អារម្មណ៍មួយក្នុងចំណេះដឹងទូទៅ។\n"
        f"• <b>គន្លឹះស្វែងយល់បន្ថែម៖</b> អ្នកអាចសាកល្បងវាយពាក្យបញ្ជា /fact ដើម្បីមើលចំណេះដឹងទូទៅប្លែកៗ ឬ /quiz ដើម្បីល្បងប្រាជ្ញា!\n\n"
        f"<i>ប្រសិនបើអ្នកមានសំណួរលម្អិតជាក់លាក់ សូមសួរដោយសេរី!</i> 📚✨"
    )

async def generate_knowledge_reply(prompt: str, user_name: str = "") -> str:
    """Generate educational reply via Gemini, OpenAI, or smart offline engine."""
    # Try Gemini API if key configured
    if config.GEMINI_API_KEY:
        ans = await _call_gemini_api(prompt)
        if ans:
            return ans

    # Try OpenAI API if key configured
    if config.OPENAI_API_KEY:
        ans = await _call_openai_api(prompt)
        if ans:
            return ans

    # Offline high-quality smart knowledge responder
    return _smart_offline_reply(prompt, user_name)
