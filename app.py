import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Kalyx", layout="wide")
DATA_FILE = "app_state.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"broadcast": "", "canicule": False, "img_url": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- SESSIONS ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "right_bar" not in st.session_state: st.session_state.right_bar = True
if "messages" not in st.session_state: st.session_state.messages = []

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if email == "gastonlesca2013@gmail.com": 
            st.session_state.email = email
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE (Navigation) ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("➕ Nouvelle discussion"): st.session_state.messages = []
    st.divider()
    page = st.radio("Menu", ["Parler à Monia", "Panneau Admin"])
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT (Principal + Barre Droite) ---
col_main, col_right = st.columns([0.8 if st.session_state.right_bar else 1.0, 0.2 if st.session_state.right_bar else 0.05])

# Barre Droite (Infos)
with col_right:
    if st.button("↔️"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Infos")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Météo : 28°C")

# --- LOGIQUE PRINCIPALE ---
with col_main:
    st.markdown("""<style>.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }</style>""", unsafe_allow_html=True)
    
    data = load_data()
    if data["canicule"]: st.error("🔥 ALERTE CANICULE")
    if data["broadcast"]: st.info(f"📢 Admin : {data['broadcast']}")
    if data["img_url"]: st.image(data["img_url"])

    if page == "Parler à Monia":
        st.header("Discuter avec Monia")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)
            
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                # "Monia" est définie ici via instruction système
                model = genai.GenerativeModel('gemini-pro', system_instruction="Tu t'appelles Monia. Tu es une IA amicale et serviable.")
                response = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Erreur connexion : {e}")

    elif page == "Panneau Admin" and st.session_state.email == "gastonlesca2013@gmail.com":
        st.header("👑 Panneau Admin")
        msg = st.text_input("Message général")
        url = st.text_input("URL Image")
        if st.button("Diffuser"): data["broadcast"] = msg; data["img_url"] = url; save_data(data)
        if st.button("Activer Canicule"): data["canicule"] = True; save_data(data)
        if st.button("Réinitialiser"): save_data({"broadcast": "", "canicule": False, "img_url": ""})
