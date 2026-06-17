import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# URLs des fonds d'écran
bg_tropical = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
bg_skull = "https://images.unsplash.com/photo-1543852786-1cf66248998d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"

# Initialisation des états
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "tropical"

# Sélection du fond d'écran
current_bg = bg_tropical if st.session_state.bg_mode == "tropical" else bg_skull

st.markdown(f"""
    <style>
    .stApp {{ background: url("{current_bg}"); background-size: cover; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)

# Barre Latérale
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    
    # Recherche et Micro alignés
    c1, c2 = st.columns([0.8, 0.2])
    with c1:
        search = st.text_input("🔍 Recherche")
    with c2:
        st.write("###") # Espace pour aligner
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic')

# Toggle Barre Droite
if st.button("↔️ Afficher/Cacher Informations"):
    st.session_state.show_right_bar = not st.session_state.show_right_bar
    st.rerun()

# Mise en page
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

# Chat
with col_main:
    st.title("🤖 Kalyx")
    
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Récupération entrée (Clavier ou Micro)
    user_input = st.chat_input("Posez votre question...")
    if audio and "text" in audio:
        user_input = audio["text"]

    if user_input:
        # COMMANDE SECRÈTE "BOOM"
        if "boom" in user_input.lower():
            st.session_state.bg_mode = "skull" if st.session_state.bg_mode == "tropical" else "tropical"
            st.rerun()
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# Barre Droite
if st.session_state.show_right_bar:
    with col_right:
        st.markdown("### ℹ️ Informations")
        st.write("• Mode vocal : Actif")
        st.write("• Fond actuel : " + st.session_state.bg_mode)
