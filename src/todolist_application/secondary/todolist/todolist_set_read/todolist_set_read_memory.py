import re
from uuid import UUID

from expression import Nothing
from todolist_hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount, TodolistKey

from todolist_application.infra.memory import Memory
from todolist_application.read.todolist.port import TaskPresentation, TodolistSetReadPort, TaskFilter


class TodolistSetReadInMemory(TodolistSetReadPort):
    def __init__(self, memory: Memory, user_key: str):
        self._user_key = user_key
        self.memory = memory

    def task_by(self, todolist_key: UUID, task_key: TaskKey) -> TaskPresentation:
        task = self.memory.task_by(user_key=self._user_key, todolist_key=todolist_key, task_key=task_key)
        return self._to_task_presentation(task)

    @staticmethod
    def _to_task_presentation(task):
        return TaskPresentation(key=task.key, name=task.name, is_open=task.is_open,
                                execution_date=task.execution_date.default_value(None))

    def all_by_name(self) -> list[TodolistName]:
        return sorted([TodolistName(name) for name in self.memory.all_todolist_by_name(user_key=self._user_key)])

    def counts_by_context(self, todolist_key: TodolistKey) -> list[tuple[TodolistContext, TodolistContextCount]]:
        tasks = self.memory.all_tasks(todolist_key=todolist_key)
        counts_by_context: dict[str, int] = {}
        for task in tasks:
            if task.is_open:
                contexts = self._extract_context_from_name(task)
                for context in contexts:
                    counts_by_context[context] = counts_by_context.get(context, 0) + 1
        return [(TodolistContext(context), TodolistContextCount(count)) for context, count in counts_by_context.items()]

    @staticmethod
    def _extract_context_from_name(task):
        contexts = re.findall(r"([#@][_A-Za-z0-9-]+)", task.name)
        return [TodolistContext(context.lower()) for context in contexts]

    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        return [self._to_task_presentation(task) for task in self.memory.all_tasks(
            todolist_key=task_filter.todolist_key) if task_filter.include(task_name=task.name)]

    def all_tasks_postponed_task(self, todolist_key: UUID):
        tasks = [self._to_task_presentation(task) for task in self.memory.all_tasks(todolist_key=todolist_key) if
                 task.is_open and task.execution_date != Nothing]
        return sorted(tasks, key=lambda task: task.execution_date)

