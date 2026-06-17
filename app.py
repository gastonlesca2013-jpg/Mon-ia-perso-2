import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# CSS pour le fond d'écran et la mise en page
# Remplacez l'URL ci-dessous par celle de votre image
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"

st.markdown(f"""
    <style>
    .stApp {{
        background: url("{bg_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

# Initialisation des états
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_right_bar" not in st.session_state:
    st.session_state.show_right_bar = True

# --- BARRE LATÉRALE GAUCHE ---
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    search = st.text_input("🔍 Recherche")

# --- GESTION DE LA BARRE DROITE ---
if st.button("↔️ Toggle Barre Droite"):
    st.session_state.show_right_bar = not st.session_state.show_right_bar
    st.rerun()

# --- MISE EN PAGE ---
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

# --- CORPS PRINCIPAL (CHAT) ---
with col_main:
    st.title("🤖 Kalyx")
    
    # Configuration API
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
    else:
        st.error("Clé API manquante.")
        st.stop()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- BARRE DROITE (ACTUALITÉS) ---
if st.session_state.show_right_bar:
    with col_right:
        st.markdown("### 📰 Polymarquette")
        st.write("• Paris : Matchs en direct")
        st.write("• Cotes en hausse")
        st.write("• Bonus disponible")
