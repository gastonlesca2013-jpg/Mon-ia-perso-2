import streamlit as st
import google.generativeai as genai
import base64

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🤖", layout="wide")

# --- 1. CONFIGURATION IMAGE DE FOND ---
# Assurez-vous d'avoir un fichier nommé 'background.png' dans votre dossier
def set_bg_hack(main_bg):
    bin_str = base64.b64encode(open(main_bg, 'rb').read()).decode()
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Appliquer l'image (si le fichier background.png existe)
try:
    set_bg_hack('background.png')
except:
    pass # Si l'image n'est pas trouvée, le site reste fonctionnel

# --- 2. BARRE LATÉRALE GAUCHE (Vos outils) ---
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🖼️ Générer une Image", use_container_width=True):
        st.write("Génération en cours...")
    st.divider()
    search_query = st.text_input("🔍 Rechercher")

# --- 3. MISE EN PAGE (Colonnes) ---
# Nous créons une colonne centrale pour le Chat et une colonne à droite pour les news
col_chat, col_news = st.columns([3, 1])

# --- CORPS PRINCIPAL (Colonne Centrale) ---
with col_chat:
    st.title("🤖 Kalyx est prêt")
    
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                # Modèle confirmé comme étant disponible pour votre clé
                model = genai.GenerativeModel("models/gemini-2.5-flash")
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erreur technique : {e}")

# --- 4. BARRE À DROITE (News Polymarquette) ---
with col_news:
    st.markdown("### 📰 Polymarquette")
    st.markdown("*(Actualités en direct)*")
    st.write("• Paris : Match de foot à 20h")
    st.write("• Côte : Les cotes sont en hausse")
    st.write("• Info : Nouveau bonus disponible")
    # Vous pouvez ajouter ici autant de lignes que nécessaire
