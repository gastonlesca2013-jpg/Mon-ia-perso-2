import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="centered")

# --- CSS POUR L'ANIMATION ET LA MISE EN PAGE ---
st.markdown("""
    <style>
    /* Suppression des marges inutiles */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Animation du cercle (10px = 1cm environ sur écran) */
    .breathing-circle {
        width: 10px; height: 10px;
        background-color: #00ffcc;
        border-radius: 50%;
        margin: 5px auto;
        animation: pulse 1.5s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(1); opacity: 0.5; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation
if "messages" not in st.session_state: st.session_state.messages = []

# --- SIDEBAR (BOUTONS) ---
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")

# --- CORPS DE L'APPLICATION ---
st.title("🤖 Kalyx")

# Affichage du chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BARRE DE SAISIE + MICRO INTÉGRÉ ---
# On utilise des colonnes pour aligner le micro et l'input
c_mic, c_input = st.columns([0.1, 0.9])

with c_mic:
    # Micro discret
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic', use_container_width=True)

with c_input:
    # Champ de saisie classique
    user_input = st.chat_input("Posez votre question...")

# Logique de réception du texte (Clavier ou Micro)
final_input = None
if audio_data and "text" in audio_data:
    final_input = audio_data["text"]
elif user_input:
    final_input = user_input

if final_input:
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.markdown(final_input)
    
    # Affichage de l'animation pendant la réflexion
    with st.chat_message("assistant"):
        # Le cercle qui pulse
        st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
        
        # Configuration API
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            response = model.generate_content(final_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun() # Pour rafraîchir et enlever le cercle
