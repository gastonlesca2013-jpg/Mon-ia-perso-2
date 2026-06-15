import streamlit as st
import google.generativeai as genai

# Configuration de la page : Titre et Émoji
st.set_page_config(page_title="Kalyx", page_icon="🧭", layout="centered")

# --- LE DESIGN CORRIGÉ, CLAIR ET ILLISIBLE-FREE ---
st.markdown("""
    <style>
    /* Importer une police moderne */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Appliquer la police partout */
    html, body, .stApp, p, span, div {
        font-family: 'Poppins', sans-serif !important;
        background-color: #0F1115 !important;
    }

    /* Style du Titre */
    h1 {
        color: #E6E8EA !important;
        font-weight: 300 !important;
        text-transform: lowercase;
        letter-spacing: 3px !important;
        font-size: 2.2rem !important;
        text-align: left;
    }

    /* --- CORRECTION DE LA SUPERPOSITION (Marge) --- */
    /* On force une marge à gauche pour tout le contenu du chat, pour qu'il soit APRÈS l'icône */
    [data-testid="stChatMessageContent"] {
        margin-left: 55px !important; /* L'espace crucial */
        padding: 5px !important;
    }

    /* --- STYLE DES BULLES DE CHAT (Uniquement le fond et les bords) --- */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border-radius: 0px !important;
        border: none !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }

    /* --- ÉCLAIRCISSEMENT ET CLARTÉ DU TEXTE --- */
    /* Utilisateur (Toi) : Police claire sur fond légèrement plus clair */
    [data-testid="stChatMessage"]:nth-child(even) p {
        color: #FFFFFF !important; /* Texte Blanc Pur pour toi */
        font-size: 15px !important;
        line-height: 1.5 !important;
    }

    /* Kalyx (Assistant) : Police très claire sur fond très sombre */
    [data-testid="stChatMessage"]:nth-child(odd) p {
        color: #D1D5DB !important; /* Texte Gris Très Clair (Blanc Cassé) pour Kalyx, hyper lisible */
        font-size: 15px !important;
        line-height: 1.5 !important;
    }

    /* Correction pour les sous-titres et listes de Kalyx (comme tes sites de casquettes) */
    h2, h3, li {
        color: #D1D5DB !important; /* Même couleur hyper claire */
    }

    /* Personnalisation de la barre d'entrée de texte */
    div[data-testid="stChatInput"] textarea {
        background-color: #1F232B !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #333C4E !important;
    }
    </style>
""", unsafe_allow_html=True)

# Affichage du titre
st.title("kalyx")

# Vérification de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante. Configure-la dans les paramètres de Streamlit.")
    st.stop()

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    # On ajoute des icônes de chat pour les différencier visuellement
    avatar = "https://raw.githubusercontent.com/streamlit/streamlit/main/assets/brand/streamlit-logo-avatar.png"
    if message["role"] == "user":
        avatar = "https://img.icons8.com/parakeet/48/face.png" # Icône visage clair
    else:
        avatar = "https://img.icons8.com/fluency/48/smart-toy.png" # Icône robot chic

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Zone d'écriture et réponse
if user_input := st.chat_input("Pose-moi une question..."):
    # Icônes pour le nouveau message
    user_avatar = "https://img.icons8.com/parakeet/48/face.png"
    bot_avatar = "https://img.icons8.com/fluency/48/smart-toy.png"

    # Message de l'utilisateur
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Réponse de l'assistant
    with st.chat_message("assistant", avatar=bot_avatar):
        try:
            # Modèle gemini-2.5-flash mis à jour pour corriger l'erreur de modèle
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
