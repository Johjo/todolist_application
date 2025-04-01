import sqlite3

import pytest
from todolist_hexagon.builder import TodolistBuilder, TaskBuilder
from todolist_hexagon.todolist.port import TodolistSetPort

from tests.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import Todolist, Task
from todolist_application.secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite


class TestTodolistSetSqlite(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.connection = sqlite3.connect(':memory:')
        self.sdk = SqliteSdk(self.connection)
        self.sdk.create_tables()

    @pytest.fixture
    def sut(self) -> TodolistSetPort:
        return TodolistSetSqlite(connection=self.connection, user_key="any user")


    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=self.todolist_to_sqlite(todolist),
                                 tasks=[self.task_to_sqlite(task) for task in todolist.to_tasks()])

    @staticmethod
    def todolist_to_sqlite(todolist: TodolistBuilder) -> Todolist:
        return Todolist(key=todolist.to_key(), name=todolist.to_name())

    @staticmethod
    def task_to_sqlite(task: TaskBuilder) -> Task:
        return Task(key=task.to_key(), name=task.to_name(), is_open=task.to_open(), execution_date=task.to_execution_date())
