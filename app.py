import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UNIFORMISER LE NOIR/GRIS SOMBRE ---
st.markdown("""
    <style>
    /* Fond global */
    .stApp { background-color: #1a1a1a !important; }
    
    /* Suppression des zones blanches */
    header { background-color: #1a1a1a !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Sidebar : Suppression de l'effet de survol (hover) */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
    }
    
    /* Boutons : Couleur fixe sans changement au survol */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
        transition: none !important;
    }
    div.stButton > button:hover {
        background-color: #262626 !important;
        border: none !important;
        color: white !important;
    }
    
    /* CORRECTION DE LA BARRE DE SAISIE : Force le fond sombre */
    /* On cible le conteneur du chat pour le rendre noir */
    .stChatInputContainer { 
        background-color: #1a1a1a !important; 
        border: none !important;
    }
    
    /* On cible l'input lui-même */
    [data-testid="stChatInput"] { 
        background-color: #262626 !important;
        border: 1px solid #444 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU PRINCIPAL ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
        <h2 style='color: white;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# --- SAISIE ---
# Remarque : si le chat_input continue d'afficher du blanc, 
# c'est une limitation native de Streamlit. 
# Le CSS ci-dessus est la méthode la plus agressive pour le masquer.
prompt = st.chat_input("Demander à Kalyx...")
