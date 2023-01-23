import io
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from core.yandex import Yandex, YandexLang
from core.object.user import User
import config
from core.logger import logger

log = logger.getLogger("handler")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User(update.effective_chat.id)
    # user.store.save()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="hello")


async def set_translate_lang_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User(update.effective_chat.id)
    user.store.set_translate_lang(YandexLang.EN.value)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Язык перевода изменен на английский")


async def set_translate_lang_tr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User(update.effective_chat.id)
    user.store.set_translate_lang(YandexLang.TR.value)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Язык перевода изменен на турецкий")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = User(update.effective_chat.id)
        text = update.message.text[:config.TRANSLATE_TEXT_MAX_LENGTH]
        yandex = Yandex()

        translated_text = yandex.translate_text(text, user.store.data.translate_lang)

        if config.TRANSLATE_SPEECH_ENABLE:
            voice_b = yandex.tts(translated_text, user.store.data.translate_lang)
            if voice_b:
                await context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice_b)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=translated_text)
    except Exception as err:
        print(err)
        log.error(err)


async def voice(update: Update, context: CallbackContext):
    try:
        user = User(update.effective_chat.id)
        file_info = await context.bot.get_file(update.message.voice.file_id)
        buffer = io.BytesIO()
        await file_info.download_to_memory(buffer)
        yandex = Yandex()
        text = yandex.recognize(buffer, user.store.data.recognize_lang)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as err:
        log.error(err)
