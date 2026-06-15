import streamlit as st
import google.generativeai as genai

# Configuration de la page en mode large pour avoir de la place
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="wide")

# --- BARRE LATÉRALE GAUCHE (MENU) ---
with st.sidebar:
    st.markdown("### 💎 kalyx")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📝 Nouveau notebook", use_container_width=True)
    
    st.markdown("---")
    st.markdown("<p style='color:#9AA0A6; font-size:14px;'>Récents</p>", unsafe_allow_html=True)
    
    # Tes recherches récentes visibles à gauche
    st.markdown("🔍 achat casquettes")
    st.markdown("🔍 bonjour")

# --- ZONE PRINCIPALE ---
st.title("kalyx")

# Vérification de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante. Configure-la dans les secrets Streamlit.")
    st.stop()

# Gestion de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages avec des émojis officiels et propres
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="⚪"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(message["content"])

# Barre de recherche du bas
if user_input := st.chat_input("Pose-moi une question..."):
    # Message de l'utilisateur
    with st.chat_message("user", avatar="⚪"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Réponse de Kalyx
    with st.chat_message("assistant", avatar="✨"):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
