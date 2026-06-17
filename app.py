import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# URLs des fonds d'écran
bg_normal = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
# Image "caca" humoristique (remplacez par votre URL si vous en avez une)
bg_caca = "https://img.freepik.com/vecteurs-libre/motif-sans-couture-emoji-caca-mignon_1308-41006.jpg"

# Initialisation des états
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "normal"
if "visio_mode" not in st.session_state: st.session_state.visio_mode = False

# Sélection du fond d'écran
current_bg = bg_normal if st.session_state.bg_mode == "normal" else bg_caca

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
    
    st.divider()
    # Bouton Visio
    if st.button("🎥 Mode Visio"):
        st.session_state.visio_mode = not st.session_state.visio_mode
        st.rerun()
    
    st.divider()
    search = st.text_input("🔍 Recherche")

# Mise en page (Barre droite)
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

# Chat
with col_main:
    st.title("🤖 Kalyx")
    
    # Indicateur Visio
    if st.session_state.visio_mode:
        st.warning("Mode Visio activé : Parlez, je vous écoute.")

    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie + Micro (Alignement)
    c_mic, c_input = st.columns([0.1, 0.9])
    
    with c_mic:
        # Micro juste au-dessus de l'input pour simuler l'intégration
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic_in_bar')
    
    with c_input:
        user_input = st.chat_input("Posez votre question...")

    # Traitement de l'entrée (Micro ou Clavier)
    final_input = None
    if audio and "text" in audio:
        final_input = audio["text"]
    elif user_input:
        final_input = user_input

    if final_input:
        # Commande Chacha
        if "chacha" in final_input.lower():
            st.session_state.bg_mode = "caca" if st.session_state.bg_mode == "normal" else "normal"
            st.rerun()
        
        st.session_state.messages.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.markdown(final_input)
        
        with st.chat_message("assistant"):
            response = model.generate_content(final_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # En mode visio, on force la réponse (simulation simple)
            if st.session_state.visio_mode:
                st.success("Je vous écoute toujours, continuez...")

# Barre Droite
with col_right:
    if st.button("↔️ Afficher/Cacher"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()
    if st.session_state.show_right_bar:
        st.markdown("### ℹ️ Informations")
        st.write(f"• Visio : {'ON' if st.session_state.visio_mode else 'OFF'}")
        st.write("• Fond : " + st.session_state.bg_mode)
