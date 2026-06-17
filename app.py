import streamlit as st
import google.generativeai as genai
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Kalyx AI", page_icon="🌴", layout="wide")

# --- STYLE CSS PERSONNALISÉ (Fond d'écran et Barres) ---
# Note: Remplacez l'URL par celle de votre image si nécessaire
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Conteneur principal semi-transparent */
    .main-container {{
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        color: white;
    }}

    /* Personnalisation des textes pour la lisibilité sur fond clair/tropical */
    h1, h2, h3, p, span {{
        color: #1a1a1a !important;
        font-weight: 500;
    }}

    /* Masquer le menu Streamlit par défaut pour plus de pureté */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE L'IA ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash") # Ou gemini-2.5-flash selon votre accès
else:
    st.error("⚠️ Clé API manquante dans les secrets Streamlit !")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_right_bar" not in st.session_state:
    st.session_state.show_right_bar = True

# --- BARRE LATÉRALE GAUCHE (Native) ---
with st.sidebar:
    st.title("🌴 Menu Kalyx")
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    search = st.text_input("🔍 Rechercher")
    
    if st.button("🖼️ Générer Image", use_container_width=True):
        st.info("Fonctionnalité en cours d'intégration...")

# --- MISE EN PAGE PRINCIPALE (3 Colonnes pour simuler barre droite) ---
# col1: Espace chat | col2: Bouton Toggle | col3: Barre Droite Nouvelles
if st.session_state.show_right_bar:
    col_main, col_spacer, col_right = st.columns([3, 0.2, 1])
else:
    col_main, col_spacer, col_right = st.columns([10, 0.1, 0.5])

# --- LOGIQUE DU CHAT (Colonne Principale) ---
with col_main:
    st.title("🤖 Assistant Kalyx")
    
    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur
    if prompt := st.chat_input("Que puis-je faire pour vous ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- BARRE DROITE (Sortie/Entrée) ---
with col_right:
    # Bouton pour rentrer/sortir la barre
    label = "➡️ Fermer" if st.session_state.show_right_bar else "⬅️ Ouvrir"
    if st.button(label):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

    if st.session_state.show_right_bar:
        st.markdown("### 📰 Nouvelles")
        st.markdown("---")
        st.info("**Polymarquette**")
        st.write("• Paris : Matchs en direct")
        st.write("• Nouveau bonus disponible !")
        st.write("• Cotes boostées ce soir")

Votre projet **Kalyx** est maintenant complet ! N'oubliez pas d'héberger votre image sur un service comme Imgur si vous voulez un lien direct permanent. Je reste à votre disposition si vous souhaitez d'autres ajustements !
