import streamlit as st
import pandas as pd
import plotly.express as px
import fitz  # PyMuPDF
import re
import os
from datetime import datetime

st.set_page_config(page_title="Rassegna Stampa", layout="wide", initial_sidebar_state="collapsed")

# --- CSS INTEGRATO E RESPONSIVE ---
st.markdown("""
    <style>
    /* 1. RIMOZIONE ELEMENTI NATIVI */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .stApp { margin-left: 0px !important; }
    header, footer, #MainMenu { visibility: hidden !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; }



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

    /* 3. STILE TASTO X (ELIMINA) */
    div[data-testid="stColumn"] button[help="Elimina file"] {
        background-color: transparent !important;
        border: 0 !important;
        color: #888 !important;
        font-size: 22px !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stColumn"] button[help="Elimina file"]:hover { color: #FF4B4B !important; }

    /* 4. LINEA ROSSA SEPARATRICE */
    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }

    /* --- 📱 OTTIMIZZAZIONE MOBILE (MEDIA QUERIES) --- */
    @media (max-width: 768px) {
        .nav-link { font-size: 18px !important; }
        .nav-wrapper { gap: 15px !important; justify-content: center; }
        h1 { font-size: 24px !important; }

        /* Trasforma le colonne dei file in blocchi verticali */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 10px !important;
        }
        div[data-testid="stColumn"] {
            width: 100% !important;
            text-align: center !important;
        }

        /* Sposta la X in alto a destra del box rassegna su mobile */
        div[data-testid="stColumn"]:has(button[help="Elimina file"]) {
            text-align: right !important;
            margin-bottom: -35px !important;
            z-index: 10;
        }

        /* Forza la legenda di Plotly in verticale su mobile */
        .js-plotly-plot .legend {
            display: flex !important;
            flex-direction: column !important;
        }

        /* Riduce altezza grafici su mobile */
        .stPlotlyChart { height: 280px !important; }
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

st.markdown("<h1 style='text-align: center;'>Rassegna Stampa</h1>", unsafe_allow_html=True)

UPLOAD_DIR = "static"
if not os.path.exists(UPLOAD_DIR): 
    os.makedirs(UPLOAD_DIR)

# --- ANALISI PDF ---
def analizza_rassegne(cartella_static):
    dati_report = []
    if not os.path.exists(cartella_static): return pd.DataFrame()
    files = [f for f in os.listdir(cartella_static) if f.endswith(".pdf")]
    
    for nome_file in files:
        match_data = re.search(r'(\d{8})\.pdf$', nome_file)
        if match_data:
            data_str = match_data.group(1)
            data_dt = datetime.strptime(data_str, "%d%m%Y")
            percorso_file = os.path.join(cartella_static, nome_file)
            doc = fitz.open(percorso_file)
            numero_articoli = 0
            for page_num in range(min(5, len(doc))): 
                testo = doc[page_num].get_text()
                trovati = re.findall(r'\d{2}/\d{2}/\d{4}', testo)
                numero_articoli += len(trovati)
            doc.close()
            dati_report.append({"Data": data_dt, "File": nome_file, "Articoli": numero_articoli})
    return pd.DataFrame(dati_report)

# --- GRAFICO 1 ---
df_analisi = analizza_rassegne(UPLOAD_DIR)
if not df_analisi.empty:
    fig = px.line(df_analisi, x="Data", y="Articoli", title="Numero di Articoli per Rassegna", markers=True)
    fig.update_traces(line=dict(color='#FF4B4B', width=4))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- RICERCA E ELIMINAZIONE ---
def elimina_file(nome_file):
    path = os.path.join(UPLOAD_DIR, nome_file)
    if os.path.exists(path):
        os.remove(path)
        st.rerun()

st.subheader("🔍 Cerca Documenti")
search_input = st.text_input("Cerca...", placeholder="Inserisci data o titolo", label_visibility="collapsed")

all_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
search_cleaned = search_input.replace("/", "").replace("-", "").replace(" ", "").lower()
filtered_files = [f for f in all_files if search_cleaned in f.lower() or search_input.lower() in f.lower()] if search_input else all_files

# --- LISTA RISULTATI ---
if filtered_files:
    for doc in filtered_files:
        with st.container(border=True):
            col_x, col_titolo, col_dl, col_open = st.columns([0.5, 10, 1.5, 1.5], gap="small", vertical_alignment="center")
            
            with col_x:
                if st.button("✖", key=f"del_{doc}", help="Elimina file"):
                    elimina_file(doc)
            with col_titolo:
                st.markdown(f"**{doc}**")
            with col_dl:
                with open(os.path.join(UPLOAD_DIR, doc), "rb") as f:
                    st.download_button("Scarica", f, file_name=doc, key=f"dl_{doc}", use_container_width=True, help="Scarica")
            with col_open:
                st.link_button("Visualizza", f"static/{doc}", use_container_width=True, help="Visualizza")
else:
    st.info("Nessun documento trovato.")
