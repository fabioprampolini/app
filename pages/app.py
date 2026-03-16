import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
st.set_page_config(page_title="Rassegna Stampa", layout="wide", initial_sidebar_state="collapsed")

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

# --- Sezione Ricerca su Titoli ---
# --- Sezione Ricerca ---
# --- Sezione Ricerca ---

# 1. RIGA SUPERIORE: Solo la Checkbox
# --- Sezione Ricerca ---
st.subheader("🔍 Cerca Documenti")

# 1. RIGA SUPERIORE: Spostiamo la checkbox a destra usando le colonne
# Creiamo due colonne: una vuota larga (7.5) e una per la checkbox (2.5)
col_vuota, col_check = st.columns([7.5, 2.5])
with col_check:
    use_date = st.checkbox("Abilita filtro data", value=False)

# 2. RIGA INFERIORE: Ricerca e Data sulla stessa linea
# Usiamo gli stessi pesi della riga sopra per allineare verticalmente
col_search, col_date = st.columns([7.5, 2.5], vertical_alignment="bottom")

with col_search:
    st.caption("Cerca per titolo")
    search_query = st.text_input(
        "Titolo", 
        placeholder="Esempio: Unimore...", 
        label_visibility="collapsed"
    )

with col_date:
    if use_date:
        st.caption("Seleziona data")
        date_query = st.date_input(
            "Data", 
            value=datetime.now(), 
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )
        filtro_data = date_query.strftime("%d%m%Y")
    else:
        # Placeholder disabilitato per mantenere il layout fermo
        st.caption("Filtro data disattivato")
        st.date_input("Data", disabled=True, label_visibility="collapsed")
        filtro_data = None

# --- LOGICA DI FILTRO ---
all_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
filtered_files = [f for f in all_files if search_query.lower() in f.lower()]

if use_date and filtro_data:
    filtered_files = [f for f in filtered_files if filtro_data in f]


# --- Visualizzazione Risultati ---
if filtered_files:
    st.write(f"Trovati {len(filtered_files)} documenti:")
    for doc in filtered_files:
        with st.container():
            col_x, col_titolo, col_dl, col_open = st.columns([0.5, 10, 1.5, 1.5], gap="small", vertical_alignment="center")
            
            with col_x:
                if st.button("✖", key=f"del_{doc}", help="Elimina file"):
                    elimina_file(doc)
                
            with col_titolo:
                st.markdown(f"{doc}")
                
            with col_dl:
                with open(os.path.join(UPLOAD_DIR, doc), "rb") as f:
                    st.download_button("Scarica", f, file_name=doc, key=f"dl_{doc}", use_container_width=True)
            
            with col_open:
                # Percorso corretto se enableStaticServing è attivo
                st.link_button("Visualizza", f"static/{doc}", use_container_width=True)
else:
    st.info("Nessun file trovato con i filtri selezionati.")
