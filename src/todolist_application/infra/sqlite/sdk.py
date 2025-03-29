from datetime import datetime
from sqlite3 import Connection
from typing import Any
from uuid import UUID

from expression import Nothing, Some
from todolist_hexagon.shared.type import UserKey

from todolist_application.infra.sqlite.type import Task, Todolist, FvpSession, TodolistDoesNotExist


class SqliteSdk:
    def __init__(self, connection: Connection):
        self._connection = connection

    def all_tasks(self, user_key: str, todolist_key: UUID) -> list[Task]:
        cursor = self._connection.cursor()
        todolist_id : int
        cursor.execute(
            "SELECT task_key, Task.name as name, is_open, execution_date from Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE todolist.user_key = ? and todolist.todolist_key = ?",
            (user_key, todolist_key.hex,))
        return [self.to_task(row) for row in cursor.fetchall()]

    @staticmethod
    def to_task(row: Any) -> Task:
        execution_date = row[3]
        task = Task(key=UUID(row[0]),
                    name=row[1],
                    is_open=row[2] == 1,
                    execution_date=Some(datetime.strptime(execution_date, "%Y-%m-%d").date()) if execution_date is not None else Nothing)
        return task

    def task_by(self, todolist_key: UUID, task_key: UUID) -> Task:
        cursor = self._connection.cursor()
        cursor.execute("SELECT task_key, Task.name as name, is_open, execution_date FROM Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE todolist.todolist_key = ? and task_key = ?", (todolist_key.hex, task_key.hex))
        fetchone = cursor.fetchone()
        return self.to_task(fetchone)

    def all_todolist(self, user_key: str) -> list[Todolist]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT todolist_key, name from Todolist WHERE user_key = ? ORDER BY name", (user_key, ))
        return [Todolist.from_row(row) for row in cursor.fetchall()]

    def all_open_tasks(self, user_key: str, todolist_key: UUID):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_key, Task.name as name, is_open, execution_date FROM Task INNER JOIN Todolist on Task.todolist_id = Todolist.id WHERE Todolist.todolist_key = ? AND is_open = ? ", (todolist_key.hex, True)
            )
        return [self.to_task(row) for row in cursor.fetchall()]

    def todolist_by(self, user_key: str, todolist_key: UUID) -> Todolist:
        cursor = self._connection.cursor()
        cursor.execute("SELECT todolist_key, name from Todolist where todolist_key = ? and user_key = ?", (todolist_key.hex, user_key))
        row = cursor.fetchone()
        if not row:
            raise TodolistDoesNotExist()
        return Todolist.from_row(row)

    def upsert_todolist(self, user_key: str, todolist: Todolist, tasks: list[Task]):
        self._delete_previous_todolist(user_key=user_key, todolist_key=todolist.key)
        self._save_todolist(user_key=user_key, todolist_key=todolist.key, todolist_name=todolist.name, tasks=tasks)

    def _save_todolist(self, user_key: str, todolist_key: UUID, todolist_name: str, tasks: list[Task]):
        cursor = self._connection.cursor()
        cursor.execute("INSERT into Todolist (user_key, todolist_key, name) VALUES (?, ?, ?) ",
                       (user_key, todolist_key.hex, todolist_name,))
        todolist_id = self._todolist_id(user_key, todolist_name)
        for task in tasks:
            cursor.execute(
                "INSERT into TASK (todolist_id, task_key, name, is_open, execution_date) VALUES (?, ?, ?, ?, ?)",
                           (todolist_id, task.key.hex, task.name, task.is_open, task.execution_date.default_value(None)))

    def _todolist_id(self, user_key: str, todolist_name: str) -> int:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id from Todolist where user_key=? and name=?", (user_key, todolist_name))
        todolist_id: int = cursor.fetchone()[0]
        return todolist_id

    def _delete_previous_todolist(self, user_key: str, todolist_key: UUID) -> None:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id from Todolist where user_key=? and todolist_key=?", (user_key, todolist_key.hex))
        row = cursor.fetchone()
        if row:
            todolist_id : int = row[0]
            cursor.execute("DELETE from Todolist where id = ?", (todolist_id, ))
            cursor.execute("DELETE from Task where todolist_id = ?", (todolist_id, ))


    def create_tables(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE Todolist(id INTEGER PRIMARY KEY AUTOINCREMENT, todolist_key, name, user_key)")
        cursor.execute("CREATE INDEX todolist_name_idx ON Todolist (name);")

        cursor.execute(
            "CREATE TABLE Task(id INTEGER PRIMARY KEY AUTOINCREMENT, todolist_id, task_key, name, is_open, execution_date)")

        cursor.execute("CREATE TABLE Session(id INTEGER PRIMARY KEY AUTOINCREMENT, user_key, ignored_task_key, chosen_task_key)")


    def upsert_fvp_session(self, user_key: str, fvp_session: FvpSession) -> None:
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Session where user_key=?", (user_key,))
        for ignored, chosen in fvp_session.priorities:
            cursor.execute("INSERT INTO Session(user_key, ignored_task_key, chosen_task_key) VALUES (?, ?, ?)", (user_key,str(ignored), str(chosen)))

    def fvp_session_by(self, user_key: UserKey) -> FvpSession:
        cursor = self._connection.cursor()
        cursor.execute("SELECT ignored_task_key, chosen_task_key FROM Session where user_key = ?", (user_key,))
        rows = cursor.fetchall()
        return FvpSession(priorities=[(UUID(session[0]), UUID(session[1])) for session in rows])

    def delete_todolist(self, user_key: str, todolist_key: UUID):
        self._delete_previous_todolist(user_key=user_key, todolist_key=todolist_key)
