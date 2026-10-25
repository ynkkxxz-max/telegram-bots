"""
Chinese Learning Module with Khmer Translations from Basic to Advanced (HSK 1 - HSK 6).
Includes Hanzi, Pinyin, Khmer translation, and practical usage examples.
"""
import random
from typing import Dict, List, Optional

CHINESE_LEVELS: Dict[int, Dict] = {
    1: {
        "title": "កម្រិត ១៖ មូលដ្ឋានគ្រឹះ & ការគួរសម (HSK 1 - Beginner)",
        "desc": "ពាក្យគួរសម សព្វនាម និងលេខរាប់ដែលត្រូវប្រើជាប្រចាំ",
        "lessons": [
            {
                "hanzi": "你好",
                "pinyin": "Nǐ hǎo",
                "khmer": "សួស្តី",
                "example": "你好！很高兴认识你。(Nǐ hǎo! Hěn gāoxìng rènshi nǐ.) = សួស្តី! រីករាយណាស់ដែលបានស្គាល់អ្នក។"
            },
            {
                "hanzi": "谢谢",
                "pinyin": "Xièxie",
                "khmer": "អរគុណ",
                "example": "太谢谢你了！(Tài xièxie nǐ le!) = អរគុណអ្នកខ្លាំងណាស់!"
            },
            {
                "hanzi": "不客气",
                "pinyin": "Bú kèqi",
                "khmer": "មិនបាច់គួរសមទេ / មិនអីទេ",
                "example": "A: 谢谢！ B: 不客气。(Bú kèqi.) = មិនបាច់គួរសមទេបាទ/ចាស។"
            },
            {
                "hanzi": "对不起",
                "pinyin": "Duìbuqǐ",
                "khmer": "សុំទោស",
                "example": "对不起，我来晚了。(Duìbuqǐ, wǒ lái wǎn le.) = សុំទោស ខ្ញុំមកយឺតហើយ។"
            },
            {
                "hanzi": "没关系",
                "pinyin": "Méi guānxi",
                "khmer": "មិនអីទេ (ឆ្លើយតបពេលគេសុំទោស)",
                "example": "没关系，别担心。(Méi guānxi, bié dānxīn.) = មិនអីទេ កុំបារម្ភអី។"
            },
            {
                "hanzi": "再见",
                "pinyin": "Zàijiàn",
                "khmer": "លាហើយ / ជួបគ្នាពេលក្រោយ",
                "example": "明天见，再见！(Míngtiān jiàn, zàijiàn!) = ថ្ងៃស្អែកជួបគ្នា លាហើយ!"
            },
            {
                "hanzi": "我 / 你 / 他 / 她",
                "pinyin": "Wǒ / Nǐ / Tā / Tā",
                "khmer": "ខ្ញុំ / អ្នក / គាត់ (ប្រុស) / នាង (ស្រី)",
                "example": "我是柬埔寨人。(Wǒ shì Jiǎnpǔzhàirén.) = ខ្ញុំជាជនជាតិកម្ពុជា។"
            },
            {
                "hanzi": "是 / 不是",
                "pinyin": "Shì / Bú shì",
                "khmer": "គឺ, មែន / មិនមែន",
                "example": "这是你的吗？不是。(Zhè shì nǐ de ma? Bú shì.) = នេះជារបស់អ្នកមែនទេ? មិនមែនទេ។"
            },
            {
                "hanzi": "多少钱？",
                "pinyin": "Duōshao qián?",
                "khmer": "តម្លៃប៉ុន្មាន?",
                "example": "这个多少钱？(Zhè ge duōshao qián?) = របស់មួយនេះតម្លៃប៉ុន្មានដែរ?"
            },
            {
                "hanzi": "រាប់លេខ ១ ដល់ ១០",
                "pinyin": "1-10",
                "khmer": "一(yī)=១, 二(èr)=២, 三(sān)=៣, 四(sì)=៤, 五(wǔ)=៥, 六(liù)=៦, 七(qī)=៧, 八(bā)=៨, 九(jiǔ)=៩, 十(shí)=១០",
                "example": "一百 (yī bǎi) = ១០០, 一千 (yī qiān) = ១,០០០"
            }
        ]
    },
    2: {
        "title": "កម្រិត ២៖ ការសន្ទនាប្រចាំថ្ងៃ & ការទិញឥវ៉ាន់ (HSK 2 - Elementary)",
        "desc": "ការទិញឥវ៉ាន់ សួរផ្លូវ ញ៉ាំអាហារ និងការប្រាស្រ័យទាក់ទងទូទៅ",
        "lessons": [
            {
                "hanzi": "你吃了吗？",
                "pinyin": "Nǐ chī le ma?",
                "khmer": "តើអ្នកញ៉ាំបាយហើយឬនៅ?",
                "example": "我吃了，你呢？(Wǒ chī le, nǐ ne?) = ខ្ញុំញ៉ាំរួចហើយ ចុះអ្នកវិញ?"
            },
            {
                "hanzi": "太贵了，可以便宜一点吗？",
                "pinyin": "Tài guì le, kěyǐ piányi yìdiǎn ma?",
                "khmer": "ថ្លៃពេកហើយ ចុះបន្តិចបានទេ?",
                "example": "老闆，太贵了，便宜一点吧！(Lǎobǎn, tài guì le, piányi yìdiǎn ba!) = មេការ ថ្លៃពេកហើយ ចុះបន្តិចមក!"
            },
            {
                "hanzi": "洗手间在哪里？",
                "pinyin": "Xǐshǒujiān zài nǎlǐ?",
                "khmer": "តើបន្ទប់ទឹកនៅឯណា?",
                "example": "请问，洗手间在哪里？(Qǐngwèn, xǐshǒujiān zài nǎlǐ?) = សូមសួរមួយ បន្ទប់ទឹកនៅឯណា?"
            },
            {
                "hanzi": "我听不懂",
                "pinyin": "Wǒ tīng bù dǒng",
                "khmer": "ខ្ញុំស្តាប់មិនយល់ទេ",
                "example": "对不起，我的中文不太好，我听不懂。(Duìbuqǐ, wǒ de zhōngwén bú tài hǎo, wǒ tīng bù dǒng.) = សុំទោស ភាសាចិនខ្ញុំមិនសូវពូកែទេ ខ្ញុំស្តាប់មិនយល់ឡើយ។"
            },
            {
                "hanzi": "请再说一遍",
                "pinyin": "Qǐng zài shuō yí biàn",
                "khmer": "សូមមេត្តានិយាយម្តងទៀត",
                "example": "请慢一点说，再说一遍。(Qǐng màn yìdiǎn shuō, zài shuō yí biàn.) = សូមនិយាយយឺតៗបន្តិច និងម្តងទៀត។"
            },
            {
                "hanzi": "我想买...",
                "pinyin": "Wǒ xiǎng mǎi...",
                "khmer": "ខ្ញុំចង់ទិញ...",
                "example": "我想买一杯咖啡。(Wǒ xiǎng mǎi yì bēi kāfēi.) = ខ្ញុំចង់ទិញកាហ្វេមួយកែវ។"
            },
            {
                "hanzi": "现在几点？",
                "pinyin": "Xiànzài jǐ diǎn?",
                "khmer": "ឥឡូវម៉ោងប៉ុន្មានហើយ?",
                "example": "现在上午九点。(Xiànzài shàngwǔ jiǔ diǎn.) = ឥឡូវម៉ោង ៩ ព្រឹក។"
            }
        ]
    },
    3: {
        "title": "កម្រិត ៣៖ កម្រិតមធ្យម ការងារ & ទំនាក់ទំនង (HSK 3-4 - Intermediate)",
        "desc": "ការពិភាក្សាការងារ ការណាត់ជួប និងការបង្ហាញអារម្មណ៍យោបល់",
        "lessons": [
            {
                "hanzi": "祝你工作顺利！",
                "pinyin": "Zhù nǐ gōngzuò shùnlì!",
                "khmer": "ជូនពរឱ្យការងាររបស់អ្នកប្រព្រឹត្តទៅដោយរលូន!",
                "example": "祝你新工作顺利，步步高升！(Zhù nǐ xīn gōngzuò shùnlì, bùbù gāoshēng!) = ជូនពរការងារថ្មីរលូន និងឡើងតំណែងជាលំដាប់!"
            },
            {
                "hanzi": "没问题，包在我身上",
                "pinyin": "Méi wèntí, bāo zài wǒ shēnshang",
                "khmer": "គ្មានបញ្ហាទេ ទុកលើខ្ញុំចុះ!",
                "example": "这件事情交给我，包在我身上！(Zhè jiàn shìqing jiāo gěi wǒ, bāo zài wǒ shēnshang!) = រឿងនេះប្រគល់មកខ្ញុំ ទុកលើខ្ញុំធានាជូន!"
            },
            {
                "hanzi": "辛苦了！",
                "pinyin": "Xīnkǔ le!",
                "khmer": "ហត់នឿយហើយ! (ពាក្យគួរសមលើកទឹកចិត្តក្រោយបំពេញការងារ)",
                "example": "今天大家辛苦了，早点休息。(Jīntiān dàjiā xīnkǔ le, zǎodiǎn xiūxi.) = ថ្ងៃនេះអ្នកទាំងអស់គ្នាហត់នឿយហើយ ឆាប់សម្រាកទៅ។"
            },
            {
                "hanzi": "按照计划进行",
                "pinyin": "Ànzhào jìhuà jìnxíng",
                "khmer": "អនុវត្តតាមផែនការដែលបានគ្រោងទុក",
                "example": "我们的项目正在按照计划进行。(Wǒmen de xiàngmù zhèngzài ànzhào jìhuà jìnxíng.) = គម្រោងរបស់យើងកំពុងដំណើរការទៅតាមផែនការ។"
            },
            {
                "hanzi": "坚持就是胜利",
                "pinyin": "Jiānchí jiù shì shènglì",
                "khmer": "ការតស៊ូព្យាយាម គឺជាជ័យជម្នះ",
                "example": "别放弃，坚持就是胜利！(Bié fàngqì, jiānchí jiù shì shènglì!) = កុំបោះបង់ ការតស៊ូព្យាយាមគង់បានជោគជ័យ!"
            },
            {
                "hanzi": "我认为...",
                "pinyin": "Wǒ rènwéi...",
                "khmer": "ខ្ញុំយល់ឃើញថា / តាមគំនិតខ្ញុំ...",
                "example": "我认为这个方案很好。(Wǒ rènwéi zhè ge fāng'àn hěn hǎo.) = ខ្ញុំយល់ឃើញថាផែនការដំណោះស្រាយនេះល្អណាស់។"
            }
        ]
    },
    4: {
        "title": "កម្រិត ៤៖ កម្រិតខ្ពស់ ធុរកិច្ច & ការចរចា (HSK 5 - Advanced Business)",
        "desc": "ពាក្យបច្ចេកទេសជំនួញ កិច្ចសន្យា ទីផ្សារ និងការវិនិយោគ",
        "lessons": [
            {
                "hanzi": "合作愉快！",
                "pinyin": "Hézuò yúkuài!",
                "khmer": "រីករាយណាស់ដែលបានសហការគ្នា!",
                "example": "希望我们合作愉快，共创辉煌。(Xīwàng wǒmen hézuò yúkuài, gòng chuàng huīhuáng.) = សង្ឃឹមថាយើងសហការគ្នាយ៉ាងរលូន និងបង្កើតជោគជ័យជាមួយគ្នា!"
            },
            {
                "hanzi": "互利共赢",
                "pinyin": "Hù lì gòng yíng",
                "khmer": "ផលប្រយោជន៍រួម និងឈ្នះ-ឈ្នះទាំងសងខាង (Win-Win Solution)",
                "example": "建立长期稳定的互利共赢合作关系。(Jiànlì chángqī wěndìng de hùlì gòngyíng hézuò guānxì.) = បង្កើតទំនាក់ទំនងសហប្រតិបត្តិការឈ្នះ-ឈ្នះរយៈពេលវែង និងរឹងមាំ។"
            },
            {
                "hanzi": "签署合同",
                "pinyin": "Qiānshǔ hétong",
                "khmer": "ចុះហត្ថលេខាលើកិច្ចសន្យា / ចុះកុងត្រា",
                "example": "双方将于明天正式签署合同。(Shuāngfāng jiāng yú míngtiān zhèngshì qiānshǔ hétong.) = ភាគីទាំងពីរនឹងចុះហត្ថលេខាលើកិច្ចសន្យាជាផ្លូវការនៅថ្ងៃស្អែក។"
            },
            {
                "hanzi": "降低成本，提高效率",
                "pinyin": "Jiàngdī chéngběn, tígāo xiàolǜ",
                "khmer": "កាត់បន្ថយថ្លៃដើម បង្កើនប្រសិទ្ធភាពការងារ",
                "example": "采用新技术可以降低成本，提高效率。(Cǎiyòng xīn jìshù kěyǐ jiàngdī chéngběn, tígāo xiàolǜ.) = ការប្រើប្រាស់បច្ចេកវិទ្យាថ្មីអាចកាត់បន្ថយថ្លៃដើម និងបង្កើនប្រសិទ្ធភាព។"
            },
            {
                "hanzi": "投资风险",
                "pinyin": "Tóuzī fēngxiǎn",
                "khmer": "ហានិភ័យនៃការវិនិយោគ",
                "example": "任何投资都有一定的风险。(Rènhé tóuzī dōu yǒu yídìng de fēngxiǎn.) = រាល់ការវិនិយោគសុទ្ធតែមានហានិភ័យកម្រិតណាមួយ។"
            },
            {
                "hanzi": "市场竞争力",
                "pinyin": "Shìchǎng jìngzhēnglì",
                "khmer": "សមត្ថភាពប្រកួតប្រជែងលើទីផ្សារ",
                "example": "提高产品质量以增强市场竞争力。(Tígāo chǎnpǐn zhìliàng yǐ zēngqiáng shìchǎng jìngzhēnglì.) = ពង្រឹងគុណភាពផលិតផលដើម្បីបង្កើនសមត្ថភាពប្រកួតប្រជែងលើទីផ្សារ។"
            }
        ]
    },
    5: {
        "title": "កម្រិត ៥៖ សុភាសិតចិនល្បីៗ & ទស្សនវិជ្ជា (HSK 6 - Chengyu & Proverbs)",
        "desc": "សុភាសិត ៤ តួអក្សរ (成语 - Chéngyǔ) បង្កប់អត្ថន័យទស្សនវិជ្ជាជ្រាលជ្រៅ",
        "lessons": [
            {
                "hanzi": "饮水思源",
                "pinyin": "Yǐn shuǐ sī yuán",
                "khmer": "«ផឹកទឹក ឱ្យគិតដល់ប្រភពទឹក» (ដឹងគុណអ្នកមានគុណ កុំភ្លេចកំណើត)",
                "example": "做人要懂得饮水思源，知恩图报。(Zuòrén yào dǒngdé yǐn shuǐ sī yuán, zhī ēn tú bào.) = ធ្វើជាមនុស្សត្រូវចេះដឹងគុណប្រភពដើម និងសងគុណអ្នកជួយយើង។"
            },
            {
                "hanzi": "千里之行，始于足下",
                "pinyin": "Qiān lǐ zhī xíng, shǐ yú zú xià",
                "khmer": "«ដំណើររាប់ពាន់យោជន៍ ចាប់ផ្តើមពីជំហានដំបូង»",
                "example": "无论目标多宏大，都要千里之行始于足下。(Wúlùn mùbiāo duō hóngdà, dōu yào qiān lǐ zhī xíng, shǐ yú zú xià.) = ទោះគោលដៅធំធេងយ៉ាងណា ក៏ត្រូវតែចាប់ផ្តើមបោះជំហានដំបូងដែរ។"
            },
            {
                "hanzi": "笨鸟先飞",
                "pinyin": "Bèn niǎo xiān fēi",
                "khmer": "«សត្វស្លាបយឺត ត្រូវហើរមុនគេ» (មនុស្សដែលមិនសូវឆ្លាត ត្រូវតែខំប្រឹងជាងគេ)",
                "example": "我基础虽然差，但我相信笨鸟先飞。(Wǒ jīchǔ suīrán chà, dàn wǒ xiāngxìn bèn niǎo xiān fēi.) = ទោះបីគ្រឹះខ្ញុំខ្សោយ តែខ្ញុំជឿជាក់ថាការខំប្រឹងមុនគេនឹងជោគជ័យ។"
            },
            {
                "hanzi": "一步一个脚印",
                "pinyin": "Yí bù yí gè jiǎoyìn",
                "khmer": "«មួយជំហាន បន្សល់ស្នាមជើងមួយ» (ដើរទៅមុខដោយរឹងមាំ និងច្បាស់លាស់ មិនរំលងជំហាន)",
                "example": "学习要一步一个脚印，不能急于求成。(Xuéxí yào yí bù yí gè jiǎoyìn, bù néng jí yú qiú chéng.) = ការរៀនសូត្រត្រូវបោះជំហានមួយៗឱ្យរឹងមាំ កុំប្រញាប់ចង់បានផលភ្លាមៗ។"
            },
            {
                "hanzi": "塞翁失马，焉知非福",
                "pinyin": "Sài wēng shī mǎ, yān zhī fēi fú",
                "khmer": "«តាជ្រុះសេះ នរណាដឹងថាជាលាភ» (ជួបរឿងមិនល្អ តែអាចនាំរឿងល្អមកវិញ)",
                "example": "这次失败也许是塞翁失马，焉知非福。(Zhè cì shībài yěxǔ shì sài wēng shī mǎ, yān zhī fēi fú.) = ការបរាជ័យលើកនេះ ប្រហែលជាជួយនាំសំណាងល្អមកវិញនៅពេលក្រោយ។"
            },
            {
                "hanzi": "入乡随俗",
                "pinyin": "Rù xiāng suí sú",
                "khmer": "«ចូលស្ទឹងតាមបត់ ចូលស្រុកតាមទេស» (គោរពទំនៀមទម្លាប់តាមតំបន់)",
                "example": "到了国外就要入乡随俗。(Dào le guówài jiù yào rù xiāng suí sú.) = ពេលទៅដល់ស្រុកក្រៅ ត្រូវតែគោរពទំនៀមទម្លាប់ទីនោះ។"
            }
        ]
    }
}

