from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import date
from typing import NewType
from uuid import UUID

from todolist_hexagon.shared.type import TodolistKey, TaskKey, TodolistName

TodolistContext = NewType('TodolistContext', str)
TodolistContextCount = NewType('TodolistContextCount', int)

class TextFilter:
    def __init__(self, included_words: tuple[str, ...], excluded_words: tuple[str, ...]):
        self._included_words = included_words
        self._excluded_words = excluded_words

    def include(self, text: str) -> bool:
        if not self.match_included_words(text):
            return False

        if self.match_excluded_words(text):
            return False

        return True

    def match_included_words(self, text: str) -> bool:
        if self._included_words == ():
            return True

        for included_word in self._included_words:
            if any(included_word == word for word in text.split()):
                return True
        return False

    def match_excluded_words(self, text: str) -> bool:
        for excluded_word in self._excluded_words:
            if any(excluded_word == word for word in text.split()):
                return True
        return False


@dataclass(frozen=True)
class Criterion:
    pass


@dataclass
class Category:
    pass


@dataclass(frozen=True)
class Include(Criterion):
    category: Category


@dataclass(frozen=True)
class Exclude(Criterion):
    category: Category


@dataclass
class Word(Category):
    value: str

@dataclass
class WithoutDate(Category):
    pass


@dataclass(frozen=True, eq=True)
class TaskFilter:
    todolist_key: TodolistKey
    criteria: tuple[Criterion, ...] = ()

    def include(self, task_name: str) -> bool:
        include_context: set[str] = set()
        exclude_context: set[str] = set()

        for criterion in self.criteria:
            match criterion:
                case Include(Word(word)):
                    include_context.add(word)
                case Exclude(Word(word)):
                    exclude_context.add(word)
                case Exclude(WithoutDate()):
                    pass
                case _:
                    raise ValueError(f"Unknown criterion {criterion}")

        text_filter = TextFilter(included_words=tuple(include_context), excluded_words=tuple(exclude_context))
        return text_filter.include(task_name)

    @classmethod
    def create(cls, todolist_key: TodolistKey, *criteria: Criterion) -> 'TaskFilter':
        return TaskFilter(todolist_key=todolist_key, criteria=tuple(criteria))



@dataclass
class TaskPresentation:
    key: UUID
    name: str
    open: bool
    execution_date: date | None


@dataclass()
class AllTasksPresentation:
    tasks: list[TaskPresentation]


class AllTaskPort(ABC):
    @abstractmethod
    def all_tasks(self, todolist_key: TodolistKey) -> AllTasksPresentation:
        pass


class TodolistSetReadPort(ABC):
    @abstractmethod
    def task_by(self, todolist_key: UUID, task_key: TaskKey) -> TaskPresentation:
        pass

    @abstractmethod
    def all_by_name(self) -> list[TodolistName]:
        pass

    @abstractmethod
    def counts_by_context(self, todolist_key: TodolistKey) -> list[tuple[TodolistContext, TodolistContextCount]]:
        pass

    @abstractmethod
    def all_tasks(self, task_filter: TaskFilter) -> list[TaskPresentation]:
        pass

    @abstractmethod
    def all_tasks_postponed_task(self, todolist_key: UUID) -> list[TaskPresentation]:
        pass
