import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Agenda Nicola Pro", layout="wide")

# Connessione al foglio usando i Secrets che hai appena salvato
conn = st.connection("gsheets", type=GSheetsConnection)

# Funzione per leggere i dati
def carica_dati():
    return conn.read(spreadsheet="INCOLLA_IL_TUO_URL_FOGLIO_QUI", ttl=0)

df = carica_dati()

st.title("🚀 Agenda Nicola Automatica")

# Selezione Settimana
lista_sett = sorted(df['Settimana'].unique())
sett_scelta = st.selectbox("📅 Scegli Settimana", lista_sett)

clienti_sett = df[df['Settimana'] == sett_scelta]

for i, row in clienti_sett.iterrows():
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            st.subheader(f"👤 {row['Cliente']}")
            st.caption(f"Stato attuale: {row['Stato']}")
            
        with col2:
            # TASTO MAGICO: Quando lo premi, l'app scrive sul foglio!
            if st.button("SPOSTA ✅", key=f"btn_{i}"):
                # Modifichiamo il foglio: cambiamo la settimana e puliamo lo stato
                df.at[i, 'Settimana'] = "Mese Prossimo - Sett 1"
                df.at[i, 'Stato'] = "Da visitare" 
                
                # Salvataggio automatico sul Foglio Google
                conn.update(spreadsheet="INCOLLA_IL_TUO_URL_FOGLIO_QUI", data=df)
                
                st.success("Spostato!")
                st.rerun()

if st.button("🔄 AGGIORNA TUTTO"):
    st.cache_data.clear()
    st.rerun()
