import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")
DATA_FILE = "data.json"

# --- GESTION DE L'ÉTAT ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"
if "sidebar_state" not in st.session_state: st.session_state.sidebar_state = True

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Connexion à Kalyx</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Adresse Email")
        password = st.text_input("Mot de passe", type="password")
        if st.form_submit_button("Se connecter"):
            if email == "gastonlesca2013@gmail.com" and password == "Napoléon 2013 !":
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            elif email and password:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("Identifiants incorrects")
    st.stop()

# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    # Bouton Admin visible uniquement pour toi
    if st.session_state.email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    
    st.divider()
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# --- CSS & STYLE ---
st.markdown("""
<style>
.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }
</style>
""", unsafe_allow_html=True)

# --- CONTENU PRINCIPAL ---
# Layout avec sidebar rétractable à droite
col_main, col_right = st.columns([0.8, 0.2] if st.session_state.sidebar_state else [1, 0.01])

with col_right:
    if st.button("⬅️" if st.session_state.sidebar_state else "➡️"):
        st.session_state.sidebar_state = not st.session_state.sidebar_state
        st.rerun()
    if st.session_state.sidebar_state:
        st.write("### ☀️ Infos")
        st.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Aix-en-Provence : 25°C")

with col_main:
    # PAGE : CHAT
    if st.session_state.page == "Parler à Kalix":
        st.header("Parler à Kalix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            try:
                # Utilisation de la clé secrète
                api_key = st.secrets.get("GEMINI_API_KEY")
                if not api_key: st.error("Clé API manquante dans les Secrets !")
                else:
                    genai.configure(api_key=api_key)
                    # Utilisation d'un modèle plus courant
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Erreur IA : {str(e)}")

    # PAGE : ADMIN
    elif st.session_state.page == "admin" and st.session_state.email == "gastonlesca2013@gmail.com":
        st.header("👑 Panneau Admin")
        msg = st.text_input("Diffuser un message :")
        if st.button("Publier message"): st.success("Message diffusé !")
        st.file_uploader("Diffuser une image (simulation)")
        if st.button("Alerte Canicule"): st.warning("Alerte Canicule activée pour tous !")

    # AUTRES PAGES
    elif st.session_state.page == "image":
        st.header("Générer Image")
        query = st.text_input("Description :")
        if st.button("Générer"): st.image(f"https://image.pollinations.ai/prompt/{query}")
    elif st.session_state.page == "activity":
        st.header("Activité")
        st.write("Utilisateur : " + st.session_state.email)
    elif st.session_state.page == "settings":
        st.header("Paramètres")
        st.write("Configuration...")
