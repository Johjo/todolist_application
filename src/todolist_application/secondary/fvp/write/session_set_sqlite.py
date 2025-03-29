import sqlite3

from todolist_hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot
from todolist_hexagon.shared.type import TaskKey, UserKey

from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import FvpSession as FvpSessionSdk


class SessionSqlite(FvpSessionSetPort):
    def __init__(self, connection: sqlite3.Connection):
        self._sdk = SqliteSdk(connection)

    def save(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        self._sdk.upsert_fvp_session(user_key=user_key,
                                     fvp_session=FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in
                                                                           snapshot.task_priorities.items()]))

    def by(self, user_key: UserKey) -> FvpSnapshot:
        session: FvpSessionSdk = self._sdk.fvp_session_by(user_key=user_key)
        return FvpSnapshot.from_primitive_dict(
            {TaskKey(ignored): TaskKey(chosen) for (ignored, chosen) in session.priorities})
