import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configurazione per telefono
st.set_page_config(page_title="Agenda Nicola Cloud", layout="wide", initial_sidebar_state="collapsed")

# --- COLLEGAMENTO GOOGLE SHEETS ---
# Ricordati di sostituire l'URL tra le virgolette con quello del tuo foglio
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/1AHzXsASD1MCW9gI31y88pYbGF5ZRKiPyuVXYVFK-Uho/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

def carica_dati():
    # Legge i dati dal foglio in tempo reale
    return conn.read(spreadsheet=URL_FOGLIO, ttl=0)

def salva_dati(df_da_salvare):
    # Sovrascrive il foglio con le modifiche
    conn.update(spreadsheet=URL_FOGLIO, data=df_da_salvare)
    st.cache_data.clear()

# Caricamento iniziale
df = carica_dati()

# Configurazione Settimane
SETTIMANE_BASE = ["Sett 1", "Sett 2", "Sett 3", "Sett 4"]
COLONNE_CORRENTI = [f"Mese Corrente - {s}" for s in SETTIMANE_BASE]
COLONNE_PROSSIME = [f"Mese Prossimo - {s}" for s in SETTIMANE_BASE]

# --- SIDEBAR: INSERIMENTO ---
with st.sidebar:
    st.header("📥 Nuovo Caricamento")
    sett_scelta = st.selectbox("In quale settimana?", COLONNE_CORRENTI, key="sel_main")
    nomi_in = st.text_area("Copia Nomi da Excel", height=150)
    
    if st.button("Aggiungi Clienti", use_container_width=True):
        lista_n = [n.strip() for n in nomi_in.split('\n') if n.strip()]
        if lista_n:
            nuovi = []
            for n in lista_n:
                nuovi.append({
                    "Cliente": n, "Settimana": sett_scelta, 
                    "Stato": "Da visitare", "Estivi": False, "Lancio": False, "Invernali": False
                })
            df_aggiornato = pd.concat([df, pd.DataFrame(nuovi)], ignore_index=True)
            salva_dati(df_aggiornato)
            st.rerun()

# --- FUNZIONE VISUALIZZAZIONE ---
def display_clienti(df_subset, is_prossimo=False):
    if df_subset.empty:
        st.caption("Nessun cliente")
        return
    
    for index, row in df_subset.iterrows():
        with st.expander(f"👤 {row['Cliente']}"):
            st.write("**Adesione Campagne:**")
            c1, c2, c3 = st.columns(3)
            
            # Checkbox con salvataggio automatico al clic
            camp_est = c1.checkbox("ESTIVI", value=bool(row['Estivi']), key=f"est_{index}_{is_prossimo}")
            camp_lan = c2.checkbox("LANCIO", value=bool(row['Lancio']), key=f"lan_{index}_{is_prossimo}")
            camp_inv = c3.checkbox("INVERNALI", value=bool(row['Invernali']), key=f"inv_{index}_{is_prossimo}")
            
            if camp_est != row['Estivi'] or camp_lan != row['Lancio'] or camp_inv != row['Invernali']:
                df.at[index, 'Estivi'] = camp_est
                df.at[index, 'Lancio'] = camp_lan
                df.at[index, 'Invernali'] = camp_inv
                salva_dati(df)
                st.rerun()

            st.divider()
            if not is_prossimo:
                st.write("**Sposta settimana:**")
                sposta_ora = st.selectbox("Cambia in:", ["Scegli..."] + COLONNE_CORRENTI, key=f"now_{index}")
                if sposta_ora != "Scegli...":
                    df.at[index, 'Settimana'] = sposta_ora
                    salva_dati(df)
                    st.rerun()
                
                st.divider()
                st.write("**Mese Prossimo:**")
                default_next = row['Settimana'].replace("Mese Corrente", "Mese Prossimo")
                scelta_next = st.selectbox("Invia a:", COLONNE_PROSSIME, 
                                          index=COLONNE_PROSSIME.index(default_next), key=f"next_{index}")
                if st.button(f"CONFERMA VISITA ✅", key=f"btn_{index}", use_container_width=True):
                    df.at[index, 'Settimana'] = scelta_next
                    salva_dati(df)
                    st.rerun()
            else:
                if st.button("⬅️ Riporta a Corrente", key=f"back_{index}", use_container_width=True):
                    df.at[index, 'Settimana'] = row['Settimana'].replace("Mese Prossimo", "Mese Corrente")
                    salva_dati(df)
                    st.rerun()

# --- CORPO PRINCIPALE ---
st.title("📑 Planner Nicola")
tab_corr, tab_pross = st.tabs(["🏙️ MESE CORRENTE", "📅 PROSSIMO MESE"])

with tab_corr:
    for i in range(4):
        st.info(f"**{SETTIMANE_BASE[i]}**")
        display_clienti(df[df['Settimana'] == COLONNE_CORRENTI[i]])
        st.write("")

with tab_pross:
    for i in range(4):
        st.success(f"**{SETTIMANE_BASE[i]}**")
        display_clienti(df[df['Settimana'] == COLONNE_PROSSIME[i]], is_prossimo=True)
        st.write("")

# --- AZIONI SIDEBAR ---
with st.sidebar:
    st.divider()
    if st.button("🔄 INIZIA NUOVO MESE"):
        df['Settimana'] = df['Settimana'].str.replace("Mese Prossimo", "Mese Corrente")
        salva_dati(df)
        st.rerun()
    if st.button("🗑️ Svuota Tutto"):
        df_vuoto = pd.DataFrame(columns=["Cliente", "Settimana", "Stato", "Estivi", "Lancio", "Invernali"])
        salva_dati(df_vuoto)
        st.rerun()
