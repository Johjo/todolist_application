import pytest
from src.todolist_hexagon.src.todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort

from todolist_hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort

from todolist_application.infra.fvp_memory import FvpMemory
from tests.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet
from todolist_application.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from todolist_application.write_adapter_dependencies_for_demo import WriteAdapterDependenciesForDemo, \
    WriteInfraDependenciesPort


class WriteInfraDependenciesForTest(WriteInfraDependenciesPort):
    def __init__(self, fvp_memory: FvpMemory | None = None):
        self._fvp_memory = fvp_memory

    def fvp_memory(self) -> FvpMemory:
        if not self._fvp_memory:
            raise Exception("fvp_memory not defined")
        return self._fvp_memory


class TestFvpSessionSetInMemory(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self) -> None:
        self._fvp_memory = FvpMemory()

    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        self._fvp_memory.feed(user_key=user_key, snapshot=snapshot)


    @pytest.fixture
    def sut(self) -> FvpSessionSetPort:
        return FvpSessionSetInMemory(fvp_memory=self._fvp_memory)
