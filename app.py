import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "all_chats" not in st.session_state: st.session_state.all_chats = {} # Stocke les messages par user
if "bg_url" not in st.session_state: st.session_state.bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"

ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email == ADMIN_EMAIL and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        elif email and pwd:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# --- CSS ET SIDEBAR ---
st.markdown(f"<style>.stApp {{ background: url('{st.session_state.bg_url}'); background-size: cover; }}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🤖 Kalyx")
    if st.button("💬 Monia / Chat"): st.session_state.page = "chat"; st.rerun()
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"; st.rerun()

# --- NAVIGATION ---
# Page Chat
if st.session_state.page == "chat":
    st.header("Discuter avec Monia")
    if prompt := st.chat_input("Dites quelque chose..."):
        # Enregistrement pour l'admin
        if st.session_state.user_email not in st.session_state.all_chats:
            st.session_state.all_chats[st.session_state.user_email] = []
        st.session_state.all_chats[st.session_state.user_email].append(f"{st.session_state.user_email}: {prompt}")
        
        if "boom" in prompt.lower():
            st.session_state.bg_url = "https://static.skyrock.fm/static/0.skyrock.fm/art/pic.99965315.2.jpg"
            st.rerun()
        st.success(f"Monia a reçu votre message : {prompt}")

# Page Image
elif st.session_state.page == "image":
    st.header("Générateur d'images")
    if st.text_input("Que voulez-vous générer ?"):
        if st.button("Valider"):
            st.image("https://via.placeholder.com/400?text=Votre+Image+Generee")

# Page Activité
elif st.session_state.page == "activity":
    st.header("📊 Activité")
    st.write(f"Nombre d'utilisateurs connectés : 1") # Simulation
    st.info("Tout fonctionne normalement.")

# Page Paramètres
elif st.session_state.page == "settings":
    st.header("⚙️ Paramètres du compte")
    st.write(f"Email : {st.session_state.user_email}")
    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# Page Admin
elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
    st.header("👑 Panneau Administration")
    st.write("--- Historique des discussions (Ce que les gens disent à Monia) ---")
    for user, msgs in st.session_state.all_chats.items():
        st.write(f"**{user} :**")
        for m in msgs: st.text(m)
