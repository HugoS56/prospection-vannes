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

    # Afficher les colonnes pour debug
    st.write("### Colonnes disponibles dans le fichier :")
    st.write(list(df.columns))

    # Filtrage simple par code INSEE
    if "l_codinsee" in df.columns:
        codes_insee = df["l_codinsee"].dropna().unique()
        ville = st.selectbox("Sélectionnez un code INSEE", sorted(codes_insee))
        filtered_df = df[df["l_codinsee"] == ville]

        st.write(f"🔍 **Nombre de biens trouvés pour la commune {ville} :** {len(filtered_df)}")
        st.dataframe(filtered_df)

        # Statistiques simples
        if "valeurfonc" in df.columns:
            st.markdown("💰 **Statistiques sur les valeurs foncières**")
            st.write(filtered_df["valeurfonc"].describe())
        else:
            st.warning("La colonne 'valeurfonc' n'a pas été trouvée dans le fichier.")
    else:
        st.error("La colonne 'l_codinsee' est manquante dans le fichier.")
else:
    st.info("Veuillez importer un fichier DVF (.csv) pour commencer.")
