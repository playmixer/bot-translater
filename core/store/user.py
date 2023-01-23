import json
import os
from dataclasses import dataclass
from core.classes.store import Store
from core.logger import logger

log = logger.getLogger("user_store")



@dataclass
class DefaultUserStore:
    user_id: int
    recognize_lang: str
    translate_lang: str

    def __init__(self, user_id=0, recognize_lang="", translate_lang=""):
        self.user_id = user_id
        self.recognize_lang = recognize_lang
        self.translate_lang = translate_lang


class UserStore(Store):
    user_id = None
    filename: str = ""
    data: DefaultUserStore

    @dataclass
    class _UserStore:
        def __init__(self):
            pass

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        path = os.path.join(self._path, "user")
        self.data = DefaultUserStore(user_id=user_id, recognize_lang="ru", translate_lang="en")
        if not os.path.exists(path):
            os.mkdir(path)

        self.filename = os.path.join(path, str(user_id) + ".cache")
        if not os.path.exists(self.filename):
            self.save()
        else:
            self.load()

    def save(self):
        with open(self.filename, "w") as f:
            data = super().toJSON(self.data.__dict__)
            f.write(data)

    def load(self):
        try:
            log.info("Загружаем данные пользователя из хранилища")
            with open(self.filename, "r") as f:
                body = json.load(f)
                self.data = DefaultUserStore(**body)
        except Exception as err:
            log.error(err)

    def set_user_id(self, user_id):
        self.data.user_id = user_id
        self.save()

    def set_translate_lang(self, lang: str):
        self.data.translate_lang = lang
        self.save()

    def set_recognize_lang(self, lang: str):
        self.data.recognize_lang = lang
        self.save()
