import streamlit as st
import requests
import base64
import os

# Configuração da Página
st.set_page_config(page_title="Kroppa Doctor", page_icon="🌿")

# Chave de API - Certifique-se que o nome no Secrets é GEMINI_API_KEY
API_KEY = st.secrets.get("GEMINI_API_KEY")

def analisar_planta(image_file):
    # Converte a imagem para Base64
    img_data = base64.b64encode(image_file.getvalue()).decode("utf-8")
    
    # URL ESTÁVEL (v1) e nome de modelo completo
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # Cabeçalho para JSON
    headers = {'Content-Type': 'application/json'}
    
    # Estrutura exata que a API v1 exige
    payload = {
        "contents": [{
            "parts": [
                {"text": "Você é um Engenheiro Agrônomo sênior. Analise esta imagem de uma planta com problema, identifique a possível causa e sugira o manejo técnico detalhado."},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg", 
                        "data": img_data
                    }
                }
            ]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erro na API ({response.status_code}): {res_json.get('error', {}).get('message', 'Erro desconhecido')}"
    except Exception as e:
        return f"Falha na conexão: {str(e)}"

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
