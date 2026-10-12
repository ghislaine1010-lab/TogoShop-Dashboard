from pathlib import Path
from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="TogoShop | Tableau de bord",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# IDENTITE VISUELLE
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --navy: #11233F;
        --navy-2: #183858;
        --teal: #08A88A;
        --teal-light: #DDF8F0;
        --sky: #4A8FE7;
        --ink: #1D2C42;
        --muted: #718096;
        --line: #E5EBF3;
        --canvas: #F4F7FB;
        --card: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', Arial, sans-serif;
    }
    .stApp,
    [data-testid="stAppViewContainer"] > .main {
        background: var(--canvas);
        color: var(--ink);
    }
    .block-container {
        max-width: 1580px;
        padding-top: 1.25rem;
        padding-bottom: 3rem;
    }
    [data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.92);
    }

    /* Barre laterale */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10213B 0%, #173C56 100%);
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    [data-testid="stSidebar"] * {
        color: #ECF4FB;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #D5E3EF !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #DDF8F0;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] * {
        color: #12364A !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div {
        border-radius: 10px;
    }
    .sidebar-brand {
        padding: 0.7rem 0 1.1rem 0;
        margin-bottom: 1.1rem;
        border-bottom: 1px solid rgba(255,255,255,0.15);
    }
    .sidebar-brand-mark {
        display: inline-flex;
        width: 42px;
        height: 42px;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: #0BA889;
        font-size: 1.35rem;
        margin-bottom: 0.55rem;
    }
    .sidebar-brand h3 {
        color: #FFFFFF !important;
        font: 800 1.22rem 'Manrope', Arial, sans-serif;
        margin: 0;
    }
    .sidebar-brand p {
        color: #BAD0E1 !important;
        margin: 0.25rem 0 0 0;
        font-size: 0.8rem;
    }

    /* En-tete principal */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(115deg, #10213B 0%, #173B59 58%, #087F73 100%);
        border-radius: 22px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 14px 32px rgba(17, 35, 63, 0.13);
    }
    .hero:after {
        content: '';
        position: absolute;
        right: -48px;
        top: -100px;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 0 0 32px rgba(255,255,255,0.035), 0 0 0 68px rgba(255,255,255,0.025);
    }
    .hero-kicker {
        display: inline-block;
        color: #9CF4D7;
        font-size: 0.72rem;
        letter-spacing: 2px;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }
    .hero h1 {
        color: white !important;
        font: 800 clamp(1.65rem, 3vw, 2.35rem) 'Manrope', Arial, sans-serif;
        line-height: 1.18;
        margin: 0;
        padding: 0;
        position: relative;
        z-index: 1;
    }
    .hero p {
        color: #D9E8F4 !important;
        font-size: 0.98rem;
        margin: 0.62rem 0 0 0;
        max-width: 760px;
        position: relative;
        z-index: 1;
    }
    .hero-chip {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.35rem 0.7rem;
        border: 1px solid rgba(220,255,245,0.28);
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
        color: #E8FFF7;
        font-size: 0.76rem;
        position: relative;
        z-index: 1;
    }

    /* Titres et separations */
    h1, h2, h3, h4 {
        font-family: 'Manrope', Arial, sans-serif;
        color: var(--navy);
    }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.02rem !important; }
    .section-heading {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        color: var(--navy);
        font: 800 1.15rem 'Manrope', Arial, sans-serif;
        margin: 1.35rem 0 0.85rem 0;
    }
    .section-marker {
        width: 5px;
        height: 25px;
        background: var(--teal);
        border-radius: 9px;
        display: inline-block;
    }
    .section-caption {
        color: var(--muted);
        font-size: 0.86rem;
        margin: -0.55rem 0 1rem 0;
    }

    /* Cartes KPI sur mesure */
    .kpi-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 17px;
        padding: 1.05rem 1.1rem 0.95rem 1.1rem;
        min-height: 132px;
        box-shadow: 0 5px 18px rgba(18, 43, 73, 0.045);
        position: relative;
        overflow: hidden;
    }
    .kpi-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 4px;
        width: 100%;
        background: var(--accent, #08A88A);
    }
    .kpi-label-row {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        min-height: 29px;
    }
    .kpi-icon {
        background: var(--icon-bg, #DDF8F0);
        border-radius: 10px;
        width: 31px;
        height: 31px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .kpi-label {
        color: #6D7D91;
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-value {
        color: var(--navy);
        font: 800 clamp(1.2rem, 1.8vw, 1.62rem) 'Manrope', Arial, sans-serif;
        line-height: 1.2;
        margin-top: 0.95rem;
        overflow-wrap: anywhere;
    }
    .kpi-foot {
        color: #91A0B1;
        font-size: 0.72rem;
        margin-top: 0.3rem;
    }

    /* Panneaux, onglets, tableaux */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.45rem;
        background: #E9EEF5;
        padding: 0.35rem;
        border-radius: 14px;
        border-bottom: 0;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 0.58rem 0.95rem;
        font-weight: 700;
        color: #60738A;
        border: 0;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: #FFFFFF;
        color: #11233F;
        box-shadow: 0 2px 8px rgba(17,35,63,0.08);
    }
    div[data-testid="stDataFrame"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 13px;
        overflow: hidden;
    }
    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 0.35rem 0.3rem 0 0.3rem;
        box-shadow: 0 4px 14px rgba(18,43,73,0.025);
    }
    div[data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: #E2E9F1; }
    .footer-note {
        color: #7E8DA0;
        font-size: 0.78rem;
        text-align: center;
        padding-top: 0.6rem;
    }

    @media (max-width: 800px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .hero { padding: 1.35rem; }
        .kpi-card { min-height: 120px; padding: 0.9rem; }
    }

    /* =========================================
   THEME COMMERCIAL ROUGE ET BLANC
   ========================================= */

:root {
    --navy: #7F1D1D;
    --navy-2: #991B1B;
    --teal: #B91C1C;
    --teal-light: #FEE2E2;
    --sky: #D94848;
    --ink: #292524;
    --muted: #78716C;
    --line: #E7DCDC;
    --canvas: #F5F5F5;
    --card: #FFFFFF;
}

/* Fond principal */

.stApp,
[data-testid="stAppViewContainer"] > .main {
    background: #F5F5F5;
    color: #292524;
}

/* Bandeau principal */

.hero {
    background: linear-gradient(
        110deg,
        #761515 0%,
        #B91C1C 100%
    );
    border-radius: 8px;
    padding: 1.5rem 1.7rem;
    box-shadow: none;
}

.hero:after {
    display: none;
}

.hero-kicker {
    color: #FEE2E2;
}

.hero-chip {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.3);
    color: #FFFFFF;
}

/* Bandeaux rouges des sections */

.section-heading {
    display: block;
    background: #8F1717;
    color: #FFFFFF;
    padding: 0.65rem 0.9rem;
    border-radius: 5px;
    font-size: 1.05rem;
    font-weight: 800;
    margin: 1.3rem 0 0.8rem 0;
}

.section-marker {
    display: none;
}

.section-caption {
    color: #737373;
    margin-top: -0.25rem;
    margin-bottom: 1rem;
}

/* Cartes des indicateurs */

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E7DCDC;
    border-radius: 10px;
    box-shadow: 0 3px 12px rgba(60, 20, 20, 0.06);
    min-height: 122px;
}

