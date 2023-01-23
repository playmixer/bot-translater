import io
import requests
from datetime import datetime, timedelta
from enum import Enum
from core.logger import logger

log = logger.getLogger("yandex")


class YandexException(Exception):
    def __init__(self, message: str):
        print("Exception:", message)


class YandexLang(Enum):
    RU = 'ru'
    EN = 'en'
    TR = 'tr'


class YandexEmotion(Enum):
    GOOD = 'good'
    EVIL = 'evil'
    NEUTRAL = 'neutral'


class YandexVoice(Enum):
    OKSANA = 'oksana'
    JANE = 'jane'
    OMAZH = 'omazh'
    ZAHAR = 'zahar'
    ERMIL = 'ermil'


class Yandex(object):
    _instance = None
    _token: str = None
    _folder: str = None
    _iam_token: str = None
    _expire_iam: datetime = datetime.now()
    _speed = None
    _emotion = None
    _voice = None
    _lang = None

    def init(self, token: str, folder: str):
        self._token = token
        self._folder = folder

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Yandex, cls).__new__(cls)
        return cls.instance

    @property
    def token(self):
        return self._token

    @property
    def folder(self):
        return self._folder

    def _check(self):
        if self._iam_token is None or self._iam_is_expired():
            self._update_iam_token()

    def _iam_is_expired(self):
        if self._expire_iam is None:
            return True
        return (self._expire_iam - datetime.utcnow()) < timedelta(hours=4)

    def _update_iam_token(self):
        try:
            print("Обновляем iam токен")
            url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
            data = {"yandexPassportOauthToken": self.token}
            res = requests.post(
                url,
                json=data
            )
            if res.status_code == 200:
                data = res.json()
                self._iam_token = data.get('iamToken')
                self._expire_iam = datetime.strptime(data.get('expiresAt')[:19], format='%Y-%m-%dT%H:%M:%S')
                if self._iam_token is None or self._iam_token == "":
                    raise YandexException("Yandex: can not update iam token")
            else:
                raise YandexException(f"""Yandex: \n
{data} \n
{res} \n
{res.text}""")
        except Exception as err:
            log.error(err)

    def translate_text(self, text: str, lang: str = YandexLang.EN.value):
        self._check()
        url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'

        headers = {"Authorization": f"Bearer {self._iam_token}"}
        data = {
            "folderId": self.folder,
            "texts": [text],
            "targetLanguageCode": lang
        }
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            translations = res.json().get('translations')
            if translations:
                return translations[0].get('text')
                # self.detected_language = translations[0].get('detectedLanguageCode')
        else:
            raise YandexException(f"""Не удалось перевести: \n
{headers} \n
{data} \n
{res} \n
{res.text}""")

        return None

    def recognize(self, voice: io.BytesIO, lang: str = "ru"):
        self._check()
        url = f'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
        headers = {
            "Authorization": f"Bearer {self._iam_token}",
        }
        data = {
            "folderId": self.folder,
            "lang": lang,
        }
        r = requests.post(url, headers=headers, params=data, data=voice.getbuffer())
        if r.status_code == 200:
            result = r.json().get('result')
            log.info(result)
            return result
        else:
            log.error(r)
            raise YandexException(f"Yandex: {r}")

    def tts(self, text: str, lang: str = YandexLang.EN.value, speed='1', emotion=YandexEmotion.NEUTRAL.value,
            voice=YandexVoice.JANE.value) -> bytes or None:
        try:
            url = f"https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"

            data = {
                'folderId': self.folder,
                'text': text,
                'lang': lang,
                'speed': speed,
                'emotion': emotion,
                'voice': voice
            }

            r = requests.post(url, headers={"Authorization": f"Bearer {self._iam_token}"}, data=data)
            log.info()
            if r.status_code == 200:
                return r.content
            else:
                log.error()
                return None
        except Exception as err:
            log.error(err)


def init(token: str, folder: str):
    Yandex().init(token, folder)
