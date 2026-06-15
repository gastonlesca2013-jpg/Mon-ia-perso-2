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

    /* ÉCLAIRCIR ET FORCER LES BOUTONS DU HAUT (Partager, Étoile, paramètres) EN BLANC */
    header, [data-testid="stHeader"], [data-testid="baseButton-header"], .stActionButton, [data-testid="stHeader"] a, [data-testid="stHeader"] button, p[data-testid="stWidgetLabel"] {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    
    /* Forcer les icônes natives du header de Streamlit à devenir blanches et visibles */
    [data-testid="stHeader"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
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

    /* REMPLACER LES AVATARS PAR UN POINT LUMINEUX STYLE RECHAMP/SMART */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #FFFFFF !important;
        border-radius: 50% !important;
        width: 12px !important;
        height: 12px !important;
        margin-top: 14px !important;
        border: 2px solid #FFFFFF !important;
    }
    
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #A8C7FA !important;
        border-radius: 50% !important;
        width: 12px !important;
        height: 12px !important;
        margin-top: 14px !important;
        border: 2px solid #A8C7FA !important;
        box-shadow: 0 0 10px #A8C7FA;
    }

    /* Ajustement des textes du chat pour éviter les coupures */
    [data-testid="stChatMessageContent"] {
        margin-left: 20px !important;
        padding: 0px !important;
    }
    
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 15px 0px !important;
        border-bottom: 1px solid #202124 !important;
    }

    /* TEXTE DE RECHERCHE ULTRA LISIBLE */
    .stMarkdown p, li {
        color: #E3E3E3 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* BARRE DE RECHERCHE DU BAS FORMAT GEMINI TOTALEMENT VISIBLE */
    div[data-testid="stChatInput"] {
        padding: 0px !important;
        background-color: transparent !important;
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
    
    /* BARRE LATÉRALE GAUCHE (SIDEBAR) */
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
    
    # Historique de tes recherches récentes
    st.caption("🔍 achat casquettes")
    st.caption("🔍 bonjour")

# --- ZONE PRINCIPALE ---
st.title("kalyx")

# Vérification de la clé API
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

# Entrée de texte (Ici la ligne a été parfaitement réparée)
if user_input := st.chat_input("Pose-moi une question ou écris ici..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
