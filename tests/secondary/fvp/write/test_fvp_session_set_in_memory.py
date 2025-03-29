import pytest
from src.todolist_hexagon.src.use_case_dependencies import AdapterDependenciesPort

from todolist_hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from todolist_application.infra.fvp_memory import FvpMemory
from todolist_application.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from tests.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


class TestFvpSessionSetInMemory(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self) -> None:
        self._fvp_memory = FvpMemory()

    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        self._fvp_memory.feed(user_key=user_key, snapshot=snapshot)

    @pytest.fixture
    def dependencies(self) -> AdapterDependenciesPort:
        raise Exception("implement there")
        # dep = Dependencies.create_empty()
        # dep = dep.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
        # dep = dep.feed_infrastructure(FvpMemory, lambda _: self._fvp_memory)
        # dep = dep.feed_data(data_name=USER_KEY, value="any user")
        # return dep