def get_chinese_menu() -> str:
    """Returns overview menu for Chinese lessons from Level 1 to 5."""
    return (
        "🇨🇳 <b>វគ្គសិក្សាភាសាចិនបកប្រែខ្មែរ (HSK 1 - HSK 6)៖</b>\n\n"
        "សូមជ្រើសរើសកម្រិតសិក្សាដែលអ្នកចង់រៀន៖\n\n"
        "🔹 <b>/chinese 1</b> : <b>កម្រិត ១ (មូលដ្ឋានគ្រឹះ)</b> - ការគួរសម សព្វនាម និងរាប់លេខ (HSK 1)\n"
        "🔹 <b>/chinese 2</b> : <b>កម្រិត ២ (ការសន្ទនាទូទៅ)</b> - ញ៉ាំបាយ ទិញឥវ៉ាន់ សួរផ្លូវ (HSK 2)\n"
        "🔹 <b>/chinese 3</b> : <b>កម្រិត ៣ (កម្រិតមធ្យម)</b> - ការងារ លើកទឹកចិត្ត និងទំនាក់ទំនង (HSK 3-4)\n"
        "🔹 <b>/chinese 4</b> : <b>កម្រិត ៤ (កម្រិតខ្ពស់/ធុរកិច្ច)</b> - ចរចាជំនួញ កិច្ចសន្យា ទីផ្សារ (HSK 5)\n"
        "🔹 <b>/chinese 5</b> : <b>កម្រិត ៥ (សុភាសិតចិន)</b> - សុភាសិត ៤ តួ (成语 - Chengyu) បង្កប់ទស្សនវិជ្ជា (HSK 6)\n\n"
        "💡 <i>ឧទាហរណ៍៖ វាយ <b>/chinese 1</b> ដើម្បីចាប់ផ្តើមរៀនកម្រិតដំបូង ឬសរសេរ «រៀនចិន» ក្នុងឆាត!</i> 📖✨"
    )

