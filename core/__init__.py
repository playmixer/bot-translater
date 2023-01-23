from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from core.bot.handlers import echo, voice, start, set_translate_lang_en, set_translate_lang_tr
from core.logger import logger

log = logger.getLogger("bot")


class BotRunner:
    TOKEN: str = ""

    def __init__(self, token: str):
        self.TOKEN = token

    def run(self):
        print("""
            Start Bot-translate
        """)
        app = ApplicationBuilder().token(self.TOKEN).build()

        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('set_translate_lang_en', set_translate_lang_en))
        app.add_handler(CommandHandler('set_translate_lang_tr', set_translate_lang_tr))

        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
        app.add_handler(MessageHandler(filters.VOICE, voice))

        app.run_polling()
