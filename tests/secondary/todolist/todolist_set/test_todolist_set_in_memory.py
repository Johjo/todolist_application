import pytest
from todolist_hexagon.builder import TodolistBuilder
from todolist_hexagon.todolist.port import TodolistSetPort

from tests.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet
from todolist_application.infra.memory import Memory
from todolist_application.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory


class TestTodolistSetInMemory(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    @pytest.fixture
    def sut(self) -> TodolistSetPort:
        return TodolistSetInMemory(memory=self.memory, user_key="any user")


    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())
