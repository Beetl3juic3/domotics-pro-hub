import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração Inicial da Página ---
st.set_page_config(
    page_title="Smarthome SPNOS",
    page_icon="📱",
    layout="wide",  # Mudado para wide para a tabela de obras ter mais espaço
    initial_sidebar_state="collapsed"
)

# ==========================================
# --- BASE DE DADOS EM MEMÓRIA (SESSIONS) ---
# ==========================================
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234" 
    }

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# Base de dados simulada para as tuas obras e checklists
if 'lista_obras' not in st.session_state:
    st.session_state.lista_obras = [
        {"ID Obra": "OBR-2026-001", "Data": "2026-06-10", "Tipo": "Fibra Óptica (FTTH)", "Estado": "Concluído", "Técnico": "marco.a.ramires"},
        {"ID Obra": "OBR-2026-002", "Data": "2026-06-14", "Tipo": "Domótica (Shelly/Home Assistant)", "Estado": "Em Curso", "Técnico": "marco.a.ramires"},
        {"ID Obra": "OBR-2026-003", "Data": "2026-06-15", "Tipo": "Sistemas de Alarme & CCTV", "Estado": "Pendente", "Técnico": "marco.a.ramires"}
    ]

# ==========================================
# --- LÓGICA DE TELAS ---
# ==========================================

# 1. ECRÃ DE LOGIN
if st.session_state.usuario_logado is None:
    
    st.markdown("""
        <style>
        .stApp { background-color: #0084d6 !important; }
        div[data-testid="stHeader"] { display: none !important; }
        div[data-testid="stSidebarNav"] { display: none !important; }
        footer { display: none !important; }
        
        .header-container { text-align: center; margin-top: 3rem; margin-bottom: 1.5rem; }
        .header-container h1 { font-weight: 700; font-size: 32px; color: #ffffff !important; margin-bottom: 5px; }
        .header-container p { font-size: 15px; color: #e2e8f0 !important; opacity: 0.9; }
        
        .login-card { background-color: #ffffff; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); margin-bottom: 2rem; }
        .login-card label, .login-card p { color: #2d3748 !important; }
        
        button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 600 !important; color: #a0aec0 !important; border-bottom-width: 2px !important; }
        button[aria-selected="true"] { color: #0084d6 !important; border-bottom-color: #0084d6 !important; }
        
        div[data-testid="stTextInput"] input { background-color: #f7fafc !important; color: #1a202c !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; height: 48px !important; }
        div[data-testid="stTextInput"] input:focus { border-color: #0084d6 !important; box-shadow: 0 0 0 1px #0084d6 !important; }
        div[data-testid="stTextInput"] label p { color: #4a5568 !important; font-weight: 600 !important; }

        div.stButton > button { background-color: #0072c6 !important; color: #ffffff !important; border-radius: 10px !important; border: none !important; height: 48px !important; width: 100% !important; font-weight: 600; margin-top: 15px !important; }
        div.stButton > button:hover { background-color: #005ea5 !important; }
        </style>
    """, unsafe_allow_html=True)

    st.write("<div style='padding-top: 2vh;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="header-container"><h1>Smarthome SPNOS</h1><p>Acede à tua área de obras e checklists</p></div>', unsafe_allow_html=True)

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

# 2. ÁREA LOGADA - GESTÃO DE OBRAS ATIVA
else:
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa !important; }
        div[data-testid="stHeader"] { display: block !important; }
        h1, h2, h3, p, label, span { color: #1a202c !important; }
        
        .logout-container button {
            background-color: #dc3545 !important;
            color: white !important;
            border-radius: 6px !important;
            height: 38px !important;
            font-size: 14px !important;
            margin-top: 8px !important;
            border: none !important;
        }
        .logout-container button:hover { background-color: #bd2130 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Topo da App
    col_logo, col_logout = st.columns([4, 1])
    with col_logo:
        st.markdown("<h2 style='margin:0;'>🔷 Painel Smarthome SPNOS</h2>", unsafe_allow_html=True)
    with col_logout:
        st.markdown('<div class="logout-container">', unsafe_allow_html=True)
        if st.button("Sair da Conta ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.write("---")
    
    user_email = st.session_state.usuario_logado
    nome_tecnico = user_email.split('@')[0]
    
    # Layout de duas colunas para a Área de Trabalho: Esquerda (Nova Obra) | Direita (Lista de Obras)
    col_form, col_tabela = st.columns([1, 2])
    
    with col_form:
        st.subheader("📝 Nova Checklist / Obra")
        with st.form("form_nova_obra", clear_on_submit=True):
            id_obra = st.text_input("ID da Obra / Serviço", placeholder="Ex: OBR-2026-X")
            tipo_obra = st.selectbox("Tipo de Intervenção", [
                "Fibra Óptica (FTTH)", 
                "Domótica (Shelly/Home Assistant)", 
                "Sistemas de Alarme & CCTV"
            ])
            estado_obra = st.selectbox("Estado Inicial", ["Pendente", "Em Curso", "Concluído"])
            
            submetido = st.form_submit_button("Registar Obra")
            if submetido:
                if id_obra.strip() == "":
                    st.error("Por favor, insira um ID de Obra válido.")
                else:
                    nova_obra = {
                        "ID Obra": id_obra,
                        "Data": datetime.now().strftime("%Y-%m-%d"),
                        "Tipo": tipo_obra,
                        "Estado": estado_obra,
                        "Técnico": nome_tecnico
                    }
                    st.session_state.lista_obras.append(nova_obra)
                    st.success(f"Obra {id_obra} adicionada com sucesso!")
                    st.rerun()

    with col_tabela:
        st.subheader("📋 Obras e Checklists Ativas")
        
        # Filtros Rápidos
        filtro_estado = st.multiselect("Filtrar por Estado:", ["Pendente", "Em Curso", "Concluído"], default=["Pendente", "Em Curso", "Concluído"])
        
        # Converter para DataFrame para mostrar de forma bonita
        if st.session_state.lista_obras:
            df_obras = pd.DataFrame(st.session_state.lista_obras)
            
            # Aplicar o filtro de estado
            df_filtrado = df_obras[df_obras["Estado"].isin(filtro_estado)]
            
            if not df_filtrado.empty:
                # Exibe a tabela interativa do Streamlit
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                
                # Resumo rápido
                st.metric(label="Total de Obras Visualizadas", value=len(df_filtrado))
            else:
                st.info("Nenhuma obra encontrada para os filtros selecionados.")
        else:
            st.info("Ainda não tens nenhuma obra registada na base de dados.")
