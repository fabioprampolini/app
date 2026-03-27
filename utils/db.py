import psycopg2
import streamlit as st

def get_connection():
    """Restituisce una connessione al database PostgreSQL."""
    return psycopg2.connect(st.secrets["DATABASE_URL"])