import streamlit as st
import pandas as pd
import time

# Configurazione Pagina
st.set_page_config(page_title="Agenda Nicola", layout="wide")

# 1. IL TUO LINK
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?usp=sharing"

# Trasformazione link per lettura
CSV_URL = URL_FOGLIO.replace('/edit?usp=sharing', '/export?format=csv')
CSV_URL = CSV_URL.replace('/edit', '/export?format=csv')
CSV_URL_FRESH = f"{CSV_URL}&cache_bust={int(time.time())}"

st.title("🚀 Agenda Nicola")

# --- TASTI DI CONTROLLO ---
col1, col2 = st.columns(2)

with col1:
    st.link_button("📝 APRI FOGLIO GOOGLE", URL_FOGLIO, use_container_width=True)

with col2:
    if st.button("🔄 AGGIORNA ELENCO", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- LOGICA DI VISUALIZZAZIONE ---
try:
    df = pd.read_csv(CSV_URL_FRESH)
    df.columns = df.columns.str.strip() # Pulizia nomi colonne

    # Funzione per vedere chi è stato visitato
    def is_visitato(riga):
        return str(riga['Stato']).strip().upper() == "X"

    # --- SEZIONE SPOSTAMENTO (SPIEGAZIONE) ---
    with st.expander("📅 GESTIONE FINE MESE"):
        st.write("Per spostare i visitati al mese successivo, segui questi passi nel Foglio Google:")
        st.info("1. Apri il Foglio Google.\n2. Filtra i clienti con la 'X'.\n3. Cambia la loro settimana in 'Sett 1'.\n4. Cancella la 'X' per ricominciare.")
        st.caption("Nota: Poiché l'app è in modalità consultazione, le modifiche massive vanno fatte direttamente sul foglio per massima sicurezza.")

    st.divider()

    # Selezione Settimana
    lista_settimane = sorted(df['Settimana'].unique()) if not df.empty else []
    settimana = st.selectbox("📅 Visualizza Settimana:", lista_settimane)
    
    # Filtro clienti
    clienti_filtrati = df[df['Settimana'] == settimana]
    
    if clienti_filtrati.empty:
        st.warning("Nessun cliente trovato per questa settimana.")
    else:
        for i, row in clienti_filtrati.iterrows():
            visitato = is_visitato(row)
            
            # Box colorato: Verde se visitato, Grigio se da fare
            with st.container(border=True):
                c1, c2 = st.columns([0.8, 0.2])
                with c1:
                    titolo = f"✅ {row['Cliente']}" if visitato else f"👤 {row['Cliente']}"
                    st.subheader(titolo)
                with c2:
                    if visitato:
                        st.write("🏆 FATTO")
                
                # Campagne
                campagne = []
                if str(row['Estivi']).strip().upper() in ["X", "TRUE"]: campagne.append("☀️ Estivi")
                if str(row['Lancio']).strip().upper() in ["X", "TRUE"]: campagne.append("🚀 Lancio")
                if str(row['Invernali']).strip().upper() in ["X", "TRUE"]: campagne.append("❄️ Invernali")
                
                if campagne:
                    st.write(" | ".join(campagne))

except Exception as e:
    st.error(f"Errore nel caricamento: {e}")
    st.info("Assicurati che il Foglio Google abbia le colonne corrette.")
