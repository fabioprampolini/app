import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Gestione Articoli", layout="wide", initial_sidebar_state="collapsed")

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
    div[data-testid="stColumn"] button[help="Elimina file"]:hover {
        color: #FF4B4B !important; /* Diventa rosso al passaggio */
        background-color: transparent !important;
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
        <a href="./" target="_self" class="nav-link">Home</a>
        <a href="./app" target="_self" class="nav-link">Gestione Articoli</a>
    </div>
    <div class="header-line"></div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Gestione Articoli</h1>", unsafe_allow_html=True)
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

st.divider()

# --- Sezione Ricerca su Titoli ---
st.subheader("🔍 Cerca tra i titoli")
search_query = st.text_input("Inserisci il nome del file da cercare...", placeholder="Esempio: Unimore_data")

# Recupera la lista dei file
all_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]

# Filtra la lista in base alla query
filtered_files = [f for f in all_files if search_query.lower() in f.lower()]

def elimina_file(nome_file):
    path = os.path.join(UPLOAD_DIR, nome_file)
    if os.path.exists(path):
        os.remove(path)
        st.rerun()

# 3. Sezione Visualizzazione
if filtered_files:
    for doc in filtered_files:
        with st.container():
            # Layout: 0.5 per la X, 10 per il titolo, 1.5 per Scarica, 1.5 per Apri
            col_x, col_titolo, col_dl, col_open = st.columns([0.5, 10, 1.5, 1.5], gap="small", vertical_alignment="center")
            
            with col_x:
                if st.button("✖", key=f"del_{doc}", help="Elimina file"):
                    elimina_file(doc)
                
            with col_titolo:
                st.markdown(f"{doc}")
                
            with col_dl:
                with open(os.path.join(UPLOAD_DIR, doc), "rb") as f:
                    st.download_button("Scarica", f, file_name=doc, key=f"dl_{doc}", use_container_width=True, help="Scarica il file")
            
            with col_open:
                st.link_button("Visualizza", f"static/{doc}", use_container_width=True, help="Apri il file un altra scheda")