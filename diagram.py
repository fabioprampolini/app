import streamlit as st
import pandas as pd
import plotly.express as px
<<<<<<< HEAD
from utils.db import get_connection
=======
import os
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a

st.set_page_config(page_title="Social Media", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
<<<<<<< HEAD
=======
    /* 1. RIMOZIONE ELEMENTI NATIVI */
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
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
<<<<<<< HEAD
    header { height: 0px !important; display: none !important; }

=======

    header { height: 0px !important; display: none !important; }

    /* 2. NAVIGAZIONE TESTUALE */
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
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

<<<<<<< HEAD
=======
    /* 3. LINEA ROSSA SEPARATRICE */
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }

<<<<<<< HEAD
=======
    /* 4. MOBILE */
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
    @media (max-width: 768px) {
        .nav-link { font-size: 18px !important; }
        .nav-wrapper { gap: 15px !important; justify-content: center; }
        h1 { font-size: 24px !important; }
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 0rem !important; }
<<<<<<< HEAD
=======
        .stMultiSelect { font-size: 14px !important; }
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
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

<<<<<<< HEAD
@st.cache_data(ttl=60)
def carica_dati_social(tabella: str) -> pd.DataFrame:
    """
    Legge i dati di un social dal database PostgreSQL.
    La cache si invalida ogni 60 secondi così i nuovi dati
    inseriti da Amministrazione appaiono senza riavviare l'app.
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {tabella} ORDER BY data ASC", conn)
        return df
    except Exception as e:
        st.warning(f"Errore nel caricamento dati '{tabella}': {e}")
        return pd.DataFrame()


def crea_sezione_social(nome_social: str, tabella: str, metriche: list) -> None:
    """Mostra il grafico interattivo per un social network."""
    st.subheader(nome_social)
    df = carica_dati_social(tabella)

    with st.container(border=True):
        if not df.empty:
            metriche_disponibili = [m for m in metriche if m in df.columns]

            if not metriche_disponibili:
                st.warning(f"Nessuna colonna attesa trovata nella tabella '{tabella}'.")
=======
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
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
                return

            scelte = st.multiselect(
                f"Filtra {nome_social}:",
                metriche_disponibili,
                default=metriche_disponibili,
                key=f"ms_{nome_social}",
            )

            if scelte:
                fig = px.line(
<<<<<<< HEAD
                    df, x="data", y=scelte,
=======
                    df, x="Data", y=scelte,
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
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
<<<<<<< HEAD

crea_sezione_social(
    "Instagram", "instagram",
    ["visualizzazioni", "interazioni", "nuovi_followers"],
)

crea_sezione_social(
    "Facebook", "facebook",
    ["visualizzazioni", "interazioni", "nuovi_followers"],
)

crea_sezione_social(
    "LinkedIn", "linkedin",
    ["comparse_ricerche", "nuovi_followers", "impressioni_post", "visitatori_pagina"],
=======

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
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
)