import streamlit as st
<<<<<<< HEAD
import re
import fitz  # PyMuPDF
import io
from datetime import datetime
from typing import Optional
from utils.db import get_connection
=======
import pandas as pd
import os
from datetime import datetime
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a

st.set_page_config(page_title="Amministrazione", layout="wide", initial_sidebar_state="collapsed")

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
    div[data-baseweb="select"] > div { font-size: 20px !important; min-height: 50px !important; }
    ul[data-baseweb="menu"] li { font-size: 20px !important; }

=======
    /* 3. SELECT BOX */
    div[data-baseweb="select"] > div {
        font-size: 20px !important;
        min-height: 50px !important;
    }
    ul[data-baseweb="menu"] li { font-size: 20px !important; }

    /* 4. LINEA ROSSA SEPARATRICE */
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
    /* 5. MOBILE */
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
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

<<<<<<< HEAD
def conta_articoli_da_bytes(contenuto: bytes) -> int:
    """
    Analizza il PDF in memoria (senza salvarlo su disco) e conta
    le occorrenze di date nel formato gg/mm/aaaa come proxy
    per il numero di articoli, esattamente come nella versione originale.
    Usa le prime 5 pagine per efficienza.
    """
    numero_articoli = 0
    try:
        with fitz.open(stream=contenuto, filetype="pdf") as doc:
            for page_num in range(min(5, len(doc))):
                testo = doc[page_num].get_text()
                trovati = re.findall(r'\d{2}/\d{2}/\d{4}', testo)
                numero_articoli += len(trovati)
    except Exception as e:
        st.warning(f"Impossibile analizzare il PDF per contare gli articoli: {e}")
    return numero_articoli


def salva_pdf(
    nome_file: str,
    data_documento: Optional[object],
    contenuto: bytes,
    numero_articoli: int,
) -> bool:
    """
    Salva il PDF nel database con il numero di articoli già calcolato.
    Restituisce True se salvato, False se il file esiste già.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO rassegna_stampa
                        (nome_file, data_documento, contenuto, numero_articoli)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (nome_file) DO NOTHING
                    RETURNING id;
                    """,
                    (nome_file, data_documento, contenuto, numero_articoli),
                )
                risultato = cur.fetchone()
            conn.commit()
        return risultato is not None
    except Exception as e:
        st.error(f"Errore nel salvataggio del PDF: {e}")
        return False


def salva_dati_social(tabella: str, data: object, valori: dict) -> None:
    """
    Inserisce o aggiorna un record nella tabella social.
    ON CONFLICT (data) DO UPDATE gestisce il reinserimento
    per la stessa data senza errori di duplicato.
    """
    colonne = ", ".join(valori.keys())
    segnaposto = ", ".join(["%s"] * len(valori))
    aggiornamenti = ", ".join([f"{k} = EXCLUDED.{k}" for k in valori.keys()])

    query = f"""
        INSERT INTO {tabella} (data, {colonne})
        VALUES (%s, {segnaposto})
        ON CONFLICT (data) DO UPDATE SET {aggiornamenti};
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, [data] + list(valori.values()))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nel salvataggio su '{tabella}': {e}")
        raise


def crea_sezione_social(nome_social: str, tabella: str, metriche: list) -> None:
    """Genera un form di inserimento dati per un social network."""
=======
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
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
    success_key = f"success_{nome_social}"

    if st.session_state.get(success_key):
        st.success("Dati salvati con successo!")
        st.session_state[success_key] = False

    with st.form(f"form_{nome_social}", clear_on_submit=True):
        st.markdown("<h3 style='text-align: center;'>Inserisci</h3>", unsafe_allow_html=True)
        d_sel = st.date_input("Giorno", datetime.now(), key=f"date_{nome_social}")

<<<<<<< HEAD
        valori = {}
        for m in metriche:
            valori[m] = st.number_input(m, min_value=0, step=1, key=f"in_{nome_social}_{m}")

        if st.form_submit_button("Invia", use_container_width=True):
            try:
                salva_dati_social(tabella, d_sel, valori)
                st.cache_data.clear()
                st.session_state[success_key] = True
                st.rerun()
            except Exception:
                pass


# --- MAIN ---

st.markdown("<h1 style='text-align: center;'>Amministrazione</h1>", unsafe_allow_html=True)

scelta = st.selectbox("", ["Rassegna stampa", "Dati Social"])

# --- SEZIONE RASSEGNA STAMPA ---
if scelta == "Rassegna stampa":
=======
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

>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
    with st.expander("➕ Carica nuovo documento"):
        uploaded_file = st.file_uploader("Scegli un file PDF", type="pdf")

        if uploaded_file:
<<<<<<< HEAD
            contenuto = uploaded_file.getbuffer().tobytes()

            # Estrai la data dal nome file (formato ddmmyyyy.pdf)
            data_documento = None
            match = re.search(r'(\d{8})\.pdf$', uploaded_file.name)
            if match:
                try:
                    data_documento = datetime.strptime(match.group(1), "%d%m%Y").date()
                except ValueError:
                    pass

            # Calcola automaticamente il numero di articoli dal PDF
            with st.spinner("Analisi del PDF in corso..."):
                numero_articoli = conta_articoli_da_bytes(contenuto)

            salvato = salva_pdf(
                uploaded_file.name,
                data_documento,
                contenuto,
                numero_articoli,
            )

            if salvato:
                st.cache_data.clear()
                st.success(
                    f"File '{uploaded_file.name}' salvato con successo! "
                    f"Articoli rilevati: **{numero_articoli}**"
                )
            else:
                st.warning(f"'{uploaded_file.name}' esiste già nel database.")

# --- SEZIONE DATI SOCIAL ---
if scelta == "Dati Social":
=======
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
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
    col_ista, col_linkedin, col_facebook = st.columns([1, 1, 1], gap="small")

    with col_ista:
        st.markdown("<h2 style='text-align: center;'>Instagram</h2>", unsafe_allow_html=True)
        crea_sezione_social(
<<<<<<< HEAD
            "Instagram", "instagram",
            ["visualizzazioni", "interazioni", "nuovi_followers"],
=======
            "Instagram",
            "data_instagram.csv",
            ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
        )

    with col_linkedin:
        st.markdown("<h2 style='text-align: center;'>LinkedIn</h2>", unsafe_allow_html=True)
        crea_sezione_social(
<<<<<<< HEAD
            "LinkedIn", "linkedin",
            ["comparse_ricerche", "nuovi_followers", "impressioni_post", "visitatori_pagina"],
=======
            "LinkedIn",
            "data_linkedin.csv",
            ["Comparse_Ricerche", "Nuovi_Followers", "Impressioni_Post", "Visitatori_Pagina"],
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
        )

    with col_facebook:
        st.markdown("<h2 style='text-align: center;'>Facebook</h2>", unsafe_allow_html=True)
        crea_sezione_social(
<<<<<<< HEAD
            "Facebook", "facebook",
            ["visualizzazioni", "interazioni", "nuovi_followers"],
=======
            "Facebook",
            "data_facebook.csv",
            ["Visualizzazioni", "Interazioni", "Nuovi_Followers"],
>>>>>>> 9253531693a2bd7310c9d57107278414bba61c6a
        )