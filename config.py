import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN", "")
YANDEX_FOLDER = os.getenv("YANDEX_FOLDER", "")

STORE = os.getenv("STORE", "store")

TRANSLATE_TEXT_MAX_LENGTH = int(os.getenv("TRANSLATE_TEXT_MAX_LENGTH", 100))
TRANSLATE_SPEECH_ENABLE = int(os.getenv("TRANSLATE_SPEECH_ENABLE", 0))
