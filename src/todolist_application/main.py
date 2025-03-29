import streamlit as st

def add_task(task):
    print(f"Nouvelle tâche ajoutée : {task}")

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
