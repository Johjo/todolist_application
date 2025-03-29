from uuid import uuid4

from todolist_hexagon.shared.type import UserKey
from todolist_hexagon.user.port import UserSnapshot
from todolist_application.secondary.user.user_repository_in_memory import UserRepositoryInMemory


def any_user_key() -> UserKey:
    return UserKey(f"any__{uuid4()}__@mail.com")


class TestUserRepositoryInMemory:
    def test_save_user(self):
        sut = UserRepositoryInMemory()
        expected_user = UserSnapshot(key=UserKey(any_user_key()), todolist=())
        sut.save(expected_user)
        assert sut.by_user(key=expected_user.key) == expected_user

    def test_save_two_users(self):
        sut = UserRepositoryInMemory()
        expected_user_one = UserSnapshot(key=UserKey(any_user_key()), todolist=())
        expected_user_two = UserSnapshot(key=UserKey(any_user_key()), todolist=())
        sut.save(expected_user_one)
        sut.save(expected_user_two)
        assert sut.by_user(key=expected_user_one.key) == expected_user_one
        assert sut.by_user(key=expected_user_two.key) == expected_user_two

    def test_nothing_when_user_does_not_exist(self):
        sut = UserRepositoryInMemory()
        assert sut.by_user(key=any_user_key()) is None
