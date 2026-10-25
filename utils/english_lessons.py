"""
English Learning Module with Khmer Translations from Basic to Advanced (A1 - C2).
Includes Word/Phrase, Pronunciation Guide, Khmer Translation, and Practical Examples.
"""
import random
from typing import Dict, List, Optional

ENGLISH_LEVELS: Dict[int, Dict] = {
    1: {
        "title": "កម្រិត ១៖ មូលដ្ឋានគ្រឹះ & ការគួរសម (A1 - Beginner)",
        "desc": "ការស្វាគមន៍ សព្វនាម ការសួរសុខទុក្ខ និងពាក្យគួរសមប្រចាំថ្ងៃ",
        "lessons": [
            {
                "phrase": "Hello / Hi",
                "pronun": "/həˈloʊ/ , /haɪ/",
                "khmer": "សួស្តី",
                "example": "Hello! Nice to meet you. = សួស្តី! រីករាយណាស់ដែលបានស្គាល់អ្នក។"
            },
            {
                "phrase": "Good morning / afternoon / evening",
                "pronun": "/ɡʊd ˈmɔːrnɪŋ/",
                "khmer": "អរុណសួស្តី (ព្រឹក) / ទិវាសួស្តី (រសៀល) / សាយណ្ហសួស្តី (ល្ងាច)",
                "example": "Good morning, everyone! Have a great day. = អរុណសួស្តីអ្នកទាំងអស់គ្នា! សូមឱ្យថ្ងៃនេះជាថ្ងៃដ៏ល្អ។"
            },
            {
                "phrase": "Thank you very much / You're welcome",
                "pronun": "/θæŋk juː/ /jʊər ˈwelkəm/",
                "khmer": "អរគុណច្រើន / មិនបាច់គួរសមទេ (មិនអីទេ)",
                "example": "A: Thank you for your help! B: You're welcome. = A: អរគុណសម្រាប់ជំនួយ! B: មិនបាច់គួរសមទេបាទ/ចាស។"
            },
            {
                "phrase": "Excuse me / I'm sorry",
                "pronun": "/ɪkˈskjuːz miː/ /aɪm ˈsɑːri/",
                "khmer": "សុំទោស (ពេលសុំផ្លូវ ឬចង់រំខានសួរ) / សុំទោស (ពេលធ្វើខុស)",
                "example": "Excuse me, where is the station? = សុំទោស តើស្ថានីយ៍នៅឯណាដែរ?"
            },
            {
                "phrase": "How are you? / I'm doing well, thank you.",
                "pronun": "/haʊ ɑːr juː/",
                "khmer": "តើអ្នកសុខសប្បាយជាទេ? / ខ្ញុំសុខសប្បាយធម្មតាទេ អរគុណ។",
                "example": "How are you today? I'm doing great! = តើថ្ងៃនេះអ្នកសុខសប្បាយជាទេ? ខ្ញុំសុខសប្បាយខ្លាំងណាស់!"
            },
            {
                "phrase": "Where are you from? / I am from Cambodia.",
                "pronun": "/weər ɑːr juː frʌm/",
                "khmer": "តើអ្នកមកពីណា? / ខ្ញុំមកពីប្រទេសកម្ពុជា។",
                "example": "Where are you from? I'm from Phnom Penh, Cambodia. = តើអ្នកមកពីណា? ខ្ញុំមកពីរាជធានីភ្នំពេញ ប្រទេសកម្ពុជា។"
            },
            {
                "phrase": "How much does this cost?",
                "pronun": "/haʊ mʌtʃ dʌz ðɪs kɔːst/",
                "khmer": "តើរបស់នេះតម្លៃប៉ុន្មានដែរ?",
                "example": "Excuse me, how much does this cost? = សុំទោស តើមួយនេះតម្លៃប៉ុន្មានដែរ?"
            },
            {
                "phrase": "See you later / Goodbye",
                "pronun": "/siː juː ˈleɪtər/ /ˌɡʊdˈbaɪ/",
                "khmer": "ជួបគ្នាពេលក្រោយ / លាហើយ",
                "example": "It was great seeing you. See you later! = ពិតជារីករាយណាស់ដែលបានជួបអ្នក។ ជួបគ្នាពេលក្រោយ!"
            }
        ]
    },
    2: {
        "title": "កម្រិត ២៖ ការសន្ទនាប្រចាំថ្ងៃ & ជីវិតរស់នៅ (A2 - Elementary)",
        "desc": "ការទិញឥវ៉ាន់ សួរផ្លូវ ញ៉ាំអាហារ និងការប្រាស្រ័យទាក់ទងពេលធ្វើដំណើរ",
        "lessons": [
            {
                "phrase": "Could you please help me?",
                "pronun": "/kʊd juː pliːz help miː/",
                "khmer": "តើអ្នកអាចជួយខ្ញុំបន្តិចបានទេ?",
                "example": "Excuse me, could you please help me with this bag? = សុំទោស តើអ្នកអាចជួយយួរកាបូបនេះបន្តិចបានទេ?"
            },
            {
                "phrase": "Where is the restroom / bathroom?",
                "pronun": "/weər ɪz ðə ˈrestruːm/",
                "khmer": "តើបន្ទប់ទឹកនៅឯណាដែរ?",
                "example": "Could you tell me where the restroom is? = តើអ្នកអាចប្រាប់ខ្ញុំបានទេថាបន្ទប់ទឹកនៅឯណា?"
            },
            {
                "phrase": "Can I have the bill / check, please?",
                "pronun": "/kæn aɪ hæv ðə bɪl pliːz/",
                "khmer": "សូមគិតលុយ (ពេលញ៉ាំអាហារនៅភោជនីយដ្ឋាន)",
                "example": "We are done. Can I have the bill, please? = ពួកយើងញ៉ាំរួចហើយ សូមគិតលុយមកបាទ/ចាស។"
            },
            {
                "phrase": "Could you speak more slowly, please?",
                "pronun": "/kʊd juː spiːk mɔːr ˈsloʊli/",
                "khmer": "សូមមេត្តានិយាយយឺតៗបន្តិចបានទេ?",
                "example": "I'm still learning English. Could you speak more slowly? = ខ្ញុំកំពុងរៀនភាសាអង់គ្លេសនៅឡើយ សូមនិយាយយឺតៗបន្តិចបានទេ?"
            },
            {
                "phrase": "I don't understand. Could you repeat that?",
                "pronun": "/aɪ doʊnt ˌʌndərˈstænd/",
                "khmer": "ខ្ញុំមិនយល់ទេ។ តើអ្នកអាចនិយាយឡើងវិញបានទេ?",
                "example": "Sorry, I didn't catch that. Could you repeat that? = សុំទោស ខ្ញុំស្តាប់មិនទាន់ទេ តើអ្នកអាចនិយាយឡើងវិញបានទេ?"
            },
            {
                "phrase": "It's too expensive. Can you give me a discount?",
                "pronun": "/ɪts tuː ɪkˈspensɪv/",
                "khmer": "ថ្លៃពេកហើយ។ តើអ្នកអាចចុះថ្លៃបន្តិចបានទេ?",
                "example": "That's a bit pricey. Can you give me a discount? = ថ្លៃបន្តិចហើយ ចុះថ្លៃឱ្យខ្ញុំបន្តិចបានទេ?"
            },
            {
                "phrase": "What do you recommend?",
                "pronun": "/wʌt duː juː ˌrekəˈmend/",
                "khmer": "តើអ្នកមានអ្វីណែនាំដែរទេ? (ម្ហូប ឬកន្លែងដើរលេង)",
                "example": "It's my first time here. What do you recommend? = នេះជាលើកទីមួយរបស់ខ្ញុំនៅទីនេះ តើអ្នកមានមុខម្ហូបអ្វីណែនាំទេ?"
            }
        ]
    },
    3: {
        "title": "កម្រិត ៣៖ កម្រិតមធ្យម ការងារ & ទំនាក់ទំនង (B1-B2 - Intermediate)",
        "desc": "ការងារការិយាល័យ ការបញ្ចេញមតិយោបល់ និងការលើកទឹកចិត្តក្រុមការងារ",
        "lessons": [
            {
                "phrase": "I look forward to working with you.",
                "pronun": "/aɪ lʊk ˈfɔːrwərd tuː ˈwɜːrkɪŋ/",
                "khmer": "ខ្ញុំទន្ទឹងរង់ចាំធ្វើការងាររួមគ្នាជាមួយអ្នក។",
                "example": "Welcome to the team! I look forward to working with you. = ស្វាគមន៍មកកាន់ក្រុមការងារ! ខ្ញុំទន្ទឹងរង់ចាំធ្វើការជាមួយអ្នក។"
            },
            {
                "phrase": "In my opinion / From my perspective",
                "pronun": "/ɪn maɪ əˈpɪnjən/",
                "khmer": "តាមយោបល់របស់ខ្ញុំ / តាមទស្សនៈរបស់ខ្ញុំ...",
                "example": "In my opinion, this strategy will save us both time and money. = តាមយោបល់ខ្ញុំ យុទ្ធសាស្ត្រនេះនឹងជួយសន្សំទាំងពេល និងលុយ។"
            },
            {
                "phrase": "Everything is under control.",
                "pronun": "/ˈevriθɪŋ ɪz ˈʌndər kənˈtroʊl/",
                "khmer": "អ្វីៗទាំងអស់ស្ថិតក្រោមការគ្រប់គ្រងបានយ៉ាងល្អ (កុំបារម្ភ)",
                "example": "Don't worry about the deadline, everything is under control. = កុំបារម្ភពីរឿងកំណត់ពេល អ្វីៗគ្រប់គ្រងបានល្អហើយ។"
            },
            {
                "phrase": "Keep up the good work!",
                "pronun": "/kiːp ʌp ðə ɡʊd wɜːrk/",
                "khmer": "បន្តការខិតខំប្រឹងប្រែងធ្វើការងារល្អបែបនេះទៀតណា៎!",
                "example": "Your presentation was fantastic! Keep up the good work. = ការធ្វើបទបង្ហាញរបស់អ្នកពូកែណាស់! បន្តការខិតខំប្រឹងប្រែងទៀតណា៎។"
            },
            {
                "phrase": "Let's reschedule the meeting.",
                "pronun": "/lets ˌriːˈskedʒuːl ðə ˈmiːtɪŋ/",
                "khmer": "ចូរយើងកំណត់កាលវិភាគប្រជុំឡើងវិញ។",
                "example": "Something urgent came up. Let's reschedule the meeting for tomorrow. = មានការបន្ទាន់កើតឡើង ចូរយើងលើកការប្រជុំទៅថ្ងៃស្អែកវិញ។"
            },
            {
                "phrase": "Could you please keep me in the loop?",
                "pronun": "/kiːp miː ɪn ðə luːp/",
                "khmer": "សូមជួយផ្ញើព័ត៌មាន ឬដំណឹងបច្ចុប្បន្នភាពឱ្យខ្ញុំដឹងផងណា៎។",
                "example": "As the project develops, please keep me in the loop. = ពេលគម្រោងវិវត្តទៅមុខ សូមជួយផ្ញើដំណឹងឱ្យខ្ញុំដឹងផង។"
            }
        ]
    },
    4: {
        "title": "កម្រិត ៤៖ កម្រិតខ្ពស់ ធុរកិច្ច & ការចរចា (C1 - Advanced Business)",
        "desc": "ភាសាជំនួញផ្លូវការ ការចរចាកិច្ចសន្យា យុទ្ធសាស្ត្រទីផ្សារ និងហិរញ្ញវត្ថុ",
        "lessons": [
            {
                "phrase": "Win-win partnership",
                "pronun": "/wɪn wɪn ˈpɑːrtnərʃɪp/",
                "khmer": "ភាពជាដៃគូដែលផ្តល់ផលប្រយោជន៍ឈ្នះ-ឈ្នះទាំងសងខាង",
                "example": "We strive to establish a long-term, win-win partnership. = យើងខិតខំកសាងភាពជាដៃគូរយៈពេលវែងដែលឈ្នះ-ឈ្នះទាំងសងខាង។"
            },
            {
                "phrase": "Reach a consensus",
                "pronun": "/riːtʃ ə kənˈsensəs/",
                "khmer": "សម្រេចបាននូវការយល់ស្របជាឯកច្ឆន្ទ (ការឯកភាពរួម)",
                "example": "After lengthy discussions, the board finally reached a consensus. = ក្រោយការពិភាក្សាយ៉ាងយូរ ក្រុមប្រឹក្សាភិបាលសម្រេចបានការឯកភាពរួម។"
            },
            {
                "phrase": "Maximize efficiency and minimize costs",
                "pronun": "/ˈmæksɪmaɪz ɪˈfɪʃnsi/",
                "khmer": "បង្កើនប្រសិទ្ធភាពការងារជាអតិបរមា និងកាត់បន្ថយការចំណាយឱ្យនៅទាបបំផុត",
                "example": "Our primary objective is to maximize efficiency and minimize costs. = គោលដៅចម្បងរបស់យើងគឺបង្កើនប្រសិទ្ធភាព និងកាត់បន្ថយថ្លៃដើម។"
            },
            {
                "phrase": "Non-Disclosure Agreement (NDA)",
                "pronun": "/ˌnɑːn dɪsˈkloʊʒər əˈɡriːmənt/",
                "khmer": "កិច្ចព្រមព្រៀងរក្សាការសម្ងាត់",
                "example": "Both parties must sign an NDA prior to reviewing confidential data. = ភាគីទាំងពីរត្រូវចុះហត្ថលេខាលើ NDA មុនពេលពិនិត្យទិន្នន័យសម្ងាត់។"
            },
            {
                "phrase": "Competitive advantage",
                "pronun": "/kəmˈpetətɪv ədˈvæntɪdʒ/",
                "khmer": "ឧត្តមភាពនៃការប្រកួតប្រជែងលើទីផ្សារ",
                "example": "Innovation is the cornerstone of our competitive advantage. = ការច្នៃប្រឌិតគឺជាគ្រឹះស្នូលនៃឧត្តមភាពប្រកួតប្រជែងរបស់យើង។"
            },
            {
                "phrase": "Return on Investment (ROI)",
                "pronun": "/rɪˈtɜːrn ɑːn ɪnˈvestmənt/",
                "khmer": "អត្រាផលចំណេញត្រឡប់មកវិញពីការវិនិយោគ",
                "example": "This marketing campaign produced an exceptional return on investment. = យុទ្ធនាការទីផ្សារនេះបានផ្តល់ផលចំណេញត្រឡប់មកវិញខ្ពស់ណាស់។"
            }
        ]
    },
    5: {
        "title": "កម្រិត ៥៖ សុភាសិត & ឃ្លា Idioms ល្បីៗ (C2 - Idioms & Proverbs)",
        "desc": "សុភាសិតអង់គ្លេសល្បីៗ និងឃ្លា Idioms បង្កប់ទស្សនវិជ្ជាជីវិតជ្រាលជ្រៅ",
        "lessons": [
            {
                "phrase": "Actions speak louder than words.",
                "pronun": "/ˈækʃnz spiːk ˈlaʊdər ðæn wɜːrdz/",
                "khmer": "«សកម្មភាពជាក់ស្តែង មានសំឡេងឮជាងពាក្យសម្តី» (ធ្វើជាក់ស្តែង ប្រសើរជាងនិយាយតែមាត់)",
                "example": "Don't just promise to change. Actions speak louder than words. = កុំគ្រាន់តែសន្យាថានឹងកែប្រែ សកម្មភាពជាក់ស្តែងសំខាន់ជាងពាក្យសម្តី!"
            },
            {
                "phrase": "A journey of a thousand miles begins with a single step.",
                "pronun": "/ə ˈdʒɜːrni əv ə ˈθaʊznd maɪlz.../",
                "khmer": "«ដំណើររាប់ពាន់ម៉ាយ ចាប់ផ្តើមពីជំហានដំបូង»",
                "example": "Starting a new business is daunting, but remember: a journey of a thousand miles begins with a single step.",
            },
            {
                "phrase": "Don't put all your eggs in one basket.",
                "pronun": "/doʊnt pʊt ɔːl jʊər eɡz ɪn wʌn ˈbæskɪt/",
                "khmer": "«កុំដាក់ពងមាន់ទាំងអស់ក្នុងកន្ត្រកតែមួយ» (កុំប្រថុយដាក់ធនធានលើរឿងតែមួយ ត្រូវចេះបែងចែកហានិភ័យ)",
                "example": "Diversify your investments. Never put all your eggs in one basket. = ចូរធ្វើពិពិធកម្មការវិនិយោគ កុំដាក់ទុនទាំងអស់ក្នុងកន្លែងតែមួយ។"
            },
            {
                "phrase": "Every cloud has a silver lining.",
                "pronun": "/ˈevri klaʊd hæz ə ˈsɪlvər ˈlaɪnɪŋ/",
                "khmer": "«ពពកខ្មៅងងឹត តែងតែមានពន្លឺចាំងពីក្រោយ» (ទោះជួបរឿងអាក្រក់យ៉ាងណា ក៏តែងតែមានរឿងល្អបង្កប់នៅខាងក្នុង)",
                "example": "I lost my job, but it motivated me to launch my own business. Every cloud has a silver lining! = ខ្ញុំបាត់បង់ការងារ តែវាជំរុញឱ្យខ្ញុំបើកអាជីវកម្មខ្លួនឯង។ ក្នុងរឿងអាក្រក់តែងមានរឿងល្អ!"
            },
            {
                "phrase": "Piece of cake",
                "pronun": "/piːs əv keɪk/",
                "khmer": "«ងាយស្រួលដូចបកចេក» (កិច្ចការដែលស្រួលធ្វើបំផុត)",
                "example": "Don't worry about the exam tomorrow, you've studied hard, it'll be a piece of cake! = កុំបារម្ភពីការប្រឡងថ្ងៃស្អែក អ្នកខំរៀនណាស់ វានឹងងាយស្រួលដូចបកចេក!"
            },
            {
                "phrase": "Break a leg!",
                "pronun": "/breɪk ə leɡ/",
                "khmer": "«ជូនពរឱ្យសំណាងល្អ និងជោគជ័យ!» (ពាក្យជូនពរពេលឡើងសម្តែង ឬប្រឡង)",
                "example": "I know you're nervous about your presentation today. Break a leg! = ខ្ញុំដឹងថាអ្នកភ័យរឿងឡើងនិយាយថ្ងៃនេះ។ ជូនពរឱ្យសំណាងល្អ និងជោគជ័យ!"
            }
        ]
    }
}

