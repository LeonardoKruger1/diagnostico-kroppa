import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Configuração de Segurança
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Configure a GEMINI_API_KEY nos Secrets do Streamlit.")
        st.stop()
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Erro na chave: {e}")
    st.stop()

# 2. Estética Kroppa
st.set_page_config(page_title="Kroppa Doctor", page_icon="🌿")
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    .stButton>button { background-color: #A3B948; color: white; border-radius: 20px; width: 100%; font-weight: bold; }
    .laudo { background-color: #f0f4e8; border-left: 5px solid #A3B948; padding: 20px; border-radius: 10px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# 3. Interface
if os.path.exists("logo_kroppa.png"):
    st.image("logo_kroppa.png", width=180)

st.title("Doutor Planta")
st.write("---")

if 'passo' not in st.session_state:
    st.session_state.passo = 1

if st.session_state.passo == 1:
    foto = st.file_uploader("📸 Envie a foto da planta", type=["jpg", "jpeg", "png"])
    if foto:
        st.image(foto, width=300)
        if st.button("Analisar Planta →"):
            st.session_state.foto = foto
            st.session_state.passo = 2
            st.rerun()

elif st.session_state.passo == 2:
    st.subheader("📋 Laudo Técnico")
    with st.spinner("IA Agronômica processando..."):
        try:
            # Usando o modelo mais estável para visão
            model = genai.GenerativeModel('gemini-pro-vision')
            img = Image.open(st.session_state.foto)
            
            prompt = "Aja como um Engenheiro Agrônomo. Identifique o problema nesta planta e sugira o tratamento."
            
            response = model.generate_content([prompt, img])
            st.markdown(f"<div class='laudo'>{response.text}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erro no diagnóstico: {e}")
    
    if st.button("Nova Consulta"):
        st.session_state.passo = 1
        st.rerun()
