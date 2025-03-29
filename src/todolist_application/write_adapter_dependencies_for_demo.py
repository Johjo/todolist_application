from abc import ABC, abstractmethod

from src.todolist_hexagon.src.todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort
from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort

from todolist_application.infra.fvp_memory import FvpMemory
from todolist_application.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory


class WriteInfraDependenciesPort(ABC):
    @abstractmethod
    def fvp_memory(self) -> FvpMemory:
        pass


class WriteAdapterDependenciesForDemo(WriteAdapterDependenciesPort):
    def __init__(self, infra_dependencies: WriteInfraDependenciesPort):
        self._infra_dependencies = infra_dependencies

    def todolist_set(self) -> TodolistSetPort:
        raise Exception("Not implemented")

    def task_key_generator(self) -> TaskKeyGeneratorPort:
        raise Exception("Not implemented")

    def fvp_session_set(self) -> FvpSessionSetPort:
        return FvpSessionSetInMemory(fvp_memory=self._infra_dependencies.fvp_memory())
