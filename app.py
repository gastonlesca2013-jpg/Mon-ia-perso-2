import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from datetime import datetime

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# CSS pour le fond d'écran et l'animation "cercle" (1mm = ~5px)
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"

st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    
    /* Animation du cercle (très petit, ~1mm) */
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

# --- SIDEBAR GAUCHE (MENU) ---
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    st.divider()
    if st.button("↔️ Toggle Infos"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# --- MISE EN PAGE PRINCIPALE ---
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]
    col_right = None

# --- CONTENU ---
with col_main:
    st.title("🤖 Kalyx")
    
    # Historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie + Micro
    c_mic, c_input = st.columns([0.1, 0.9])
    with c_mic:
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic')
    with c_input:
        user_input = st.chat_input("Posez votre question...")

    # Traitement
    final_input = audio["text"] if audio and "text" in audio else user_input
    
    if final_input:
        st.session_state.messages.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.markdown(final_input)
        
        with st.chat_message("assistant"):
            # Animation cercle
            st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
            
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(final_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()

# --- BARRE DROITE (INFOS) ---
if col_right:
    with col_right:
        st.markdown("### 📅 Aujourd'hui")
        st.write(f"**Date :** {datetime.now().strftime('%d/%m/%Y')}")
        st.write(f"**Heure :** {datetime.now().strftime('%H:%M')}")
        st.info("Système Kalyx opérationnel.")
