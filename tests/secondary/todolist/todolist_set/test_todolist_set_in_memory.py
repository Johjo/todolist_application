import pytest
from src.todolist_hexagon.src.todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort
from todolist_hexagon.builder import TodolistBuilder

from tests.secondary.todolist.todolist_set.base_test_todolist_set import BaseTestTodolistSet
from todolist_application.infra.memory import Memory


class TestTodolistSetInMemory(BaseTestTodolistSet):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    @pytest.fixture
    def dependencies(self, current_user: str) -> ReadAdapterDependenciesPort:
        raise Exception("implement there")

        # all_dependencies = Dependencies.create_empty()
        # all_dependencies = all_dependencies.feed_adapter(TodolistSetPort, TodolistSetInMemory.factory)
        # all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        # all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        # return all_dependencies

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())
