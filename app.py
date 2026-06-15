import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="wide")

# --- DESIGN LUXE & INTERFACE COMPLÈTE GEMINI STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Fond général et police */
    html, body, .stApp, p, span, div, li {
        font-family: 'Inter', sans-serif !important;
        background-color: #131314 !important;
        color: #E3E3E3 !important;
    }

    /* --- ÉCLAIRCIR LES BOUTONS EN HAUT À DROITE --- */
    button[data-testid="baseButton-header"], .stActionButton, [data-testid="stHeader"] a, [data-testid="stHeader"] button {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Style du grand titre kalyx */
    h1 {
        color: #FFFFFF !important;
        font-weight: 400 !important;
        letter-spacing: 2px !important;
        font-size: 2.8rem !important;
        margin-bottom: 20px !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* --- EFFACER LES AVATARS MAUVAIS ET METTRE UN POINT ÉPURÉ --- */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #FFFFFF !important;
        border-radius: 50% !important;
        width: 12px !important;
        height: 12px !important;
        margin-top: 12px !important;
        border: 2px solid #FFFFFF !important;
    }
    /* Le point de Kalyx sera légèrement bleuté/lumineux */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #4285F4 !important;
        border-color: #4285F4 !important;
        box-shadow: 0 0 8px #4285F4;
    }

    /* Ajustement des textes du chat pour éviter les collisions */
    [data-testid="stChatMessageContent"] {
        margin-left: 20px !important;
        padding: 0px !important;
    }
    
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 15px 0px !important;
        border-bottom: 1px solid #202124 !important;
    }

    /* --- TEXTE DE RECHERCHE ULTRA LISIBLE --- */
    .stMarkdown p, li {
        color: #E3E3E3 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* --- BARRE DE RECHERCHE DU BAS FORMAT GEMINI --- */
    div[data-testid="stChatInput"] {
        padding: 0px !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #A8C7FA !important;
    }
    
    /* --- STYLE DE LA BARRE LATÉRALE GAUCHE --- */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #3C4043 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRE LATÉRALE GAUCHE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h3 style='color:white; font-weight:400;'>Kalyx Menu</h3>", unsafe_allow_html=True)
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📝 Nouveau notebook", use_container_width=True)
    
    st.markdown("<br><hr style='border-color:#3C4043;'><br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9AA0A6; font-size:14px;'>Récents</p>", unsafe_allow_html=True)
    
    # Simulation des recherches récentes
    st.caption("🔍 achat casquettes")
    st.caption("🔍 bonjour")

# --- ZONE PRINCIPALE ---
st.title("kalyx")

# Clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée de texte
if user_input := st.chat_input("Pose
