import sqlite3

import pytest
from src.todolist_hexagon.src.todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort
from todolist_hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort

from tests.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import FvpSession as FvpSessionSdk
from todolist_application.secondary.fvp.write.session_set_sqlite import SessionSqlite


@pytest.fixture()
def connection():
    connection = sqlite3.connect(':memory:')
    sdk = SqliteSdk(connection)
    sdk.create_tables()
    return connection


class TestFvpSessionSetSqlite(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        sdk = SqliteSdk(self._connection)
        sdk.upsert_fvp_session(user_key=user_key,
                               fvp_session=FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in
                                                                     snapshot.task_priorities.items()]))

    @pytest.fixture
    def dependencies(self) -> WriteAdapterDependenciesPort:
        raise Exception("implement there")
        #
        # dependencies = Dependencies.create_empty()
        # dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionSqlite.factory)
        # dependencies = dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self._connection)
        # return dependencies
