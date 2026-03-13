import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
st.set_page_config(page_title="Inserisci Dati", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    
    /* 2. Nasconde il footer "Made with Streamlit" in basso */
    footer {visibility: hidden !important;}

    /* 3. Opzionale: Nasconde il menu a tre puntini (se non l'hai già fatto) */
    #MainMenu {visibility: none !important;}
     /* 2. Nasconde il pulsante dell'host/account in basso a destra */
    .stAppDeployButton {
        display: none !important;
    }
    
    /* 3. Rimuove lo spazio vuoto in fondo alla pagina */
    .stApp [data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }
    /* NAVIGAZIONE TESTUALE */
    .nav-wrapper {
        display: flex;
        gap: 40px;
        padding: 10px 0;
        margin-bottom: 5px;
    }

    div[data-baseweb="select"] > div {
        font-size: 20px !important;
        min-height: 50px !important; /* Aumenta l'altezza per ospitare il testo più grande */
    }

    /* 3. Aumenta la dimensione delle opzioni nel menu a tendina quando è aperto */
    ul[data-baseweb="menu"] li {
        font-size: 20px !important;
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
    .nav-link:hover {
        color: #FF4B4B !important; /* Il tuo rosso */
        border-bottom: 3px solid #FF4B4B;
    }
        div[data-testid="stColumn"] button[help="Elimina file"] {
        background-color: transparent !important;
        border: 0 !important;
        text-align: center !important;
        color: #888 !important; /* Grigio di base */
        font-size: 20px !important;
        padding: 0 !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }
    
    /* LINEA ROSSA DI SEPARAZIONE */
    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }
    </style>

    <div class="nav-wrapper">
        <a href="./" target="_self" class="nav-link">Social Media</a>
        <a href="./app" target="_self" class="nav-link">Rassegna Stampa</a>
        <a href="./inser" target="_self" class="nav-link">Inserisci Dati</a>
    </div>
    <div class="header-line"></div>
    """, unsafe_allow_html=True)

def salva_dati(file_csv, data, dict_valori):
    nuovo = pd.DataFrame({'Data': [pd.to_datetime(data)], **dict_valori})
    if os.path.exists(file_csv):
        df = pd.read_csv(file_csv, parse_dates=['Data'])
        df = pd.concat([df, nuovo], ignore_index=True).sort_values('Data')
    else:
        df = nuovo
    df.to_csv(file_csv, index=False)

def crea_sezione_social(nome_social, file_csv, metriche):
    with st.form(f"form_{nome_social}", clear_on_submit=True):
                st.markdown("<h3 style='text-align: center;'>Inserisci</h3>", unsafe_allow_html=True)
                d_sel = st.date_input("Giorno", datetime.now(), key=f"date_{nome_social}")
                
                input_valori = {}
                for m in metriche:
                    input_valori[m] = [st.number_input(m, min_value=0, step=1, key=f"in_{nome_social}_{m}")]
                
                if st.form_submit_button(f"Invia", use_container_width=True):
                    salva_dati(file_csv, d_sel, input_valori)
                    st.rerun()


st.markdown("<h1 style='text-align: center;'>Inserisci Dati</h1>", unsafe_allow_html=True)

scelta_social = st.selectbox(
 "Scegli che dati devi inserire:",
 ["Rassegne stampa", "Dati Social" ]
)
if scelta_social == "Rassegne stampa":
    st.subheader("📄Inserisci Il file degli articoli")
    UPLOAD_DIR = "static"
    if not os.path.exists(UPLOAD_DIR): 
        os.makedirs(UPLOAD_DIR)
# --- Sezione Upload ---
    with st.expander("➕ Carica nuovo documento"):
        uploaded_file = st.file_uploader("Scegli un file PDF", type="pdf")
        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
             f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' salvato con successo!")

if scelta_social == "Dati Social":
    col_ista, col_linkedin, col_facebook = st.columns([1, 1, 1], gap="small")
    with col_ista:
        st.markdown("<h2 style='text-align: center;'>Instagram</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "Instagram", 
            "data_instagram.csv", 
         ["Visualizzazioni", "Interazioni", "Nuovi_Followers"]
        )
    
    with col_linkedin:
        st.markdown("<h2 style='text-align: center;'>LinkedIn</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "LinkedIn", 
         "data_linkedin.csv", 
         ["Comparse_Ricerche", "Nuovi_Followers", "Impressioni_Post", "Visitatori_Pagina"]
        )
    
    with col_facebook:
        st.markdown("<h2 style='text-align: center;'>Facebook</h2>", unsafe_allow_html=True)
        crea_sezione_social(
            "Facebook", 
            "data_facebook.csv", 
            ["Visualizzazioni", "Interazioni", "Nuovi_Followers"]
        )

     