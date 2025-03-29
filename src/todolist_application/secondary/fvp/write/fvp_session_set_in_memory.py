from todolist_hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from todolist_hexagon.shared.type import UserKey
from todolist_application.infra.fvp_memory import FvpMemory


class FvpSessionSetInMemory(FvpSessionSetPort):
    def __init__(self, fvp_memory: FvpMemory) -> None:
        self._memory = fvp_memory

    def save(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        self._memory.save(user_key=user_key, snapshot=snapshot)

    def by(self, user_key: UserKey) -> FvpSnapshot:
        return self._memory.by(user_key=user_key)
