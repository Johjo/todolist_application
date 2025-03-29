from collections import OrderedDict

from todolist_hexagon.fvp.aggregate import FvpSnapshot
from todolist_hexagon.shared.type import TaskKey, UserKey


class FvpMemory:
    def __init__(self) -> None:
        self._snapshots: dict[UserKey, FvpSnapshot] = {}

    def save(self, user_key: UserKey, snapshot: FvpSnapshot):
        self._snapshots[user_key] = snapshot

    def feed(self, user_key: UserKey, snapshot: FvpSnapshot):
        self._snapshots[user_key] = snapshot

    def by(self, user_key: UserKey) -> FvpSnapshot:
        if user_key not in self._snapshots:
            return FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        return self._snapshots[user_key]
