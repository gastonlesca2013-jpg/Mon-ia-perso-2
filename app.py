import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS PERSONNALISÉ CORRIGÉ ---
st.markdown("""
    <style>
    /* Fond principal sombre */
    .stApp { background-color: #1a1a1a; }
    
    /* Barre latérale sombre */
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Titre central - Positionnement vertical ajusté */
    .main-text { color: white; text-align: center; font-size: 32px; margin-top: 200px; }
    
    /* Barre de recherche centrée et proportionnelle */
    .stChatInput { 
        position: fixed; 
        bottom: 50px; 
        width: 60%; 
        left: 20%; 
        right: 20%;
        background-color: #262626 !important; 
        border-radius: 25px; 
    }
    
    /* Style du carré violet avec le K */
    .logo-box {
        background-color: #7b2cbf; 
        color: white; 
        width: 30px; 
        height: 30px; 
        display: inline-flex; 
        align-items: center; 
        justify-content: center; 
        border-radius: 5px; 
        margin-right: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Barre de gauche) ---
with st.sidebar:
    # Intégration du logo avec le K
    st.markdown("<div><span class='logo-box'>K</span> Kalyx</div>", unsafe_allow_html=True)
    st.write("") # Espace
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", type="secondary")
    st.button("• bonjour", type="secondary")

# --- CONTENU PRINCIPAL ---
# Titre (Le menu du haut a été supprimé comme demandé)
st.markdown("<div class='main-text'>De nouvelles idées à explorer ?</div>", unsafe_allow_html=True)

# Barre de recherche (Centrée via le CSS ci-dessus)
prompt = st.chat_input("Demander à Kalyx...")
