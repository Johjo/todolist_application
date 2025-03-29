import streamlit as st

def main():
    st.set_page_config(page_title="Todo List", page_icon="✅", layout="wide")
    
    st.title("Ma Liste de Tâches")
    
    # Section pour ajouter une nouvelle tâche
    st.header("Ajouter une tâche")
    new_task = st.text_input("Entrez une nouvelle tâche")
    st.button("Ajouter la tâche")
    
    # Section pour afficher les tâches
    st.header("Mes Tâches")
    st.write("Aucune tâche pour le moment.")

if __name__ == "__main__":
    main()
