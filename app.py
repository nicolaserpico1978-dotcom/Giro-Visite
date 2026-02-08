import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Agenda Nicola Pro", layout="wide")

# Connessione al foglio
conn = st.connection("gsheets", type=GSheetsConnection)

URL = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Lettura dati (ttl=0 forza l'aggiornamento ogni volta)
df = conn.read(spreadsheet=URL, ttl=0)

st.title("🚀 Agenda Nicola")

# Filtro Settimana
lista_sett = sorted(df['Settimana'].unique())
scelta = st.selectbox("📅 Seleziona Settimana", lista_sett)

clienti = df[df['Settimana'] == scelta]

for i, row in clienti.iterrows():
    with st.container(border=True):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.subheader(row['Cliente'])
            st.write(f"Stato: {row['Stato']}")
        with col2:
            if st.button("SPOSTA ✅", key=f"btn_{i}"):
                # Modifica la settimana: se è Sett 1 va a Sett 2, ecc.
                # Per ora facciamo che li rimette tutti in Sett 1 "nuova"
                df.at[i, 'Settimana'] = "Sett 1 (Mese Succ)"
                df.at[i, 'Stato'] = "" # Pulisce la X
                
                # Invia al foglio
                conn.update(spreadsheet=URL, data=df)
                st.success("Spostato!")
                st.rerun()

if st.button("🔄 REFRESH"):
    st.cache_data.clear()
    st.rerun()
