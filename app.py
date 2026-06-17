import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# CSS : Fond d'écran + Animation cercle (1mm) + Ajustement inputs
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"

st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    
    /* Animation du cercle (très petit) */
    .breathing-circle {{
        width: 6px; height: 6px;
        background-color: #00ffcc;
        border-radius: 50%;
        margin: 5px;
        animation: pulse 1.5s infinite ease-in-out;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.5; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion à Kalyx")
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")

# --- GESTION MISE EN PAGE ET BOUTON TOGGLE ---
# Si on veut la barre à droite
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]
    col_right = None

# --- CONTENU PRINCIPAL ---
with col_main:
    # Bouton pour gérer la barre (à droite)
    if not st.session_state.show_right_bar:
        if st.button("⬅️ Ouvrir Infos"):
            st.session_state.show_right_bar = True
            st.rerun()
    
    st.title("🤖 Kalyx")
    
    # Historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie (sans micro)
    user_input = st.chat_input("Posez votre question...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            # Animation cercle
            st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
            
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()

# --- BARRE DROITE (INFOS) ---
if col_right:
    with col_right:
        if st.button("➡️ Fermer Infos"):
            st.session_state.show_right_bar = False
            st.rerun()
        st.markdown("### 📅 Aujourd'hui")
        st.write(f"**Date :** {datetime.now().strftime('%d/%m/%Y')}")
        st.write(f"**Heure :** {datetime.now().strftime('%H:%M')}")
        st.info("Système Kalyx opérationnel.")