def get_chinese_level(level: int) -> str:
    """Returns lessons for a specific level (1 to 5)."""
    if level not in CHINESE_LEVELS:
        return get_chinese_menu()

    data = CHINESE_LEVELS[level]
    lines = [
        f"🇨🇳 <b>{data['title']}</b>",
        f"<i>{data['desc']}</i>\n"
    ]

    for idx, item in enumerate(data["lessons"], 1):
        lines.append(f"<b>{idx}. {item['hanzi']}</b>  <code>[{item['pinyin']}]</code>")
        lines.append(f"👉 <b>ប្រែខ្មែរ៖</b> {item['khmer']}")
        lines.append(f"💬 <b>ឧទាហរណ៍៖</b> {item['example']}\n")

    next_cmd = f"/chinese {level + 1}" if level < 5 else "/chinese 1"
    lines.append(f"👉 <i>បន្តរៀនកម្រិតបន្ទាប់៖ វាយ {next_cmd}</i> 📚✨")
    return "\n".join(lines)

def get_random_chinese_card() -> str:
    """Returns one random Chinese vocabulary card across all levels."""
    level = random.choice(list(CHINESE_LEVELS.keys()))
    lesson = random.choice(CHINESE_LEVELS[level]["lessons"])
    return (
        f"🇨🇳 <b>ពាក្យចិនប្រចាំថ្ងៃ ({CHINESE_LEVELS[level]['title'].split('៖')[1].strip()})៖</b>\n\n"
        f"🔤 <b>អក្សរចិន៖</b> {lesson['hanzi']}\n"
        f"🗣️ <b>ភីនអ៊ីន (Pinyin)៖</b> <code>{lesson['pinyin']}</code>\n"
        f"🇰🇭 <b>ប្រែជាខ្មែរ៖</b> <b>{lesson['khmer']}</b>\n\n"
        f"💬 <b>ឧទាហរណ៍ប្រយោគ៖</b>\n{lesson['example']}\n\n"
        f"💡 <i>វាយ <b>/chinese</b> ដើម្បីមើលមេរៀនគ្រប់កម្រិតពី ១ ដល់ ៥!</i>"
    )

