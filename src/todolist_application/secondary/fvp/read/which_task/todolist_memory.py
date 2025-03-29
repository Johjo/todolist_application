from todolist_hexagon.fvp.aggregate import Task
from todolist_hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from todolist_hexagon.shared.type import UserKey
from todolist_application.infra.memory import Memory


class TodolistInMemory(TodolistPort):
    def __init__(self, memory: Memory):
        self.memory = memory

    def all_open_tasks(self, user_key: UserKey, task_filter: WhichTaskFilter) -> list[Task]:
        tasks = [task for task in self.memory.all_tasks(todolist_key=task_filter.todolist_key)
                 if task.is_open]
        return [Task(key=task.key) for task in tasks if
                task_filter.include(task.name, task.execution_date)]
