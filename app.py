import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Kalyx",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS AVANCÉ (STYLE GEMINI & TEXTES LISIBLES) ---
st.markdown("""
    <style>
    /* Fond principal sombre et dégradé subtil style Gemini */
    .stApp {
        background: radial-gradient(circle at center, #18191b 0%, #0b0c0d 100%);
        color: #f0f4f9;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    
    /* Barre du haut Streamlit (Rendre les écritures comme "Share" blanches et lisibles) */
    header, [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: #ffffff !important;
    }
    header a, header button, header div {
        color: #ffffff !important;
    }
    
    /* Sidebar (Barre latérale gauche) */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #2d2f31;
    }
    
    /* Titre "Récents" bien blanc et visible */
    [data-testid="stSidebar"] .stCaption {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }
    
    /* Boutons principaux de la sidebar (Nouvelle discussion / Notebook) */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #131314;
        color: #e3e3e3;
        border: 1px solid #444746;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282a2c;
        border-color: #8e918f;
        color: #ffffff;
    }
    
    /* Style spécial pour les boutons de l'historique "Récents" (Juste un texte et un point blanc) */
    div.element-container:has(button[key^="chat_"]) button {
        background: none !important;
        border: none !important;
        color: #c4c7c5 !important;
        padding: 6px 10px !important;
        font-size: 14px !important;
        text-align: left !important;
        width: 100% !important;
        border-radius: 8px !important;
    }
    div.element-container:has(button[key^="chat_"]) button:hover {
        background-color: #2d2f31 !important;
        color: #ffffff !important;
    }
    
    /* Zone centrale d'accueil */
    .welcome-text {
        text-align: center;
        font-size: 44px;
        font-weight: 500;
        margin-top: 12vh;
        margin-bottom: 5vh;
        color: #f0f4f9;
        letter-spacing: -0.5px;
    }
    
    /* Logo Kalyx personnalisé avec des couleurs vives */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 30px;
        padding-left: 5px;
    }
    .logo-icon {
        background: linear-gradient(135deg, #1a73e8, #a142f4, #ea4335);
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 18px;
        box-shadow: 0 0 15px rgba(161, 66, 244, 0.6);
    }
    .logo-text {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    
    /* Fix pour la barre de recherche tout en bas (Style Gemini arrondi) */
    [data-testid="stChatInput"] {
        border-radius: 32px !important;
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES DE SESSION ---
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Accueil"

# Base de données de simulation des discussions (avec de vraies réponses de l'IA)
if "chats_historique" not in st.session_state:
    st.session_state.chats_historique = {
        "achat casquettes": [
            {"role": "user", "content": "Je cherche des casquettes stylées"},
            {"role": "assistant", "content": "Salut ! Tu devrais regarder du côté des marques comme Stone Island ou C.P. Company, leurs casquettes avec lunettes ou patchs intégrés sont super tendances en ce moment. Tu cherches un style plutôt techwear ou classique ?"}
        ],
        "bonjour": [
            {"role": "user", "content": "bonjour comment va tu"},
            {"role": "assistant", "content": "Bonjour ! Je vais super bien, merci. Je suis Kalyx, ton assistante perso. Qu'est-ce qu'on crée de beau aujourd'hui ? 🚀"}
        ]
    }

# --- BARRE LATÉRALE (SIDEBAR GAUCHE) ---
with st.sidebar:
    # Logo Kalyx en haut à gauche
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">K</div>
            <div class="logo-text">Kalyx</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Boutons d'action principaux
    if st.button("➕ Nouvelle discussion", key="btn_new_chat"):
        st.session_state.current_chat = "Accueil"
        st.rerun()
        
    if st.button("📝 Nouveau notebook", key="btn_notebook"):
        st.session_state.current_chat = "Notebook"
        st.rerun()
        
    st.caption("Récents")
    
    # Section Récents avec un point blanc (•) à la place des bulles grises
    for chat_title in st.session_state.chats_historique.keys():
        if st.button(f"•  {chat_title}", key=f"chat_{chat_title}"):
            st.session_state.current_chat = chat_title
            st.rerun()

# --- ZONE CENTRALE (CONTENU PRINCIPAL) ---

if st.session_state.current_chat == "Accueil":
    # Écran d'accueil style Gemini
    st.markdown('<div class="welcome-text">De nouvelles idées à explorer ?</div>', unsafe_allow_html=True)
    
    # Barre de recherche centrale
    user_input = st.chat_input("Demander à Kalyx...")
    if user_input:
        # Créer dynamiquement une nouvelle discussion basée sur la question
        new_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        st.session_state.chats_historique[new_title] = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"Je reçois bien ton message ! Tu as dit : '{user_input}'. Dis-moi comment je peux t'aider plus précisément ! ✨"}
        ]
        st.session_state.current_chat = new_title
        st.rerun()

elif st.session_state.current_chat == "Notebook":
    st.title("🗒️ Mode Notebook")
    st.write("Espace de travail et de notes de Kalyx.")

else:
    # FIL DE DISCUSSION ACTIF (Quand on clique sur un truc Récent)
    st.markdown(f"### 💬 {st.session_state.current_chat}")
    st.write("---")
    
    # Affichage des messages avec les vraies bulles de chat Streamlit (très proches de Gemini)
    for message in st.session_state.chats_historique[st.session_state.current_chat]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Barre pour continuer à répondre en bas
    next_input = st.chat_input("Répondre à Kalyx...")
    if next_input:
        # On ajoute la question de l'utilisateur
        st.session_state.chats_historique[st.session_state.current_chat].append(
            {"role": "user", "content": next_input}
        )
        # Réponse instantanée automatique
        st.session_state.chats_historique[st.session_state.current_chat].append(
            {"role": "assistant", "content": "Je suis là et je te réponds instantanément ! Que veux-tu savoir de plus ?"}
        )
        st.rerun()
