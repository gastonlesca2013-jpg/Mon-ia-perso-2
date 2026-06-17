import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"
if "email" not in st.session_state: st.session_state.email = ""

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        st.session_state.logged_in = True
        st.session_state.email = email
        st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LOGIQUE ---
if st.session_state.page == "Parler à Kalix":
    st.header("Parler à Kalix")
    if prompt := st.chat_input("Votre message..."):
        st.chat_message("user").markdown(prompt)
        try:
            # On configure l'API
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # On utilise le modèle le plus basique possible
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except Exception as e:
            st.error(f"Erreur : {e}")

elif st.session_state.page == "admin":
    st.header("👑 Panneau Admin")
    st.write("Si l'IA ne marche pas, clique sur ce bouton pour voir les modèles disponibles :")
    if st.button("Voir les modèles autorisés"):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            for m in genai.list_models():
                st.write(f"Modèle trouvé : {m.name}")
        except Exception as e:
            st.error(f"Impossible de lister les modèles : {e}")

elif st.session_state.page == "image":
    st.header("Générateur d'image")
    query = st.text_input("Description :")
    if st.button("Générer"): st.image(f"https://image.pollinations.ai/prompt/{query}")
