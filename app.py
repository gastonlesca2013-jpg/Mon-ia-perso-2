import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🤖", layout="wide")

# Initialisation de l'état de la session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# --- BARRE LATÉRALE (Toutes vos fonctionnalités) ---
with st.sidebar:
    st.title("Menu Kalyx")
    
    # 1. Nouvelle Discussion
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # 2. Générer Image (Bouton d'action)
    if st.button("🖼️ Générer une Image", use_container_width=True):
        st.write("Fonctionnalité en cours de développement...")
        # Note : Pour générer des images, il faudra connecter l'API Imagen
    
    st.divider()
    
    # 3. Recherche dans les discussions
    search_query = st.text_input("🔍 Rechercher dans l'historique")
    
    st.divider()
    
    # 4. Recherches récentes (Votre zone "jaune" déplacée ici pour rester fonctionnelle)
    st.subheader("Discussions récentes")
    if st.session_state.messages:
        # On affiche un résumé de la première phrase de la discussion
        preview = st.session_state.messages[0]["content"][:30] + "..."
        st.write(f"💬 {preview}")

# --- LOGIQUE DE RECHERCHE ---
# Si une recherche est tapée, on filtre les messages
if search_query:
    st.sidebar.write("Résultats de recherche :")
    for msg in st.session_state.messages:
        if search_query.lower() in msg["content"].lower():
            st.sidebar.markdown(f"- {msg['content'][:20]}...")

# --- CORPS PRINCIPAL ---
st.title("🤖 Kalyx")

# Configuration API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion du chat
if user_input := st.chat_input("Posez votre question..."):
    # Ajouter au chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Réponse IA
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur technique : {e}")
