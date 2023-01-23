from config import TELEGRAM_BOT_TOKEN, YANDEX_TOKEN, YANDEX_FOLDER
from core import BotRunner
from core.bot import handlers
from core.yandex import init as yandex_init, Yandex

yandex_init(YANDEX_TOKEN, YANDEX_FOLDER)

if __name__ == "__main__":
    bot = BotRunner(TELEGRAM_BOT_TOKEN)
    bot.run()