/* Graphiques */

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E7DCDC;
    border-radius: 9px;
    box-shadow: 0 3px 12px rgba(60, 20, 20, 0.04);
}

/* Barre latérale assortie */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #651616 0%,
        #8F1717 100%
    );
}

.sidebar-brand-mark {
    background: #FEE2E2;
    color: #8F1717;
}

/* Tableaux */

div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #E7DCDC;
    border-radius: 9px;
}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CHARGEMENT ET VALIDATION DES DONNEES
# ============================================================
DATA_PATH = Path(__file__).resolve().parent / "ecommerce_togo.csv"

if not DATA_PATH.exists():
    st.error(
        "Le fichier **ecommerce_togo.csv** est introuvable. "
        "Placez-le dans le même dossier que `dashboard.py`."
    )
    st.stop()

try:
    data = pd.read_csv(DATA_PATH)
except Exception as exc:
    st.error(f"Impossible de lire le fichier CSV : {exc}")
    st.stop()

required_columns = [
    "id_commande", "id_client", "ville", "categorie",
    "canal_achat", "mode_paiement", "montant_total_fcfa",
]
missing_required = [column for column in required_columns if column not in data.columns]
if missing_required:
    st.error("Colonnes indispensables absentes : " + ", ".join(missing_required))
    st.info("Vérifiez les noms des colonnes dans ecommerce_togo.csv.")
    st.stop()

