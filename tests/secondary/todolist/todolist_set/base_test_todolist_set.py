
import pytest
from dateutil.utils import today
from expression import Nothing, Some
from faker import Faker
from todolist_hexagon.builder import TodolistFaker, TodolistBuilder

from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort

from todolist_application.secondary.todolist.todolist_set.todolist_set_sqlite import TodolistSetSqlite


class BaseTestTodolistSet:
    def test_get_by_when_one_todolist(self, sut: TodolistSetPort, fake: TodolistFaker, current_user: str):
        # given
        expected_todolist = fake.a_todolist()
        self.feed_todolist(user_key=current_user, todolist=expected_todolist)

        # when
        actual = sut.by(todolist_key=expected_todolist.to_key())

        # then
        assert actual.value == expected_todolist.to_snapshot()

    def test_get_by_when_two_todolist(self, sut: TodolistSetPort, fake: TodolistFaker, current_user: str):
        # given
        todolist_one = fake.a_todolist().having(tasks=fake.many_task(3))
        todolist_two = fake.a_todolist().having(tasks=fake.many_task(4))
        self.feed_todolist(user_key=current_user, todolist=todolist_one)
        self.feed_todolist(user_key=current_user, todolist=todolist_two)
        self.feed_todolist(user_key=fake.a_user_key(), todolist=fake.a_todolist(todolist_one.name).having(tasks=fake.many_task(2)))

        # when / then
        assert sut.by(todolist_key=todolist_one.to_key()).value == todolist_one.to_snapshot()
        assert sut.by(todolist_key=todolist_two.to_key()).value == todolist_two.to_snapshot()

    def test_get_by_when_todolist_has_tasks(self, sut: TodolistSetPort, fake: TodolistFaker, current_user: str):
        # given
        expected_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task().having(execution_date=today().date())])
        other_user_todolist = fake.a_todolist(name=expected_todolist.to_name()).having(tasks=fake.many_task(2))

        self.feed_todolist(user_key=current_user, todolist=fake.a_todolist().having(tasks=fake.many_task(2)))
        self.feed_todolist(user_key=current_user, todolist=expected_todolist)
        self.feed_todolist(user_key=fake.a_user_key(), todolist=other_user_todolist)

        #when
        actual = sut.by(todolist_key=expected_todolist.to_key())

        # then
        assert actual.value.tasks[1] == expected_todolist.to_snapshot().tasks[1]
        assert actual == Some(expected_todolist.to_snapshot())

    @staticmethod
    def test_get_when_todolist_does_not_exist(sut: TodolistSetPort, fake: TodolistFaker):
        # given
        unknown_todolist = fake.a_todolist()

        # when
        actual = sut.by(todolist_key=unknown_todolist.to_key())

        # then
        assert actual == Nothing

    @staticmethod
    def test_insert_todolist(sut: TodolistSetPort, fake: TodolistFaker):
        # given
        expected_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])

        # when
        sut.save_snapshot(expected_todolist.to_snapshot())

        # then
        assert sut.by(todolist_key=expected_todolist.to_key()).value == expected_todolist.to_snapshot()

    @staticmethod
    def test_update_todolist(sut: TodolistSetSqlite, fake: TodolistFaker):
        # given
        initial_todolist = fake.a_todolist().having(tasks=[fake.a_task(), fake.a_task()])
        sut.save_snapshot(todolist=initial_todolist.to_snapshot())

        # when
        expected_todolist = initial_todolist.having(tasks=[fake.a_task(), fake.a_task()])
        sut.save_snapshot(todolist=expected_todolist.to_snapshot())

        # then
        assert sut.by(todolist_key=expected_todolist.to_key()).value == expected_todolist.to_snapshot()

    def test_delete_todolist(self, sut: TodolistSetPort, fake: TodolistFaker, current_user: str):
        # given
        todolist = fake.a_todolist()
        self.feed_todolist(user_key=current_user, todolist=todolist)

        # when
        sut.delete(todolist_key=todolist.to_key())

        # then
        assert sut.by(todolist_key=todolist.to_key()) == Nothing

    @pytest.fixture
    def sut(self, dependencies: WriteAdapterDependenciesPort) -> TodolistSetPort:
        raise Exception("implement there")
        # return dependencies.get_adapter(TodolistSetPort)

    @pytest.fixture
    def dependencies(self, current_user: str) -> WriteAdapterDependenciesPort:
        raise NotImplementedError()

    @pytest.fixture
    def current_user(self, fake: TodolistFaker) -> str:
        return fake.a_user_key()

    def feed_todolist(self, user_key: str, todolist: TodolistBuilder) -> None:
        raise NotImplementedError()

    @pytest.fixture
    def fake(self) -> TodolistFaker:
        return TodolistFaker(Faker())

