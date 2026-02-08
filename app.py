import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configurazione pagina
st.set_page_config(page_title="Agenda Nicola Pro", layout="wide")

# Connessione sicura tramite il Service Account (Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# Il link del tuo foglio
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Funzione per caricare i dati in tempo reale
def carica_dati():
    return conn.read(spreadsheet=URL_FOGLIO, ttl=0)

try:
    df = carica_dati()
    # Pulizia nomi colonne
    df.columns = df.columns.str.strip()

    st.title("🚀 Agenda Nicola Automatica")

    # Selezione Settimana
    lista_sett = sorted(df['Settimana'].unique())
    sett_scelta = st.selectbox("📅 Seleziona Settimana", lista_sett)

    clienti_sett = df[df['Settimana'] == sett_scelta]

    if clienti_sett.empty:
        st.info("Nessun cliente in questa settimana.")
    else:
        for i, row in clienti_sett.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([0.6, 0.4])
                
                with col1:
                    # Se lo stato è X, aggiunge una spunta verde
                    visita_fatta = str(row['Stato']).strip().upper() == "X"
                    titolo = f"✅ {row['Cliente']}" if visita_fatta else f"👤 {row['Cliente']}"
                    st.subheader(titolo)
                
                with col2:
                    # TASTO PER SPOSTARE AL MESE SUCCESSIVO
                    if st.button("SPOSTA PROSS. MESE", key=f"btn_{i}"):
                        with st.spinner("Spostamento in corso sul Foglio Google..."):
                            # 1. Modifica i dati nel dataframe
                            # Esempio: sposta alla settimana 1 e pulisce lo stato
                            df.at[i, 'Settimana'] = "Sett 1" 
                            df.at[i, 'Stato'] = "" 
                            
                            # 2. Invia tutto il pacchetto aggiornato al Foglio Google
                            conn.update(spreadsheet=URL_FOGLIO, data=df)
                            
                            st.success(f"{row['Cliente']} spostato!")
                            st.rerun()

    st.divider()
    if st.button("🔄 AGGIORNA ELENCO"):
        st.cache_data.clear()
        st.rerun()

except Exception as e:
    st.error("C'è un problema di connessione.")
    st.info("Verifica di aver condiviso il foglio con l'email del robot e che i Secrets siano corretti.")
    st.expander("Dettaglio errore per Nicola").write(e)
