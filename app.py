import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Prospection Vannes", layout="wide")

st.title("📍 Outil de Prospection Immobilière – Vannes")

# Upload CSV
st.sidebar.header("📁 Charger un fichier DVF")
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
    st.success("Fichier chargé avec succès.")

    # Nettoyage de la colonne l_codinsee (si elle contient des listes en string)
    if df["l_codinsee"].dtype == object and df["l_codinsee"].str.startswith("[").any():
        try:
            df["l_codinsee"] = df["l_codinsee"].apply(ast.literal_eval)
            df = df.explode("l_codinsee")
        except Exception as e:
            st.error(f"Erreur lors du traitement de 'l_codinsee' : {e}")

    # Filtrage par code INSEE
    if "l_codinsee" in df.columns:
        codes_insee = df["l_codinsee"].dropna().unique()
        ville = st.selectbox("Sélectionnez un code INSEE", sorted(codes_insee))
        filtered_df = df[df["l_codinsee"] == ville]

        st.write(f"🔍 **Nombre de biens trouvés pour la commune {ville} :** {len(filtered_df)}")
        st.dataframe(filtered_df)

        # Statistiques
        if "valeurfonc" in df.columns:
            st.markdown("💰 **Statistiques sur les valeurs foncières**")
            st.write(filtered_df["valeurfonc"].describe())
        else:
            st.warning("La colonne 'valeurfonc' n'existe pas dans ce fichier.")
    else:
        st.error("Colonne 'l_codinsee' manquante.")
else:
    st.info("Veuillez importer un fichier DVF (.csv) pour commencer.")
