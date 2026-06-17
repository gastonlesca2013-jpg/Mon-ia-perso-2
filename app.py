import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "tropical"

# Liens images (Remplacez par vos propres liens permanents)
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png" 
BG_TROPICAL = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
BG_JUL = "https://www.public.fr/styles/desktop/public/2023-04/jul.jpg"

# --- STYLE CSS ---
current_bg = BG_TROPICAL if st.session_state.bg_mode == "tropical" else BG_JUL

st.markdown(f"""
    <style>
    .stApp {{ background: url("{current_bg}"); background-size: cover; background-attachment: fixed; }}
    .breathing-circle {{ width: 6px; height: 6px; background-color: #00ffcc; border-radius: 50%; margin: 5px; animation: pulse 1.5s infinite; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.3); }} 100% {{ transform: scale(1); }} }}
    </style>
""", unsafe_allow_html=True)

# --- LOGIN (Sécurité) ---
if not st.session_state.logged_in:
    st.image(LOGO_URL, width=100)
    st.title("Connexion Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email and pwd: # Ajoutez ici votre logique de vérification
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR COMPLÈTE ---
with st.sidebar:
    st.image(LOGO_URL, width=40)
    st.title("Kalyx")
    
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    
    st.text_input("🔍 Rechercher...")
    
    st.subheader("Bibliothèque")
    st.button("🖼️ Mes Images")
    
    st.subheader("Récent")
    # Simulation d'historique
    st.write("Dernière discussion...")
    
    st.divider()
    st.subheader("Compte")
    st.button("📊 Activité")
    st.button("⚙️ Paramètres")
    st.write("👤 Profil Utilisateur")

# --- CHAT ET LOGIQUE ---
st.title("🤖 Monia IA")

# Configuration API
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Utilisation de gemini-1.5-flash (plus stable)
        model = genai.GenerativeModel("gemini-1.5-flash")
    else:
        st.error("Clé API introuvable.")
except Exception as e:
    st.error(f"Erreur init API: {e}")

# Affichage message
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Votre message..."):
    # Commande Boom
    if "boom" in prompt.lower():
        st.session_state.bg_mode = "jul" if st.session_state.bg_mode == "tropical" else "tropical"
        st.rerun()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Erreur de connexion avec l'IA. Vérifiez votre modèle.")
