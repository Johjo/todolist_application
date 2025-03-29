import sqlite3

import pytest
from src.todolist_hexagon.src.todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort
from todolist_hexagon.builder import TodolistBuilder

from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite
from tests.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet


class TestTodolistSetSqlite(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.connection = sqlite3.connect(':memory:')
        self.sdk = SqliteSdk(self.connection)
        self.sdk.create_tables()

    @pytest.fixture
    def dependencies(self, current_user: str) -> WriteAdapterDependenciesPort:
        raise Exception("implement there")
        # all_dependencies = Dependencies.create_empty()
        # all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetSqlite.factory)
        # all_dependencies = all_dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self.connection)
        # all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        # return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        raise Exception("implement there")
        # self.sdk.upsert_todolist(user_key=user_key, todolist=todolist.to_sqlite_sdk(),
        #                          tasks=[task.to_sqlite_sdk() for task in todolist.to_tasks()])
