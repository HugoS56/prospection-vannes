import streamlit as st
import pandas as pd

st.set_page_config(page_title="Prospection Vannes", layout="wide")

st.title("📍 Outil de Prospection Immobilière – Vannes")

# Upload CSV
st.sidebar.header("📁 Charger un fichier DVF")
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
    st.success("Fichier chargé avec succès.")
    
    # Filtrage simple
    st.write("Colonnes disponibles :", df.columns.tolist())
    ville = st.selectbox("Sélectionnez une commune", sorted(villes))
    
    filtered_df = df[df["commune"] == ville]
    st.write(f"🔍 **Nombre de biens trouvés à {ville} :** {len(filtered_df)}")
    st.dataframe(filtered_df)
    
    # Statistiques simples
    if "valeur_fonciere" in df.columns:
        st.write("💰 **Statistiques sur les valeurs foncières**")
        st.write(filtered_df["valeur_fonciere"].describe())
else:
    st.info("Veuillez importer un fichier DVF (.csv) pour commencer.")
