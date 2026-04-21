import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Doutor Planta - Kroppa Agro",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DEFINIÇÃO DE CORES KROPPA AGRO ---
COR_VERDE = "#A3B948"
COR_DOURADO = "#C9941C"
COR_FUNDO = "#FDFDFD" # Off-white para fundo limpo
COR_TEXTO = "#333333"

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown(f"""
    <style>
    /* Fundo da Aplicação */
    .stApp {{
        background-color: {COR_FUNDO};
        color: {COR_TEXTO};
    }}
    
    /* Estilo dos Botões */
    .stButton>button {{
        background-color: {COR_VERDE};
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {COR_DOURADO};
        color: white;
        transform: scale(1.05);
    }}
    
    /* Títulos e Subtítulos */
    h1, h2, h3 {{
        color: {COR_TEXTO} !important;
    }}
    
    /* Inputs de Texto e Selectbox */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {{
        border-color: {COR_VERDE};
        border-radius: 10px;
    }}
    
    /* Área de Upload */
    .stFileUploader>div>div>button {{
        color: {COR_VERDE};
        border-color: {COR_VERDE};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO COM LOGOTIPO ---
# Centralizando o logotipo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Verificação para evitar erro se o arquivo não existir localmente
    if os.path.exists("logo_kroppa.png"):
       st.image("logo_kroppa.png", width="stretch")
    else:
        st.warning("⚠️ Arquivo 'logo_kroppa.png' não encontrado. Suba o arquivo para ver a logo.")

st.markdown("<h1 style='text-align: center;'>Doutor Planta</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: {COR_VERDE};'>Seu assistente técnico para diagnóstico vegetal</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- LÓGICA DE ESTADO (Para manter a conversa) ---
if 'passo' not in st.session_state:
    st.session_state.passo = 1
    st.session_state.dados = {}

# --- FLUXO DE ANAMNESE ---

# PASSO 1: Upload da Foto
if st.session_state.passo == 1:
    st.markdown("### 📸 Passo 1: O que está acontecendo?")
    foto = st.file_uploader("Envie uma foto bem nítida da parte afetada da planta", type=["jpg", "jpeg", "png"])
    if foto:
        st.image(foto, caption="Imagem recebida! Nossos agrônomos estão analisando...", use_container_width="stretch")
        col_btn1, col_btn2 = st.columns([1,1])
        with col_btn2:
            if st.button("Continuar para identificação →"):
                st.session_state.passo = 2
                st.rerun()

# PASSO 2: Identificação Botânica
elif st.session_state.passo == 2:
    st.markdown("### 🏷️ Passo 2: Identificação")
    st.write("Para um diagnóstico mais preciso, precisamos saber com quem estamos falando.")
    nome_planta = st.text_input("Você sabe o nome desta planta (ou nome científico)?", placeholder="Ex: Rosa do Deserto, Jiboia...")
    st.markdown(f"_<span style='color: {COR_DOURADO};'>Se não souber, tudo bem! Nossa IA e agrônomos identificarão pela foto.</span>_", unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        if st.button("← Voltar"):
            st.session_state.passo = 1
            st.rerun()
    with col_btn2:
        if st.button("Confirmar e ir para a Anamnese →"):
            st.session_state.dados['nome'] = nome_planta
            st.session_state.passo = 3
            st.rerun()

# PASSO 3: Rega e Ambiente
elif st.session_state.passo == 3:
    st.markdown("### 🏠 Passo 3: Histórico de Cuidados")
    st.write("Vamos entender a rotina da sua planta.")
    
    rega = st.selectbox("Com que frequência você rega?", ["Escolha uma opção...", "Diário", "2x por semana", "1x por semana", "Apenas quando a terra seca", "Raro"])
    metodo = st.radio("Como você rega?", ["Direto no substrato", "Molho as folhas também (borrifo)"])
    luz = st.selectbox("Quanta luz ela recebe?", ["Escolha uma opção...", "Sol direto (mais de 4h/dia)", "Luz filtrada/Claridade constante", "Sombra/Interior com pouca luz"])
    
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        if st.button("← Voltar"):
            st.session_state.passo = 2
            st.rerun()
    with col_btn2:
        # Só habilita se tiver escolhido as opções
        if rega != "Escolha uma opção..." and luz != "Escolha uma opção...":
            if st.button("Próximo passo →"):
                st.session_state.dados['rega'] = rega
                st.session_state.dados['metodo'] = metodo
                st.session_state.dados['luz'] = luz
                st.session_state.passo = 4
                st.rerun()
        else:
            st.warning("Por favor, preencha todas as opções.")

# PASSO 4: Substrato e Nutrição
elif st.session_state.passo == 4:
    st.markdown("### 🧪 Passo 4: Nutrição e Solo")
    st.write("As últimas perguntas antes do veredito.")
    
    tempo_vaso = st.number_input("Há quantos meses ela está nesse mesmo vaso e substrato?", min_value=0, step=1, help="Isso nos ajuda a avaliar a compactação e exaustão do solo.")
    adubacao = st.text_area("Qual foi a última vez que você adubou e o que usou?", placeholder="Ex: Nunca adubei / Usei NPK 10-10-10 faz 2 meses / Uso adubo orgânico mensalmente...")
    
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        if st.button("← Voltar"):
            st.session_state.passo = 3
            st.rerun()
    with col_btn2:
        if st.button("Gerar Diagnóstico ✅"):
            st.session_state.passo = 5
            st.session_state.dados['tempo_vaso'] = tempo_vaso
            st.session_state.dados['adubacao'] = adubacao
            st.rerun()

# PASSO 5: Resultado Final (Simulado para o Beta)
elif st.session_state.passo == 5:
    st.markdown(f"### <span style='color: {COR_VERDE};'>✅ Diagnóstico Kroppa em Processamento</span>", unsafe_allow_html=True)
    st.write(f"Obrigado por completar a anamnese da sua **{st.session_state.dados.get('nome', 'planta')}**!")
    st.write("Como estamos na nossa **Fase Beta de Testes**, seus dados e fotos foram enviados para a análise criteriosa dos nossos agrônomos.")
    
    st.info("📣 **O que acontece agora?**\n\nNós revisaremos as informações e, em breve, você receberá o veredito técnico completo e as recomendações de manejo diretamente no canal onde recebeu este link.")
    
    st.markdown("---")
    st.write("### Ajude-nos a melhorar!")
    st.write("Em uma escala de 1 a 5, o quanto este processo de perguntas foi fácil e claro para você?")
    feedback_nota = st.slider("Nota", 1, 5, 5)
    
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn2:
        if st.button("Enviar Feedback e Finalizar"):
            st.success("Feedback enviado! Obrigado por nos ajudar a construir a Kroppa Agro.")
            if st.button("Reiniciar nova consulta"):
                st.session_state.passo = 1
                st.session_state.dados = {}
                st.rerun()
