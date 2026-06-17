import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Kalyx AI", page_icon="🌴", layout="wide")

# --- INITIALISATION DES VARIABLES ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "normal"

# Liens des images
LOGO_URL = "https://storage.googleapis.com/generate-images-v1/image_collection/image_retrieval/1247963246369165313"
BG_TROPICAL = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1353&q=80"
BG_JUL = "https://static.skyrock.fm/static/0.skyrock.fm/art/pic.99965315.2.jpg" # Image de Jul

# --- 1. PORTAIL DE CONNEXION AVEC LOGO ---
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(LOGO_URL, width=80)
    with col2:
        st.title("Kalyx - Connexion")
    
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter / S'inscrire"):
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 2. STYLE ET FOND D'ÉCRAN ---
current_bg = BG_TROPICAL if st.session_state.bg_mode == "normal" else BG_JUL

st.markdown(f"""
    <style>
    .stApp {{ background: url("{current_bg}"); background-size: cover; background-attachment: fixed; }}
    
    /* Animation du cercle (1mm) */
    .breathing-circle {{
        width: 6px; height: 6px;
        background-color: #00ffcc;
        border-radius: 50%;
        margin: 5px;
        animation: pulse 1.5s infinite ease-in-out;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.5; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRE DE TÂCHE GAUCHE (Logo + Kalyx + Récent) ---
with st.sidebar:
    # Logo et Nom en haut à gauche
    col_l1, col_l2 = st.columns([1, 3])
    with col_l1:
        st.image(LOGO_URL, width=40)
    with col_l2:
        st.markdown("### Kalyx")
    
    st.divider()
    
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # SECTION RÉCENT (Historique)
    st.subheader("🕒 Récent")
    if not st.session_state.messages:
        st.write("Aucun historique")
    else:
        # Affiche les 5 dernières questions posées
        recent_queries = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        for q in recent_queries[-5:]:
            st.info(f"{q[:20]}...")

# --- 4. GESTION DES COLONNES ---
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]
    col_right = None

# --- 5. CONTENU PRINCIPAL (CHAT) ---
with col_main:
    st.title("🤖 Monia AI")
    
    # Correction erreur 404 : Utilisation de gemini-1.5-flash
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
    else:
        st.error("Clé API manquante dans les Secrets.")
        st.stop()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Posez votre question..."):
        # COMMANDE BOOM (Changement fond Jul)
        if "boom" in user_input.lower():
            st.session_state.bg_mode = "jul" if st.session_state.bg_mode == "normal" else "normal"
            st.rerun()

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
            try:
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- 6. BARRE DE TÂCHE DROITE (Infos) ---
if col_right:
    with col_right:
        if st.button("➡️ Fermer", use_container_width=True):
            st.session_state.show_right_bar = False
            st.rerun()
        st.markdown("### ℹ️ Infos")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Statut : Connecté")
else:
    # Bouton discret pour rouvrir si fermée
    if st.button("⬅️ Infos"):
        st.session_state.show_right_bar = True
        st.rerun()
