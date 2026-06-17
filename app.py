import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# CSS PERSONNALISÉ
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white !important; }
    h1, h2, h3, label, p { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
# Variables globales partagées pour l'Admin
if "broadcast_msg" not in st.session_state: st.session_state.broadcast_msg = None
if "forced_image" not in st.session_state: st.session_state.forced_image = None
if "active_users" not in st.session_state: st.session_state.active_users = []

ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            if email not in st.session_state.active_users: st.session_state.active_users.append(email)
            st.rerun()
    st.stop()

# --- SIDEBAR (NAVIGATION) ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Kalyx vous écoute"): st.session_state.page = "chat"; st.rerun()
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"; st.rerun()
    
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- AFFICHAGE DES FORÇAGES ADMIN (Images/Messages) ---
if st.session_state.broadcast_msg:
    st.warning(f"📢 MESSAGE DE L'ADMIN : {st.session_state.broadcast_msg}")
if st.session_state.forced_image:
    st.image(st.session_state.forced_image, caption="Message urgent de l'Admin")

# --- PAGES ---
# Page CHAT
if st.session_state.page == "chat":
    st.header("Kalyx vous écoute")
    if prompt := st.chat_input("Votre message pour Monia..."):
        st.chat_message("user").markdown(prompt)
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except: st.error("Monia ne répond pas. Vérifiez la clé API.")

# Page ADMIN
elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
    st.header("👑 Panneau Administration")
    
    # 1. Suppression utilisateurs
    if st.button("🗑️ Effacer tous les comptes connectés"):
        st.session_state.active_users = []
        st.success("Comptes réinitialisés.")
    
    # 2. Message Broadcast
    msg = st.text_input("Message à diffuser à tous :")
    if st.button("Envoyer le message à tous"):
        st.session_state.broadcast_msg = msg
        st.rerun()
        
    # 3. Image Canicule
    if st.button("🔥 Activer ALERTE CANICULE"):
        st.session_state.forced_image = "https://images.unsplash.com/photo-1530521954074-e64f6810b32d"
        st.rerun()
        
    # 4. Upload Image Perso
    uploaded_file = st.file_uploader("Envoyer une image pour tout le monde :", type=["jpg", "png"])
    if uploaded_file is not None:
        if st.button("Diffuser mon image"):
            st.session_state.forced_image = uploaded_file
            st.rerun()

    # 5. Reset affichage
    if st.button("Réinitialiser l'écran des utilisateurs"):
        st.session_state.broadcast_msg = None
        st.session_state.forced_image = None
        st.rerun()

# Autres pages (Image, Activité, Paramètres)
elif st.session_state.page == "image":
    st.header("Générateur d'image")
    query = st.text_input("Que voulez-vous générer ?")
    if st.button("Rechercher"):
        st.image(f"https://image.pollinations.ai/prompt/{query}")

elif st.session_state.page == "activity":
    st.header("Activité")
    st.write(f"Nombre de connexions aujourd'hui : {len(st.session_state.active_users)}")

elif st.session_state.page == "settings":
    st.header("Paramètres")
    st.write(f"Email : {st.session_state.user_email}")
    st.write("Mot de passe : ************")
