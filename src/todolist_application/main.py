from uuid import UUID, uuid4

import streamlit as st
from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.shared.type import TodolistKey, TaskKey, TaskName
from todolist_hexagon.todolist.aggregate import TaskSnapshot
from todolist_hexagon.todolist.port import TaskKeyGeneratorPort, TodolistSetPort
from todolist_hexagon.todolist.write.open_task import OpenTaskUseCase
from todolist_hexagon.use_case_dependencies import UseCaseDependencies
from todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort

from todolist_application.infra.fvp_memory import FvpMemory
from todolist_application.infra.memory import Memory
from todolist_application.read.todolist.port import AllTasksPresentation
from todolist_application.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from todolist_application.secondary.todolist.task_key_generator_random import TaskKeyGeneratorRandom
from todolist_application.secondary.todolist.todolist_set.todolist_set_in_memory import TodolistSetInMemory


class WriteAdapterDependencies(WriteAdapterDependenciesPort):
    def __init__(self, memory: Memory):
        self._fvp_memory = FvpMemory()
        self._memory = memory

    def todolist_set(self) -> TodolistSetPort:
        return TodolistSetInMemory(memory=self._memory, user_key="any user")

    def task_key_generator(self) -> TaskKeyGeneratorPort:
        return TaskKeyGeneratorRandom()

    def fvp_session_set(self) -> FvpSessionSetPort:
        return FvpSessionSetInMemory(fvp_memory=self._fvp_memory)


memory = Memory()
dependencies = WriteAdapterDependencies(memory)

def add_task(task: str) -> None:
    open_task = UseCaseDependencies(adapter_dependencies=dependencies).open_task()
    open_task.execute(todolist_key=TodolistKey(UUID(int=1)), task_key=TaskKey(uuid4()), name=TaskName(task))

def list_task() -> list[TaskSnapshot]:
    tasks = memory.all_tasks(todolist_key=TodolistKey(UUID(int=1)))
    return tasks

def main():
    st.set_page_config(page_title="Todo List", page_icon="✅", layout="wide")

    st.title("Ma Liste de Tâches")

    # Section pour ajouter une nouvelle tâche
    st.header("Ajouter une tâche")
    new_task = st.text_input("Entrez une nouvelle tâche")
    if st.button("Ajouter la tâche"):
        add_task(new_task)
    
    # Section pour afficher les tâches
    st.header("Mes Tâches")
    st.write("Aucune tâche pour le moment.")

if __name__ == "__main__":
    main()
