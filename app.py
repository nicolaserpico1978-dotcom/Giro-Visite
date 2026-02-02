import streamlit as st
import pandas as pd
import os

# Configurazione Mobile-Friendly
st.set_page_config(page_title="Agenda Nicola", layout="wide", initial_sidebar_state="collapsed")

# --- CONFIGURAZIONE ---
DATA_FILE = "giro_mensile_ciclico.csv"
SETTIMANE_BASE = ["Sett 1", "Sett 2", "Sett 3", "Sett 4"]
COLONNE_CORRENTI = [f"Mese Corrente - {s}" for s in SETTIMANE_BASE]
COLONNE_PROSSIME = [f"Mese Prossimo - {s}" for s in SETTIMANE_BASE]

# Caricamento dati
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    # Verifichiamo che le colonne siano corrette
    for col in ["Estivi", "Lancio", "Invernali"]:
        if col not in df.columns: df[col] = False
else:
    df = pd.DataFrame(columns=["Cliente", "Settimana", "Stato", "Estivi", "Lancio", "Invernali"])

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
                    "Cliente": n, "Settimana": settlement_scelta, 
                    "Stato": "Da visitare", "Estivi": False, "Lancio": False, "Invernali": False
                })
            df = pd.concat([df, pd.DataFrame(nuovi)], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

# --- FUNZIONE VISUALIZZAZIONE ---
def display_clienti(df_subset, is_prossimo=False):
    if df_subset.empty:
        st.caption("Nessun cliente")
    for index, row in df_subset.iterrows():
        with st.expander(f"👤 {row['Cliente']}"):
            st.write("**Adesione Campagne:**")
            c1, c2, c3 = st.columns(3)
            
            # Qui abbiamo cambiato "LAN" in "LANCIO" per evitare l'errore di traduzione
            camp_est = c1.checkbox("ESTIVI", value=row['Estivi'], key=f"est_{index}_{is_prossimo}")
            camp_lan = c2.checkbox("LANCIO", value=row.get('Lancio', False), key=f"lan_{index}_{is_prossimo}")
            camp_inv = c3.checkbox("INVERNALI", value=row['Invernali'], key=f"inv_{index}_{is_prossimo}")
            
            if camp_est != row['Estivi'] or camp_lan != row.get('Lancio', False) or camp_inv != row['Invernali']:
                df.at[index, 'Estivi'] = camp_est
                df.at[index, 'Lancio'] = camp_lan
                df.at[index, 'Invernali'] = camp_inv
                df.to_csv(DATA_FILE, index=False)
                st.rerun()

            st.divider()
            if not is_prossimo:
                st.write("**Sposta in questo mese:**")
                sposta_ora = st.selectbox("Cambia in:", ["Scegli..."] + COLONNE_CORRENTI, key=f"now_{index}")
                if sposta_ora != "Scegli...":
                    df.at[index, 'Settimana'] = sposta_ora
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                st.divider()
                st.write("**Prossimo Mese:**")
                default_next = row['Settimana'].replace("Mese Corrente", "Mese Prossimo")
                scelta_next = st.selectbox("Invia a:", COLONNE_PROSSIME, 
                                          index=COLONNE_PROSSIME.index(default_next), key=f"next_{index}")
                if st.button(f"CONFERMA VISITA ✅", key=f"btn_{index}", use_container_width=True):
                    df.at[index, 'Settimana'] = scelta_next
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
            else:
                if st.button("⬅️ Riporta a Corrente", key=f"back_{index}", use_container_width=True):
                    df.at[index, 'Settimana'] = row['Settimana'].replace("Mese Prossimo", "Mese Corrente")
                    df.to_csv(DATA_FILE, index=False)
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
        df.to_csv(DATA_FILE, index=False)
        st.rerun()
    if st.button("🗑️ Svuota Tutto"):
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.rerun()