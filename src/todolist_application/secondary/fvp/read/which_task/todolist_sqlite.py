import sqlite3

from todolist_hexagon.fvp.aggregate import Task
from todolist_hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from todolist_hexagon.shared.type import UserKey

from todolist_application.infra.sqlite.sdk import SqliteSdk


class TodolistSqlite(TodolistPort):
    def __init__(self, connection: sqlite3.Connection, user_key: str):
        self._sdk = SqliteSdk(connection)
        self._user_key = user_key

    def all_open_tasks(self, user_key: UserKey, task_filter: WhichTaskFilter) -> list[Task]:
        all_tasks = self._sdk.all_open_tasks(user_key=self._user_key, todolist_key=task_filter.todolist_key)
        return [Task(key=task.key) for task in all_tasks if
                task_filter.include(task_name=task.name, task_date=task.execution_date)]
