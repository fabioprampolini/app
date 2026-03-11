import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Gestione Articoli", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 1. RIMOZIONE SIDEBAR TOTALE */
    [data-testid="collapsedControl"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    
    .stApp {
        background-color: #ffffff !important;
    }
    /* 3. MENU DI NAVIGAZIONE */
    .nav-container {
        display: flex;
        justify-content: flex-start;
        gap: 50px;
        padding: 20px 0;
    }
    
    .nav-link {
        text-decoration: none !important;
        color: #58595b !important;
        font-size: 30px;
        font-weight: 500;
        transition: 0.3s;
        border-bottom: 2px solid transparent;
        padding-bottom: 5px;
    }
    
    .nav-link:hover {
        color: #58595b !important;
        border-bottom: 2px solid red;
    }

    /* Colore per tutti i titoli nativi di Streamlit */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #58595b !important;
    }

    /* Applica il colore anche ai sottotitoli specifici di Streamlit */
    .st-emotion-cache-isw95m, .st-emotion-cache-10trblm { 
    color: #58595b !important;
    }
    </style>
    
    <div class="nav-container">
        <a href="/" target="_self" class="nav-link">Home</a>
        <a href="/app" target="_self" class="nav-link">Gestione Articoli</a>
    </div>
    <hr>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Gestione Articoli</h1>", unsafe_allow_html=True)
st.subheader("📄 Inserisci Il file degli articoli")

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