import sqlite3
from typing import cast

from expression import Option, Some, Nothing
from todolist_hexagon.shared.type import TodolistName, TaskKey, TaskName, TaskOpen, TaskExecutionDate, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from todolist_hexagon.todolist.port import TodolistSetPort

from todolist_application.infra.sqlite.sdk import SqliteSdk
from todolist_application.infra.sqlite.type import TodolistDoesNotExist, Todolist as TodolistSdk, Task as TaskSdk


class TodolistSetSqlite(TodolistSetPort):
    def __init__(self, connection: sqlite3.Connection, user_key: str):
        self._sdk = SqliteSdk(connection)
        self._user_key = user_key

    def by(self, todolist_key: TodolistKey) -> Option[TodolistSnapshot]:
        try:
            todolist = self._sdk.todolist_by(user_key=self._user_key, todolist_key=todolist_key)
            tasks = self._sdk.all_tasks(user_key=self._user_key, todolist_key=todolist_key)
            return Some(self._to_todolist_snapshot(todolist, tasks))
        except TodolistDoesNotExist:
            return Nothing

    def _to_todolist_snapshot(self, todolist: TodolistSdk, tasks: list[TaskSdk]) -> TodolistSnapshot:
        return TodolistSnapshot(key=TodolistKey(todolist.key),
                                name=TodolistName(todolist.name),
                                tasks=tuple([self._to_task_snapshot(task) for task in tasks]))

    @staticmethod
    def _to_task_snapshot(task: TaskSdk) -> TaskSnapshot:
        return TaskSnapshot(key=TaskKey(task.key), name=TaskName(task.name), is_open=TaskOpen(task.is_open),
                            execution_date=cast(Option[TaskExecutionDate], task.execution_date))

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._sdk.upsert_todolist(user_key=self._user_key,
                                  todolist=TodolistSdk(key=todolist.key, name=todolist.name),
                                  tasks=[TaskSdk(key=task.key, name=task.name, is_open=task.is_open,
                                                 execution_date=task.execution_date) for task in todolist.tasks])

    def delete(self, todolist_key: TodolistKey) -> None:
        self._sdk.delete_todolist(user_key=self._user_key, todolist_key=todolist_key)