for column in ["montant_total_fcfa", "delai_livraison_jours", "satisfaction_1_5", "mois"]:
    if column in data.columns:
        data[column] = pd.to_numeric(data[column], errors="coerce") if column != "mois" else data[column]


def clean_label(value):
    if pd.isna(value):
        return "Non renseigné"
    return str(value).strip()


def premium_label(value):
    if pd.isna(value):
        return "Non renseigné"
    text_value = str(value).strip().lower()
    if text_value in {"1", "1.0", "true", "oui", "yes", "premium"}:
        return "Premium"
    if text_value in {"0", "0.0", "false", "non", "no", "non premium"}:
        return "Non premium"
    return str(value).strip()


def binary_rate(series):
    if series is None or series.empty:
        return None
    numeric = pd.to_numeric(series, errors="coerce")
    valid = numeric.dropna()
    if not valid.empty and set(valid.unique()).issubset({0, 1}):
        return float(valid.mean() * 100)
    mapping = {
        "1": 1, "1.0": 1, "true": 1, "oui": 1, "yes": 1,
        "0": 0, "0.0": 0, "false": 0, "non": 0, "no": 0,
    }
    mapped = series.astype("string").str.strip().str.lower().map(mapping).dropna()
    return float(mapped.mean() * 100) if not mapped.empty else None


def fmt_fcfa(value):
    try:
        return f"{float(value):,.0f}".replace(",", " ") + " FCFA"
    except (TypeError, ValueError):
        return "N/D"


def fmt_number(value):
    return f"{int(value):,}".replace(",", " ")


def fmt_percent(value):
    return f"{value:.1f} %" if value is not None and pd.notna(value) else "N/D"


def kpi_card(label, value, icon, accent="#08A88A", icon_bg="#DDF8F0", foot=""):
    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_icon = escape(str(icon))
    safe_foot = escape(str(foot))
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent};--icon-bg:{icon_bg};">
            <div class="kpi-label-row">
                <span class="kpi-icon">{safe_icon}</span>
                <span class="kpi-label">{safe_label}</span>
            </div>
            <div class="kpi-value">{safe_value}</div>
            <div class="kpi-foot">{safe_foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title, caption=None):
    st.markdown(
        f'<div class="section-heading"><span class="section-marker"></span>{escape(title)}</div>',
        unsafe_allow_html=True,
    )
    if caption:
        st.markdown(f'<div class="section-caption">{escape(caption)}</div>', unsafe_allow_html=True)


def style_figure(fig, height=365):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=14, r=14, t=35, b=15),
        font=dict(family="DM Sans, Arial, sans-serif", color="#43546B", size=12),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#11233F", font_color="#FFFFFF", font_family="DM Sans, Arial, sans-serif"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E9EEF4", zeroline=False, linecolor="#DDE5EE")
    fig.update_yaxes(showgrid=False, zeroline=False, linecolor="#DDE5EE")
    return fig


if "client_premium" in data.columns:
    data["statut_client"] = data["client_premium"].apply(premium_label)
else:
    data["statut_client"] = "Non renseigné"

# ============================================================
# BARRE LATERALE ET FILTRES
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark">🛍️</div>
            <h3>TogoShop</h3>
            <p>Centre de pilotage commercial</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Affiner l'analyse")
    st.caption("Laissez un filtre vide pour conserver toutes les valeurs.")

    city_options = sorted(data["ville"].dropna().astype(str).unique().tolist())
    category_options = sorted(data["categorie"].dropna().astype(str).unique().tolist())
    channel_options = sorted(data["canal_achat"].dropna().astype(str).unique().tolist())
    payment_options = sorted(data["mode_paiement"].dropna().astype(str).unique().tolist())
    month_options = sorted(data["mois"].dropna().astype(str).unique().tolist(), key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x)) if "mois" in data.columns else []
    segment_options = sorted(data["statut_client"].dropna().astype(str).unique().tolist())

    selected_cities = st.multiselect("📍 Ville", city_options)
    selected_categories = st.multiselect("🛍️ Catégorie", category_options)
    selected_channels = st.multiselect("🛒 Canal d'achat", channel_options)
    selected_payments = st.multiselect("💳 Mode de paiement", payment_options)
    selected_months = st.multiselect("📅 Mois", month_options) if month_options else []
    selected_segments = st.multiselect("👥 Statut client", segment_options)

    st.markdown("---")
    st.caption(f"Base chargée : {fmt_number(len(data))} lignes · {data.shape[1]} colonnes")

