import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Social Media",layout="wide",initial_sidebar_state="collapsed")

def crea_sezione_social(nome_social, file_csv, metriche):
    st.subheader(f"{nome_social}")
    df = pd.read_csv(file_csv, parse_dates=['Data']) if os.path.exists(file_csv) else pd.DataFrame()
    
    with st.container(border=True):
        if not df.empty:
            scelte = st.multiselect(f"Filtra {nome_social}:", metriche, default=metriche, key=f"ms_{nome_social}")
            fig = px.line(df, x='Data', y=scelte, markers=True, template="plotly_white", height=350)            
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend_orientation="h")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Nessun dato per {nome_social}. Inseriscili nel modulo a destra.")


st.markdown("""
    <style>
     /* 1. RIMOZIONE TOTALE SIDEBAR E PULSANTE DI CONTROLLO */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* 2. FORZA IL CONTENUTO AD OCCUPARE TUTTA LA LARGHEZZA */
    .stApp {
        margin-left: 0px !important;
    }
    header {visibility: hidden !important;}
    /* 2. Nasconde il footer "Made with Streamlit" in basso */
    footer {visibility: hidden !important;}
    /* 3. Opzionale: Nasconde il menu a tre puntini (se non l'hai già fatto) */
    #MainMenu {visibility: none !important;}
 
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
        color: #FF4B4B !important; 
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
        <a href="./" target="_self" class="nav-link">Social Media</a>
        <a href="./app" target="_self" class="nav-link">Rassegna Stampa</a>
        <a href="./inser" target="_self" class="nav-link">Inserisci Dati</a>
    </div>
    <div class="header-line"></div>
    """, unsafe_allow_html=True)


st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)
# --- MAIN APP ---
st.markdown("<h1 style='text-align: center;'>Social Media</h1>", unsafe_allow_html=True)

# 1. SEZIONE INSTAGRAM
crea_sezione_social(
    "Instagram", 
    "data_instagram.csv", 
    ["Visualizzazioni", "Interazioni", "Nuovi_Followers"]
)

# 2. SEZIONE FACEBOOK
crea_sezione_social(
    "Facebook", 
    "data_facebook.csv", 
    ["Visualizzazioni", "Interazioni", "Nuovi_Followers"]
)

# 3. SEZIONE LINKEDIN
crea_sezione_social(
    "LinkedIn", 
    "data_linkedin.csv", 
    ["Comparse_Ricerche", "Nuovi_Followers", "Impressioni_Post", "Visitatori_Pagina"]
)


