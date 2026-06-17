import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# CSS pour le fond d'écran
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)

# Initialisation
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True

# Sidebar (Gauche)
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    search = st.text_input("🔍 Recherche")

# Toggle Barre Droite
if st.button("↔️ Afficher/Cacher Informations"):
    st.session_state.show_right_bar = not st.session_state.show_right_bar
    st.rerun()

# Mise en page
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

# Chat (Centre)
with col_main:
    st.title("🤖 Kalyx")
    
    # Configuration API
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- LE DÉTAIL DU MICRO ---
    audio_value = mic_recorder(start_prompt="🎙️ Dicter", stop_prompt="⏹️ Arrêter", just_once=True, use_container_width=True)
    
    user_input = st.chat_input("Posez votre question...")
    
    # Si le micro a capté quelque chose, on l'utilise comme entrée
    if audio_value and "text" in audio_value:
        user_input = audio_value["text"]

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# Barre Droite (Informations)
if st.session_state.show_right_bar:
    with col_right:
        st.markdown("### ℹ️ Informations")
        st.write("• Système en ligne")
        st.write("• Mode vocal activé")
        st.write("• Prêt pour vos requêtes")
