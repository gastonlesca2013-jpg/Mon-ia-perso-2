import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Kalyx",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS PERSONNALISÉ (STYLE GEMINI) ---
st.markdown("""
    <style>
    /* Fond principal sombre et dégradé subtil style Gemini */
    .stApp {
        background: radial-gradient(circle at center, #13121d 0%, #08070c 100%);
        color: #e3e3e3;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar (Barre latérale gauche) */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #2d2f31;
    }
    
    /* Boutons de la sidebar */
    .stButton > button {
        background-color: #282a2c;
        color: #e3e3e3;
        border: 1px solid #444746;
        border-radius: 20px;
        padding: 8px 20px;
        transition: all 0.3s ease;
        width: 100%;
        text-align: left;
    }
    .stButton > button:hover {
        background-color: #333537;
        border-color: #8e918f;
        color: #fff;
    }
    
    /* Liens / Boutons invisibles pour l'historique récent */
    .recent-link {
        display: block;
        padding: 8px 12px;
        color: #c4c7c5;
        text-decoration: none;
        border-radius: 8px;
        margin-bottom: 5px;
        font-size: 14px;
        transition: background 0.2s;
    }
    .recent-link:hover {
        background-color: #2d2f31;
        color: #fff;
    }
    
    /* Zone centrale d'accueil */
    .welcome-text {
        text-align: center;
        font-size: 40px;
        font-weight: 400;
        margin-top: 10vh;
        margin-bottom: 4vh;
        color: #e3e3e3;
    }
    
    /* Conteneur de la barre de recherche centrale style Gemini */
    .search-container {
        background-color: #1e1f20;
        border-radius: 30px;
        padding: 15px 25px;
        border: 1px solid #444746;
        max-width: 700px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* Logo Kalyx personnalisé */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 25px;
        padding-left: 10px;
    }
    .logo-icon {
        background: linear-gradient(135deg, #4285f4, #9b51e0);
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 10px rgba(155, 81, 224, 0.5);
    }
    .logo-text {
        font-size: 22px;
        font-weight: 600;
        color: #fff;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTION DE L'ÉTAT (NAVIGATION DES DISCUSSIONS) ---
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Accueil"

# Dictionnaire simulant le contenu de tes anciennes discussions
chats_historique = {
    "achat casquettes": "Voici l'historique de votre discussion concernant l'**achat de casquettes**...",
    "bonjour": "Voici l'historique de votre discussion de bienvenue (**bonjour**)..."
}

# --- BARRE LATÉRALE (SIDEBAR GAUCHE) ---
with st.sidebar:
    # Logo personnalisé Kalyx en haut à gauche
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">K</div>
            <div class="logo-text">Kalyx</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Boutons d'action principaux
    if st.button("➕ Nouvelle discussion"):
        st.session_state.current_chat = "Accueil"
        st.rerun()
        
    if st.button("📝 Nouveau notebook"):
        st.session_state.current_chat = "Notebook"
        st.rerun()
        
    st.write("")
    st.caption("Récents")
    
    # Section des éléments récents cliquables
    for chat_title in chats_historique.keys():
        if st.button(f"💬 {chat_title}", key=chat_title):
            st.session_state.current_chat = chat_title
            st.rerun()

# --- ZONE CENTRALE (CONTENU PRINCIPAL) ---

if st.session_state.current_chat == "Accueil":
    st.markdown('<div class="welcome-text">De nouvelles idées à explorer ?</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        user_input = st.chat_input("Demander à Kalyx...")
        if user_input:
            st.write(f"Vous avez dit : {user_input}")

elif st.session_state.current_chat == "Notebook":
    st.title("🗒️ Mode Notebook")
    st.write("Espace de travail et de note.")

else:
    st.title(f"💬 {st.session_state.current_chat}")
    st.write(chats_historique[st.session_state.current_chat])
    st.chat_input("Continuer la discussion...")
