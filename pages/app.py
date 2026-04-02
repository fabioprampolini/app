import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import re
from typing import Optional
from utils.db import get_connection

st.set_page_config(page_title="Rassegna Stampa", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .stApp { margin-left: 0px !important; }
    header, footer, #MainMenu { visibility: hidden !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    header { height: 0px !important; display: none !important; }

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

    .header-line {
        border: 0;
        height: 1px;
        background: #FF4B4B;
        margin-bottom: 30px;
        opacity: 0.5;
    }

    @media (max-width: 768px) {
        .nav-link { font-size: 18px !important; }
        .nav-wrapper { gap: 15px !important; justify-content: center; }
        h1 { font-size: 24px !important; }
        div[data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 10px !important; }
        div[data-testid="stColumn"] { width: 100% !important; text-align: center !important; }
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


# --- FUNZIONI ---

@st.cache_data(ttl=60)
def carica_elenco_pdf() -> pd.DataFrame:
    try:
        with get_connection() as conn:
            df = pd.read_sql(
                """SELECT id, nome_file, data_documento, numero_articoli, caricato_il
                   FROM rassegna_stampa
                   ORDER BY data_documento DESC NULLS LAST""",
                conn,
            )
        return df
    except Exception as e:
        st.warning(f"Errore nel caricamento dei PDF: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=60)
def carica_contenuto_pdf(nome_file: str) -> Optional[bytes]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT contenuto FROM rassegna_stampa WHERE nome_file = %s",
                    (nome_file,),
                )
                risultato = cur.fetchone()
        return bytes(risultato[0]) if risultato else None
    except Exception as e:
        st.warning(f"Errore nel caricamento del file '{nome_file}': {e}")
        return None


def elimina_pdf(nome_file: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM rassegna_stampa WHERE nome_file = %s RETURNING id",
                    (nome_file,),
                )
                risultato = cur.fetchone()
            conn.commit()
        return risultato is not None
    except Exception as e:
        st.error(f"Errore nell'eliminazione di '{nome_file}': {e}")
        return False


def normalizza_ricerca(testo: str) -> str:
    match = re.match(r'^(\d{2})[/\-](\d{2})[/\-](\d{4})$', testo.strip())
    if match:
        return f"{match.group(1)}{match.group(2)}{match.group(3)}"
    return testo


# --- GRAFICO ---
df_pdf = carica_elenco_pdf()

if not df_pdf.empty and df_pdf["data_documento"].notna().any():
    df_grafico = df_pdf.dropna(subset=["data_documento"]).sort_values("data_documento")
    fig = px.line(
        df_grafico,
        x="data_documento",
        y="numero_articoli",
        title="Numero di Articoli per Rassegna",
        markers=True,
    )
    fig.update_traces(line=dict(color="#FF4B4B", width=4))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, use_container_width=True)

# --- RICERCA ---
st.subheader("🔍 Cerca Documenti")
search_input = st.text_input(
    "Cerca...",
    placeholder="Inserisci data o titolo",
    label_visibility="collapsed",
)

# --- POPUP CONFERMA ELIMINAZIONE ---
# Se è in corso una richiesta di eliminazione, mostra il dialog di conferma
if "conferma_elimina" in st.session_state and st.session_state["conferma_elimina"]:
    nome_da_eliminare = st.session_state["conferma_elimina"]

    @st.dialog("Conferma eliminazione")
    def dialog_elimina():
        st.warning(f"Sei sicuro di voler eliminare **'{nome_da_eliminare}'**? L'operazione è irreversibile.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sì, elimina", use_container_width=True, type="primary"):
                if elimina_pdf(nome_da_eliminare):
                    st.cache_data.clear()
                st.session_state["conferma_elimina"] = None
                st.rerun()
        with col2:
            if st.button("Annulla", use_container_width=True):
                st.session_state["conferma_elimina"] = None
                st.rerun()

    dialog_elimina()

# --- LISTA RISULTATI ---
if not df_pdf.empty:
    if search_input:
        termine = normalizza_ricerca(search_input)
        mask = df_pdf["nome_file"].str.contains(termine, case=False, na=False, regex=False)
        df_filtrato = df_pdf[mask]
        if df_filtrato.empty:
            st.warning(f"Nessun documento trovato per la ricerca **'{search_input}'**.")
    else:
        df_filtrato = df_pdf

    if not df_filtrato.empty:
        for _, row in df_filtrato.iterrows():
            with st.container(border=True):
                col_x, col_titolo, col_articoli, col_dl, col_open = st.columns(
                    [0.5, 8, 2, 1.5, 1.5], gap="small", vertical_alignment="center"
                )

                with col_x:
                    # FIX: invece di eliminare subito, imposta la conferma
                    if st.button("✖", key=f"del_{row['nome_file']}", help="Elimina file"):
                        st.session_state["conferma_elimina"] = row["nome_file"]
                        st.rerun()

                with col_titolo:
                    st.markdown(f"**{row['nome_file']}**")

                with col_articoli:
                    n = int(row["numero_articoli"]) if pd.notna(row["numero_articoli"]) else 0
                    st.markdown(f"**{n}** articoli")

                with col_dl:
                    contenuto = carica_contenuto_pdf(row["nome_file"])
                    if contenuto:
                        st.download_button(
                            "Scarica",
                            contenuto,
                            file_name=row["nome_file"],
                            mime="application/pdf",
                            key=f"dl_{row['nome_file']}",
                            use_container_width=True,
                        )

                with col_open:
                    # FIX: apre il PDF in una nuova scheda tramite blob URL generato in JS
                    contenuto_view = carica_contenuto_pdf(row["nome_file"])
                    if contenuto_view:
                        b64 = base64.b64encode(contenuto_view).decode("utf-8")
                        pdf_id = str(row["id"])
                        st.components.v1.html(
                            f"""
                            <script>
                            function apriPDF_{pdf_id}() {{
                                const b64 = "{b64}";
                                const binary = atob(b64);
                                const bytes = new Uint8Array(binary.length);
                                for (let i = 0; i < binary.length; i++) {{
                                    bytes[i] = binary.charCodeAt(i);
                                }}
                                const blob = new Blob([bytes], {{ type: "application/pdf" }});
                                const url = URL.createObjectURL(blob);
                                window.open(url, "_blank");
                            }}
                            </script>
                            <style>
                                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                                body {{ background: transparent; }}
                                button {{
                                    width: 100%;
                                    height: 38px;
                                    background-color: transparent;
                                    border: 1px solid rgba(49, 51, 63, 0.2);
                                    border-radius: 0.5rem;
                                    font-size: 0.875rem;
                                    font-family: "Source Sans Pro", sans-serif;
                                    font-weight: 400;
                                    color: rgb(49, 51, 63);
                                    cursor: pointer;
                                    transition: background-color 0.1s, border-color 0.1s, color 0.1s;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    gap: 6px;
                                }}
                                button:hover {{
                                    background-color: rgba(49, 51, 63, 0.08);
                                
                                }}
                                button:active {{
                                    background-color: rgba(49, 51, 63, 0.08);
                                    transform: scale(0.98);
                                }}
                                svg {{
                                    flex-shrink: 0;
                                }}
                            </style>
                            <button onclick="apriPDF_{pdf_id}()">
                                Visualizza
                            </button>
                            """,
                            height=42,
                            scrolling=False,
                        )
    else:
        st.info("Nessun documento trovato.")
else:
    st.info("Nessun documento presente. Caricane uno dalla pagina Amministrazione.")