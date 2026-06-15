import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Testeur de Modèles")
st.title("Diagnostic des modèles")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    st.write("Voici les modèles disponibles pour votre clé :")
    try:
        models = genai.list_models()
        for m in models:
            st.write(f"- {m.name}")
    except Exception as e:
        st.error(f"Erreur : {e}")
else:
    st.error("Ajoutez GEMINI_API_KEY dans les secrets.")
