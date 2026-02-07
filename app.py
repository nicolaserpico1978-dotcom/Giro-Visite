import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Agenda Nicola Pro", layout="wide")

# CONFIGURAZIONE
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"
CSV_URL = URL_FOGLIO.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit', '/export?format=csv')

# Funzione per caricare i dati
def load_data():
    return pd.read_csv(f"{CSV_URL}&cache_bust={int(time.time())}")

df = load_data()

st.title("🚀 Nicola: Gestione Giri")

if st.button("🔄 AGGIORNA LISTA"):
    st.rerun()

st.divider()

# Selezione Settimana
settimane = sorted(df['Settimana'].unique())
sett_scelta = st.selectbox("📅 Settimana attuale:", settimane)

clienti_sett = df[df['Settimana'] == sett_scelta]

for i, row in clienti_sett.iterrows():
    with st.container(border=True):
        col_nome, col_azione = st.columns([0.6, 0.4])
        
        with col_nome:
            st.subheader(f"👤 {row['Cliente']}")
            # Mostra stato attuale
            if str(row['Stato']).upper() == "X":
                st.success("Già visitato questo mese")
        
        with col_azione:
            # TASTO MAGICO
            if st.button("SPOSTA AL PROSSIMO MESE", key=f"btn_{i}"):
                st.warning("Stiamo spostando il cliente... (Questa funzione richiede autorizzazione speciale)")
                st.info("Nicola, per spostare senza aprire il foglio, l'app deve simulare un click. Al momento i browser bloccano la scrittura diretta senza 'Service Account'.")
                st.write("👉 **Soluzione rapida:** Clicca il link sotto per spostare il cliente istantaneamente tramite un modulo veloce.")
