import streamlit as st

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Smarthome SPNOS - Técnico",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# --- BASE DE DADOS EM MEMÓRIA (Session State) ---
# ==========================================
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234"
    }

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# Base de dados simulada de obras e checklists de domótica
if 'obras' not in st.session_state:
    st.session_state.obras = {
        "Apartamento 302 - Bloco A": {
            "estado": "Em Progresso",
            "checklist": {
                "Instalar Shelly Wave 1PM Mini na iluminação": True,
                "Configurar Gateway/Painel Central": False,
                "Testar sensores de segurança e alarmes": False,
                "Validar integração no Home Assistant": False
            }
        },
        "Apartamento 105 - Premium": {
            "estado": "Pendente",
            "checklist": {
                "Passagem de cablagem/Fibra ótica": False,
                "Instalação de tomadas inteligentes": False,
                "Configuração de cenários de domótica": False,
                "Testes de carga e monitorização de energia": False
            }
        },
        "Apartamento 44 - Cobertura": {
            "estado": "Concluída",
            "checklist": {
                "Instalar automação de estores": True,
                "Configurar controlo de acessos QR Code": True,
                "Sincronizar câmaras IP com o NVR": True,
                "Formação de utilização ao cliente": True
            }
        }
    }

# ==========================================
# --- LÓGICA DE INTERFACE (Ecrãs) ---
# ==========================================

# --- 1. ECRÃ DE LOGIN ---
if st.session_state.usuario_logado is None:
    
    # CSS Customizado para o Login (Fundo Azul Integral)
    st.markdown("""
        <style>
        .stApp {
            background-color: #0084d6 !important;
        }
        div[data-testid="stHeader"] { display: none !important; }
        footer { display: none !important; }
        
        .header-container {
            text-align: center;
            margin-top: 3rem;
            margin-bottom: 2rem;
            color: #ffffff;
        }
        .header-container h1 {
            font-weight: bold;
            font-size: 32px;
            color: #ffffff !important;
        }
        .header-container p {
            font-size: 15px;
            opacity: 0.9;
            color: #ffffff !important;
        }
        
        /* Estilos do formulário de login */
        label, div[data-testid="stMarkdownContainer"] p {
            color: #4a5568 !important;
            font-weight: 500 !important;
        }
        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            color: #222222 !important;
            border: 1px solid #dcdfe6 !important;
            border-radius: 8px !important;
            height: 45px !important;
        }
        div.stButton > button {
            background-color: #006ce6 !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            border: none !important;
            height: 50px !important;
            width: 100% !important;
            font-weight: bold !important;
            font-size: 16px !important;
            margin-top: 10px !important;
        }
        div.stButton > button:hover {
            background-color: #005bb5 !important;
        }
        .forgot-password {
            text-align: center;
            margin-top: 15px;
            font-size: 14px;
            color: #ecf0f1 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="header-container">
            <h1>Smarthome SPNOS</h1>
            <p>Acede à tua área de obras e checklists</p>
        </div>
    """, unsafe_allow_html=True)

    # Abas Entrar / Registar
    aba_login, aba_registro = st.tabs(["         Entrar         ", "         Registar         "])
    
    with aba_login:
        with st.form(key="formulario_login", clear_on_submit=False):
            email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
            pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
            
            submetido = st.form_submit_button("Entrar", use_container_width=True)
            
            if submetido:
                if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                    st.session_state.usuario_logado = email_input
                    st.rerun()
                else:
                    st.error("Email ou Palavra-passe incorretos.")
                    
        st.markdown("<p class='forgot-password'>Esqueci a password</p>", unsafe_allow_html=True)
        
    with aba_registro:
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

# --- 2. ÁREA PROTEGIDA (GESTÃO DE OBRAS E CHECKLISTS) ---
else:
    # Resetar o estilo para o painel de trabalho (Fundo Claro)
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        label, div[data-testid="stMarkdownContainer"] p { color: #333333 !important; }
        .obra-card {
            background-color: #ffffff;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-top: 15px;
            margin-bottom: 10px;
            border-left: 5px solid #0084d6;
        }
        .obra-card h3 {
            margin: 0px !important;
            color: #1a202c !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Barra Superior / Header do Painel
    col_logo, col_logout = st.columns([3, 1])
    with col_logo:
        st.subheader("🔷 Painel Técnico - SPNOS")
    with col_logout:
        if st.button("Sair ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.write(f"*Sessão iniciada como: {st.session_state.usuario_logado}*")
    st.divider()

    st.title("📋 Gestão de Obras e Intervenções")
    st.write("Seleciona e atualiza o estado dos apartamentos e valida as tarefas de domótica em curso.")
    st.write(" ")

    # --- LISTAGEM DE OBRAS ---
    for nome_obra, dados in st.session_state.obras.items():
        
        # 1. Título do Apartamento dentro do Card Estilizado
        st.markdown(f"""
        <div class="obra-card">
            <h3>🏠 {nome_obra}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Colunas para o Estado e Progresso
        col_estado, col_progresso = st.columns([1, 1])
        
        with col_estado:
            lista_estados = ["Pendente", "Em Progresso", "Concluída"]
            indice_atual = lista_estados.index(dados["estado"]) if dados["estado"] in lista_estados else 0
            
            novo_estado = st.selectbox(
                "Estado da Obra",
                options=lista_estados,
                index=indice_atual,
                key=f"estado_{nome_obra}"
            )
            st.session_state.obras[nome_obra]["estado"] = novo_estado

        with col_progresso:
            total_tarefas = len(dados["checklist"])
            tarefas_concluidas = sum(1 for concluida in dados["checklist"].values() if concluida)
            percentagem = tarefas_concluidas / total_tarefas if total_tarefas > 0 else 0.0
            
            st.write("Progresso técnico:")
            st.progress(percentagem)
            st.caption(f"{tarefas_concluidas} de {total_tarefas} tarefas validadas.")

        # 3. Secção da Checklist
        st.markdown("**Checklist de Instalação:**")
        
        tarefas = list(dados["checklist"].keys())
        for tarefa in tarefas:
            concluida = dados["checklist"][tarefa]
            chave_tarefa = f"chk_{nome_obra}_{tarefa}"
            
            status_tarefa = st.checkbox(
                tarefa, 
                value=concluida, 
                key=chave_tarefa
            )
            st.session_state.obras[nome_obra]["checklist"][tarefa] = status_tarefa
        
        # Linha divisória limpa entre apartamentos
        st.divider()
