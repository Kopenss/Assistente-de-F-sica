import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title = "Fí-Tech",
    page_icon = "⚛️",
    layout= "wide",
    initial_sidebar_state= "expanded"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #0a0e1a;
    color: #c9d1e0;
  }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220 0%, #0a0e1a 100%);
    border-right: 1px solid #1e2d4a;
  }

  /* Título principal */
  .main-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2rem;
    color: #00d4ff;
    text-shadow: 0 0 20px rgba(0,212,255,0.4);
    letter-spacing: 3px;
    margin-bottom: 0.2rem;
  }

  .sub-title {
    font-size: 0.8rem;
    color: #4a6fa5;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
  }

  /* Balões de chat */
  .msg-user {
    background: linear-gradient(135deg, #0f2040 0%, #1a3560 100%);
    border: 1px solid #1e4080;
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    color: #a8c8ff;
    box-shadow: 0 2px 8px rgba(0,100,255,0.1);
  }

  .msg-bot {
    background: linear-gradient(135deg, #0d1e10 0%, #122418 100%);
    border: 1px solid #1a4020;
    border-radius: 12px 12px 12px 2px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    color: #90e0a0;
    font-family: 'Share Tech Mono', monospace;
    box-shadow: 0 2px 8px rgba(0,200,80,0.08);
    white-space: pre-wrap;
    line-height: 1.6;
  }

  .label-user {
    font-size: 0.7rem;
    color: #4a6fa5;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .label-bot {
    font-size: 0.7rem;
    color: #2a6040;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  /* Botões da sidebar */
  .stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid #1e3a5f;
    color: #4a8fc0;
    border-radius: 6px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    padding: 8px;
    transition: all 0.2s;
    margin-bottom: 4px;
  }

  .stButton > button:hover {
    background: #1e3a5f;
    color: #00d4ff;
    border-color: #00d4ff;
    box-shadow: 0 0 10px rgba(0,212,255,0.2);
  }

  /* Botão sair */
  .btn-sair > button {
    border-color: #5f1e1e !important;
    color: #c04a4a !important;
  }

  .btn-sair > button:hover {
    background: #5f1e1e !important;
    color: #ff6060 !important;
    border-color: #ff6060 !important;
    box-shadow: 0 0 10px rgba(255,60,60,0.2) !important;
  }

  /* Botão gabarito */
  .btn-gabarito > button {
    border-color: #3a5f1e !important;
    color: #7ac04a !important;
  }

  .btn-gabarito > button:hover {
    background: #2a4a10 !important;
    color: #a0ff60 !important;
    border-color: #a0ff60 !important;
  }

  /* Selectbox */
  .stSelectbox > div > div {
    background: #0d1220;
    border: 1px solid #1e3a5f;
    color: #4a8fc0;
    font-family: 'Share Tech Mono', monospace;
  }

  /* Input de texto */
  .stTextInput > div > div > input {
    background: #0d1220;
    border: 1px solid #1e3a5f;
    color: #c9d1e0;
    font-family: 'Share Tech Mono', monospace;
    border-radius: 6px;
  }

  .stTextInput > div > div > input:focus {
    border-color: #00d4ff;
    box-shadow: 0 0 8px rgba(0,212,255,0.2);
  }

  /* Chat input */
  .stChatInput > div {
    background: #0d1220;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
  }

  /* Divisor */
  hr {
    border-color: #1e2d4a;
    margin: 12px 0;
  }

  /* Área do chat */
  .chat-container {
    max-height: 65vh;
    overflow-y: auto;
    padding: 8px 0;
  }

  /* Badge de nível */
  .nivel-badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 2px;
    margin-bottom: 12px;
  }

  .nivel-facil    {{ background: #0d2010; color: #4aff80; border: 1px solid #2a5030; }}
  .nivel-medio    {{ background: #1e1a08; color: #ffd060; border: 1px solid #5a4a10; }}
  .nivel-dificil  {{ background: #200d0d; color: #ff7060; border: 1px solid #5a2020; }}
  .nivel-ita      {{ background: #100d20; color: #b060ff; border: 1px solid #3a2060; }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 4px; }}
  ::-webkit-scrollbar-track {{ background: #0a0e1a; }}
  ::-webkit-scrollbar-thumb {{ background: #1e3a5f; border-radius: 2px; }}
</style>
""",unsafe_allow_html=True)


template = """Você é um assistente especializado em Física para nível de graduação em Licenciatura.
Responda sempre em português de forma clara, organizada e didática.
O usuário tem TDAH, então estruture sempre as respostas com títulos, tópicos e exemplos práticos.

## Áreas de conhecimento
Você domina todas as seguintes áreas:
- Mecânica Clássica
- Termodinâmica
- Eletromagnetismo
- Física Moderna e Quântica
- Ondas e Óptica

## Suas capacidades

### 📐 Fórmulas
Quando apresentar uma fórmula, siga sempre este formato:

Nome: Segunda Lei de Newton
Fórmula: F = m · a
Variáveis:
  - F = Força resultante (N)
  - m = massa (kg)
  - a = aceleração (m/s²)
Quando usar: quando há força resultante não nula agindo sobre um corpo

### 🔬 Aplicabilidade em Experimentos Reais
Sempre que apresentar uma fórmula ou conceito, inclua um exemplo de aplicação real:

Experimento: Plano inclinado com atrito
Contexto: Um bloco de 2kg desliza por uma rampa de 30°
Fórmulas aplicadas: F = m·a, f = μ·N
Resultado esperado: ...

### 📏 Constantes Físicas
Quando solicitado ou necessário, forneça o valor exato das constantes:

- Velocidade da luz: c = 3,00 × 10⁸ m/s
- Constante de Planck: h = 6,626 × 10⁻³⁴ J·s
- Constante gravitacional: G = 6,674 × 10⁻¹¹ N·m²/kg²
- Carga do elétron: e = 1,602 × 10⁻¹⁹ C
- Constante de Boltzmann: k = 1,381 × 10⁻²³ J/K
- Número de Avogadro: Nₐ = 6,022 × 10²³ mol⁻¹
- Permissividade do vácuo: ε₀ = 8,854 × 10⁻¹² F/m
- Permeabilidade do vácuo: μ₀ = 4π × 10⁻⁷ T·m/A

### 📝 Geração de Questões
Quando solicitado, gere questões seguindo este formato:

Nível: [Fácil / Médio / Difícil]
Área: [ex: Mecânica Clássica]
Questão: ...
Dados fornecidos: ...

Alternativas:
  A) ...
  B) ...
  C) ...
  D) ...
  E) ...

⚠️ REGRA IMPORTANTE: Nunca mostre a resposta ou resolução junto com a questão.
Apenas apresente a questão e as alternativas e aguarde.

### 📋 Gabarito
Somente quando o usuário solicitar explicitamente o gabarito, responda neste formato:

Resposta correta: [letra]
Resolução passo a passo:
  Passo 1: ...
  Passo 2: ...
Resposta final: ...

### 📌 Nível Cálculo Avançado — ITA
Quando o nível for Cálculo Avançado, a questão deve:

- Ser inspirada no padrão ITA/IME — considerado o vestibular mais difícil do Brasil
- Exigir obrigatoriamente o uso de integrais e/ou derivadas na resolução
- Combinar dois ou mais ramos da física na mesma questão
  (ex: Mecânica + Termodinâmica, Eletromagnetismo + Física Quântica)
- Envolver raciocínio em múltiplas etapas não triviais
- Exigir manipulação algébrica avançada antes de chegar ao resultado
- Usar quando aplicável:
    - Equações Diferenciais Ordinárias (EDOs)
    - Integrais de linha, duplas ou triplas
    - Operadores diferenciais: ∇, ∂/∂x, d/dt
    - Séries de Taylor para aproximações físicas
    - Transformadas quando necessário
- As alternativas devem ser expressões matemáticas complexas,
  não valores numéricos simples — dificultando eliminação por chute
- A questão deve ter solução única e rigorosamente correta,
  sem ambiguidade

⚠️ Objetivo: gerar questões que desafiem estudantes de graduação
avançada e profissionais da área — nível de olimpíada de física ou
vestibular ITA.

## Formatação para Terminal
- NUNCA use notação LaTeX 
- Escreva fórmulas em texto simples legível no terminal:
  ✅ E = (μ₀ · e · v²) / (4π · r²)
  ✅ F = m · a
  ✅ ∫F·dr = ΔKE
- Use caracteres Unicode para símbolos:
  ⁺⁻ᐟ⁽⁾ꜝ para operações com expoentes
  ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ para operações logaritimicas
  · para multiplicação
  ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹  para expoentes simples
  ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ para expoentes incognitas
  ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ para logaritimos incognitas
  ± ∓ × ÷ ∶ … ≤ ≥ ≠ √ ∛ ∜ ∑ ∏ ∞ ♾ ℕ ℤ ℚ ℝ ℂ ∈ ∉ ∅ ≅ ≈ para operações matematicas
  ∆ para variação: Vm = ∆S/∆t
  ∫∬∭ ∂ ∇ Σ π μ ω φ θ λ σ ε para símbolos físicos
  → para vetores: F→ = m · a→


## Regras
- Sempre use notação científica quando necessário
- Sempre especifique as unidades de medida (SI)
- Se a pergunta for vaga, pergunte o tema ou área antes de responder
- Relacione sempre a teoria com aplicações práticas reais
- Respostas organizadas com títulos e tópicos — essencial para leitura com TDAH

⚠️ REGRA IMPORTANTE: 
- Ignore qualquer pergunta sobre assuntos que não são ou não estão relacionados a fisica ou matemática e nem faça conexões fisicas sobre o assunto.
- Apenas diga ao usuário que não é uma pergunta sobre fisica ou matematica e peça para fazer outra pergunta
"""
if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state.store = {}

if "encerrar" not in st.session_state:
    st.session_state.encerrar = False
    

@st.cache_resource
def get_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    llm = ChatGroq(
        temperature=0.7,
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    return prompt | llm

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

chain = get_chain()

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

with st.sidebar:
    st.markdown('<div class="main-title">⚛️ FÍSICA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Assistente de Graduação</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Seletor de nível
    st.markdown("**NÍVEL DAS QUESTÕES**")
    nivel = st.selectbox(
        "Nível",
        ["Fácil", "Médio", "Difícil", "Cálculo Avançado — ITA"],
        label_visibility="collapsed"
    )

    nivel_map = {
        "Fácil": ("facil", "FÁCIL"),
        "Médio": ("medio", "MÉDIO"),
        "Difícil": ("dificil", "DIFÍCIL"),
        "Cálculo Avançado — ITA": ("ita", "ITA")
    }
    nivel_class, nivel_label = nivel_map[nivel]
    st.markdown(
        f'<div class="nivel-badge nivel-{nivel_class}">{nivel_label}</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**AÇÕES RÁPIDAS**")

    # Botão gerar questão
    if st.button("📝  Gerar Questão"):
        st.session_state.messages.append({
            "role": "user",
            "content": f"Crie uma questão de nível {nivel}."
        })
        st.rerun()

    # Botão gabarito
    st.markdown('<div class="btn-gabarito">', unsafe_allow_html=True)
    if st.button("✅  Ver Gabarito"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Mostre o gabarito com a resolução completa passo a passo."
        })
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Botão limpar histórico
    if st.button("🗑️  Limpar Histórico"):
        st.session_state.messages = []
        st.session_state.store = {}
        st.rerun()

    st.markdown("---")

    # Botão sair
    st.markdown('<div class="btn-sair">', unsafe_allow_html=True)
    if st.button("⏻  Encerrar"):
        st.session_state.encerrar = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.encerrar:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:60vh; gap:16px;">
      <div style="font-family:'Share Tech Mono',monospace; font-size:3rem;
                  color:#ff4040; text-shadow: 0 0 30px rgba(255,60,60,0.5);">
        ⏻
      </div>
      <div style="font-family:'Share Tech Mono',monospace; font-size:1.2rem;
                  color:#ff6060; letter-spacing:4px;">
        SESSÃO ENCERRADA
      </div>
      <div style="color:#4a6fa5; font-size:0.8rem; letter-spacing:2px;">
        Feche a aba ou reinicie para continuar
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


st.markdown('<div class="main-title" style="font-size:1.2rem;">ASSISTENTE DE FÍSICA ⚛️</div>', unsafe_allow_html=True)
st.markdown("---")

# Exibir histórico
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="label-user">▶ VOCÊ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="label-bot">⚛ ASSISTENTE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    ultima = st.session_state.messages[-1]["content"]
    with st.spinner("⚛️ Processando..."):
        resposta = chain_with_history.invoke(
            {"input": ultima},
            config={"configurable": {"session_id": "user123"}}
        )
    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta.content
    })
    st.rerun()

st.markdown("---")
user_input = st.chat_input("Digite sua pergunta de física...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    st.rerun()
