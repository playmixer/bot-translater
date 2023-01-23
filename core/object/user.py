from core.store.user import UserStore


class User:
    store: UserStore

    def __init__(self, user_id):
        self.store = UserStore(user_id)
