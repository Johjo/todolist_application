from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort


class QueryAdapterDependencies:
    def todolist(self) -> TodolistPort: ...

    def fvp_session_set(self) -> FvpSessionSetPort: ...
