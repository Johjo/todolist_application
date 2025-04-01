from uuid import uuid4

import streamlit as st
from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort
from todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort
from todolist_hexagon.shared.type import TodolistKey, TaskKey, TaskName, TodolistName
from todolist_hexagon.todolist.aggregate import TaskSnapshot
from todolist_hexagon.todolist.port import TaskKeyGeneratorPort, TodolistSetPort
from todolist_hexagon.use_case_dependencies import UseCaseDependencies
from todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort

from todolist_application.infra.fvp_memory import FvpMemory
from todolist_application.infra.memory import Memory
from todolist_application.secondary.fvp.read.which_task.todolist_memory import TodolistInMemory
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


if "memory" not in st.session_state:
    st.session_state["memory"] = Memory()
memory = st.session_state["memory"]

if "fvp_memory" not in st.session_state:
    st.session_state["fvp_memory"] = FvpMemory()
fvp_memory = st.session_state["fvp_memory"]

if "todolist_key" not in st.session_state:
    st.session_state["todolist_key"] = uuid4()
todolist_key = st.session_state["todolist_key"]


write_dependencies = WriteAdapterDependencies(memory=memory)


class ReadAdapterDependencies(ReadAdapterDependenciesPort):
    def todolist(self) -> TodolistPort:
        return TodolistInMemory(memory=memory)

    def fvp_session_set(self) -> FvpSessionSetPort:
        return FvpSessionSetInMemory(fvp_memory=fvp_memory)


read_dependencies = ReadAdapterDependencies()



create_todolist_use_case = UseCaseDependencies(adapter_dependencies=write_dependencies).create_todolist()
create_todolist_use_case.execute(todolist_key=todolist_key, todolist_name=TodolistName("test"))


def add_task(task_name: str) -> None:
    open_task = UseCaseDependencies(adapter_dependencies=write_dependencies).open_task()
    open_task.execute(todolist_key=todolist_key, task_key=TaskKey(uuid4()), name=TaskName(task_name))

def list_task() -> list[TaskSnapshot]:
    tasks = memory.all_tasks(todolist_key=todolist_key)
    return [task for task in tasks if task.is_open]

def close_task(task_key: TaskKey) -> None:
    use_case = UseCaseDependencies(adapter_dependencies=write_dependencies).close_task()
    use_case.execute(todolist_key=todolist_key, task_key=task_key)

def which_task():
    UseCaseDependencies(adapter_dependencies=read_dependencies).which_task()


def task_component(task: TaskSnapshot):
    def on_task_checkbox_change():
        close_task(task_key=task.key)
    st.checkbox(label=task.name, key=task.key, on_change=on_task_checkbox_change)



def task_list_component():
    st.header("Mes Tâches")
    tasks = list_task()
    if tasks:
        for task in tasks:
            task_component(task=task)
    else:
        st.write("Aucune tâche pour le moment.")




def main():
    st.set_page_config(page_title="Todo List", page_icon="✅", layout="wide")

    add_task_component()
    task_list_component()


    # # Page de sélection/création de todolist
    # st.title("Mes Todolists")
    #
    # # Option de création de nouvelle todolist
    # new_todolist_name = st.text_input("Créer une nouvelle todolist")
    # if st.button("Créer"):
    #     todolist_key = create_todolist(new_todolist_name)
    #     st.session_state['current_todolist'] = todolist_key
    #
    # # Liste des todolists existantes
    # st.header("Mes Todolists")
    # todolists = memory.all_todolist_by_user
    # for (user, key), todolist in todolists.items():
    #     if st.button(f"Ouvrir {todolist.name}"):
    #         st.session_state['current_todolist'] = key
    #
    # # Page de gestion de todolist si une todolist est sélectionnée
    # if 'current_todolist' in st.session_state:
    #     st.title(f"Todolist : {todolists[('any user', st.session_state['current_todolist'])].name}")
    #
    #     # Section pour ajouter une nouvelle tâche
    #     st.header("Ajouter une tâche")
    #     new_task = st.text_input("Entrez une nouvelle tâche")
    #     if st.button("Ajouter la tâche"):
    #         add_task(new_task, st.session_state['current_todolist'])
    #         st.rerun()
    #
    #     # Section pour afficher les tâches
    #     st.header("Mes Tâches")
    #     tasks = list_task(st.session_state['current_todolist'])
    #     if tasks:
    #         for task in tasks:
    #             st.write(f"- {task.name}")
    #     else:
    #         st.write("Aucune tâche pour le moment.")


def add_task_component():
    def on_click_add_task():
        add_task(task_name=task_name)
        st.session_state['todolist_new_task'] = ""

    st.header("Ajouter une tâche")
    task_name = st.text_input("Créer une nouvelle tâche", key="todolist_new_task")
    st.button("Créer", on_click=on_click_add_task)




if __name__ == "__main__":
    main()