def get_english_menu() -> str:
    """Returns overview menu for English lessons from Level 1 to 5."""
    return (
        "🇬🇧 <b>វគ្គសិក្សាភាសាអង់គ្លេសបកប្រែខ្មែរ (A1 - C2)៖</b>\n\n"
        "សូមជ្រើសរើសកម្រិតសិក្សាដែលអ្នកចង់រៀន៖\n\n"
        "🔹 <b>/english 1</b> : <b>កម្រិត ១ (មូលដ្ឋានគ្រឹះ)</b> - ការស្វាគមន៍ សព្វនាម និងការគួរសម (A1)\n"
        "🔹 <b>/english 2</b> : <b>កម្រិត ២ (ការសន្ទនាទូទៅ)</b> - ញ៉ាំអាហារ ទិញឥវ៉ាន់ សួរផ្លូវ ធ្វើដំណើរ (A2)\n"
        "🔹 <b>/english 3</b> : <b>កម្រិត ៣ (កម្រិតមធ្យម)</b> - ការងារការិយាល័យ បញ្ចេញមតិ លើកទឹកចិត្ត (B1-B2)\n"
        "🔹 <b>/english 4</b> : <b>កម្រិត ៤ (កម្រិតខ្ពស់/ធុរកិច្ច)</b> - ចរចាជំនួញ កិច្ចសន្យា ទីផ្សារ វិនិយោគ (C1)\n"
        "🔹 <b>/english 5</b> : <b>កម្រិត ៥ (សុភាសិត & Idioms)</b> - ឃ្លាល្បីៗ និងទស្សនវិជ្ជាជីវិត (C2)\n\n"
        "💡 <i>ឧទាហរណ៍៖ វាយ <b>/english 1</b> ដើម្បីចាប់ផ្តើមរៀនកម្រិតដំបូង ឬសរសេរ «រៀនអង់គ្លេស» ក្នុងឆាត!</i> 📖✨"
    )

