import streamlit as st
import requests
import base64
import os

# Configuração da Página
st.set_page_config(page_title="Kroppa Doctor", page_icon="🌿")

# Chave de API
API_KEY = st.secrets.get("GEMINI_API_KEY")

def analisar_planta(image_file):
    # Converte a imagem para Base64
    img_data = base64.b64encode(image_file.getvalue()).decode("utf-8")
    
    # URL da API do Google (Conexão Direta)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # Monta o "pacote" de dados para enviar
    payload = {
        "contents": [{
            "parts": [
                {"text": "Aja como um Engenheiro Agrônomo. Analise esta imagem, identifique a doença ou praga e sugira o manejo técnico."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
            ]
        }]
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Erro na análise: {response.text}"

# Interface Visual
if os.path.exists("logo_kroppa.png"):
    st.image("logo_kroppa.png", width=150)
st.title("Doutor Planta Kroppa")

if 'foto' not in st.session_state:
    foto = st.file_uploader("📸 Envie a foto da planta", type=["jpg", "jpeg", "png"])
    if foto:
        st.session_state.foto = foto
        st.rerun()
else:
    st.image(st.session_state.foto, width=300)
    if st.button("Gerar Diagnóstico Especializado"):
        with st.spinner("Consultando base de dados agronômica..."):
            resultado = analisar_planta(st.session_state.foto)
            st.markdown("### 📋 Laudo Técnico")
            st.write(resultado)
    
    if st.button("Nova Consulta"):
        del st.session_state.foto
        st.rerun()
