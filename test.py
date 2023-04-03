import streamlit as st

# Créer des onglets
tabs = ["Page 1", "Page 2", "Page 3"]
page = st.sidebar.selectbox("Sélectionner une page", tabs)

# Générer un identifiant unique pour chaque page
selected_page = hash(page)

# Définir les paramètres d'URL pour chaque page
params = {"page": selected_page}

# Mettre à jour l'URL avec les paramètres sélectionnés
st.experimental_set_query_params(**params)

# Afficher le contenu de la page sélectionnée
if page == "Page 1":
    st.write("Contenu de la page 1")
elif page == "Page 2":
    st.write("Contenu de la page 2")
else:
    st.write("Contenu de la page 3")

