# Bloc de diagnostic à ajouter pour voir ce qui est dispo
import google.generativeai as genai
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
for m in genai.list_models():
    st.write(m.name)
