import streamlit as st

# --- Configuração da Página (Ícone e Título do Navegador) ---
st.set_page_config(page_title="Smarthome SPNOS - Login", page_icon="⚙️", layout="centered")

# =========================================================
# --- INJEÇÃO DE CSS PERSONALIZADO (A Mágica do Visual) ---
# Isto garante que o Streamlit ignore o tema padrão e use as tuas cores.
# =========================================================
st.markdown("""
    <style>
    /* 1. Fundo Azul Integral da Página (exatamente como na imagem) */
    .stApp {
        background-color: #0084d6 !important;
    }
    
    /* 2. Centralizar o conteúdo verticalmente e remover paddings desnecessários */
    div.block-container {
        padding-top: 5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }

    /* 3. Estilo do Card Branco Central */
    .login-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.15);
        max-width: 480px;
        width: 100%;
        margin: 0 auto;
        color: #333333;
    }

    /* 4. Estilo do Título e Subtítulo (Branco sobre Fundo Azul) */
    .header-text {
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 30px;
    }
    .header-text h2 {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .header-text p {
        font-size: 15px;
        opacity: 0.9;
        margin-top: 5px;
    }

    /* 5. Estilo das Etiquetas (Email, Palavra-passe) e Inputs */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #333333 !important; /* Cor escura para dentro do card branco */
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

    /* 6. Estilo do Botão Azul 'Entrar' */
    div.stButton > button {
        background-color: #006ce6 !important; /* Azul original */
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-top: 15px !important;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #005bb5 !important; /* Azul mais escuro no hover */
    }

    /* 7. Estilo do Link 'Esqueci a password' */
    .forgot-password {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #718096;
        cursor: pointer;
    }

    /* 8. Esconder elementos nativos do Streamlit que quebram o design */
    div[data-testid="stHeader"] {display:none;}
    div[data-testid="stSidebarNav"] {display:none;}
    footer {display:none;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# --- INICIALIZAÇÃO DE BASE DE DADOS EM MEMÓRIA ---
# (Para testes, o utilizador padrão)
# =========================================================
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234" 
    }

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# =========================================================
# --- LÓGICA DO ECRÃ DE LOGIN ---
# =========================================================

# Só mostra o login se ninguém estiver logado
if st.session_state.usuario_logado is None:

    # --- HEADER FORA DO CARD (TÍTULOS BRANCOS SOBRE AZUL) ---
    st.markdown("""
        <div class="header-text">
            <h2>Smarthome SPNOS</h2>
            <p>Acede à tua área de obras e checklists</p>
        </div>
    """, unsafe_allow_html=True)

    # --- INÍCIO DO CARD BRANCO CENTRAL (Com logins) ---
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Abas nativas Entrar / Registar
    aba_login, aba_registro = st.tabs(["         Entrar         ", "         Registar         "])
    
    # -- Conteúdo da Aba 'Entrar' --
    with aba_login:
        st.write(" ") # Pequeno espaçamento
        # Inputs nativos do Streamlit estilizados pelo CSS acima
        email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
        pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
        
        st.write(" ") # Espaçamento antes do botão
        # Botão 'Entrar'
        if st.button("Entrar", use_container_width=True, key="btn_login"):
            # Validação simples
            if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                st.session_state.usuario_logado = email_input
                st.success("Login efetuado com sucesso!")
                st.rerun() # Atualiza para entrar na área protegida
            else:
                st.error("Email ou Palavra-passe incorretos.")
                
        # Link de 'Esqueci'
        st.markdown("<p class='forgot-password'>Esqueci a password</p>", unsafe_allow_html=True)
        
    # -- Conteúdo da Aba 'Registar' (Simplificado para o exemplo) --
    with aba_registro:
        st.write(" ")
        novo_email = st.text_input("Novo Email", placeholder="exemplo@parceiros.nos.pt", key="reg_email")
        nova_pass = st.text_input("Criar Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
        
        st.write(" ")
        if st.button("Criar Conta", use_container_width=True, key="btn_register"):
            if not novo_email or not nova_pass:
                st.error("Preencha todos os campos.")
            elif novo_email in st.session_state.usuarios:
                st.error("Este email já está registado.")
            else:
                st.session_state.usuarios[novo_email] = nova_pass
                st.success("Conta criada! Alterne para a aba 'Entrar'.")
                
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Card Branco

# =========================================================
# --- ÁREA LOGADA (SISTEMA DE OBRAS) ---
# =========================================================
else:
    # Se logado, muda para a interface de trabalho clara
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        label, div[data-testid="stMarkdownContainer"] p { color: #333333 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Header da Área de Trabalho
    col_logo, col_user = st.columns([2, 1.5])
    with col_logo:
        st.subheader("🔷 Smarthome SPNOS")
    with col_user:
        user_email = st.session_state.usuario_logado
        st.write(f"<div style='text-align: right; font-size: 13px; color: #6c757d; margin-bottom:5px;'>{user_email}</div>", unsafe_allow_html=True)
        if st.button("Sair da Conta", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.write("---")
    
    # Exemplo simples de conteúdo da área de obras
    st.title("Obras")
    st.markdown("Bem-vindo à área de gestão de obras. Utilize as checklists abaixo para monitorizar o progresso.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🚧 Obra: Terramar, Lote 5")
        st.checkbox("Instalar Switches Shelly 1PM", value=True)
        st.checkbox("Configurar Home Assistant")
        st.checkbox("Testar CCTV")
    with col2:
        st.info("🚧 Obra: Lidador, Piso 2")
        st.checkbox("FTTH Fibra Óptica")
        st.checkbox("Automatizar Estores", value=True)
