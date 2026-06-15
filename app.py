import streamlit as st

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Smarthome SPNOS - Técnico",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="auto"
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

# --- 1. ECRÃ DE LOGIN (ESTILO MINIMALISTA) ---
if st.session_state.usuario_logado is None:
    
    # CSS Minimalista: Fundo limpo, cantos suaves e tons neutros
    st.markdown("""
        <style>
        /* Fundo geral limpo e cinza ultra-claro */
        .stApp {
            background-color: #fafafa !important;
        }
        div[data-testid="stHeader"] { display: none !important; }
        footer { display: none !important; }
        
        /* Cabeçalho Minimalista */
        .header-container {
            text-align: center;
            margin-top: 4rem;
            margin-bottom: 1.5rem;
        }
        .header-container h1 {
            font-weight: 300;
            font-size: 28px;
            color: #2d3748 !important;
            letter-spacing: -0.5px;
        }
        .header-container p {
            font-size: 14px;
            color: #718096 !important;
            margin-top: -5px;
        }
        
        /* Inputs elegantes */
        label, div[data-testid="stMarkdownContainer"] p {
            color: #4a5568 !important;
            font-weight: 500 !important;
            font-size: 14px;
        }
        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            color: #2d3748 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 6px !important;
            height: 42px !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4a5568 !important;
            box-shadow: none !important;
        }
        
        /* Botão Principal discreto */
        div.stButton > button {
            background-color: #2d3748 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: none !important;
            height: 42px !important;
            width: 100% !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            margin-top: 15px !important;
            transition: background 0.2s;
        }
        div.stButton > button:hover {
            background-color: #1a202c !important;
            color: #ffffff !important;
        }
        
        /* Abas Estilizadas */
        div[data-testid="stTabs"] button {
            font-size: 14px !important;
            color: #718096 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #2d3748 !important;
            font-weight: 600;
        }
        
        .forgot-password {
            text-align: center;
            margin-top: 20px;
            font-size: 13px;
            color: #a0aec0 !important;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="header-container">
            <h1>Smarthome SPNOS</h1>
            <p>Plataforma de Gestão Técnica</p>
        </div>
    """, unsafe_allow_html=True)

    # Centralizar o formulário no ecrã de forma limpa
    col_central, _ = st.columns([1, 0.01]) # Truque para manter o alinhamento focado
    
    with col_central:
        aba_login, aba_registro = st.tabs(["Entrar", "Criar Conta"])
        
        with aba_login:
            with st.form(key="formulario_login", clear_on_submit=False):
                email_input = st.text_input("Email", placeholder="nome@exemplo.pt", key="login_email")
                pass_input = st.text_input("Palavra-passe", type="password", placeholder="••••••••", key="login_pass")
                submetido = st.form_submit_button("Aceder ao Painel", use_container_width=True)
                
                if submetido:
                    if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                        st.session_state.usuario_logado = email_input
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas.")
                        
            st.markdown("<p class='forgot-password'>Recuperar palavra-passe</p>", unsafe_allow_html=True)
            
        with aba_registro:
            novo_email = st.text_input("Email Profissional", placeholder="nome@parceiros.nos.pt", key="reg_email")
            nova_pass = st.text_input("Definir Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
            
            if st.button("Registar Técnico", use_container_width=True):
                if not novo_email or not nova_pass:
                    st.error("Por favor, preencha todos os campos.")
                elif novo_email in st.session_state.usuarios:
                    st.error("Este utilizador já se encontra registado.")
                else:
                    st.session_state.usuarios[novo_email] = nova_pass
                    st.success("Registo efetuado com sucesso!")

# --- 2. ÁREA PROTEGIDA (GESTÃO DE OBRAS E CHECKLISTS) ---
else:
    # Estilização do Painel de Trabalho (Mantém-se limpo e profissional)
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        label, div[data-testid="stMarkdownContainer"] p { color: #333333 !important; }
        .obra-card {
            background-color: #ffffff; padding: 15px 20px; border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-top: 15px; margin-bottom: 10px;
            border-left: 5px solid #0084d6;
        }
        .obra-card h3 { margin: 0px !important; color: #1a202c !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- MENU LATERAL (SIDEBAR) PARA ADICIONAR/MODIFICAR OBRAS ---
    with st.sidebar:
        st.header("⚙️ Painel de Administração")
        
        st.subheader("➕ Nova Obra / Apartamento")
        with st.form("criar_obra_form", clear_on_submit=True):
            nova_obra_nome = st.text_input("Nome do Apartamento", placeholder="Ex: Apartamento 501 - Bloco B")
            estado_inicial = st.selectbox("Estado Inicial", ["Pendente", "Em Progresso", "Concluída"])
            
            st.write("Tarefas Iniciais (uma por linha):")
            tarefas_texto = st.text_area("Tarefas", value="Instalar Shelly Wave 1PM Mini\nValidar no Home Assistant", height=100)
            
            botao_criar = st.form_submit_button("Criar Obra", use_container_width=True)
            
            if botao_criar and nova_obra_nome:
                if nova_obra_nome not in st.session_state.obras:
                    lista_t = [t.strip() for t in tarefas_texto.split("\n") if t.strip()]
                    dict_checklist = {t: False for t in lista_t}
                    
                    st.session_state.obras[nova_obra_nome] = {
                        "estado": estado_inicial,
                        "checklist": dict_checklist
                    }
                    st.success(f"{nova_obra_nome} adicionado!")
                    st.rerun()
                else:
                    st.error("Essa obra já existe!")

        st.divider()
        
        if st.session_state.obras:
            st.subheader("📝 Modificar / Eliminar")
            obra_selecionada = st.selectbox("Escolha a Obra", list(st.session_state.obras.keys()))
            
            nova_tarefa_avulsa = st.text_input("Adicionar tarefa a esta obra", placeholder="Ex: Sincronizar alarmes")
            if st.button("Adicionar Tarefa", use_container_width=True) and nova_tarefa_avulsa:
                st.session_state.obras[obra_selecionada]["checklist"][nova_tarefa_avulsa] = False
                st.success("Tarefa adicionada!")
                st.rerun()

            st.write("---")
            if st.button("🗑️ Eliminar Obra Selecionada", type="primary", use_container_width=True):
                del st.session_state.obras[obra_selecionada]
                st.warning(f"Obra {obra_selecionada} removida.")
                st.rerun()

    # Barra Superior do Painel Principal
    col_logo, col_logout = st.columns([3, 1])
    with col_logo:
        st.subheader("🔷 Painel Técnico - SPNOS")
    with col_logout:
        if st.button("Sair ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.write(f"*Sessão iniciada como: {st.session_state.usuario_logado}*")
    st.caption("👈 Abre a barra lateral esquerda (Sidebar) para criar, modificar ou apagar obras e tarefas.")
    st.divider()

    st.title("📋 Gestão de Obras e Intervenções")
    st.write("Seleciona e atualiza o estado dos apartamentos e valida as tarefas de domótica em curso.")
    st.write(" ")

    # --- LISTAGEM DE OBRAS ---
    for nome_obra, dados in st.session_state.obras.items():
        
        st.markdown(f"""
        <div class="obra-card">
            <h3>🏠 {nome_obra}</h3>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        st.divider()
