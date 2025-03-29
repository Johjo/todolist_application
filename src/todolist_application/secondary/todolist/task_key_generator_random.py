from uuid import uuid4

from todolist_hexagon.shared.type import TaskKey
from todolist_hexagon.todolist.port import TaskKeyGeneratorPort


class TaskKeyGeneratorRandom(TaskKeyGeneratorPort):
    def generate(self) -> TaskKey:
        return TaskKey(uuid4())
