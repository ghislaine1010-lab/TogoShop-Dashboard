import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard TogoShop",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

data = pd.read_csv("ecommerce_togo.csv")

# --------------------------------------------------
# TITRE
# --------------------------------------------------

st.title("🛒 Tableau de bord commercial - TogoShop")

st.write("Analyse des performances commerciales de TogoShop")

# --------------------------------------------------
# CALCUL DES KPIs
# --------------------------------------------------

ca_total = data["montant_total_fcfa"].sum()

nombre_commandes = data["id_commande"].nunique()

nombre_clients = data["id_client"].nunique()

panier_moyen = data["montant_total_fcfa"].mean()

# --------------------------------------------------
# AFFICHAGE DES KPIs
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Chiffre d'affaires",
        f"{ca_total:,.0f} FCFA"
    )

with col2:
    st.metric(
        "🛒 Commandes",
        f"{nombre_commandes:,}"
    )

with col3:
    st.metric(
        "Clients",
        f"{nombre_clients:,}"
    )

with col4:
    st.metric(
        "Panier moyen",
        f"{panier_moyen:,.0f} FCFA"
    )

# --------------------------------------------------
# CHIFFRE D'AFFAIRES PAR CATÉGORIE
# --------------------------------------------------

st.subheader("Chiffre d'affaires par catégorie")

ca_categorie = (
    data.groupby("categorie")["montant_total_fcfa"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(ca_categorie)
# --------------------------------------------------
# AUTRES KPIs
# --------------------------------------------------

nombre_categories = data["categorie"].nunique()

categorie_top = data["categorie"].value_counts().idxmax()

ville_top = (
    data.groupby("ville")["montant_total_fcfa"]
    .sum()
    .idxmax()
)

delai_moyen = data["delai_livraison_jours"].mean()

taux_retard = data["retard_livraison"].mean() * 100

satisfaction_moyenne = data["satisfaction_1_5"].mean()

# --------------------------------------------------
# AFFICHAGE DES NOUVEAUX KPIs
# --------------------------------------------------

st.subheader("Indicateurs complémentaires")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Catégories",
        f"{nombre_categories}"
    )

with col6:
    st.metric(
        "Catégorie la plus vendue",
        categorie_top
    )

with col7:
    st.metric(
        "Ville avec le plus de CA",
        ville_top
    )

col8, col9, col10 = st.columns(3)

with col8:
    st.metric(
        "Délai moyen",
        f"{delai_moyen:.1f} jours"
    )

with col9:
    st.metric(
        "Taux de retard",
        f"{taux_retard:.1f}%"
    )

with col10:
    st.metric(
        "Satisfaction moyenne",
        f"{satisfaction_moyenne:.1f}/5"
    )


    # --------------------------------------------------
# AUTRES KPIs
# --------------------------------------------------

nombre_categories = data["categorie"].nunique()

categorie_top = data["categorie"].value_counts().idxmax()

ville_top = (
    data.groupby("ville")["montant_total_fcfa"]
    .sum()
    .idxmax()
)

delai_moyen = data["delai_livraison_jours"].mean()

taux_retard = data["retard_livraison"].mean() * 100

satisfaction_moyenne = data["satisfaction_1_5"].mean()

# --------------------------------------------------
# AFFICHAGE DES NOUVEAUX KPIs
# --------------------------------------------------

st.subheader("Indicateurs complémentaires")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Nombre de catégories",
        nombre_categories
    )

with col6:
    st.metric(
        "Catégorie la plus vendue",
        categorie_top
    )

with col7:
    st.metric(
        "Ville avec le plus de CA",
        ville_top
    )

col8, col9, col10 = st.columns(3)

with col8:
    st.metric(
        "Délai moyen",
        f"{delai_moyen:.1f} jours"
    )

with col9:
    st.metric(
        "Taux de retard",
        f"{taux_retard:.1f}%"
    )

with col10:
    st.metric(
        "Satisfaction moyenne",
        f"{satisfaction_moyenne:.1f}/5"
    )



    # ==================================================