def get_english_level(level: int) -> str:
    """Returns lessons for a specific English level (1 to 5)."""
    if level not in ENGLISH_LEVELS:
        return get_english_menu()

    data = ENGLISH_LEVELS[level]
    lines = [
        f"🇬🇧 <b>{data['title']}</b>",
        f"<i>{data['desc']}</i>\n"
    ]

    for idx, item in enumerate(data["lessons"], 1):
        lines.append(f"<b>{idx}. {item['phrase']}</b>")
        if item.get("pronun"):
            lines.append(f"🗣️ <code>{item['pronun']}</code>")
        lines.append(f"👉 <b>ប្រែខ្មែរ៖</b> {item['khmer']}")
        lines.append(f"💬 <b>ឧទាហរណ៍៖</b> {item['example']}\n")

    next_cmd = f"/english {level + 1}" if level < 5 else "/english 1"
    lines.append(f"👉 <i>បន្តរៀនកម្រិតបន្ទាប់៖ វាយ {next_cmd}</i> 📚✨")
    return "\n".join(lines)

def get_random_english_card() -> str:
    """Returns one random English phrase card across all levels."""
    level = random.choice(list(ENGLISH_LEVELS.keys()))
    lesson = random.choice(ENGLISH_LEVELS[level]["lessons"])
    return (
        f"🇬🇧 <b>ភាសាអង់គ្លេសប្រចាំថ្ងៃ ({ENGLISH_LEVELS[level]['title'].split('៖')[1].strip()})៖</b>\n\n"
        f"🔤 <b>ឃ្លាអង់គ្លេស៖</b> <b>{lesson['phrase']}</b>\n"
        f"🗣️ <b>បញ្ចេញសំឡេង៖</b> <code>{lesson.get('pronun', '')}</code>\n"
        f"🇰🇭 <b>ប្រែជាខ្មែរ៖</b> {lesson['khmer']}\n\n"
        f"💬 <b>ឧទាហរណ៍៖</b>\n{lesson['example']}\n\n"
        f"💡 <i>វាយ <b>/english</b> ដើម្បីមើលមេរៀនគ្រប់កម្រិតពី ១ ដល់ ៥!</i>"
    )

