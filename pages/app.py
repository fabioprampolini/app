import streamlit as st
import pandas as pd
import plotly.express as px
import fitz  # PyMuPDF
import re
import os
from datetime import datetime

st.set_page_config(page_title="Rassegna Stampa", layout="wide", initial_sidebar_state="collapsed")

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

    @media (max-width: 768px) {
    /* 1. Navigazione: riduce font e spazio */
    .nav-link {
        font-size: 18px !important;
        gap: 15px !important;
    }
    .nav-wrapper {
        gap: 15px !important;
        justify-content: center;
    }

    /* 2. Titolo principale più piccolo */
    h1 {
        font-size: 24px !important;
    }

    /* 3. Trasforma le colonne dei file in righe singole */
    /* Streamlit usa div[data-testid="stHorizontalBlock"] per le colonne */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }

    /* 4. Forza i bottoni (Scarica/Visualizza) a larghezza piena su mobile */
    div[data-testid="stColumn"] {
        width: 100% !important;
        margin-bottom: 10px;
    }
    
    /* 5. Nasconde la "X" su mobile o la sposta per non rompere il layout */
    div[data-testid="stColumn"]:first-child {
        text-align: right;
    }
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


def analizza_rassegne(cartella_static):
    dati_report = []
    
    # Prendi tutti i PDF nella cartella
    files = [f for f in os.listdir(cartella_static) if f.endswith(".pdf")]
    
    for nome_file in files:
        # 1. Estrazione Data dal Titolo (Ultime 8 cifre prima di .pdf)
        # Esempio: Unimore15022026.pdf -> 15022026
        match_data = re.search(r'(\d{8})\.pdf$', nome_file)
        if match_data:
            data_str = match_data.group(1)
            data_dt = datetime.strptime(data_str, "%d%m%Y")
            
            # 2. Conteggio Articoli nel PDF
            percorso_file = os.path.join(cartella_static, nome_file)
            doc = fitz.open(percorso_file)
            numero_articoli = 0
            
            # Leggiamo solo le prime pagine (dove solitamente c'è l'indice)
            for page_num in range(min(5, len(doc))): 
                testo = doc[page_num].get_text()
                # Cerchiamo righe che iniziano con una data GG/MM/AAAA (tipico degli indici)
                trovati = re.findall(r'\d{2}/\d{2}/\d{4}', testo)
                numero_articoli += len(trovati)
            
            doc.close()
            
            dati_report.append({
                "Data": data_dt,
                "File": nome_file,
                "Articoli": numero_articoli
            })
            
    return pd.DataFrame(dati_report)

# --- Visualizzazione in Streamlit ---
# --- Visualizzazione Grafici in Verticale ---

# 1. IL TUO PRIMO GRAFICO (Analisi Articoli)
df_analisi = analizza_rassegne("static")

fig = px.line(
    df_analisi,
    x="Data",
    y="Articoli",
    title="Numero di Articoli per Rassegna",
    markers=True
)
fig.update_traces(line=dict(color='#FF4B4B', width=3))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Data Rassegna",
    yaxis_title="Numero Articoli",
    font=dict(color="white")
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # Spazio tra i due grafici

# 2. SECONDO GRAFICO VUOTO
# Creiamo un grafico senza dati ma con lo stesso stile e sfondo trasparente
fig_vuoto = px.line(
    title="Analisi Secondaria (In attesa di dati)",
)
fig_vuoto.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    annotations=[{
        "text": "Nessun dato aggiuntivo disponibile",
        "xref": "paper", "yref": "paper",
        "showarrow": False, 
        "font": {"size": 18, "color": "gray"}
    }]
)
st.plotly_chart(fig_vuoto, use_container_width=True)


def elimina_file(nome_file):
    path = os.path.join(UPLOAD_DIR, nome_file)
    if os.path.exists(path):
        os.remove(path)
        st.rerun()
# --- Sezione Ricerca Unificata ---
st.subheader("🔍 Cerca Documenti")

search_input = st.text_input(
    label="Cerca per titolo o data",
    placeholder="Inserisci la data o il titolo della rassegna stampa",
    label_visibility="collapsed"
)

# --- LOGICA DI FILTRO SMART ---
all_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]

if search_input:
    # PULIZIA DELLA RICERCA: Rimuoviamo /, - e spazi se l'utente li inserisce
    # Es: "17/03/2026" diventa "17032026"
    search_cleaned = search_input.replace("/", "").replace("-", "").replace(" ", "").lower()
    
    # Filtriamo i file: cerchiamo sia il testo originale che quello "pulito"
    # Così se cerca "Unimore" lo trova, e se cerca "17/03" trova "1703"
    filtered_files = [
        f for f in all_files 
        if search_cleaned in f.lower() or search_input.lower() in f.lower()
    ]
else:
    filtered_files = all_files

# --- Visualizzazione Risultati (rimane uguale) ---
if filtered_files:
    st.write(f"Trovati {len(filtered_files)} documenti:")
    for doc in filtered_files:
        with st.container():
            col_x, col_titolo, col_dl, col_open = st.columns([0.5, 10, 1.5, 1.5], gap="small", vertical_alignment="center")
            
            with col_x:
                if st.button("✖", key=f"del_{doc}", help="Elimina file"):
                    elimina_file(doc)
                
            with col_titolo:
                st.markdown(f"**{doc}**")
                
            with col_dl:
                with open(os.path.join(UPLOAD_DIR, doc), "rb") as f:
                    st.download_button("Scarica", f, file_name=doc, key=f"dl_{doc}", use_container_width=True)
            
            with col_open:
                st.link_button("Visualizza", f"static/{doc}", use_container_width=True)
else:
    st.info("Nessun documento trovato.")
