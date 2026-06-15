import streamlit as st

# --- Configuração Inicial da Página ---
st.set_page_config(
    page_title="Smarthome SPNOS",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
# --- LÓGICA DE TELAS ---
# ==========================================

# 1. ECRÃ DE LOGIN
if st.session_state.usuario_logado is None:
    
    # Injetar o CSS específico de login APENAS aqui dentro
    st.markdown("""
        <style>
        /* Fundo Azul Integral da Página de Login */
        .stApp {
            background-color: #0084d6 !important;
        }
        
        /* Remover elementos nativos no login */
        div[data-testid="stHeader"] { display: none !important; }
        div[data-testid="stSidebarNav"] { display: none !important; }
        footer { display: none !important; }
        
        /* Container do Título (Fora do Card) */
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
        
        /* O CARD BRANCO CENTRALIZADO */
        .login-card {
            background-color: #ffffff;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            margin-bottom: 2rem;
        }
        
        /* Cor dos labels dentro do card */
        .login-card label, .login-card p {
            color: #2d3748 !important;
        }
        
        /* Estilização das Abas (Tabs) */
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
        
        /* Inputs de Texto */
        div[data-testid="stTextInput"] input {
            background-color: #f7fafc !important;
            color: #1a202c !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            height: 48px !important;
            font-size: 15px !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #0084d6 !important;
            box-shadow: 0 0 0 1px #0084d6 !important;
            background-color: #ffffff !important;
        }
        div[data-testid="stTextInput"] label p {
            color: #4a5568 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* Botão Principal Azul no Login */
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
        }
        div.stButton > button:hover { background-color: #005ea5 !important; }
        
        .forgot-password-container { text-align: center; margin-top: 20px; }
        .forgot-password-link { font-size: 14px; color: #718096 !important; text-decoration: none; }
        </style>
    """, unsafe_allow_html=True)

    st.write("<div style='padding-top: 2vh;'></div>", unsafe_allow_html=True)

    # Títulos
    st.markdown("""
        <div class="header-container">
            <h1>Smarthome SPNOS</h1>
            <p>Acede à tua área de obras e checklists</p>
        </div>
    """, unsafe_allow_html=True)

    # Card de Login
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    aba_login, aba_registro = st.tabs(["Entrar", "Registar"])
    
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
                
        st.markdown('<div class="forgot-password-container"><span class="forgot-password-link">Esqueci a password</span></div>', unsafe_allow_html=True)
        
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
                
    st.markdown('</div>', unsafe_allow_html=True)

# 2. ÁREA LOGADA (ÁREA DE TRABALHO CLEAN)
else:
    # Forçar o reset completo do CSS para o padrão do Streamlit
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        div[data-testid="stHeader"] { display: block !important; }
        
        /* Limpar as margens e redefinir cores dos textos da área interna */
        h1, h2, h3, p, label, span { color: #1a202c !important; }
        
        /* Estilo específico para o botão de logout não herdar o CSS do login */
        .logout-container button {
            background-color: #dc3545 !important;
            color: white !important;
            border-radius: 6px !important;
            height: 38px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            margin-top: 0px !important;
            border: none !important;
        }
        .logout-container button:hover { background-color: #bd2130 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Topo da aplicação
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h3 style='margin-top:10px;'>🔷 Smarthome SPNOS</h3>", unsafe_allow_html=True)
    with col2:
        # Envolvido numa div com classe própria para controlar o botão de sair de forma isolada
        st.markdown('<div class="logout-container">', unsafe_allow_html=True)
        if st.button("Sair da Conta ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.write("---")
    
    # Conteúdo principal da tua App
    user_email = st.session_state.usuario_logado
    st.title(f"👋 Bem-vindo, {user_email.split('@')[0]}")
    st.markdown("Esta é a tua área de trabalho segura. Já podes começar a construir os teus formulários, relatórios ou gestão de obras aqui em baixo.")
    
    # Podes começar a adicionar os teus componentes (inputs, tabelas, etc) aqui:
    st.info("Dica: Todo o código adicionado aqui aparecerá no fundo claro padrão do Streamlit.")
