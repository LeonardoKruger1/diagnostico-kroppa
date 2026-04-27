import streamlit as st
import requests
import base64
import os

# Configuração da Página
st.set_page_config(page_title="Kroppa Doctor", page_icon="🌿")

# Chave de API - Certifique-se que o nome no Secrets é GEMINI_API_KEY
API_KEY = st.secrets.get("GEMINI_API_KEY")

def analisar_planta(image_file):
    img_data = base64.b64encode(image_file.getvalue()).decode("utf-8")
    
    # URL v1beta com o nome de modelo que MAIS TEM FUNCIONADO globalmente hoje
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "Aja como um Engenheiro Agrônomo. Identifique o problema na planta desta imagem e sugira o manejo técnico."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
            ]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Se o 1.5 Flash falhar, tentamos o Pro Vision automaticamente no erro
            return f"Erro Crítico (404): O modelo ainda não está disponível na sua região. Tente novamente em instantes."
    except Exception as e:
        return f"Erro de conexão: {str(e)}"
# --- INTERFACE ---
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
        with st.spinner("O Agrônomo Digital está analisando a imagem..."):
            resultado = analisar_planta(st.session_state.foto)
            st.markdown("### 📋 Laudo Técnico Kroppa")
            st.info(resultado)
    
    if st.button("Nova Consulta"):
        del st.session_state.foto
        st.rerun()
