import streamlit as str
import google.generativeai as genai

# 1. Configuration de la page
str.set_page_config(page_title="Mon IA Perso", page_icon="🤖")
str.title("🤖 Mon IA Super Efficace")

# 2. Connexion à l'IA (On récupère la clé stockée en secret)
if "GEMINI_API_KEY" in str.secrets:
    genai.configure(api_key=str.secrets["GEMINI_API_KEY"])
else:
    str.error("Clé API manquante. Configure-la dans les paramètres de Streamlit.")
    str.stop()

# 3. Initialisation de l'historique de discussion
if "messages" not in str.session_state:
    str.session_state.messages = []

# 4. Affichage des anciens messages
for message in str.session_state.messages:
    with str.chat_message(message["role"]):
        str.markdown(message["content"])

# 5. Zone de saisie pour l'utilisateur
if user_input := str.chat_input("Pose-moi une question..."):
    # Afficher le message de l'utilisateur
    with str.chat_message("user"):
        str.markdown(user_input)
    str.session_state.messages.append({"role": "user", "content": user_input})

    # Demander la réponse à Gemini
    with str.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            str.markdown(response.text)
            str.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            str.error(f"Erreur : {e}")
