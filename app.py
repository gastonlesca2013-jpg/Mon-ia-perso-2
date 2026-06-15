import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Kalyx",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS CORRECTIF POUR ENLEVER LE BLANC ET RENDRE TOUT VISIBLE ---
st.markdown("""
    <style>
    /* Fond principal style Gemini */
    .stApp {
        background: radial-gradient(circle at center, #13121d 0%, #08070c 100%) !important;
        color: #f0f4f9 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    
    /* CORRECTION DU BLOC BLANC EN BAS : On force le conteneur global du bas à être transparent */
    [data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    /* LA BARRE DE RECHERCHE EN NOIR CLAIR ET BIEN VISIBLE */
    [data-testid="stChatInput"] {
        border-radius: 32px !important;
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        padding: 6px !important;
    }
    
    /* Zone de texte à l'intérieur de la barre de recherche */
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: transparent !important;
        font-size: 16px !important;
    }
    
    /* Bouton d'envoi (la flèche) dans la barre de recherche */
    [data-testid="stChatInput"] button {
        background-color: #2f3032 !important;
        color: #ffffff !important;
        border-radius: 50% !important;
    }
    
    /* LISIBILITÉ DU TEXTE "RÉCENTS" EN JAUNE SUR TA PHOTO */
    [data-testid="stSidebar"] .stCaption {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-top: 25px !important;
        margin-bottom: 12px !important;
        opacity: 1 !important;
    }
    
    /* LISIBILITÉ DES LOGOS/ICÔNES EN HAUT À DROITE */
    header, [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    [data-testid="stHeader"] button, 
    [data-testid="stHeader"] a, 
    [data-testid="stHeader"] svg {
        color: #e3e3e3 !important;
        fill: #e3e3e3 !important;
    }
    
    /* Barre latérale gauche (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #2d2f31;
    }
    
    /* Boutons de navigation (Nouvelle discussion / Notebook) */
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
    
    /* Boutons de l'historique récent (juste un texte et un point blanc) */
    div.element-container:has(button[key^="chat_"]) button {
        background: none !important;
        border: none !important;
        color: #c4c7c5 !important;
        padding: 6px 10px !important;
        font-size: 15px !important;
        text-align: left !important;
        width: 100% !important;
        border-radius: 8px !important;
    }
    div.element-container:has(button[key^="chat_"]) button:hover {
        background-color: #2d2f31 !important;
        color: #ffffff !important;
    }
    
    /* Titre d'accueil au centre */
    .welcome-text {
        text-align: center;
        font-size: 44px;
        font-weight: 500;
        margin-top: 15vh;
        margin-bottom: 5vh;
        color: #ffffff;
    }
    
    /* Logo Kalyx */
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
    }
    </style>
""", unsafe_allow_html=True)

# --- ENREGISTREMENT DES SESSIONS ---
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Accueil"

if "chats_historique" not in st.session_state:
    st.session_state.chats_historique = {
        "achat casquettes": [
            {"role": "user", "content": "Je cherche des casquettes stylées"},
            {"role": "assistant", "content": "Salut ! Tu devrais regarder du côté des marques comme Stone Island ou C.P. Company."}
        ],
        "bonjour": [
            {"role": "user", "content": "bonjour comment va tu"},
            {"role": "assistant", "content": "Bonjour ! Je vais super bien, je suis Kalyx, ton assistante perso. Qu'est-ce qu'on crée aujourd'hui ? 🚀"}
        ]
    }

# --- MENU LATÉRAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">K</div>
            <div class="logo-text">Kalyx</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Nouvelle discussion", key="btn_new_chat"):
        st.session_state.current_chat = "Accueil"
        st.rerun()
        
    if st.button("📝 Nouveau notebook", key="btn_notebook"):
        st.session_state.current_chat = "Notebook"
        st.rerun()
        
    st.caption("Récents")
    
    for chat_title in st.session_state.chats_historique.keys():
        if st.button(f"•  {chat_title}", key=f"chat_{chat_title}"):
            st.session_state.current_chat = chat_title
            st.rerun()

# --- ZONE CENTRALE DE L'APPLICATION ---

if st.session_state.current_chat == "Accueil":
    st.markdown('<div class="welcome-text">De nouvelles idées à explorer ?</div>', unsafe_allow_html=True)
    
    # La barre de recherche s'affiche parfaitement ici, sans bloc blanc dessous
    user_input = st.chat_input("Demander à Kalyx...")
    if user_input:
        new_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        st.session_state.chats_historique[new_title] = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"Je te réponds tout de suite ! Tu as écrit : '{user_input}'."}
        ]
        st.session_state.current_chat = new_title
        st.rerun()

elif st.session_state.current_chat == "Notebook":
    st.title("🗒️ Mode Notebook")
    st.write("Espace de notes de ton application.")

else:
    st.markdown(f"### 💬 {st.session_state.current_chat}")
    st.write("---")
    
    for message in st.session_state.chats_historique[st.session_state.current_chat]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    next_input = st.chat_input("Répondre à Kalyx...")
    if next_input:
        st.session_state.chats_historique[st.session_state.current_chat].append(
            {"role": "user", "content": next_input}
        )
        st.session_state.chats_historique[st.session_state.current_chat].append(
            {"role": "assistant", "content": "Je suis là et je réponds au quart de tour ! Quel est ton projet ?"}
        )
        st.rerun()
