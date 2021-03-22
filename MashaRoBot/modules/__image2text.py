from MashaRoBot import telethn as tbot
import json
import os
import time
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from MashaRoBot import *

from MashaRoBot.events import bot as register

configuration = cloudmersive_ocr_api_client.Configuration()
configuration.api_key["Apikey"] = VIRUS_API_KEY
api_instance = cloudmersive_ocr_api_client.ImageOcrApi(
    cloudmersive_ocr_api_client.ApiClient(configuration)
)


@register(pattern="^/read (.*)")
async def parse_ocr_space_api(event):
    gg = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    language = lang_code
    downloaded_file_name = await tbot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY
    )
    try:
        api_response = api_instance.image_ocr_post(
            downloaded_file_name, language=language
        )
    except ApiException as e:
        print(e)
        os.remove(downloaded_file_name)
        await gg.edit("Some error occurred.")
        return
    await gg.edit("{}".format(api_response.text_result))
    os.remove(downloaded_file_name)


@register(pattern="^/img2textlang")
async def get_ocr_languages(event):
    if event.fwd_from:
        return
    languages = """**These are the available languages 👇**\n
ENG (English)
ARA (Arabic)
ZHO (Chinese - Simplified)
ZHO-HANT (Chinese - Traditional)
ASM (Assamese)
AFR (Afrikaans)
AMH (Amharic)
AZE (Azerbaijani)
AZE-CYRL (Azerbaijani - Cyrillic)
BEL (Belarusian)
BEN (Bengali)
BOD (Tibetan)
BOS (Bosnian)
BUL (Bulgarian)
CAT (Catalan; Valencian)
CEB (Cebuano)
CES (Czech)
CHR (Cherokee)
CYM (Welsh)
DAN (Danish)
DEU (German)
DZO (Dzongkha)
ELL (Greek)
ENM (Archaic/Middle English)
EPO (Esperanto)
EST (Estonian)
EUS (Basque)
FAS (Persian)
FIN (Finnish)
FRA (French)
FRK (Frankish)
FRM (Middle-French)
GLE (Irish)
GLG (Galician)
GRC (Ancient Greek)
HAT (Hatian)
HEB (Hebrew)
HIN (Hindi)
HRV (Croatian)
HUN (Hungarian)
IKU (Inuktitut)
IND (Indonesian)
ISL (Icelandic)
ITA (Italian)
ITA-OLD (Old - Italian)
JAV (Javanese)
JPN (Japanese)
KAN (Kannada)
KAT (Georgian)
KAT-OLD (Old-Georgian)
KAZ (Kazakh)
KHM (Central Khmer)
KIR (Kirghiz)
KOR (Korean)
KUR (Kurdish)
LAO (Lao)
LAT (Latin)
LAV (Latvian)
LIT (Lithuanian)
MAL (Malayalam)
MAR (Marathi)
MKD (Macedonian)
MLT (Maltese)
MSA (Malay)
MYA (Burmese)
NEP (Nepali)
NLD (Dutch)
NOR (Norwegian)
ORI (Oriya)
PAN (Panjabi)
POL (Polish)
POR (Portuguese)
PUS (Pushto)
RON (Romanian)
RUS (Russian)
SAN (Sanskrit)
SIN (Sinhala)
SLK (Slovak)
SLV (Slovenian)
SPA (Spanish)
SPA-OLD (Old Spanish)
SQI (Albanian)
SRP (Serbian)
SRP-LAT (Latin Serbian)
SWA (Swahili)
SWE (Swedish)
SYR (Syriac)
TAM (Tamil)
TEL (Telugu)
TGK (Tajik)
TGL (Tagalog)
THA (Thai)
TIR (Tigrinya)
TUR (Turkish)
UIG (Uighur)
UKR (Ukrainian)
URD (Urdu)
UZB (Uzbek)
UZB-CYR (Cyrillic Uzbek)
VIE (Vietnamese)
YID (Yiddish) (optional)
    """
    await event.reply(languages)
