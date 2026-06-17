import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "chat"
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "is_pro" not in st.session_state: st.session_state.is_pro = False
if "chat_count" not in st.session_state: st.session_state.chat_count = 0
if "img_count" not in st.session_state: st.session_state.img_count = 0
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "default"

# URLS (Remplacez par vos images hébergées)
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# CSS
st.markdown("""
    <style>
    .stApp { background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e"); background-size: cover; }
    [data-testid="stSidebar"] { background-color: rgba(0,0,0,0.8) !important; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.logged_in:
    st.image(LOGO_URL, width=100)
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.image(LOGO_URL, width=50)
    st.markdown("### Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.page = "chat"
        st.rerun()
    if st.button("🎨 Générer une image"):
        st.session_state.page = "image_gen"
    if st.button("📊 Activité"):
        st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"):
        st.session_state.page = "settings"
    st.divider()
    if st.button("👁️ Infos (Basculer)"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# --- LAYOUT PRINCIPAL (HEADER + BODY) ---
# En-tête avec bouton Upgrade
col_h1, col_h2 = st.columns([3, 1])
with col_h2:
    if not st.session_state.is_pro:
        if st.button("🚀 Mettre à niveau (9,99€)"):
            st.session_state.is_pro = True
            st.success("Passage en mode Pro activé !")
            st.rerun()

# Gestion Sidebar Droite
if st.session_state.show_right_bar:
    main_col, right_col = st.columns([0.8, 0.2])
else:
    main_col = st.container()
    right_col = None

# --- LOGIQUE PAGES ---
with main_col:
    # 1. CHAT
    if st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        if not st.session_state.is_pro and st.session_state.chat_count >= 30:
            st.error("Limite de 30 questions atteinte. Passez en mode Pro.")
        else:
            if prompt := st.chat_input("Votre message..."):
                if "boom" in prompt.lower():
                    st.session_state.bg_mode = "on"
                st.session_state.chat_count += 1
                st.write(f"Réponse simulée (IA) - Question n°{st.session_state.chat_count}")

    # 2. IMAGE GEN
    elif st.session_state.page == "image_gen":
        st.header("Générateur d'images")
        if not st.session_state.is_pro and st.session_state.img_count >= 5:
            st.error("Limite de 5 images gratuite atteinte.")
        else:
            text = st.text_input("Description de l'image")
            if st.button("Générer"):
                st.session_state.img_count += 1
                st.image("https://via.placeholder.com/300?text=Image+Generée")

    # 3. ACTIVITÉ
    elif st.session_state.page == "activity":
        st.header("Rapports d'activité")
        st.write(f"Questions posées : {st.session_state.chat_count}")
        st.write(f"Images générées : {st.session_state.img_count}")

    # 4. PARAMÈTRES
    elif st.session_state.page == "settings":
        st.header("Paramètres du compte")
        st.write("Email: utilisateur@kalyx.com")
        st.write(f"Statut: {'Pro' if st.session_state.is_pro else 'Basique'}")

# --- SIDEBAR DROITE ---
if right_col:
    with right_col:
        st.markdown("### ℹ️ Infos")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
        st.write("Discussions : En cours")
