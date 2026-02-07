import streamlit as st
import pandas as pd

# Configurazione Mobile
st.set_page_config(page_title="Agenda Nicola Cloud", layout="wide", initial_sidebar_state="collapsed")

# --- CONFIGURAZIONE ---
# Incolla qui il tuo link (assicurati che finisca con /edit...)
URL_FOGLIO = "IL_TUO_LINK_DEL_FOGLIO_GOOGLE"

# --- CONFIGURAZIONE ---
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Questa riga qui sotto lasciala esattamente così (con le virgolette e i punti)
CSV_URL = URL_FOGLIO.replace('/edit', '/export?format=csv')

def carica_dati():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return pd.DataFrame(columns=["Cliente", "Settimana", "Stato", "Estivi", "Lancio", "Invernali"])

# Caricamento
df = carica_dati()

# Configurazione Settimane
SETTIMANE_BASE = ["Sett 1", "Sett 2", "Sett 3", "Sett 4"]
COLONNE_CORRENTI = [f"Mese Corrente - {s}" for s in SETTIMANE_BASE]
COLONNE_PROSSIME = [f"Mese Prossimo - {s}" for s in SETTIMANE_BASE]

# --- SIDEBAR: ISTRUZIONI ---
with st.sidebar:
    st.header("⚙️ Istruzioni")
    st.write("Se l'app non salva, usa il link di Google Sheets per modificare i dati a mano.")
    st.link_button("Apri il Foglio Google", URL_FOGLIO)
    
    st.divider()
    st.header("📥 Caricamento")
    sett_scelta = st.selectbox("In quale settimana?", COLONNE_CORRENTI)
    nomi_in = st.text_area("Copia Nomi da Excel")
    
    if st.button("Aggiungi Clienti"):
        lista_n = [n.strip() for n in nomi_in.split('\n') if n.strip()]
        st.warning("⚠️ Per aggiungere nuovi clienti, incollali direttamente nel Foglio Google. Questa versione cloud è in sola lettura per sicurezza.")

# --- VISUALIZZAZIONE ---
def display_clienti(df_subset):
    if df_subset.empty:
        st.caption("Nessun cliente")
        return
    for index, row in df_subset.iterrows():
        with st.expander(f"👤 {row['Cliente']}"):
            st.write(f"Stato: **{row['Stato']}**")
            st.info(f"Campagne attive sul foglio: " + 
                    ("✅EST " if row['Estivi'] else "") + 
                    ("✅LANCIO " if row['Lancio'] else "") + 
                    ("✅INV" if row['Invernali'] else ""))

st.title("📑 Planner Nicola")
tab_corr, tab_pross = st.tabs(["🏙️ MESE CORRENTE", "📅 PROSSIMO MESE"])

with tab_corr:
    for i in range(4):
        st.info(f"**{SETTIMANE_BASE[i]}**")
        display_clienti(df[df['Settimana'] == COLONNE_CORRENTI[i]])

with tab_pross:
    for i in range(4):
        st.success(f"**{SETTIMANE_BASE[i]}**")
        display_clienti(df[df['Settimana'] == COLONNE_PROSSIME[i]])

