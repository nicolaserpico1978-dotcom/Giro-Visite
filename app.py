import streamlit as st
import pandas as pd
import time

# Configurazione Pagina
st.set_page_config(page_title="Agenda Nicola", layout="wide")

# 1. IL TUO LINK
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Trasformazione link con "trucco" per forzare l'aggiornamento
CSV_URL = URL_FOGLIO.replace('/edit?usp=sharing', '/export?format=csv')
CSV_URL = CSV_URL.replace('/edit', '/export?format=csv')
CSV_URL = f"{CSV_URL}&cache_bust={int(time.time())}"

st.title("🚀 Agenda Nicola")

# Tasti di controllo
st.link_button("📝 APRI FOGLIO PER SEGNARE VISITE", URL_FOGLIO, use_container_width=True)

if st.button("🔄 AGGIORNA DATI", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.divider()

# Lettura dati
try:
    # Usiamo ttl=0 per dire a Streamlit di non tenere nulla in memoria troppo a lungo
    df = pd.read_csv(CSV_URL)
    
    # Pulizia nomi colonne (toglie spazi vuoti se presenti)
    df.columns = df.columns.str.strip()

    # Selezione Settimana
    lista_settimane = sorted(df['Settimana'].unique())
    settimana = st.selectbox("📅 Seleziona Settimana", lista_settimane)
    
    # Filtro
    clienti_filtrati = df[df['Settimana'] == settimana]
    
    for i, row in clienti_filtrati.iterrows():
        with st.container(border=True):
            # Se nel foglio metti una X o scrivi qualcosa in "Stato", lui lo mostra
            visita_fatta = str(row['Stato']).strip().upper() == "X"
            
            titolo = f"✅ {row['Cliente']}" if visita_fatta else f"👤 {row['Cliente']}"
            
            st.subheader(titolo)
            
            # Mostra le campagne se hanno una X o sono TRUE
            campagne = []
            if str(row['Estivi']).strip().upper() in ["X", "TRUE"]: campagne.append("☀️ Estivi")
            if str(row['Lancio']).strip().upper() in ["X", "TRUE"]: campagne.append("🚀 Lancio")
            if str(row['Invernali']).strip().upper() in ["X", "TRUE"]: campagne.append("❄️ Invernali")
            
            if campagne:
                st.write(" | ".join(campagne))
            else:
                st.caption("Nessuna campagna attiva")

except Exception as e:
    st.error("Caricamento in corso o Foglio non raggiungibile.")
    st.info("Controlla che il Foglio Google abbia le colonne: Cliente, Settimana, Stato, Estivi, Lancio, Invernali")
