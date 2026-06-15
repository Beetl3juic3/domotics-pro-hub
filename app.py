import streamlit as st
from datetime import datetime

# --- Configuração Inicial da Página (Ícone e Título do Navegador) ---
st.set_page_config(
    page_title="Smarthome SPNOS - Login",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# --- ESTILIZAÇÃO CUSTOMIZADA (CSS Nativo) ---
# Isto força o Streamlit a usar as tuas cores, inputs e layout.
# ==========================================
st.markdown("""
    <style>
    /* 1. Fundo Azul Integral da Página */
    .stApp {
        background-color: #0084d6 !important;
    }
    
    /* 2. Remover elementos nativos do Streamlit que quebram o design */
    div[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stSidebarNav"] { display: none !important; }
    footer { display: none !important; }
    
    /* 3. Estilo dos Títulos (Fora do Card) - Brancos sobre Fundo Azul */
    .header-container {
        text-align: center;
        margin-top: 5rem;
        margin-bottom: 2rem;
        color: #ffffff;
    }
    .header-container h1 {
        font-weight: bold;
        font-size: 32px;
        margin-bottom: 0px;
        color: #ffffff !important;
    }
    .header-container p {
        font-size: 15px;
        opacity: 0.9;
        margin-top: 5px;
        color: #ffffff !important;
    }
    
    /* 4. Estilo das Etiquetas (Email, Palavra-passe) e Inputs */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #4a5568 !important; /* Cor escura para dentro do card branco */
        font-weight: 500 !important;
        margin-bottom: 5px;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important; /* Forçar input branco */
        color: #222222 !important; /* Texto escuro dentro do input */
        border: 1px solid #dcdfe6 !important;
        border-radius: 8px !important;
        height: 45px !important;
    }

    /* 5. Estilo do Botão Azul 'Entrar' */
    div.stButton > button {
        background-color: #006ce6 !important; /* Azul original */
        color: #ffffff !important;
        border-radius: 12px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-top: 20px !important;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #005bb5 !important; /* Azul mais escuro no hover */
    }

    /* 6. Estilo do Link 'Esqueci a password' */
    .forgot-password {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #718096;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# --- INICIALIZAÇÃO DE BASE DE DADOS EM MEMÓRIA ---
# (Utilizador padrão sugerido nas imagens)
# ==========================================
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234" 
    }

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# ==========================================
# --- LÓGICA DO ECRÃ DE LOGIN ---
# ==========================================

# Só mostra o login se ninguém estiver logado
if st.session_state.usuario_logado is None:

    # Centralizar o card verticalmente de forma simples
    st.write("<div style='padding-top: 5vh;'></div>", unsafe_allow_html=True)

    # --- HEADER FORA DO CARD (TÍTULOS BRANCOS) ---
    st.markdown("""
        <div class="header-container">
            <h1>Smarthome SPNOS</h1>
            <p>Acede à tua área de obras e checklists</p>
        </div>
    """, unsafe_allow_html=True)

    # --- INÍCIO DO CARD BRANCO CENTRAL (Com logins) ---
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Abas nativas Entrar / Registar igual à imagem
    aba_login, aba_registro = st.tabs(["         Entrar         ", "         Registar         "])
    
    # -- Conteúdo da Aba 'Entrar' --
    with aba_login:
        email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
        pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
        
        # Botão 'Entrar'
        if st.button("Entrar", use_container_width=True):
            # Validação simples
            if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                st.session_state.usuario_logado = email_input
                st.rerun() # Atualiza para entrar na área protegida
            else:
                st.error("Email ou Palavra-passe incorretos.")
                
        # Link de 'Esqueci'
        st.markdown("<p class='forgot-password'>Esqueci a password</p>", unsafe_allow_html=True)
        
    # -- Conteúdo da Aba 'Registar' (Simplificado) --
    with aba_registro:
        st.write(" ")
        novo_email = st.text_input("Novo Email", placeholder="exemplo@parceiros.nos.pt", key="reg_email")
        nova_pass = st.text_input("Criar Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
        
        if st.button("Criar Conta", use_container_width=True):
            if not novo_email or not nova_pass:
                st.error("Preencha todos os campos.")
            elif novo_email in st.session_state.usuarios:
                st.error("Este email já está registado.")
            else:
                st.session_state.usuarios[novo_email] = nova_pass
                st.success("Conta criada! Alterne para a aba 'Entrar'.")
                
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Card Branco

# ==========================================
# --- ÁREA LOGADA (Apenas para Testar) ---
# ==========================================
else:
    # Resetar o fundo para a área de trabalho
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        label, div[data-testid="stMarkdownContainer"] p { color: #333333 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Header simples
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🔷 Smarthome SPNOS")
    with col2:
        if st.button("Sair da Conta ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.write("---")
    user_email = st.session_state.usuario_logado
    st.title(f"Bem-vindo, {user_email.split('@')[0]}")
    st.markdown("Esta é a área protegida do Smarthome SPNOS. O login foi efetuado com sucesso!")
