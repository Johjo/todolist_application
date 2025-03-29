from datetime import datetime

from todolist_application.dependencies import Dependencies
from todolist_application.primary.controller.write.todolist import DateTimeProviderPort


class DateTimeProvider(DateTimeProviderPort):
    def now(self) -> datetime:
        return datetime.now()

    @classmethod
    def factory(cls, _: Dependencies) -> 'DateTimeProvider':
        return DateTimeProvider()