def handle_english_query(query: str) -> Optional[str]:
    """Inspect user text and return targeted English lesson if relevant."""
    q = query.lower()

    # Mapping of level number patterns (both Arabic and Khmer digits)
    level_mappings = [
        (1, ["1", "១", "ដំបូង", "មូលដ្ឋាន", "beginner", "a1"]),
        (2, ["2", "២", "សន្ទនា", "elementary", "a2"]),
        (3, ["3", "៣", "មធ្យម", "intermediate", "b1", "b2"]),
        (4, ["4", "៤", "ខ្ពស់", "ធុរកិច្ច", "ជំនួញ", "business", "advanced", "c1"]),
        (5, ["5", "៥", "សុភាសិត", "idiom", "idioms", "proverb", "proverbs", "c2"]),
    ]

    # Check for specific level queries first
    for lvl, keywords in level_mappings:
        for kw in keywords:
            patterns = [
                f"កម្រិត{kw}", f"កម្រិត {kw}",
                f"level {kw}", f"level{kw}",
                f"អង់គ្លេស{kw}", f"អង់គ្លេស {kw}",
                f"english{kw}", f"english {kw}",
            ]
            if any(p in q for p in patterns):
                return get_english_level(lvl)

    # Thematic keywords
    if any(k in q for k in ["អង់គ្លេសកម្រិតខ្ពស់", "ធុរកិច្ចអង់គ្លេស", "business english"]):
        return get_english_level(4)

    if any(k in q for k in ["សុភាសិតអង់គ្លេស", "idiom", "idioms", "proverb"]):
        return get_english_level(5)

    if any(k in q for k in ["អង់គ្លេសដំបូង", "អង់គ្លេសមូលដ្ឋាន", "english basic"]):
        return get_english_level(1)

    # General English learning query -> show menu
    if any(k in q for k in ["រៀនអង់គ្លេស", "ភាសាអង់គ្លេស", "អង់គ្លេស", "learn english"]):
        return get_english_menu()

    return None
