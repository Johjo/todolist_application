from abc import abstractmethod, ABC

from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort
from todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort

from todolist_application.infra.fvp_memory import FvpMemory
from todolist_application.infra.memory import Memory
from todolist_application.secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
from todolist_application.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory


class ReadInfraDependenciesPort(ABC):
    @abstractmethod
    def memory(self) -> Memory:
        pass

    @abstractmethod
    def fvp_memory(self) -> FvpMemory:
        pass


class ReadAdapterDependenciesForDemo(ReadAdapterDependenciesPort):
    def __init__(self, dependencies: ReadInfraDependenciesPort):
        self._dependencies = dependencies

    def todolist(self) -> TodolistPort:
        return TodolistInMemory(memory=self._dependencies.memory())

    def fvp_session_set(self) -> FvpSessionSetPort:
        return FvpSessionSetInMemory(fvp_memory=self._dependencies.fvp_memory())
