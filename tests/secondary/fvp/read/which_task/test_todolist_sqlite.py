import sqlite3
from sqlite3 import Connection

import pytest
from todolist_hexagon.builder import TodolistBuilder, TaskBuilder
from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort
from todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort

from tests.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import Todolist, Task
from todolist_application.secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite


class ReadAdapterDependenciesSqlite(ReadAdapterDependenciesPort):
    def __init__(self, user_key: str, connection: Connection):
        self._connection = connection
        self._user_key = user_key


    def todolist(self) -> TodolistPort:
        return TodolistSqlite(user_key=self._user_key, connection=self._connection)

    def fvp_session_set(self) -> FvpSessionSetPort:
        pass


class TestTodolistSqlite(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._connection = sqlite3.connect(':memory:')
        self._sdk = SqliteSdk(self._connection)
        self._sdk.create_tables()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self._sdk.upsert_todolist(
            user_key=user_key,
            todolist=self._todolist_to_sqlite_sdk(todolist),
            tasks=[self._task_to_sqlite_sdk(task) for task in todolist.to_tasks()])

    @pytest.fixture
    def dependencies(self, current_user: str) -> ReadAdapterDependenciesPort:
        all_dependencies = ReadAdapterDependenciesSqlite(user_key="user@mail.fr", connection=self._connection)
        return all_dependencies

    @staticmethod
    def _todolist_to_sqlite_sdk(todolist: TodolistBuilder) -> Todolist:
        return Todolist(key=todolist.to_key(), name=todolist.to_name())

    @staticmethod
    def _task_to_sqlite_sdk(task: TaskBuilder) -> Task:
        return Task(key=task.to_key(), name=task.to_name(), is_open=task.to_open(), execution_date=task.to_execution_date())
