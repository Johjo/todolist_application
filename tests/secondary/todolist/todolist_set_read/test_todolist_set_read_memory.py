import pytest
from faker import Faker
from todolist_hexagon.builder import TodolistFaker, TodolistBuilder

from tests.secondary.todolist.todolist_set_read.base_test_todolist_set_read import BaseTestTodolistSetRead
from todolist_application.infra.memory import Memory
from todolist_application.read.todolist.port import TodolistSetReadPort
from todolist_application.secondary.todolist.todolist_set_read.todolist_set_read_memory import TodolistSetReadInMemory


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


class TestTodolistSetReadMemory(BaseTestTodolistSetRead):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    def feed_todolist(self, user_key:str, todolist: TodolistBuilder):
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())

    @pytest.fixture
    def sut(self) -> TodolistSetReadPort:
        return TodolistSetReadInMemory(memory=self.memory, user_key="any user")