filtered = data.copy()
if selected_cities:
    filtered = filtered[filtered["ville"].astype(str).isin(selected_cities)]
if selected_categories:
    filtered = filtered[filtered["categorie"].astype(str).isin(selected_categories)]
if selected_channels:
    filtered = filtered[filtered["canal_achat"].astype(str).isin(selected_channels)]
if selected_payments:
    filtered = filtered[filtered["mode_paiement"].astype(str).isin(selected_payments)]
if selected_months and "mois" in filtered.columns:
    filtered = filtered[filtered["mois"].astype(str).isin(selected_months)]
if selected_segments:
    filtered = filtered[filtered["statut_client"].astype(str).isin(selected_segments)]

# ============================================================
# EN-TETE
# ============================================================
filter_description = "Toutes les données" if len(filtered) == len(data) else f"{fmt_number(len(filtered))} lignes après filtrage"
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">BUSINESS INTELLIGENCE · TOGO</div>
        <h1>Tableau de bord commercial</h1>
        <p>Une lecture visuelle des ventes, des villes, des clients et des habitudes d'achat pour mieux orienter les décisions de TogoShop.</p>
        <span class="hero-chip">● {escape(filter_description)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("Aucune donnée ne correspond aux filtres choisis. Retirez au moins un filtre dans la barre latérale.")
    st.stop()

# ============================================================
# INDICATEURS PRINCIPAUX
# ============================================================
section_heading("Indicateurs clés", "Les chiffres se mettent à jour selon les filtres sélectionnés.")
revenue = float(filtered["montant_total_fcfa"].sum(skipna=True))
orders_count = int(filtered["id_commande"].nunique())
clients_count = int(filtered["id_client"].nunique())
average_basket = revenue / orders_count if orders_count else 0

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    kpi_card("Chiffre d'affaires", fmt_fcfa(revenue), "💰", "#08A88A", "#DDF8F0", "Revenus sur la sélection")
with k2:
    kpi_card("Commandes", fmt_number(orders_count), "🧾", "#4A8FE7", "#E4EFFF", "Commandes distinctes")
with k3:
    kpi_card("Clients uniques", fmt_number(clients_count), "👥", "#8B5CF6", "#F0E8FF", "Clients distincts")
with k4:
    kpi_card("Panier moyen", fmt_fcfa(average_basket), "🛍️", "#F59E0B", "#FFF1D6", "CA total ÷ commandes")

# KPIs de qualite / operationnels si les colonnes sont disponibles
operational = []
if "delai_livraison_jours" in filtered.columns:
    value = filtered["delai_livraison_jours"].mean()
    operational.append(("Délai moyen", f"{value:.1f} jours" if pd.notna(value) else "N/D", "🚚", "#4A8FE7", "#E4EFFF", "Livraison"))
if "retard_livraison" in filtered.columns:
    operational.append(("Commandes en retard", fmt_percent(binary_rate(filtered["retard_livraison"])), "⏱️", "#EF6A5B", "#FFE9E6", "Part des commandes"))
if "satisfaction_1_5" in filtered.columns:
    value = filtered["satisfaction_1_5"].mean()
    operational.append(("Satisfaction moyenne", f"{value:.1f}/5" if pd.notna(value) else "N/D", "⭐", "#F59E0B", "#FFF1D6", "Note moyenne"))
if "retour_produit" in filtered.columns:
    operational.append(("Taux de retour", fmt_percent(binary_rate(filtered["retour_produit"])), "↩️", "#8B5CF6", "#F0E8FF", "Part des retours"))

if operational:
    st.markdown("<div style='height:0.45rem'></div>", unsafe_allow_html=True)
    section_heading("Qualité opérationnelle", "Suivi de la livraison et de l'expérience client.")
    columns = st.columns(min(4, len(operational)), gap="medium")
    for index, item in enumerate(operational):
        label, value, icon, accent, icon_bg, foot = item
        with columns[index % len(columns)]:
            kpi_card(label, value, icon, accent, icon_bg, foot)

st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
st.caption(f"Affichage calculé sur {fmt_number(len(filtered))} lignes filtrées, sur {fmt_number(len(data))} lignes au total.")

# ============================================================
# ONGLETS D'ANALYSE
# ============================================================
tab_overview, tab_cities, tab_clients, tab_channels, tab_data = st.tabs(
    ["📊 Vue générale", "📍 Villes & catégories", "👥 Clients", "🛒 Canaux & paiements", "🗃️ Dataset"]
)

PALETTE = ["#08A88A", "#4A8FE7", "#F59E0B", "#8B5CF6", "#EF6A5B", "#38BDF8", "#64748B"]

with tab_overview:
    section_heading("Vue d'ensemble des ventes", "Comparez les revenus, les catégories et les canaux d'achat.")
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("#### Chiffre d'affaires par ville")
        revenue_city = (
            filtered.groupby("ville", as_index=False)["montant_total_fcfa"]
            .sum()
            .rename(columns={"montant_total_fcfa": "Chiffre d'affaires"})
            .sort_values("Chiffre d'affaires", ascending=True)
        )
        height = max(330, min(560, len(revenue_city) * 31 + 80))
        fig = px.bar(
            revenue_city, x="Chiffre d'affaires", y="ville", orientation="h",
            text="Chiffre d'affaires", color_discrete_sequence=["#08A88A"],
            labels={"ville": "Ville"},
        )
        fig.update_traces(texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False, marker_line_width=0)
        fig.update_xaxes(tickformat=",.0f", title="CA (FCFA)")
        fig.update_layout(yaxis_title="", showlegend=False)
        st.plotly_chart(style_figure(fig, height=height), width="stretch", config={"displayModeBar": False})

    with right:
        st.markdown("#### Chiffre d'affaires par catégorie")
        revenue_category = (
            filtered.groupby("categorie", as_index=False)["montant_total_fcfa"]
            .sum()
            .rename(columns={"montant_total_fcfa": "Chiffre d'affaires"})
            .sort_values("Chiffre d'affaires", ascending=True)
        )
        fig = px.bar(
            revenue_category, x="Chiffre d'affaires", y="categorie", orientation="h",
            text="Chiffre d'affaires", color_discrete_sequence=["#4A8FE7"],
            labels={"categorie": "Catégorie"},
        )
        fig.update_traces(texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False, marker_line_width=0)
        fig.update_xaxes(tickformat=",.0f", title="CA (FCFA)")
        fig.update_layout(yaxis_title="", showlegend=False)
        st.plotly_chart(style_figure(fig, height=max(330, min(560, len(revenue_category) * 36 + 80))), width="stretch", config={"displayModeBar": False})

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("#### Répartition des commandes par canal")
        channel_orders = (
            filtered.groupby("canal_achat", as_index=False)["id_commande"]
            .nunique()
            .rename(columns={"id_commande": "Commandes"})
            .sort_values("Commandes", ascending=False)
        )
        fig = px.pie(
            channel_orders, names="canal_achat", values="Commandes", hole=0.67,
            color_discrete_sequence=PALETTE,
        )
        fig.update_traces(textposition="inside", textinfo="percent", hole=0.67,
                          hovertemplate="%{label}<br>Commandes : %{value:,}<br>Part : %{percent}<extra></extra>")
        fig.update_layout(annotations=[dict(text=f"{orders_count:,}<br><span style='font-size:11px'>commandes</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=19, color="#11233F"))])
        st.plotly_chart(style_figure(fig, height=360), width="stretch", config={"displayModeBar": False})

    with right:
        st.markdown("#### Évolution mensuelle du chiffre d'affaires")
        if "mois" in filtered.columns:
            monthly = filtered.groupby("mois", as_index=False)["montant_total_fcfa"].sum()
            monthly["_tri"] = pd.to_numeric(monthly["mois"], errors="coerce")
            if monthly["_tri"].notna().all():
                monthly = monthly.sort_values("_tri")
            else:
                monthly = monthly.sort_values("mois", key=lambda s: s.astype(str))
            fig = px.line(
                monthly, x="mois", y="montant_total_fcfa", markers=True,
                color_discrete_sequence=["#08A88A"],
                labels={"mois": "Mois", "montant_total_fcfa": "Chiffre d'affaires"},
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=8), fill="tozeroy", fillcolor="rgba(8,168,138,0.10)")
            fig.update_yaxes(tickformat=",.0f", title="CA (FCFA)")
            fig.update_xaxes(title="Mois")
            st.plotly_chart(style_figure(fig, height=360), width="stretch", config={"displayModeBar": False})
        else:
            st.info("La colonne `mois` n'existe pas dans cette base. Le graphique mensuel ne peut pas être affiché.")


    # ============================================================
    # ANALYSE DU VOLUME VENDU ET DU PRIX UNITAIRE
    # ============================================================
    section_heading(
        "Volume vendu et prix unitaire",
        "Comparez les quantités vendues, les prix unitaires moyens et le chiffre d'affaires par catégorie."
    )

    analyse_source = filtered.copy()
    analyse_source["quantite"] = pd.to_numeric(analyse_source["quantite"], errors="coerce").fillna(0)
    analyse_source["prix_unitaire_fcfa"] = pd.to_numeric(analyse_source["prix_unitaire_fcfa"], errors="coerce")
    analyse_source["montant_total_fcfa"] = pd.to_numeric(analyse_source["montant_total_fcfa"], errors="coerce").fillna(0)

    performance_categorie = analyse_source.groupby("categorie", as_index=False).agg(
        quantite_vendue=("quantite", "sum"),
        chiffre_affaires=("montant_total_fcfa", "sum"),
        prix_unitaire_moyen=("prix_unitaire_fcfa", "mean"),
        commandes=("id_commande", "nunique"),
    )
    ca_total_categories = performance_categorie["chiffre_affaires"].sum()
    if ca_total_categories != 0:
        performance_categorie["part_ca_pct"] = (
            performance_categorie["chiffre_affaires"] / ca_total_categories * 100
        )
    else:
        performance_categorie["part_ca_pct"] = 0.0

    gauche, droite = st.columns(2, gap="large")
    with gauche:
        st.markdown("#### Quantité vendue par catégorie")
        quantites = performance_categorie.sort_values("quantite_vendue", ascending=True)
        fig = px.bar(
            quantites, x="quantite_vendue", y="categorie", orientation="h",
            text="quantite_vendue", color_discrete_sequence=["#B91C1C"],
            labels={"quantite_vendue": "Quantité vendue", "categorie": "Catégorie"},
        )
        fig.update_traces(texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(yaxis_title="", showlegend=False)
        st.plotly_chart(style_figure(fig, height=350), width="stretch", config={"displayModeBar": False})

    with droite:
        st.markdown("#### Prix unitaire moyen par catégorie")
        prix = performance_categorie.sort_values("prix_unitaire_moyen", ascending=True)
        fig = px.bar(
            prix, x="prix_unitaire_moyen", y="categorie", orientation="h",
            text="prix_unitaire_moyen", color_discrete_sequence=["#D97706"],
            labels={"prix_unitaire_moyen": "Prix unitaire moyen (FCFA)", "categorie": "Catégorie"},
        )
        fig.update_traces(texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_xaxes(tickformat=",.0f")
        fig.update_layout(yaxis_title="", showlegend=False)
        st.plotly_chart(style_figure(fig, height=350), width="stretch", config={"displayModeBar": False})

    st.markdown("#### Tableau comparatif des catégories")
    tableau_performance = performance_categorie.sort_values(
        "chiffre_affaires", ascending=False
    ).rename(columns={
        "categorie": "Catégorie",
        "quantite_vendue": "Quantité vendue",
        "chiffre_affaires": "Chiffre d'affaires (FCFA)",
        "prix_unitaire_moyen": "Prix unitaire moyen (FCFA)",
        "commandes": "Commandes distinctes",
        "part_ca_pct": "Part du CA (%)",
    })
    st.dataframe(
        tableau_performance.style.format({
            "Quantité vendue": "{:,.0f}",
            "Chiffre d'affaires (FCFA)": "{:,.0f}",
            "Prix unitaire moyen (FCFA)": "{:,.0f}",
            "Commandes distinctes": "{:,.0f}",
            "Part du CA (%)": "{:.1f} %",
        }),
        width="stretch",
        hide_index=True,
    )

    if not performance_categorie.empty:
        categorie_ca = performance_categorie.loc[performance_categorie["chiffre_affaires"].idxmax()]
        categorie_volume = performance_categorie.loc[performance_categorie["quantite_vendue"].idxmax()]
        if categorie_ca["categorie"] == categorie_volume["categorie"]:
            st.info(
                f"**À retenir :** {categorie_ca['categorie']} arrive en tête du chiffre d'affaires "
                f"et du volume vendu. Comparez aussi son prix unitaire moyen pour mieux comprendre sa performance."
            )
        else:
            st.info(
                f"**À retenir :** {categorie_ca['categorie']} génère le chiffre d'affaires le plus élevé "
                f"({fmt_fcfa(categorie_ca['chiffre_affaires'])}), tandis que {categorie_volume['categorie']} "
                f"enregistre la plus grande quantité vendue ({fmt_number(categorie_volume['quantite_vendue'])} articles). "
                "Le prix unitaire moyen aide à comparer ces performances, mais ces indicateurs seuls ne prouvent pas une causalité."
            )

with tab_cities:
    section_heading("Villes & catégories", "Identifiez les zones les plus performantes et les catégories qui y sont commandées.")
    city_summary = filtered.groupby("ville").agg(
        nombre_commandes=("id_commande", "nunique"),
        chiffre_affaires=("montant_total_fcfa", "sum"),
        clients_uniques=("id_client", "nunique"),
    )
    city_summary["panier_moyen"] = city_summary["chiffre_affaires"] / city_summary["nombre_commandes"].where(city_summary["nombre_commandes"] != 0)
    city_summary = city_summary.sort_values("chiffre_affaires", ascending=False).rename(
        columns={
            "nombre_commandes": "Commandes",
            "chiffre_affaires": "Chiffre d'affaires (FCFA)",
            "clients_uniques": "Clients uniques",
            "panier_moyen": "Panier moyen (FCFA)",
        }
    )
    st.dataframe(city_summary.round(2), width="stretch", hide_index=False)

    st.markdown("#### Catégories commandées par ville")
    city_order = filtered.groupby("ville")["montant_total_fcfa"].sum().nlargest(12).index.tolist()
    city_category = (
        filtered[filtered["ville"].isin(city_order)]
        .groupby(["ville", "categorie"])["id_commande"]
        .nunique()
        .reset_index(name="Commandes")
    )
    fig = px.bar(
        city_category, x="ville", y="Commandes", color="categorie", barmode="stack",
        color_discrete_sequence=PALETTE,
        labels={"ville": "Ville", "categorie": "Catégorie"},
    )
    fig.update_xaxes(title="Ville", tickangle=-25)
    fig.update_yaxes(title="Commandes")
    st.plotly_chart(style_figure(fig, height=440), width="stretch", config={"displayModeBar": False})
    st.caption("Le graphique compte les commandes distinctes par ville et catégorie. Les quantités réelles vendues sont analysées dans la section Volume vendu et prix unitaire de la vue générale.")

with tab_clients:
    section_heading("Profil des clients", "Répartition des clients uniques selon leur statut et les caractéristiques disponibles.")
    left, right = st.columns([1, 1.25], gap="large")
    with left:
        client_segments = filtered[["id_client", "statut_client"]].dropna(subset=["id_client"]).drop_duplicates("id_client")
        segment_counts = client_segments.groupby("statut_client")["id_client"].nunique().reset_index(name="Clients")
        segment_counts = segment_counts.sort_values("Clients", ascending=False)
        fig = px.pie(
            segment_counts, names="statut_client", values="Clients", hole=0.64,
            color_discrete_sequence=["#08A88A", "#4A8FE7", "#9AA8B8", "#F59E0B"],
        )
        fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>Clients : %{value:,}<br>Part : %{percent}<extra></extra>")
        fig.update_layout(annotations=[dict(text=f"{clients_count:,}<br><span style='font-size:11px'>clients</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#11233F"))])
        st.plotly_chart(style_figure(fig, height=355), width="stretch", config={"displayModeBar": False})
    with right:
        st.markdown("#### Détail des segments")
        st.dataframe(segment_counts, width="stretch", hide_index=True)
        st.markdown("#### Clients premium par ville")
        premium_by_city = (
            filtered[filtered["statut_client"] == "Premium"]
            .groupby("ville")["id_client"].nunique()
            .sort_values(ascending=False)
            .rename("Clients premium")
            .to_frame()
        )
        st.dataframe(premium_by_city, width="stretch")

    if "genre" in filtered.columns:
        st.markdown("#### Répartition des clients par genre")
        clients_gender = filtered[["id_client", "genre"]].dropna(subset=["id_client"]).drop_duplicates("id_client")
        gender_counts = clients_gender.groupby("genre")["id_client"].nunique().reset_index(name="Clients")
        fig = px.bar(gender_counts, x="genre", y="Clients", color="genre", color_discrete_sequence=PALETTE,
                     labels={"genre": "Genre"})
        fig.update_layout(showlegend=False, xaxis_title="Genre", yaxis_title="Clients")
        st.plotly_chart(style_figure(fig, height=315), width="stretch", config={"displayModeBar": False})

with tab_channels:
    section_heading("Canaux d'achat & paiements", "Comprenez où les clients achètent et comment ils paient.")
    st.markdown("#### Canaux d'achat par ville")
    city_channel = (
        filtered.groupby(["ville", "canal_achat"])["id_commande"]
        .nunique().reset_index(name="Commandes")
    )
    channel_city_order = filtered.groupby("ville")["id_commande"].nunique().nlargest(12).index.tolist()
    city_channel_top = city_channel[city_channel["ville"].isin(channel_city_order)]
    fig = px.bar(
        city_channel_top, x="ville", y="Commandes", color="canal_achat", barmode="stack",
        color_discrete_sequence=PALETTE,
        labels={"ville": "Ville", "canal_achat": "Canal d'achat"},
    )
    fig.update_xaxes(title="Ville", tickangle=-25)
    fig.update_yaxes(title="Commandes")
    st.plotly_chart(style_figure(fig, height=420), width="stretch", config={"displayModeBar": False})
    city_channel_table = city_channel.pivot(index="ville", columns="canal_achat", values="Commandes").fillna(0).astype(int)
    st.dataframe(city_channel_table, width="stretch")

    st.markdown("#### Canaux d'achat par mode de paiement")
    channel_payment = (
        filtered.groupby(["canal_achat", "mode_paiement"])["id_commande"]
        .nunique().reset_index(name="Commandes")
    )
    fig = px.bar(
        channel_payment, x="canal_achat", y="Commandes", color="mode_paiement", barmode="stack",
        color_discrete_sequence=PALETTE,
        labels={"canal_achat": "Canal d'achat", "mode_paiement": "Mode de paiement"},
    )
    fig.update_xaxes(title="Canal d'achat")
    fig.update_yaxes(title="Commandes")
    st.plotly_chart(style_figure(fig, height=410), width="stretch", config={"displayModeBar": False})
    channel_payment_table = channel_payment.pivot(index="canal_achat", columns="mode_paiement", values="Commandes").fillna(0).astype(int)
    st.dataframe(channel_payment_table, width="stretch")

with tab_data:
    section_heading("Exploration du dataset", "Vérifiez la structure de la base et les valeurs manquantes.")
    row1, row2, row3 = st.columns(3, gap="medium")
    with row1:
        kpi_card("Lignes", fmt_number(data.shape[0]), "📄", "#4A8FE7", "#E4EFFF", "Enregistrements")
    with row2:
        kpi_card("Colonnes", fmt_number(data.shape[1]), "📊", "#08A88A", "#DDF8F0", "Variables disponibles")
    with row3:
        kpi_card("Clients distincts", fmt_number(data["id_client"].nunique()), "👥", "#F59E0B", "#FFF1D6", "Base complète")

    st.markdown("#### Aperçu des données filtrées")
    st.dataframe(filtered.head(100), width="stretch", hide_index=True)
    st.caption("Aperçu limité aux 100 premières lignes.")
    csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Télécharger les données filtrées (CSV)",
        data=csv_bytes,
        file_name="togoshop_donnees_filtrees.csv",
        mime="text/csv",
    )

    st.markdown("#### Valeurs manquantes dans la base complète")
    missing_summary = data.isna().sum().to_frame("Valeurs manquantes")
    missing_summary = missing_summary[missing_summary["Valeurs manquantes"] > 0].sort_values("Valeurs manquantes", ascending=False)
    if missing_summary.empty:
        st.success("Aucune valeur manquante détectée dans la base.")
    else:
        missing_summary = missing_summary.reset_index(names="Colonne")
        fig = px.bar(
            missing_summary.sort_values("Valeurs manquantes", ascending=True),
            x="Valeurs manquantes", y="Colonne", orientation="h",
            color_discrete_sequence=["#F59E0B"],
        )
        fig.update_layout(showlegend=False, xaxis_title="Nombre de valeurs manquantes", yaxis_title="")
        st.plotly_chart(style_figure(fig, height=max(300, len(missing_summary) * 35 + 60)), width="stretch", config={"displayModeBar": False})
        st.dataframe(missing_summary, width="stretch", hide_index=True)

st.markdown("---")
st.markdown(
    '<div class="footer-note">TOGOSHOP · PILOTAGE COMMERCIAL · Les indicateurs et graphiques évoluent selon les filtres sélectionnés.</div>',
    unsafe_allow_html=True,
)
