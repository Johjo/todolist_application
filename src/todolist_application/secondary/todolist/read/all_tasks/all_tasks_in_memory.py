from todolist_hexagon.shared.type import TodolistKey
from todolist_application.infra.memory import Memory
from todolist_application.read.todolist.port import AllTaskPort, AllTasksPresentation, TaskPresentation


class AllTaskInMemory(AllTaskPort):
    def __init__(self, memory: Memory):
        self._memory = memory

    def all_tasks(self, todolist_key: TodolistKey) -> AllTasksPresentation:
        all_tasks = self._memory.all_tasks(todolist_key=todolist_key)
        return AllTasksPresentation(tasks=tuple(TaskPresentation(key=task.key, name=task.name, open=task.is_open, execution_date=task.execution_date.default_value(None)) for task in all_tasks))

