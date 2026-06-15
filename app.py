import streamlit as st

# --- Configuração Inicial da Página ---
st.set_page_config(
    page_title="Smarthome SPNOS - Login",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# --- ESTILIZAÇÃO CUSTOMIZADA (CSS Nativo) ---
# ==========================================
st.markdown("""
    <style>
    /* 1. Fundo Azul Integral da Página de Login */
    .stApp {
        background-color: #0084d6 !important;
    }
    
    /* 2. Remover elementos nativos que quebram o layout */
    div[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stSidebarNav"] { display: none !important; }
    footer { display: none !important; }
    
    /* 3. Container do Título (Fora do Card) */
    .header-container {
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
    }
    .header-container h1 {
        font-weight: 700;
        font-size: 32px;
        color: #ffffff !important;
        margin-bottom: 5px;
    }
    .header-container p {
        font-size: 15px;
        color: #e2e8f0 !important;
        opacity: 0.9;
    }
    
    /* 4. O CARD BRANCO CENTRALIZADO */
    .login-card {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
    }
    
    /* Ajuste para garantir que o texto dentro do card seja escuro */
    .login-card label, .login-card p {
        color: #2d3748 !important;
    }
    
    /* Estilização das Abas (Tabs) do Streamlit */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #a0aec0 !important;
        border-bottom-width: 2px !important;
    }
    button[aria-selected="true"] {
        color: #0084d6 !important;
        border-bottom-color: #0084d6 !important;
    }
    
    /* 5. Inputs de Texto Modificados */
    div[data-testid="stTextInput"] input {
        background-color: #f7fafc !important;
        color: #1a202c !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        height: 48px !important;
        font-size: 15px !important;
        transition: all 0.2s;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #0084d6 !important;
        box-shadow: 0 0 0 1px #0084d6 !important;
        background-color: #ffffff !important;
    }
    
    /* Forçar a cor dos labels das caixas de texto */
    div[data-testid="stTextInput"] label p {
        color: #4a5568 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* 6. Botão Principal Azul */
    div.stButton > button {
        background-color: #0072c6 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        height: 48px !important;
        width: 100% !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-top: 15px !important;
        cursor: pointer;
        transition: background-color 0.2s, transform 0.1s;
    }
    div.stButton > button:hover {
        background-color: #005ea5 !important;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* 7. Link Esqueci a Password */
    .forgot-password-container {
        text-align: center;
        margin-top: 20px;
    }
    .forgot-password-link {
        font-size: 14px;
        color: #718096 !important;
        text-decoration: none;
        cursor: pointer;
        transition: color 0.2s;
    }
    .forgot-password-link:hover {
        color: #4a5568 !important;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# --- BASE DE DADOS EM MEMÓRIA ---
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

if st.session_state.usuario_logado is None:

    # Espaçamento superior
    st.write("<div style='padding-top: 2vh;'></div>", unsafe_allow_html=True)

    # --- TÍTULOS (FORA DO CARD) ---
    st.markdown("""
        <div class="header-container">
            <h1>Smarthome SPNOS</h1>
            <p>Acede à tua área de obras e checklists</p>
        </div>
    """, unsafe_allow_html=True)

    # --- CARD BRANCO INJETADO VIA HTML ---
    # Usamos blocos HTML combinados com containers do Streamlit para o conteúdo ficar bem fechado
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Abas para alternar entre Entrar e Registar
    aba_login, aba_registro = st.tabs(["Entrar", "Registar"])
    
    # -- Conteúdo da Aba 'Entrar' --
    with aba_login:
        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
        pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
        
        if st.button("Entrar", use_container_width=True, key="btn_entrar"):
            if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                st.session_state.usuario_logado = email_input
                st.rerun()
            else:
                st.error("Email ou Palavra-passe incorretos.")
                
        st.markdown("""
            <div class="forgot-password-container">
                <span class="forgot-password-link">Esqueci a password</span>
            </div>
        """, unsafe_allow_html=True)
        
    # -- Conteúdo da Aba 'Registar' --
    with aba_registro:
        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        novo_email = st.text_input("Novo Email", placeholder="exemplo@parceiros.nos.pt", key="reg_email")
        nova_pass = st.text_input("Criar Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
        
        if st.button("Criar Conta", use_container_width=True, key="btn_registar"):
            if not novo_email or not nova_pass:
                st.error("Preencha todos os campos.")
            elif novo_email in st.session_state.usuarios:
                st.error("Este email já está registado.")
            else:
                st.session_state.usuarios[novo_email] = nova_pass
                st.success("Conta criada! Alterne para a aba 'Entrar'.")
                
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Card Branco

# ==========================================
# --- ÁREA LOGADA (ÁREA DE TRABALHO) ---
# ==========================================
else:
    # Reset total do estilo para a área de trabalho ficar limpa e profissional
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        div[data-testid="stHeader"] { display: block !important; background-color: #ffffff !important; }
        label, div[data-testid="stMarkdownContainer"] p { color: #2d3748 !important; }
        h1, h2, h3 { color: #1a202c !important; }
        /* Reset do botão na área interna para não herdar o tamanho total do login */
        div.stButton > button { margin-top: 0px !important; height: 40px !important; }
        </style>
    """, unsafe_allow_html=True)

    # Barra superior da área logada
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h3 style='margin:0;'>🔷 Smarthome SPNOS</h3>", unsafe_allow_html=True)
    with col2:
        if st.button("Sair da Conta ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.write("---")
    user_email = st.session_state.usuario_logado
    st.title(f"Bem-vindo, {user_email.split('@')[0]}")
    st.markdown("Esta é a área protegida do Smarthome SPNOS. O login foi efetuado com sucesso!")
