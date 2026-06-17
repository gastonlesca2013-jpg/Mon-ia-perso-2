import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# CSS POUR FORCE LE TEXTE BLANC ET LE STYLE
st.markdown("""
    <style>
    .stApp { color: white !important; }
    div[data-testid="stMarkdownContainer"] p, h1, h2, h3, label { color: white !important; }
    .stTextInput label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
# Historique global des logs (pour l'admin)
if "user_logs" not in st.session_state: st.session_state.user_logs = []

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

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Kalyx vous écoute"): st.session_state.page = "chat"; st.rerun()
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    # Bouton Admin protégé
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"; st.rerun()
    
    st.divider()
    if st.button("Déconnexion"): 
        st.session_state.logged_in = False; st.rerun()

# --- PAGES ---
if st.session_state.page == "chat":
    st.header("Kalyx vous écoute")
    
    # Interface Chat
    if prompt := st.chat_input("Votre message pour Kalyx..."):
        # Enregistrer l'action pour l'admin
        st.session_state.user_logs.append(f"{st.session_state.user_email} a demandé: {prompt}")
        
        st.chat_message("user").markdown(prompt)
        
        # Réponse IA
        try:
            # Assure-toi que la clé API est dans les Secrets Streamlit
            model = genai.GenerativeModel("gemini-pro") 
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except Exception as e:
            st.error("Erreur de connexion à l'IA. Vérifiez votre clé API.")

elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
    st.header("👑 Panneau Admin")
    st.info("Interface de supervision")
    
    # 1. Voir qui est connecté et ce qu'ils font
    st.subheader("Journal d'activité des utilisateurs")
    if not st.session_state.user_logs:
        st.write("Aucune activité pour le moment.")
    else:
        for log in st.session_state.user_logs:
            st.text(f"• {log}")

elif st.session_state.page == "activity":
    st.header("📊 Activité")
    st.write(f"Utilisateur actuel : {st.session_state.user_email}")
    st.write("Tout fonctionne normalement.")

elif st.session_state.page == "settings":
    st.header("⚙️ Paramètres")
    st.write(f"Connecté avec : {st.session_state.user_email}")

else:
    st.write("Bienvenue sur Kalyx.")
