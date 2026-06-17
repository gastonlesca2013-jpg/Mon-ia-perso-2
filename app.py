import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "bg_url" not in st.session_state: st.session_state.bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True

# --- LOGOS ET CONFIG (REMPLACEZ CES LIENS) ---
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png" 

# --- CSS POUR FOND D'ÉCRAN ---
st.markdown(f"""
    <style>
    .stApp {{ background: url("{st.session_state.bg_url}"); background-size: cover; background-attachment: fixed; }}
    [data-testid="stSidebar"] {{ background-color: rgba(20, 20, 20, 0.9); }}
    </style>
""", unsafe_allow_html=True)

# --- PAGE DE CONNEXION ---
if not st.session_state.logged_in:
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.image(LOGO_URL, width=150)
    with col_r:
        st.title("Connexion Kalyx")
        email = st.text_input("Adresse Email")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            if email and pwd:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.image(LOGO_URL, width=50)
    st.title("Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.text_input("🔍 Rechercher...")
    st.divider()
    st.button("🖼️ Bibliothèque d'images")
    st.button("📊 Activité")
    st.button("⚙️ Paramètres")
    st.write("👤 Profil")
    if st.button("Afficher/Masquer Infos"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# --- LAYOUT PRINCIPAL ---
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([4, 1])
else:
    col_main = st.container()
    col_right = None

with col_main:
    st.header("Kalyx vous écoute")
    
    # API CONFIG
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro") # Modèle standard
    except:
        st.error("Erreur API : Vérifiez votre clé dans les secrets.")

    # Affichage messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input
    if prompt := st.chat_input("Votre message..."):
        if "boom" in prompt.lower():
            st.session_state.bg_url = "https://www.public.fr/styles/desktop/public/2023-04/jul.jpg"
            st.rerun()
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        try:
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("L'IA n'a pas pu répondre.")

# --- SIDEBAR DROITE ---
if col_right:
    with col_right:
        st.subheader("ℹ️ Infos")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Status : Actif")
        st.write("Discussions récentes :")
        st.write("- Projet Python")
