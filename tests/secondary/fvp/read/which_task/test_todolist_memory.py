import pytest
from todolist_hexagon.builder import TodolistBuilder
from todolist_hexagon.query_dependencies import QueryAdapterDependenciesPort

from todolist_application.query_adapter_dependencies import QueryAdapterDependencies
from todolist_application.infra.memory import Memory
from tests.secondary.fvp.read.which_task.base_test_todolist import BaseTestTodolist


class TestTodolistMemory(BaseTestTodolist):
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.memory = Memory()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        self.memory.save(user_key=user_key, todolist=todolist.to_snapshot())

    @pytest.fixture
    def dependencies(self, current_user: str) -> QueryAdapterDependenciesPort:
        all_dependencies = QueryAdapterDependencies()
        # all_dependencies = all_dependencies.feed_adapter(TodolistPort, TodolistInMemory.factory)
        # all_dependencies = all_dependencies.feed_infrastructure(Memory, lambda _: self.memory)
        # all_dependencies = all_dependencies.feed_data(data_name=USER_KEY, value=current_user)
        return all_dependencies
