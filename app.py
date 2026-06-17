import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
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

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion à Kalyx")
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email: 
            st.session_state.email = email
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("➕ Nouvelle discussion"): st.session_state.messages = []
    page = st.radio("Navigation", ["Parler à Monia", "Panneau Admin"])
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT DROITE ---
col_main, col_right = st.columns([0.8, 0.2])
with col_right:
    if st.button("↔️ Rétracter/Afficher"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Infos")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Météo : 28°C")

# --- LOGIQUE PRINCIPALE ---
with col_main:
    st.markdown("""<style>.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }</style>""", unsafe_allow_html=True)
    
    data = load_data()
    if data.get("canicule"): st.error("🔥 ALERTE CANICULE EN COURS")
    if data.get("broadcast"): st.info(f"📢 Admin : {data['broadcast']}")
    
    # Correction de l'erreur MediaFileStorageError
    img_url = data.get("img_url")
    if img_url and img_url.startswith("http"): 
        st.image(img_url)

    if page == "Parler à Monia":
        st.header("Discuter avec Monia")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Votre message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)
            
            try:
                # Vérification présence clé
                if "GEMINI_API_KEY" not in st.secrets:
                    st.error("ERREUR : GEMINI_API_KEY manquante dans les Secrets.")
                else:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Erreur IA : {str(e)}")

    elif page == "Panneau Admin" and st.session_state.email == "gastonlesca2013@gmail.com":
        st.header("👑 Panneau Admin")
        msg = st.text_input("Message à diffuser")
        url = st.text_input("URL Image")
        if st.button("Diffuser"): data["broadcast"] = msg; data["img_url"] = url; save_data(data)
        if st.button("Activer Canicule"): data["canicule"] = True; save_data(data)
        if st.button("Réinitialiser"): save_data({"broadcast": "", "canicule": False, "img_url": ""})
