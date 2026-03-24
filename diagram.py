import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Social Media", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 1. RIMOZIONE ELEMENTI NATIVI */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .stApp { margin-left: 0px !important; }
    header, footer, #MainMenu { visibility: hidden !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    header { height: 0px !important; display: none !important; }

    /* 2. NAVIGAZIONE TESTUALE */
    .nav-wrapper {
        display: flex;
        gap: 40px;
        padding: 10px 0;
        margin-bottom: 5px;
        flex-wrap: wrap;
    }
    .nav-link {
        font-size: 30px;
        font-weight: 500;
        color: #000000 !important;
        text-decoration: none !important;
        transition: 0.3s;
        cursor: pointer;
        border-bottom: 3px solid transparent;
    }
    .nav-link:hover { color: #FF4B4B !important; border-bottom: 3px solid #FF4B4B; }

    /* 3. LINEA ROSSA SEPARATRICE */
    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }

    /* 4. MOBILE */
    @media (max-width: 768px) {
        .nav-link { font-size: 18px !important; }
        .nav-wrapper { gap: 15px !important; justify-content: center; }
        h1 { font-size: 24px !important; }
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 0rem !important; }
        .stMultiSelect { font-size: 14px !important; }
    }
    </style>

    <div class="nav-wrapper">
        <a href="./" target="_self" class="nav-link">Social Media</a>
        <a href="./app" target="_self" class="nav-link">Rassegna Stampa</a>
        <a href="./inser" target="_self" class="nav-link">Amministrazione</a>
    </div>
    <div class="header-line"></div>
    """, unsafe_allow_html=True)


# --- FUNZIONI ---

# FIX 1: Lettura CSV separata e cachata per evitare di rileggere
# il file dal disco ad ogni interazione dell'utente (es. cambio multiselect).
@st.cache_data
def carica_dati(file_csv: str) -> pd.DataFrame:
    """Legge il CSV e restituisce un DataFrame. Risultato cachato da Streamlit."""
    if not os.path.exists(file_csv):
        return pd.DataFrame()
    try:
        return pd.read_csv(file_csv, parse_dates=["Data"])
    except Exception as e:
        st.warning(f"Impossibile leggere '{file_csv}': {e}")
        return pd.DataFrame()


def crea_sezione_social(nome_social: str, file_csv: str, metriche: list) -> None:
    """
    Mostra il grafico interattivo per un social network.
    FIX 2: le metriche selezionabili vengono filtrate in base alle colonne
    effettivamente presenti nel CSV, evitando crash di Plotly se le colonne
    non corrispondono (es. dopo una modifica alle metriche in inser.py).
    """
    st.subheader(nome_social)
    df = carica_dati(file_csv)

    with st.container(border=True):
        if not df.empty:
            # FIX 2: filtra le metriche alle sole colonne presenti nel DataFrame.
            metriche_disponibili = [m for m in metriche if m in df.columns]

            if not metriche_disponibili:
                st.warning(f"Il file '{file_csv}' non contiene le colonne attese.")
                return

            scelte = st.multiselect(
                f"Filtra {nome_social}:",
                metriche_disponibili,
                default=metriche_disponibili,
                key=f"ms_{nome_social}",
            )

            if scelte:
                fig = px.line(
                    df, x="Data", y=scelte,
                    markers=True, template="plotly_white", height=350,
                )
                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend_orientation="h",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Seleziona almeno una metrica da visualizzare.")
        else:
            st.info(f"Nessun dato per {nome_social}. Inseriscili dalla pagina Amministrazione.")


# --- MAIN ---

st.markdown("<h1 style='text-align: center;'>Social Media</h1>", unsafe_allow_html=True)

# FIX 3: rimossa la riga st.markdown('<div class="red-line"></div>')
# che faceva riferimento a una classe CSS inesistente (residuo di versione precedente).

crea_sezione_social(
    "Instagram",
    "data_instagram.csv",
    ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
)

crea_sezione_social(
    "Facebook",
    "data_facebook.csv",
    ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
)

crea_sezione_social(
    "LinkedIn",
    "data_linkedin.csv",
    ["Comparse_Ricerche", "Nuovi_Followers", "Impressioni_Post", "Visitatori_Pagina"],
)