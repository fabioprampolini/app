import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURAZIONE PAGINA E RIMOZIONE LINK TITOLI ---
st.set_page_config(layout="wide", page_title="Home")


# --- FUNZIONI DI GESTIONE DATI ---
def salva_dati(file_csv, data, dict_valori):
    nuovo = pd.DataFrame({'Data': [pd.to_datetime(data)], **dict_valori})
    if os.path.exists(file_csv):
        df = pd.read_csv(file_csv, parse_dates=['Data'])
        df = pd.concat([df, nuovo], ignore_index=True).sort_values('Data')
    else:
        df = nuovo
    df.to_csv(file_csv, index=False)

def crea_sezione_social(nome_social, file_csv, metriche):
    st.subheader(f"{nome_social}")
    df = pd.read_csv(file_csv, parse_dates=['Data']) if os.path.exists(file_csv) else pd.DataFrame()
    
    with st.container(border=True):
        col_chart, col_input = st.columns([3, 1])

        
        # --- COLONNA SINISTRA: GRAFICO ---
        with col_chart:
            if not df.empty:
                scelte = st.multiselect(f"Filtra {nome_social}:", metriche, default=metriche, key=f"ms_{nome_social}")
                fig = px.line(df, x='Data', y=scelte, markers=True, template="plotly_white", height=350)
                fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend_orientation="h")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Nessun dato per {nome_social}. Inseriscili nel modulo a destra.")

        # --- COLONNA DESTRA: INPUT ---
        with col_input:
            with st.form(f"form_{nome_social}", clear_on_submit=True):
                st.markdown("<h3 style='text-align: center;'>Inserisci</h3>", unsafe_allow_html=True)
                d_sel = st.date_input("Giorno", datetime.now(), key=f"date_{nome_social}")
                
                input_valori = {}
                for m in metriche:
                    input_valori[m] = [st.number_input(m, min_value=0, step=1, key=f"in_{nome_social}_{m}")]
                
                if st.form_submit_button(f"Inserisci", use_container_width=True):
                    salva_dati(file_csv, d_sel, input_valori)
                    st.rerun()

# --- CSS PER IL MENU A LINK CENTRALI ---
st.markdown("""
    <style>
    /* 1. RIMOZIONE SIDEBAR TOTALE */
    [data-testid="collapsedControl"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    
    /* 2. RIMOZIONE ICONE LINK TITOLI */
    .stHeader a { display: none !important; }
    
    /* Contenitore Menu */
    .nav-container {
        display: flex;
        justify-content: flex-start;
        gap: 50px;
        padding: 20px 0;
        font-family: 'sans serif';
    }
    
  .nav-link {
        text-decoration: none !important; /* Forza la rimozione della sottolineatura */
        color: #58595b !important;
        font-size: 30px;
        font-weight: 500;
        transition: 0.3s;
        border-bottom: 2px solid transparent;
        padding-bottom: 5px;
    }
    
    .nav-link:hover {
        text-decoration: none !important;
        color: #58595b !important;
        border-bottom: 2px solid red; /* Effetto linea rossa solo al passaggio del mouse */
    }

    /* Colore per tutti i titoli nativi di Streamlit */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #58595b !important;}


    /* Applica il colore anche ai sottotitoli specifici di Streamlit */
    .st-emotion-cache-isw95m, .st-emotion-cache-10trblm { 
    color: #58595b !important;
    }
    </style>
    
    <div class="nav-container">
        <a href="/" " class="nav-link">Home</a>
        <a href="/app"  class="nav-link">Gestione Articoli</a>
    </div>
    <hr>
    """, unsafe_allow_html=True)


# --- MAIN APP ---
st.markdown("<h1 style='text-align: center;'>Grafici dei social media</h1>", unsafe_allow_html=True)

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


