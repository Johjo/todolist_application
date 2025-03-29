from uuid import UUID, uuid4

import streamlit as st
from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.shared.type import TodolistKey, TaskKey, TaskName, TodolistName
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

def create_todolist(todolist_name: str) -> None:
    create_todolist_use_case = UseCaseDependencies(adapter_dependencies=dependencies).create_todolist()
    todolist_key = TodolistKey(uuid4())
    create_todolist_use_case.execute(todolist_key=todolist_key, todolist_name=TodolistName(todolist_name))
    return todolist_key

def add_task(task: str, todolist_key: TodolistKey) -> None:
    open_task = UseCaseDependencies(adapter_dependencies=dependencies).open_task()
    open_task.execute(todolist_key=todolist_key, task_key=TaskKey(uuid4()), name=TaskName(task))

def list_task(todolist_key: TodolistKey) -> list[TaskSnapshot]:
    tasks = memory.all_tasks(todolist_key=todolist_key)
    return tasks

def main():
    st.set_page_config(page_title="Todo List", page_icon="✅", layout="wide")

    # Page de sélection/création de todolist
    st.title("Mes Todolists")
    
    # Option de création de nouvelle todolist
    new_todolist_name = st.text_input("Créer une nouvelle todolist")
    if st.button("Créer"):
        todolist_key = create_todolist(new_todolist_name)
        st.session_state['current_todolist'] = todolist_key

    # Liste des todolists existantes
    st.header("Mes Todolists")
    todolists = memory.all_todolist_by_user
    for (user, key), todolist in todolists.items():
        if st.button(f"Ouvrir {todolist.name}"):
            st.session_state['current_todolist'] = key

    # Page de gestion de todolist si une todolist est sélectionnée
    if 'current_todolist' in st.session_state:
        st.title(f"Todolist : {todolists[('any user', st.session_state['current_todolist'])].name}")

        # Section pour ajouter une nouvelle tâche
        st.header("Ajouter une tâche")
        new_task = st.text_input("Entrez une nouvelle tâche")
        if st.button("Ajouter la tâche"):
            add_task(new_task, st.session_state['current_todolist'])
            st.rerun()

        # Section pour afficher les tâches
        st.header("Mes Tâches")
        tasks = list_task(st.session_state['current_todolist'])
        if tasks:
            for task in tasks:
                st.write(f"- {task.name}")
        else:
            st.write("Aucune tâche pour le moment.")

if __name__ == "__main__":
    main()
