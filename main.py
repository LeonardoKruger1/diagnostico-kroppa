import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configuração de Segurança com verificação simples
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave API não encontrada nos Secrets.")

st.set_page_config(page_title="Kroppa Doctor", page_icon="🌿")

# Tenta carregar a logo, se falhar não trava o site
if os.path.exists("logo_kroppa.png"):
    st.image("logo_kroppa.png", width=150)

st.title("Doutor Planta Kroppa")

if 'passo' not in st.session_state:
    st.session_state.passo = 1

# Passo 1: Upload
if st.session_state.passo == 1:
    foto = st.file_uploader("📸 Envie a foto da planta", type=["jpg", "jpeg", "png"])
    if foto:
        st.session_state.foto = foto
        st.session_state.passo = 2
        st.rerun()

# Passo 2: Diagnóstico
elif st.session_state.passo == 2:
    st.image(st.session_state.foto, width=300)
    if st.button("Gerar Laudo Técnico"):
        with st.spinner("Analisando..."):
            try:
                # Usando o modelo mais básico e estável de todos
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(st.session_state.foto)
                response = model.generate_content(["Identifique o problema nesta planta e sugira o tratamento como agrônomo.", img])
                st.success("Análise Concluída!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro na IA: {e}")
    
    if st.button("Nova Consulta"):
        st.session_state.passo = 1
        st.rerun()
