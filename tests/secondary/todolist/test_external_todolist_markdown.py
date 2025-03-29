from datetime import date

import pytest
from expression import Some, Nothing
from faker import Faker
from todolist_hexagon.builder import TodolistFaker, TaskBuilder
from todolist_hexagon.shared.type import TaskName, TaskOpen, TaskExecutionDate
from todolist_hexagon.todolist.write.import_many_task import TaskImported

from todolist_application.secondary.todolist.markdown_todolist import MarkdownTodolist


def test_read_no_task_from_markdown():
    sut = MarkdownTodolist("")
    assert sut.all_tasks() == []


def test_ignore_empty_lines():
    markdown = "- [ ] line 1\n\n- [ ] line 2"
    sut = MarkdownTodolist(markdown)
    assert sut.all_tasks() == [TaskImported(name="line 1", is_open=True, execution_date=Nothing),
                               TaskImported(name="line 2", is_open=True, execution_date=Nothing)]


def test_read_one_task_from_markdown(fake: TodolistFaker):
    expected_task = imported_task_from(fake.a_task())

    markdown = markdown_from_tasks(expected_task)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == [expected_task]


@pytest.mark.parametrize("line_separator", [
    "\n",
    "\r",
    "\r\n"
])
def test_read_many_task_from_markdown(fake: TodolistFaker, line_separator):
    expected_tasks = [imported_task_from(fake.a_task()), imported_task_from(fake.a_task()),
                      imported_task_from(fake.a_task())]

    markdown = markdown_from_tasks(*expected_tasks, line_separator=line_separator)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


def test_read_closed_task(fake: TodolistFaker):
    expected_tasks = [imported_task_from(fake.a_closed_task())]

    markdown = markdown_from_tasks(*expected_tasks)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


@pytest.mark.parametrize("text, expected", [
    ["- [ ] l{execution_date=2022-07-13}",
     TaskImported(name=TaskName("l"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],
    ["- [ ] le{execution_date=2022-07-13}",
     TaskImported(name=TaskName("le"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],
    ["- [ ] left{execution_date=2022-07-13}",
     TaskImported(name=TaskName("left"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],
    ["- [ ] left{execution_date=2022-07-13}r",
     TaskImported(name=TaskName("left r"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],
    ["- [ ] left{execution_date=2022-07-13}ri",
     TaskImported(name=TaskName("left ri"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],

    ["- [ ] left{execution_date=2022-07-13}right",
     TaskImported(name=TaskName("left right"), is_open=TaskOpen(True),
                  execution_date=Some(TaskExecutionDate(date(2022, 7, 13))))],
])
def test_read_execution_date(text, expected):
    sut = MarkdownTodolist(text)

    assert sut.all_tasks() == [expected]


@pytest.mark.parametrize("text, expected", [
    ["- [ ] left}2022-07-13{right",
     TaskImported(name=TaskName("left}2022-07-13{right"), is_open=TaskOpen(True), execution_date=Nothing)],
])
def test_ignore_bad_caracters(text, expected):
    sut = MarkdownTodolist(text)

    assert sut.all_tasks() == [expected]


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def markdown_from_tasks(*tasks: TaskImported, line_separator="\n") -> str:
    return line_separator.join([f"- [{" " if task.is_open else "x"}] {task.name}" for task in tasks])


def imported_task_from(task: TaskBuilder) -> TaskImported:
    return TaskImported(name=task.to_name(), is_open=task.to_open(), execution_date=task.to_execution_date())
