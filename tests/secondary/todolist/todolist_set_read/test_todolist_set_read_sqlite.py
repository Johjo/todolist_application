import sqlite3

import pytest
from faker import Faker
from todolist_hexagon.builder import TodolistFaker, TodolistBuilder, TaskBuilder

from tests.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead
from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import Todolist, Task
from todolist_application.read.todolist.port import TodolistSetReadPort
from todolist_application.secondary.todolist.todolist_set_read.todolist_set_read_sqlite import TodolistSetReadSqlite


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


class TestTodolistSetReadSqlite(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._connection = sqlite3.connect(':memory:')
        self.sdk = SqliteSdk(self._connection)
        self.sdk.create_tables()

    @pytest.fixture
    def sut(self) -> TodolistSetReadPort:
        return TodolistSetReadSqlite(connection=self._connection, user_key="any user")


    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.sdk.upsert_todolist(user_key=user_key, todolist=self.todolist_to_sqlite(todolist),
                                 tasks=[self.task_to_sqlite(task) for task in todolist.to_tasks()])

    @staticmethod
    def todolist_to_sqlite(todolist: TodolistBuilder) -> Todolist:
        return Todolist(key=todolist.to_key(), name=todolist.to_name())

    @staticmethod
    def task_to_sqlite(task: TaskBuilder) -> Task:
        return Task(key=task.to_key(), name=task.to_name(), is_open=task.to_open(),
                    execution_date=task.to_execution_date())
