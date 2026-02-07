import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agenda Nicola", layout="wide")

# 1. IL TUO LINK (Mettilo tra le virgolette)
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Trasformazione per leggere i dati
import time # Aggiungi questa riga in alto insieme agli altri import

# Modifica la parte del link così:
CSV_URL = URL_FOGLIO.replace('/edit?usp=sharing', '/export?format=csv')
CSV_URL = CSV_URL.replace('/edit', '/export?format=csv')
# Questa riga dice a Google: "Dammi i dati freschi di adesso!"
CSV_URL = f"{CSV_URL}&cache_bust={int(time.time())}"

st.title("🚀 Agenda Nicola")

# Tasto gigante per scrivere (Apre direttamente l'app Fogli Google)
st.link_button("📝 APRI FOGLIO PER SEGNARE VISITE", URL_FOGLIO, use_container_width=True)

st.divider()

# Lettura dati
try:
    df = pd.read_csv(CSV_URL)
    
    # Filtro rapido per settimana
    settimana = st.selectbox("Seleziona Settimana", df['Settimana'].unique())
    
    # Mostra i clienti della settimana scelta
    clienti_filtrati = df[df['Settimana'] == settimana]
    
    for i, row in clienti_filtrati.iterrows():
        # Un box colorato per ogni cliente
        with st.container(border=True):
            st.subheader(f"👤 {row['Cliente']}")
            st.write(f"Stato: {row['Stato']}")
            # Qui vedi le spunte che hai messo sul foglio
            if row['Estivi'] == True or str(row['Estivi']).upper() == "TRUE":
                st.success("✅ CAMPAGNA ESTIVA")

except Exception as e:
    st.error("Caricamento in corso... Se non vedi i dati, assicurati di aver aggiunto almeno un cliente sul Foglio Google!")
    st.info("Assicurati che il foglio abbia queste colonne: Cliente, Settimana, Stato, Estivi, Lancio, Invernali")

