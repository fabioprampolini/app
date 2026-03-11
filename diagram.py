import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Il Mio Progetto",layout="wide")
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
                
                if st.form_submit_button(f"Invia", use_container_width=True):
                    salva_dati(file_csv, d_sel, input_valori)
                    st.rerun()

# 1. Configurazione Pagina (Deve essere SEMPRE la prima riga)

st.markdown("""
    <style>
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


st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)
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