def handle_chinese_query(query: str) -> Optional[str]:
    """Inspect user text and return targeted Chinese lesson if relevant."""
    q = query.lower()

    # Mapping of level number patterns (both Arabic and Khmer digits)
    level_mappings = [
        (1, ["1", "១", "ដំបូង", "មូលដ្ឋាន"]),
        (2, ["2", "២", "សន្ទនា"]),
        (3, ["3", "៣", "មធ្យម"]),
        (4, ["4", "៤", "ខ្ពស់", "ធុរកិច្ច", "ជំនួញ", "កិច្ចសន្យា"]),
        (5, ["5", "៥", "សុភាសិត", "chengyu", "成语", "ទស្សនវិជ្ជា"]),
    ]

    # Check for specific level queries first
    for lvl, keywords in level_mappings:
        for kw in keywords:
            patterns = [
                f"កម្រិត{kw}", f"កម្រិត {kw}",
                f"level {kw}", f"level{kw}",
                f"ចិន{kw}", f"ចិន {kw}",
                f"hsk{kw}", f"hsk {kw}",
            ]
            if any(p in q for p in patterns):
                return get_chinese_level(lvl)

    # Thematic keywords
    if any(k in q for k in ["កម្រិតខ្ពស់", "ចិនខ្ពស់", "ធុរកិច្ចចិន", "ជំនួញចិន"]):
        return get_chinese_level(4)

    if any(k in q for k in ["សុភាសិតចិន", "chengyu", "成语", "ទស្សនវិជ្ជាចិន"]):
        return get_chinese_level(5)

    if any(k in q for k in ["មូលដ្ឋាន", "ចិនដំបូង"]):
        return get_chinese_level(1)

    # General Chinese learning query -> show menu
    if any(k in q for k in ["រៀនចិន", "ភាសាចិន", "ចិន", "chinese", "hsk", "pinyin"]):
        return get_chinese_menu()

    return None
