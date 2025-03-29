from datetime import date

import pytest
from faker import Faker
from todolist_hexagon.builder import TodolistFaker, TodolistBuilder
from todolist_hexagon.fvp.aggregate import Task
from todolist_hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter
from todolist_hexagon.query_dependencies import QueryAdapterDependenciesPort
from todolist_hexagon.shared.type import UserKey

from todolist_application.secondary.fvp.read.which_task.todolist_sqlite import TodolistSqlite


class BaseTestTodolist:
    def test_should_list_open_tasks(self, sut: TodolistPort, fake: TodolistFaker, current_user: UserKey):
        expected_tasks = [fake.a_task(), fake.a_task()]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task().having(is_open=False)])
        another_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)
        self.feed_todolist(user_key=current_user, todolist=another_todolist)

        assert sut.all_open_tasks(user_key=current_user, task_filter=
        WhichTaskFilter(todolist_key=expected_todolist.to_key(), reference_date=fake.a_date())) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    def test_should_list_only_task_having_one_included_context(self, sut: TodolistPort, fake: TodolistFaker,
                                                               current_user: UserKey):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"),
                          fake.a_task().having(name="buy the water #supermarket")]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        task_filter = WhichTaskFilter(todolist_key=expected_todolist.to_key(), include_context=("#supermarket",),
                                      reference_date=fake.a_date())
        assert sut.all_open_tasks(user_key=current_user, task_filter=task_filter) == [Task(key=task.to_key()) for task
                                                                                      in
                                                                                      expected_tasks]

    def test_should_list_only_task_having_any_included_context(self, sut: TodolistPort, fake: TodolistFaker,
                                                               current_user: UserKey):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"),
                          fake.a_task().having(name="jogging #sport")]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks, fake.a_task()])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        assert sut.all_open_tasks(user_key=current_user,
                                  task_filter=WhichTaskFilter(todolist_key=expected_todolist.to_key(),
                                                              include_context=("#supermarket", "#sport"),
                                                              reference_date=fake.a_date())) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    def test_should_not_list_task_having_any_excluded_context(self, sut: TodolistPort, fake: TodolistFaker,
                                                              current_user: UserKey):
        expected_tasks = [fake.a_task().having(name="buy the milk #supermarket"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket #sport")])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        assert sut.all_open_tasks(user_key=current_user,
                                  task_filter=WhichTaskFilter(todolist_key=expected_todolist.to_key(),
                                                              include_context=("#supermarket",),
                                                              exclude_context=("#sport",),
                                                              reference_date=fake.a_date())) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    def test_should_include_only_task_matching_full_context(self, sut: TodolistPort, fake: TodolistFaker,
                                                            current_user: UserKey):
        expected_tasks = [fake.a_task().having(name="become #super man"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="buy the water #supermarket")])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        assert sut.all_open_tasks(user_key=current_user,
                                  task_filter=WhichTaskFilter(todolist_key=expected_todolist.to_key(),
                                                              include_context=("#super",), exclude_context=(),
                                                              reference_date=fake.a_date())) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    def test_should_exclude_only_task_matching_full_context(self, sut: TodolistPort, fake: TodolistFaker,
                                                            current_user: UserKey):
        expected_tasks = [fake.a_task().having(name="buy the water #supermarket"), ]
        expected_todolist = fake.a_todolist().having(
            tasks=[*expected_tasks, fake.a_task().having(name="become #super man")])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        assert sut.all_open_tasks(user_key=current_user,
                                  task_filter=WhichTaskFilter(todolist_key=expected_todolist.to_key(),
                                                              include_context=(),
                                                              exclude_context=("#super",),
                                                              reference_date=fake.a_date())) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    def test_should_exclude_task_having_execution_task_in_future(self, sut: TodolistPort, fake: TodolistFaker,
                                                                 current_user: UserKey):
        reference_date: date = fake.a_date()
        expected_tasks = [fake.a_task(), fake.a_task().having(execution_date=fake.a_date(before=reference_date))]
        expected_todolist = fake.a_todolist().having(tasks=[*expected_tasks,
                                                            fake.a_task().having(is_open=False),
                                                            fake.a_task().having(
                                                                execution_date=fake.a_date(after=reference_date))])

        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        assert sut.all_open_tasks(user_key=current_user,
                                  task_filter=WhichTaskFilter(todolist_key=expected_todolist.to_key(),
                                                              reference_date=reference_date)) == [
                   Task(key=task.to_key()) for task in expected_tasks]

    @staticmethod
    def test_should_no_task_when_todolist_does_not_exist(sut: TodolistPort, fake: TodolistFaker):
        unknown_todolist = fake.a_todolist()
        assert sut.all_open_tasks(user_key=UserKey(fake.a_user_key()),
                                  task_filter=WhichTaskFilter(todolist_key=unknown_todolist.to_key(),
                                                              reference_date=fake.a_date())) == []

    @pytest.fixture
    def dependencies(self, current_user: str) -> QueryAdapterDependenciesPort:
        raise NotImplementedError()

    def feed_todolist(self, user_key: UserKey, todolist: TodolistBuilder) -> None:
        raise NotImplementedError()

    @pytest.fixture
    def fake(self) -> TodolistFaker:
        return TodolistFaker(Faker())

    @pytest.fixture
    def sut(self, dependencies: QueryAdapterDependenciesPort) -> TodolistPort:
        return dependencies.todolist()

    @pytest.fixture
    def current_user(self, fake: TodolistFaker) -> UserKey:
        return UserKey(fake.a_user_key())
