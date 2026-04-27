import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# --- CONFIGURAÇÃO DA INTELIGÊNCIA ---
# Busca a chave nos Secrets do Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Erro: Chave de API não configurada nos Secrets.")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="KROPPA DOCTOR - Kroppa Agro", page_icon="🌿")

# Estilo Kroppa
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    .stButton>button { background-color: #A3B948; color: white; width: 100%; border-radius: 20px; font-weight: bold; }
    .diagnostico-box { background-color: #f0f4e8; border-left: 5px solid #A3B948; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'passo' not in st.session_state:
    st.session_state.passo = 1
    st.session_state.dados = {}

# --- FLUXO ---

if st.session_state.passo == 1:
    if os.path.exists("logo_kroppa.png"):
        st.image("logo_kroppa.png", width=200)
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
        # Preparando o Prompt para a IA
        img = Image.open(st.session_state.foto)
        prompt = f"""
        Aja como um Engenheiro Agrônomo especialista em fitossanidade. 
        Analise a imagem e os dados: 
        Planta: {st.session_state.dados['nome']}
        Manejo: Rega {st.session_state.dados['rega']}, Luz {st.session_state.dados['luz']}, Adubação: {st.session_state.dados['adubo']}.
        
        Forneça um laudo estruturado:
        1. Identificação do Problema (Doença, Praga ou Distúrbio Fisiológico).
        2. Causa provável baseada no manejo relatado.
        3. Prescrição Técnica (O que fazer agora).
        4. Recomendação de Produto (Indique um tipo de insumo ou nutriente).
        Use um tom profissional, direto e prático.
        """
        
        response = model.generate_content([prompt, img])
        
        st.markdown(f"<div class='diagnostico-box'>{response.text}</div>", unsafe_allow_html=True)
        
    st.write("---")
    st.warning("⚠️ Este é um diagnóstico assistido por IA. Para decisões em larga escala, consulte um agrônomo presencialmente.")
    
    if st.button("Nova Consulta"):
        st.session_state.passo = 1
        st.rerun()
