from dataclasses import dataclass
from datetime import date, datetime
from typing import Any
from uuid import UUID

from expression import Option, Some, Nothing


@dataclass(frozen=True, eq=True)
class Task:
    key: UUID
    name: str
    is_open: bool
    execution_date: Option[date]

    @classmethod
    def from_row(cls, row: Any) -> 'Task':
        task = Task(key=UUID(row[1]),
                    name=row[3],
                    is_open=row[4] == 1,
                    execution_date=Some(datetime.strptime(row[5], "%Y-%m-%d").date()) if row[
                                                                                             5] is not None else Nothing)
        return task


@dataclass(frozen=True, eq=True)
class Todolist:
    key: UUID
    name: str

    @classmethod
    def from_row(cls, row: Any) -> 'Todolist':
        key: UUID = UUID(hex=row[0])
        name: str = row[1]
        return Todolist(key=key, name=name)


@dataclass(frozen=True, eq=True)
class FvpSession:
    priorities: list[tuple[UUID, UUID]]


class TodolistDoesNotExist(Exception):
    pass
