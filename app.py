import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS PERSONNALISÉ POUR LE DESIGN EXACT ---
st.markdown("""
    <style>
    /* Couleurs de fond */
    .stApp { background-color: #1a1a1a; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Titre central */
    .main-text { color: white; text-align: center; font-size: 32px; margin-top: 150px; }
    
    /* Barre de recherche (Input) */
    .stChatInput { 
        position: fixed; bottom: 50px; width: 60%; margin-left: 20%;
        background-color: #262626 !important; border-radius: 25px; 
    }
    
    /* Boutons sidebar */
    div.stButton > button { background-color: #262626; color: white; border: none; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Barre de gauche) ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray;'>Récents</p>", unsafe_allow_html=True)
    if st.button("• achat casquettes"):
        st.write("Chargement : achat casquettes...")
    if st.button("• bonjour"):
        st.write("Chargement : bonjour...")

# --- CONTENU PRINCIPAL ---
# Zone supérieure droite (Menu)
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 10])
with col5:
    st.markdown("Share &nbsp; ⭐ &nbsp; ✎ &nbsp; 🎧 &nbsp; ⋮")

# Titre
st.markdown("<div class='main-text'>De nouvelles idées à explorer ?</div>", unsafe_allow_html=True)

# Barre de recherche (Simulée via chat_input)
prompt = st.chat_input("Demander à Kalyx...")

# Note : Le "Flash" et le micro sont des éléments visuels natifs 
# de l'interface chat_input dans Streamlit.
