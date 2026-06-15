import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# Injection de style CSS pour reproduire l'interface
st.markdown("""
    <style>
    /* Fond sombre global */
    .stApp { background-color: #1a1a1a; }
    
    /* Sidebar sombre */
    [data-testid="stSidebar"] { background-color: #121212 !important; }
    
    /* Zone de texte centrée */
    .main-title { color: white; text-align: center; margin-top: 150px; font-size: 40px; }
    
    /* Barre de saisie en bas */
    .stChatInput { position: fixed; bottom: 30px; width: 60%; margin-left: 20%; }
    </style>
""", unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.write("---")
    st.caption("Récents")
    st.text("• achat casquettes")
    st.text("• bonjour")

# Contenu principal
st.markdown("<div class='main-title'>De nouvelles idées à explorer ?</div>", unsafe_allow_html=True)

# Zone de saisie
prompt = st.chat_input("Demander à Kalyx...")
if prompt:
    st.write(f"Vous avez dit : {prompt}")
