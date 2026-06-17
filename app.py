import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# CSS POUR L'INTERFACE (FOND, COULEURS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white !important; }
    h1, h2, h3, label { color: white !important; }
    .sidebar .sidebar-content { background-color: #1a1a1a !important; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DES VARIABLES ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "bg_url" not in st.session_state: st.session_state.bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
if "logs" not in st.session_state: st.session_state.logs = [] # Pour voir ce que font les gens

ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email == ADMIN_EMAIL and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        elif email and pwd:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# --- SIDEBAR (BARRE DE NAVIGATION) ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Kalyx vous écoute"): st.session_state.page = "chat"; st.rerun()
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"; st.rerun()
    
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT PRINCIPAL (COLONNES POUR LA BARRE DE TÂCHE) ---
main_col, side_col = st.columns([0.8, 0.2])

with side_col:
    st.markdown("### ℹ️ Infos Système")
    st.write(f"Utilisateur : {st.session_state.user_email}")
    st.write("Statut : Connecté")
    st.write("Barre de tâches active.")

with main_col:
    # --- PAGE CHAT ---
    if st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        prompt = st.chat_input("Dites quelque chose à Monia...")
        
        if prompt:
            # Enregistrement du log pour l'admin
            st.session_state.logs.append(f"{st.session_state.user_email} : {prompt}")
            
            # Commande BOOM
            if "boom" in prompt.lower():
                st.session_state.bg_url = "https://static.skyrock.fm/static/0.skyrock.fm/art/pic.99965315.2.jpg"
                st.rerun()
            
            st.chat_message("user").markdown(prompt)
            # Appel API (Vérifie bien tes secrets !)
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except:
                st.error("Monia ne répond pas. Vérifie ta clé API dans les secrets.")

    # --- PAGE GÉNÉRATEUR IMAGE ---
    elif st.session_state.page == "image":
        st.header("🎨 Générateur d'Image")
        img_prompt = st.text_input("Décris l'image que tu veux :")
        if st.button("Générer maintenant"):
            st.info(f"Génération de : {img_prompt}...")
            st.image("https://via.placeholder.com/600x300?text=Kalyx+IA+Generation")

    # --- PAGE ADMIN ---
    elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
        st.header("👑 Panneau Administration (Total)")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("👥 Utilisateurs connectés")
            st.write(f"1. {st.session_state.user_email} (Admin)")
            
        with col_b:
            st.subheader("📡 Actions Admin")
            if st.button("Supprimer les logs"): 
                st.session_state.logs = []
                st.rerun()

        st.subheader("📜 Historique détaillé des activités")
        for log in st.session_state.logs:
            st.text(f"Action : {log}")

    else:
        st.write("Bienvenue sur Kalyx.")

# --- CSS FINAL (FOND D'ÉCRAN) ---
st.markdown(f"""
    <style>
    .stApp {{ background: url("{st.session_state.bg_url}"); background-size: cover; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)