# 1. TAILLE DE LA BASE DE DONNEES
# ==================================================

st.subheader("Taille de la base de données")

taille_memoire = data.memory_usage(deep=True).sum() / (1024 ** 2)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nombre de lignes", f"{data.shape[0]:,}")

with col2:
    st.metric("Nombre de colonnes", f"{data.shape[1]}")

with col3:
    st.metric("Mémoire occupée", f"{taille_memoire:.2f} Mo")


# ==================================================
# 2. CHIFFRE D'AFFAIRES PAR VILLE
# ==================================================

st.subheader("Répartition du chiffre d'affaires par ville")

ca_par_ville = (
    data.groupby("ville")["montant_total_fcfa"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(ca_par_ville)


# ==================================================
# 3. COMMANDES, CA, CLIENTS ET PANIER MOYEN PAR VILLE
# ==================================================

st.subheader("Performance commerciale par ville")

tableau_villes = data.groupby("ville").agg(
    nombre_commandes=("id_commande", "nunique"),
    chiffre_affaires=("montant_total_fcfa", "sum"),
    clients_uniques=("id_client", "nunique"),
    panier_moyen=("montant_total_fcfa", "mean")
).sort_values(
    by="chiffre_affaires",
    ascending=False
)

st.dataframe(
    tableau_villes.round(2),
    use_container_width=True
)


# ==================================================
# 4. CATEGORIES VENDUES DANS CHAQUE VILLE
# ==================================================

st.subheader("Répartition des ventes par ville et catégorie")

ventes_ville_categorie = (
    data.groupby(["ville", "categorie"])["id_commande"]
    .nunique()
    .unstack(fill_value=0)
)

st.bar_chart(ventes_ville_categorie)

st.write("Détail des commandes par ville et catégorie :")

st.dataframe(
    ventes_ville_categorie,
    use_container_width=True
)


# ==================================================
# 5. REPARTITION DES CLIENTS PAR STATUT PREMIUM
# ==================================================

st.subheader("👥 Répartition des clients par statut")

valeurs_premium = (
    data["client_premium"]
    .astype("string")
    .str.strip()
    .str.lower()
)

correspondance_premium = {
    "1": "Premium",
    "1.0": "Premium",
    "true": "Premium",
    "oui": "Premium",
    "premium": "Premium",
    "0": "Non premium",
    "0.0": "Non premium",
    "false": "Non premium",
    "non": "Non premium",
    "non premium": "Non premium"
}

segment_client = valeurs_premium.map(correspondance_premium)

segment_client = segment_client.fillna(
    valeurs_premium.fillna("Non renseigné")
)

clients_par_segment = (
    pd.DataFrame({
        "id_client": data["id_client"],
        "segment": segment_client
    })
    .groupby("segment")["id_client"]
    .nunique()
    .sort_values(ascending=False)
)

st.bar_chart(clients_par_segment)

st.dataframe(
    clients_par_segment.rename("Nombre de clients").to_frame(),
    use_container_width=True
)


# ==================================================
# 6. CANAUX D'ACHAT PAR VILLE
# ==================================================

st.subheader("🛒 Répartition des canaux d'achat par ville")

commandes_ville_canal = (
    data.groupby(["ville", "canal_achat"])["id_commande"]
    .nunique()
    .unstack(fill_value=0)
)

st.bar_chart(commandes_ville_canal)

st.dataframe(
    commandes_ville_canal,
    use_container_width=True
)


# ==================================================
# 7. CANAUX D'ACHAT PAR MODE DE PAIEMENT
# ==================================================

st.subheader("💳 Canaux d'achat par mode de paiement")

commandes_canal_paiement = (
    data.groupby(["canal_achat", "mode_paiement"])["id_commande"]
    .nunique()
    .unstack(fill_value=0)
)

st.bar_chart(commandes_canal_paiement)

st.dataframe(
    commandes_canal_paiement,
    use_container_width=True
)