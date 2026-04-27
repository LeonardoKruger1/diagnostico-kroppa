import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO DA INTELIGÊNCIA ---
try:
    # Busca a chave nos Secrets do Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Usando o nome completo do modelo para evitar o erro 404
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Erro de Configuração: {e}")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KROPPA DOCTOR - Agro", page_icon="🌿")

# Estilo Kroppa
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    .stButton>button { background-color: #A3B948; color: white; width: 100%; border-radius: 20px; font-weight: bold; height: 3em;}
    .diagnostico-box { background-color: #f0f4e8; border-left: 5px solid #A3B948; padding: 20px; border-radius: 10px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

if 'passo' not in st.session_state:
    st.session_state.passo = 1
    st.session_state.dados = {}

# --- CABEÇALHO ---
if os.path.exists("logo_kroppa.png"):
    st.image("logo_kroppa.png", width=200)

# --- FLUXO ---

if st.session_state.passo == 1:
    st.title("Doutor Planta")
    st.subheader("Análise Agronômica em Tempo Real")
    
    foto = st.file_uploader("Suba a foto da planta afetada", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, width=300)
        st.session_state.foto = foto
        if st.button("Iniciar Consultoria →"):
            st.session_state.passo = 2
            st.rerun()

elif st.session_state.passo == 2:
    st.header("Anamnese Técnica")
    nome = st.text_input("Nome da Planta:", placeholder="Ex: Soja, Orquídea, Milho...")
    rega = st.selectbox("Frequência de Rega:", ["Diária", "2x por semana", "1x por semana", "Só quando seca"])
    luz = st.selectbox("Exposição Solar:", ["Pleno Sol", "Meia Sombra", "Sombra/Interno"])
    adubo = st.text_input("Última adubação (o que e quando):")
    
    if st.button("Gerar Diagnóstico Especializado"):
        st.session_state.dados = {"nome": nome, "rega": rega, "luz": luz, "adubo": adubo}
        st.session_state.passo = 3
        st.rerun()

elif st.session_state.passo == 3:
    st.header("📋 Laudo Técnico Kroppa")
    
    with st.spinner("Analisando tecidos vegetais e histórico..."):
        try:
            img = Image.open(st.session_state.foto)
            prompt = f"""
            Aja como um Engenheiro Agrônomo especialista em fitossanidade. 
            Analise a imagem e os dados: 
            Planta: {st.session_state.dados['nome']}
            Manejo: Rega {st.session_state.dados['rega']}, Luz {st.session_state.dados['luz']}, Adubação: {st.session_state.dados['adubo']}.
            
            Forneça um laudo estruturado:
            1. Identificação do Problema.
            2. Causa provável.
            3. Prescrição Técnica.
            4. Sugestão de Insumo/Nutriente.
            """
            
            response = model.generate_content([prompt, img])
            st.markdown(f"<div class='diagnostico-box'>{response.text}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erro ao gerar diagnóstico: {e}")
            st.info("Verifique se sua API Key no AI Studio tem permissão para o modelo Gemini 1.5 Flash.")
    
    if st.button("Nova Consulta"):
        st.session_state.passo = 1
        st.rerun()
