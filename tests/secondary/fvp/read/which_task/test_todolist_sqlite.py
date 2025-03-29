import sqlite3

import pytest
from todolist_hexagon.builder import TodolistBuilder

from todolist_hexagon.fvp.read.which_task import TodolistPort
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.query_adapter_dependencies import QueryAdapterDependencies
from todolist_application.secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite
from tests.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistSqlite(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._connection = sqlite3.connect(':memory:')
        self._sdk = SqliteSdk(self._connection)
        self._sdk.create_tables()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        raise Exception("implement there")
        # self._sdk.upsert_todolist(
        #     user_key=user_key,
        #     todolist=todolist.to_sqlite_sdk(),
        #     tasks=[task.to_sqlite_sdk() for task in todolist.to_tasks()])

    @pytest.fixture
    def dependencies(self, current_user: str) -> QueryAdapterDependencies:
        all_dependencies = QueryAdapterDependencies()
        # all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistSqlite.factory)
        # all_dependencies = all_dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self._connection)
        # all_dependencies= all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies
