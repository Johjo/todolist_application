
from expression import Option

from todolist_hexagon.shared.type import TodolistName, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistSnapshot
from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_application.infra.memory import Memory


class TodolistSetInMemory(TodolistSetPort):
    def __init__(self, memory: Memory, user_key: str):
        self.memory = memory
        self._user_key = user_key

    def by(self, todolist_key: TodolistKey) -> Option[TodolistSnapshot]:
        return self.memory.by(user_key=self._user_key, todolist_key=todolist_key)

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self.memory.save(user_key=self._user_key, todolist=todolist)

    def delete(self, todolist_key: TodolistKey) -> None:
        self.memory.delete(user_key=self._user_key, todolist_key=todolist_key)
