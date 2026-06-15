import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS CORRIGÉ ---
st.markdown("""
    <style>
    /* Fond principal */
    .stApp { background-color: #1a1a1a; }
    
    /* Barre latérale */
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* BLOQUER LE CHANGEMENT DE COULEUR AU SURVOL */
    div.stButton > button:hover {
        background-color: #262626 !important;
        border: none !important;
        color: white !important;
    }
    
    /* Boutons de la sidebar style gris fixe */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
    }

    /* BARRE DE SAISIE ADAPTATIVE */
    /* On utilise une marge gauche automatique pour qu'elle ne soit pas écrasée */
    .stChatInput { 
        position: fixed; 
        bottom: 50px; 
        width: 60%; 
        left: 20%; 
        right: 20%;
    }
    
    /* Ajustement spécifique pour que le texte soit centré dans la barre */
    [data-testid="stChatInput"] { background-color: #262626; border-radius: 25px; }

    .logo-box { background-color: #7b2cbf; color: white; width: 25px; height: 25px; display: inline-flex; align-items: center; justify-content: center; border-radius: 4px; margin-right: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div><span class='logo-box'>K</span> Kalyx</div>", unsafe_allow_html=True)
    st.write("")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU ---
st.markdown("<h2 style='color: white; text-align: center; margin-top: 200px;'>De nouvelles idées à explorer ?</h2>", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
