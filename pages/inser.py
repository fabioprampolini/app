import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Amministrazione", layout="wide", initial_sidebar_state="collapsed")

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

    /* 3. SELECT BOX */
    div[data-baseweb="select"] > div {
        font-size: 20px !important;
        min-height: 50px !important;
    }
    ul[data-baseweb="menu"] li { font-size: 20px !important; }

    /* 4. LINEA ROSSA SEPARATRICE */
    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }

    /* 5. MOBILE */
    @media (max-width: 768px) {
        .nav-link { font-size: 18px !important; }
        .nav-wrapper { gap: 15px !important; justify-content: center; }
        h1 { font-size: 24px !important; }
        div[data-testid="stHorizontalBlock"] { flex-direction: column !important; }
        div[data-testid="stColumn"] { width: 100% !important; }
        .block-container { padding: 1rem !important; }
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

def salva_dati(file_csv: str, data, dict_valori: dict) -> None:
    """
    Aggiunge una riga al CSV con la data e i valori forniti.
    FIX 1: dict_valori ora contiene scalari (non liste), quindi
    il DataFrame viene costruito correttamente con pd.DataFrame([{...}]).
    FIX 2: la lettura del CSV esistente è protetta da try/except per
    gestire file corrotti o con colonne incompatibili senza mandare
    in crash l'app.
    """
    nuovo = pd.DataFrame([{"Data": pd.to_datetime(data), **dict_valori}])

    if os.path.exists(file_csv):
        try:
            df = pd.read_csv(file_csv, parse_dates=["Data"])
            df = pd.concat([df, nuovo], ignore_index=True).sort_values("Data")
        except Exception as e:
            # FIX 2: CSV danneggiato → si ricrea da zero avvisando l'utente.
            st.warning(f"Il file '{file_csv}' era danneggiato e verrà ricreato. ({e})")
            df = nuovo
    else:
        df = nuovo

    df.to_csv(file_csv, index=False)


def crea_sezione_social(nome_social: str, file_csv: str, metriche: list) -> None:
    """
    Genera un form di inserimento dati per un social network.
    FIX 3: i valori di input_valori sono scalari, non liste con un elemento.
    FIX 4: mostra st.success() prima del rerun tramite session_state,
    così l'utente vede il feedback anche dopo il refresh della pagina.
    """
    # Chiave per mostrare il messaggio di successo dopo il rerun
    success_key = f"success_{nome_social}"

    if st.session_state.get(success_key):
        st.success("Dati salvati con successo!")
        st.session_state[success_key] = False

    with st.form(f"form_{nome_social}", clear_on_submit=True):
        st.markdown("<h3 style='text-align: center;'>Inserisci</h3>", unsafe_allow_html=True)
        d_sel = st.date_input("Giorno", datetime.now(), key=f"date_{nome_social}")

        # FIX 3: valori scalari, non liste
        input_valori = {}
        for m in metriche:
            input_valori[m] = st.number_input(m, min_value=0, step=1, key=f"in_{nome_social}_{m}")

        if st.form_submit_button("Invia", use_container_width=True):
            salva_dati(file_csv, d_sel, input_valori)
            # FIX 4: segnala il successo tramite session_state,
            # poi ricarica — il messaggio verrà mostrato all'inizio della funzione.
            st.session_state[success_key] = True
            st.rerun()


# --- UI ---

st.markdown("<h1 style='text-align: center;'>Amministrazione</h1>", unsafe_allow_html=True)

scelta_social = st.selectbox("", ["Rassegna stampa", "Dati Social"])

# --- SEZIONE RASSEGNA STAMPA ---
if scelta_social == "Rassegna stampa":
    UPLOAD_DIR = "static"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    with st.expander("➕ Carica nuovo documento"):
        uploaded_file = st.file_uploader("Scegli un file PDF", type="pdf")

        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

            # FIX 5: controlla se il file esiste già prima di salvarlo.
            # Mostra un avviso e richiede conferma esplicita, evitando
            # la sovrascrittura silenziosa di file esistenti.
            if os.path.exists(file_path):
                st.warning(f"⚠️ Il file **'{uploaded_file.name}'** esiste già.")
                if st.button("Sì, sovrascrivi"):
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"File '{uploaded_file.name}' sovrascritto con successo!")
            else:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File '{uploaded_file.name}' salvato con successo!")

# --- SEZIONE DATI SOCIAL ---
if scelta_social == "Dati Social":
    col_ista, col_linkedin, col_facebook = st.columns([1, 1, 1], gap="small")

    with col_ista:
        st.markdown("<h2 style='text-align: center;'>Instagram</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "Instagram",
            "data_instagram.csv",
            ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
        )

    with col_linkedin:
        st.markdown("<h2 style='text-align: center;'>LinkedIn</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "LinkedIn",
            "data_linkedin.csv",
            ["Comparse_Ricerche", "Nuovi_Followers", "Impressioni_Post", "Visitatori_Pagina"],
        )

    with col_facebook:
        st.markdown("<h2 style='text-align: center;'>Facebook</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "Facebook",
            "data_facebook.csv",
            ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
        )