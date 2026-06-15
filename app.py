import streamlit as st
import google.generativeai as genai

# Configuration de la page en mode large
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="wide")

# --- INTERFACE ET STYLE GEMINI SOMBRE PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Fond ultra sombre général et police premium */
    html, body, .stApp, p, span, div, li {
        font-family: 'Inter', sans-serif !important;
        background-color: #131314 !important;
        color: #FFFFFF !important; /* Écriture blanche partout */
    }

    /* Style des textes du chat pour une lisibilité parfaite */
    .stMarkdown p, li {
        color: #FFFFFF !important; /* Blanc pur pour l'utilisateur et l'assistant */
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* --- EFFET BULLES ÉPURÉES COMME LA PHOTO --- */
    [data-testid="stChatMessage"] {
        background-color: #1E1F20 !important; /* Couleur de la bulle Gemini */
        border-radius: 18px !important;
        padding: 18px 24px !important;
        margin-bottom: 12px !important;
        border: none !important;
    }

    /* Barre latérale gauche style Gemini */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #2D2F31 !important;
    }

    /* Ajustement du titre principal */
    h1 {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 2.2rem !important;
    }

    /* Barre de recherche du bas */
    div[data-testid="stChatInput"] textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        padding: 14px 24px !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #A8C7FA !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuration de l'historique de session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- BARRE LATÉRALE GAUCHE (MENU) ---
with st.sidebar:
    # Marqué kalyx en haut à gauche
    st.markdown("<h2 style='color: white; font-weight: 500; margin-bottom: 25px;'>kalyx</h2>", unsafe_allow_html=True)
    
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.button("📝 Nouveau notebook", use_container_width=True)
    
    st.markdown("<br><hr style='border-color:#3C4043;'><br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9AA0A6; font-size:14px; font-weight:500;'>Récents</p>", unsafe_allow_html=True)
    
    # Boutons cliquables pour l'historique récent avec l'icône 💬 à la place des loupes
    if st.button("💬 achat casquettes", use_container_width=True, type="secondary"):
        st.session_state.messages = [
            {"role": "user", "content": "en me donnant plein d exemple de site pour acheter des casquette"},
            {"role": "assistant", "content": "Voici une liste très complète de sites : \n\n1. **New Era Cap** (newera.com)\n2. **47 Brand** (47brand.com)\n3. **Chapoteca**"}
        ]
        
    if st.button("💬 bonjour", use_container_width=True, type="secondary"):
        st.session_state.messages = [
            {"role": "user", "content": "bonjour"},
            {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}
        ]

# --- ZONE PRINCIPALE DE DISCUSSION ---
# Titre de la zone principale caché ou discret pour faire comme Gemini
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Vérification de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante. Configure-la dans les secrets de Streamlit.")
    st.stop()

# Affichage des messages sous forme de bulles Gemini
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="⚪"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(message["content"])

# Barre de recherche du bas pour envoyer un message
if user_input := st.chat_input("Pose-moi une question..."):
    with st.chat_message("user", avatar="⚪"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant", avatar="✨"):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
