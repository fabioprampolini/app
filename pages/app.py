import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Gestione Articoli", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* RIMOZIONE ELEMENTI NATIVI */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none !important;}
    .stHeader a { display: none !important; }
    
    /* RIMOZIONE DEI TRE PUNTINI IN ALTO A DESTRA */
    #MainMenu {display: none !important;}
    header {visibility: hidden !important;}
    
    /* RIMOZIONE DEL FOOTER "MADE WITH STREAMLIT" (Opzionale) */
    footer {visibility: hidden !important;}
    
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

if filtered_files:
    st.write(f"Trovati {len(filtered_files)} documenti:")
    for doc in filtered_files:
        # Usiamo vertical_alignment per allineare testo e bottoni sulla stessa linea
        col1, col2 = st.columns([2, 1], gap="small", vertical_alignment="center")
        
        with col1:
            st.text(f"📄 {doc}")
            
            
        with col2:
            # Creiamo sottocolonne con larghezza fissa/piccola per "stringere" i bottoni
            sub_col1, sub_col2 = st.columns([1, 1], gap="small")
            
            with sub_col1:
                with open(os.path.join(UPLOAD_DIR, doc), "rb") as f:
                    st.download_button("Scarica", f, file_name=doc, key=f"dl_{doc}")
            
            with sub_col2:
                # Nota: rimosso 'key' che causava l'errore
                st.link_button("Apri", f"app/static/{doc}")