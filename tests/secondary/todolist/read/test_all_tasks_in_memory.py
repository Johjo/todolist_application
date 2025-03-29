from dataclasses import dataclass
from uuid import uuid4, UUID

import pytest
from faker import Faker
from todolist_hexagon.builder import TodolistFaker
from todolist_hexagon.shared.type import TaskExecutionDate

from todolist_application.infra.memory import Memory
from todolist_application.secondary.todolist.read.all_tasks.all_tasks_in_memory import AllTaskInMemory


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


@dataclass(frozen=True, eq=True)
class TaskPresentation:
    key: UUID
    name: str
    open: bool
    execution_date: TaskExecutionDate | None


@dataclass(frozen=True, eq=True)
class AllTasksPresentation:
    tasks: tuple[TaskPresentation, ...]


def test_xxx(fake: TodolistFaker):
    # GIVEN
    memory = Memory()
    sut = AllTaskInMemory(memory=memory)
    task_one = fake.a_task().having(execution_date=fake.a_date(), is_open=False)
    task_two = fake.a_task().having(is_open=True)

    todolist = fake.a_todolist().having(tasks=[task_one, task_two])
    memory.save(user_key=f"any_user{uuid4()}", todolist=todolist.to_snapshot())

    # WHEN
    actual = sut.all_tasks(todolist_key=todolist.to_key())

    # THEN
    assert str(actual) == str(AllTasksPresentation(tasks=(
        TaskPresentation(key=task_one.to_key(), name=task_one.to_name(), open=False,
                         execution_date=task_one.to_execution_date().value),
        TaskPresentation(key=task_two.to_key(), name=task_two.to_name(), open=True, execution_date=None),
    )))
