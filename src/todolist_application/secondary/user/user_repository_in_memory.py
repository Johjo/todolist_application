from todolist_hexagon.shared.type import UserKey
from todolist_hexagon.user.port import UserRepositoryPort, UserSnapshot


class UserRepositoryInMemory(UserRepositoryPort):
    def __init__(self) -> None:
        self.user : dict[UserKey, UserSnapshot] = {}

    def save(self, user: UserSnapshot) -> None:
        self.user[user.key] = user

    def by_user(self, key: UserKey) -> UserSnapshot | None:
        if key not in self.user:
            return None
        return self.user[key]

