import streamlit as st
import google.generativeai as genai

# Configuration de la page avec un émoji diamant chic
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="centered")

# --- DESIGN GLOBAL ET POLICES D'ÉCRITURE ---
st.markdown("""
    <style>
    /* Importer une police ultra moderne et haut de gamme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* Appliquer la police partout sur le site */
    html, body, [class*="css"], .stMarkdown, p, span {
        font-family: 'Inter', sans-serif !important;
    }

    /* Fond de l'application (Noir très chic, pas totalement sombre) */
    .stApp {
        background-color: #0B0C10 !important;
    }

    /* Style du titre "kalyx" en lettres épurées blanches */
    h1 {
        color: #FFFFFF !important;
        font-weight: 300 !important;
        letter-spacing: 4px !important;
        text-transform: lowercase;
        font-size: 2.5rem !important;
        margin-bottom: 30px !important;
    }

    /* --- COULEUR ET STYLE DES BULLES DE DISCUSSION --- */
    
    /* La bulle de l'utilisateur (Toi) : Fond gris foncé texturé, écriture blanche */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #1F2833 !important;
        border-radius: 15px !important;
        color: #FFFFFF !important;
        border: 1px solid #2C3540 !important;
    }

    /* La bulle de l'assistant (Kalyx) : Fond noir bleuté, écriture blanc cassé très lisible */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #15161B !important;
        border-radius: 15px !important;
        color: #E5E7EB !important;
        border: 1px solid #22232A !important;
    }

    /* Modifier la couleur du texte à l'intérieur des bulles pour qu'il ressorte parfaitement */
    .stMarkdown p {
        color: #F3F4F6 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* Personnalisation de la barre d'écriture tout en bas */
    div[data-testid="stChatInput"] textarea {
        background-color: #1F2833 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #45A29E !important;
    }
    </style>
""", unsafe_allow_html=True)

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
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone d'écriture et réponse
if user_input := st.chat_input("Écris ton message pour Kalyx..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            # Modèle 2.5 stable mis à jour
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
        
