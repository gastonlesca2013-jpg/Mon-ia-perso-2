import streamlit as st
import google.generativeai as genai
import os

# Configuration de la page
st.set_page_config(page_title="Kalyx", layout="wide", page_icon="logo.png")

# --- INITIALISATION DES ÉTATS ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "page" not in st.session_state: st.session_state.page = "chat"

# --- CSS POUR LE PLEIN ÉCRAN ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e"); 
             background-size: cover; color: white; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    </style>
""", unsafe_allow_html=True)

# --- SYSTÈME DE CONNEXION ---
if not st.session_state.logged_in:
    st.image("logo.png", width=150) # Votre logo sur la page de connexion
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email and password: # Ajoutez ici votre logique de vérification
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        if os.path.exists("logo.png"): st.image("logo.png", width=40)
    with col2:
        st.markdown("### Kalyx")
    
    st.divider()
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🖼️ Bibliothèque d'images", use_container_width=True):
        st.session_state.page = "images"
    
    st.divider()
    st.button("📊 Activité", use_container_width=True)
    st.button("⚙️ Paramètres", use_container_width=True)
    st.write("👤 Profil: Connecté")
    
    if st.button("Toggle Infos (Droite)"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# --- LAYOUT PRINCIPAL (COLONNES) ---
if st.session_state.show_right_bar:
    main_col, right_col = st.columns([3, 1])
else:
    main_col = st.container()
    right_col = None

# --- CONTENU GAUCHE (CHAT) ---
with main_col:
    st.header("Kalyx vous écoute")
    
    # Configuration API
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

    if st.session_state.page == "chat":
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Dites quelque chose..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Erreur API : {e}")
    else:
        st.write("Section Bibliothèque d'images en cours de développement.")

# --- BARRE DROITE (INFO) ---
if right_col:
    with right_col:
        st.markdown("### ℹ️ Infos")
        st.write("Statut: En ligne")
        st.write("Date: 17/06/2026")
        st.info("Discussions récentes affichées ici.")
