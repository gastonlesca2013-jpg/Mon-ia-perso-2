import streamlit as st
import google.generativeai as genai
import os
import json

st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if email == "gastonlesca2013@gmail.com" and password == "Napoléon 2013 !":
            st.session_state.logged_in = True
            st.session_state.admin = True
            st.rerun()
        elif email and password:
            st.session_state.logged_in = True
            st.session_state.admin = False
            st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.session_state.admin:
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    if st.button("🚪 Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LOGIQUE CHAT ---
if st.session_state.page == "Parler à Kalix":
    st.header("Parler à Kalix")
    if prompt := st.chat_input("Message..."):
        st.chat_message("user").markdown(prompt)
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # UTILISATION DE GEMINI-PRO (Le plus standard)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except Exception as e:
            st.error(f"Erreur technique : {e}")

# --- PANNEAU ADMIN DEBUG ---
elif st.session_state.page == "admin" and st.session_state.admin:
    st.header("👑 Panneau Admin")
    if st.button("Lister les modèles disponibles"):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            models = genai.list_models()
            for m in models:
                st.write(f"Modèle : {m.name}")
        except Exception as e:
            st.error(f"Erreur : {e}")
