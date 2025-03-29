from datetime import date

import pytest
from dateutil.utils import today
from src.todolist_hexagon.src.todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort
from todolist_hexagon.builder import TodolistFaker, TodolistBuilder, TaskBuilder

from todolist_application.read.todolist.port import TodolistSetReadPort, TaskFilter, Include, Word, Exclude, \
    TaskPresentation


class BaseTestTodolistSetRead:
    def test_read_task_by(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_task = fake.a_task()
        todolist = fake.a_todolist().having(tasks=[fake.a_task(), expected_task, fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        assert sut.task_by(todolist_key=todolist.to_key(), task_key=expected_task.to_key()) == self.to_presentation(expected_task)

    def test_read_task_having_execution_date(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_task = fake.a_task().having(execution_date=today().date())
        todolist = fake.a_todolist().having(tasks=[fake.a_task(), expected_task, fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        assert sut.task_by(todolist_key=todolist.to_key(), task_key=expected_task.to_key()) == self.to_presentation(expected_task)

    def test_read_all_by_name(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        todolist_1 = fake.a_todolist()
        todolist_2 = fake.a_todolist()
        todolist_3 = fake.a_todolist()
        self.feed_todolist(user_key=current_user, todolist=todolist_1)
        self.feed_todolist(user_key=current_user, todolist=todolist_2)
        self.feed_todolist(user_key=current_user, todolist=todolist_3)
        self.feed_todolist(user_key=fake.a_user_key(), todolist=fake.a_todolist())

        assert sut.all_by_name() == sorted([todolist_1.to_name(), todolist_2.to_name(), todolist_3.to_name()])

    def test_read_counts_by_context(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        todolist = fake.a_todolist().having(tasks=[fake.a_task().having(name="title #context1 #context2"),
                                                   fake.a_task().having(name="#Con_Text3 title #context2"),
                                                   fake.a_task().having(name="@ConText4 title"),
                                                   fake.a_task().having(name="@Con-Text5 title #context2"),
                                                   fake.a_task().having(name="#context1 title #context2",
                                                                        is_open=False),
                                                   ])
        self.feed_todolist(user_key=current_user, todolist=todolist)
        self.feed_todolist(user_key=fake.a_user_key(), todolist=fake.a_todolist(todolist.name).having(tasks=[fake.a_task().having(name="title #context1 #context2")]))

        assert sut.counts_by_context(todolist_key=todolist.to_key()) == [("#context1", 1), ("#context2", 3), ("#con_text3", 1),
                                                        ("@context4", 1), ("@con-text5", 1)]

    def test_read_all_tasks(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_tasks = [fake.a_task().having(name="#include1 buy the milk"), fake.a_task().having(name="buy the water #include2")]
        todolist_1 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task().having(execution_date=today().date())])
        todolist_2 = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(name="#include1 #exclude2"), fake.a_task().having(name="#include2 #exclude1")])
        todolist_3 = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        self.feed_todolist(user_key=current_user, todolist=todolist_1)
        self.feed_todolist(user_key=current_user, todolist=todolist_2)
        self.feed_todolist(user_key=current_user, todolist=todolist_3)

        task_filter = TaskFilter.create(todolist_2.to_key(),
                                        Include(Word("#include1")), Include(Word("#include2")), Exclude(Word("#exclude1")), Exclude(Word("#exclude2")))

        actual = sut.all_tasks(task_filter)

        assert actual == [self.to_presentation(task) for task in expected_tasks]

    def test_read_all_postponed_tasks(self, sut: TodolistSetReadPort, fake: TodolistFaker, current_user: str):
        expected_tasks = [fake.a_task().having(execution_date=date(2018, 10, 17)),
                          fake.a_task().having(execution_date=date(2019, 10, 17)),
                          fake.a_task().having(execution_date=date(2020, 10, 17)),
                          fake.a_task().having(execution_date=date(2021, 11, 23))]
        todolist = fake.a_todolist().having(tasks=[expected_tasks[2], expected_tasks[1], fake.a_task(), expected_tasks[3], fake.a_closed_task(), expected_tasks[0]])
        self.feed_todolist(user_key=current_user, todolist=todolist)

        actual = sut.all_tasks_postponed_task(todolist_key=todolist.to_key())

        assert actual == [self.to_presentation(task) for task in expected_tasks]

    @pytest.fixture
    def current_user(self, fake: TodolistFaker) -> str:
        return "any user"
        # todo : return fake.a_user_key()

    @pytest.fixture
    def sut(self) -> TodolistSetReadPort:
        raise NotImplementedError()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder):
        raise NotImplementedError() # pragma: no cover

    @staticmethod
    def to_presentation(expected_task: TaskBuilder) -> TaskPresentation:
        return TaskPresentation(key=expected_task.to_key(), name=expected_task.to_name(), open=expected_task.to_open(), execution_date=expected_task.to_execution_date().default_value(None))
