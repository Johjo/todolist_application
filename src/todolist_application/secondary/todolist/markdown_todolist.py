import re
from datetime import datetime
from typing import Tuple

from expression import Nothing, Some, Option

from todolist_hexagon.shared.type import TaskName, TaskOpen, TaskExecutionDate
from todolist_hexagon.todolist.write.import_many_task import ExternalTodoListPort, TaskImported

TASK_NAME_KEY = "task_name"
EXECUTION_DATE_KEY = "execution_date"

class MarkdownTodolist(ExternalTodoListPort):
    def __init__(self, markdown: str) -> None:
        self._markdown = markdown

    def all_tasks(self) -> list[TaskImported]:
        tasks_and_empties = (self.to_task(line=line) for line in self._markdown.splitlines())
        return [task.value for task in tasks_and_empties if task != Nothing]

    @staticmethod
    def to_task(line: str) -> Option[TaskImported]:
        pattern = r"- (\[[x ]\]) (.+)"
        task = re.match(pattern, line)
        if task:
            is_open = task.group(1) == "[ ]"
            body =  task.group(2)
            name, execution_date = MarkdownTodolist.from_body(body)
            return Some(TaskImported(name=name, is_open=TaskOpen(is_open), execution_date=execution_date))
        return Nothing

    @staticmethod
    def from_body(body: str) -> Tuple[TaskName, Option[TaskExecutionDate]]:
        values : dict[str, str] = MarkdownTodolist.extract_name_and_values(body)
        return MarkdownTodolist.to_task_name(body, values), MarkdownTodolist.to_execution_date(values)

    @staticmethod
    def extract_name_and_values(body: str) -> dict[str, str]:
        values = {}
        left_end = body.find("{")
        if left_end != -1:
            left = body[0: left_end]
            right_start = body.find("}")
            if left_end < right_start:
                right = body[right_start + 1:]
                if right != "":
                    values[TASK_NAME_KEY] = left + " " + right
                else:
                    values[TASK_NAME_KEY] = left

                start_value = body.find("=", left_end)
                values[EXECUTION_DATE_KEY] = body[start_value + 1: right_start]
        return values

    @staticmethod
    def to_task_name(body, values):
        task_name = values.get(TASK_NAME_KEY, body)
        name = TaskName(task_name)
        return name

    @staticmethod
    def to_execution_date(values: dict[str, str]) -> Option[TaskExecutionDate]:
        value: str | None = values.get("execution_date", None)
        if not value:
            return Nothing

        execute_date_as_date = datetime.strptime(value, "%Y-%m-%d").date()
        execution_date = Some(TaskExecutionDate(execute_date_as_date))
        return execution_date

