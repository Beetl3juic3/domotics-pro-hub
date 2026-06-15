import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Smarthome SPNOS", page_icon="📱", layout="centered")

# --- FORÇAR DESIGN EXATAMENTE IGUAL AO ORIGINAL ---
st.markdown("""
    <style>
    /* Forçar o fundo azul da página apenas no ecrã de login se não estiver logado */
    .stApp {
        background-color: #f8f9fa; /* Fundo padrão claro para a app */
    }
    
    /* Quando não está logado, vamos pintar o fundo de azul vivo */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa;
    }
    
    /* Card Branco Central do Login */
    .login-container {
        background-color: #ffffff !important;
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
        max-width: 480px;
        margin: 0 auto;
        border: 1px solid #eef0f3;
    }
    
    /* Ajustar inputs do Streamlit para ficarem brancos com borda cinza clara */
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdfe6 !important;
        border-radius: 8px !important;
        height: 42px;
    }
    
    /* Forçar texto das etiquetas em preto/cinza escuro */
    label {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    /* Estilo dos Cards de Obras e Apartamentos */
    .card-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e6e9ef;
        margin-bottom: 12px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.01);
    }
    
    .subtext {
        color: #8c939f;
        font-size: 13px;
    }
    
    /* Customização das abas de login para parecerem botões ovais */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #eef2f7;
        padding: 4px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 6px 16px;
        color: #4a5568;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        color: #1a202c !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA BASE DE DADOS EM MEMÓRIA ---
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234" 
    }

if 'obras_data' not in st.session_state:
    st.session_state.obras_data = {
        "Terramar": {
            "modificado_por": "marco.a.ramires",
            "data_modificacao": "12/05/2026",
            "apartamentos": {
                "A1": {"estado": "Concluída", "modificado_por": "marco.a.ramires", "data": "15/06/2026", "tarefas": [{"texto": "Falta instalar cilindro e a fechadura", "feita": True, "autor": "marco.a.ramires", "data": "15/06/2026"}]},
                "F1": {"estado": "Concluída", "modificado_por": "marco.a.ramires", "data": "12/05/2026", "tarefas": []},
                "B1": {"estado": "Concluída", "modificado_por": "marco.a.ramires", "data": "12/05/2026", "tarefas": []},
                "D1": {"estado": "Concluída", "modificado_por": "marco.a.ramires", "data": "12/05/2026", "tarefas": []},
                "E2": {"estado": "Em curso", "modificado_por": "marco.a.ramires", "data": "12/05/2026", "tarefas": []}
            }
        },
        "Lidador": {
            "modificado_por": "marco.a.ramires",
            "data_modificacao": "12/05/2026",
            "apartamentos": {}
        }
    }

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None
if 'obra_selecionada' not in st.session_state:
    st.session_state.obra_selecionada = None
if 'ap_selecionado' not in st.session_state:
    st.session_state.ap_selecionado = None

# ==========================================
# ECRÃ DE LOGIN ESTILIZADO (Igual à imagem anterior)
# ==========================================
if st.session_state.usuario_logado is None:
    # Injetar o fundo azul vivo apenas neste ecrã
    st.markdown("<style>[data-testid='stAppViewContainer'] { background-color: #0084d6 !important; }</style>", unsafe_allow_html=True)
    
    st.write("<div style='padding-top: 5vh;'></div>", unsafe_allow_html=True)
    
    # Início do Bloco Branco Central
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logotipo Azul Redondo
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
            <div style='background-color:#006ce6; width:60px; height:60px; border-radius:14px; display:flex; align-items:center; justify-content:center; margin: 0 auto 15px auto; color:white; font-size:28px; font-weight:bold; line-height:60px; text-align:center;'>
            ⚙️
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align: center; color: #1a202c; font-weight: 600; margin-bottom: 0;'>Smarthome SPNOS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096; font-size: 14px; margin-top: 5px; margin-bottom: 25px;'>Acede à tua área de obras e checklists</p>", unsafe_allow_html=True)
    
    aba_login, aba_registro = st.tabs(["         Entrar         ", "         Registar         "])
    
    with aba_login:
        st.write(" ")
        email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
        pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
        st.write(" ")
        
        if st.button("Entrar", use_container_width=True, type="primary"):
            if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                st.session_state.usuario_logado = email_input
                st.error("") # Limpa avisos
                st.rerun()
            else:
                st.error("Email ou Palavra-passe incorretos.")
                
        st.markdown("<p style='text-align:center; font-size:13px; color:#718096; margin-top:20px;'>Esqueci a password</p>", unsafe_allow_html=True)
        
    with aba_registro:
        st.write(" ")
        novo_email = st.text_input("Email", placeholder="exemplo@parceiros.nos.pt", key="reg_email")
        nova_pass = st.text_input("Criar Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
        
        if st.button("Criar Conta", use_container_width=True, type="primary"):
            if novo_email and nova_pass:
                st.session_state.usuarios[novo_email] = nova_pass
                st.success("Conta criada! Alterne para 'Entrar'.")
            else:
                st.error("Preencha os campos.")
                
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Bloco Branco

# ==========================================
# ÁREA LOGADA (SISTEMA DE GESTÃO DE OBRAS - FUNDO CLARO)
# ==========================================
else:
    col_logo, col_user = st.columns([2, 1.5])
    with col_logo:
        st.markdown("<h3 style='color:#1a202c; margin:0;'>Smarthome SPNOS</h3>", unsafe_allow_html=True)
    with col_user:
        user_clean = st.session_state.usuario_logado.split('@')[0]
        st.write(f"<div style='text-align: right; font-size: 13px; color: #4a5568;'>{st.session_state.usuario_logado} &nbsp;|&nbsp; <a href='javascript:window.location.reload();' style='color:#006ce6; text-decoration:none;'>Sair</a></div>", unsafe_allow_html=True)
        if st.button("Sair da Conta", key="act_logout"):
            st.session_state.usuario_logado = None
            st.rerun()
            
    st.markdown("<hr style='margin-top:10px; margin-bottom:20px; border-color:#e2e8f0;'>", unsafe_allow_html=True)
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    # ECRÃ 3: DETALHES DO APARTAMENTO
    if st.session_state.obra_selecionada and st.session_state.ap_selecionado:
        obra = st.session_state.obra_selecionada
        ap = st.session_state.ap_selecionado
        ap_info = st.session_state.obras_data[obra]["apartamentos"][ap]
        
        if st.button("← Voltar à obra"):
            st.session_state.ap_selecionado = None
            st.rerun()
            
        st.markdown(f"<h1 style='color:#1a202c; margin-bottom:0;'>{ap}</h1>", unsafe_allow_html=True)
        
        total_t = len(ap_info["tarefas"])
        concluidas_t = sum(1 for t in ap_info["tarefas"] if t["feita"])
        st.markdown(f"<div class='subtext'>{concluidas_t} / {total_t} tarefas concluídas</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtext' style='margin-bottom:15px;'>Última alteração: {ap_info['modificado_por']} · {ap_info['data']}</div>", unsafe_allow_html=True)
        
        novo_estado = st.selectbox("Estado:", ["Planeado", "Em curso", "Concluída"], index=["Planeado", "Em curso", "Concluída"].index(ap_info["estado"]))
        if novo_estado != ap_info["estado"]:
            st.session_state.obras_data[obra]["apartamentos"][ap]["estado"] = novo_estado
            st.session_state.obras_data[obra]["apartamentos"][ap]["modificado_por"] = user_clean
            st.session_state.obras_data[obra]["apartamentos"][ap]["data"] = data_hoje
            st.rerun()

        st.markdown("<div class='card-box'><h5>Checklist</h5>", unsafe_allow_html=True)
        col_t_in, col_t_btn = st.columns([5, 1])
        with col_t_in:
            nova_tarefa_txt = st.text_input("Adicionar tarefa...", key="input_nova_tarefa", label_visibility="collapsed", placeholder="Adicionar tarefa...")
        with col_t_btn:
            if st.button("＋", key="btn_add_tarefa", use_container_width=True):
                if nova_tarefa_txt:
                    st.session_state.obras_data[obra]["apartamentos"][ap]["tarefas"].append({
                        "texto": nova_tarefa_txt, "feita": False, "autor": user_clean, "data": data_hoje
                    })
                    st.rerun()
                        
        for idx, t in enumerate(ap_info["tarefas"]):
            col_chk, col_txt = st.columns([1, 10])
            with col_chk:
                status_chk = st.checkbox("", value=t["feita"], key=f"chk_{idx}")
                if status_chk != t["feita"]:
                    st.session_state.obras_data[obra]["apartamentos"][ap]["tarefas"][idx]["feita"] = status_chk
                    st.session_state.obras_data[obra]["apartamentos"][ap]["modificado_por"] = user_clean
                    st.session_state.obras_data[obra]["apartamentos"][ap]["data"] = data_hoje
                    st.rerun()
            with col_txt:
                if t["feita"]:
                    st.markdown(f"~~{t['texto']}~~ <span class='subtext'>— {t['autor']} · {t['data']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{t['texto']} <span class='subtext'>— {t['autor']} · {t['data']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ECRÃ 2: APARTAMENTOS
    elif st.session_state.obra_selecionada:
        obra = st.session_state.obra_selecionada
        obra_info = st.session_state.obras_data[obra]
        
        if st.button("← Todas as obras"):
            st.session_state.obra_selecionada = None
            st.rerun()
            
        st.markdown(f"<h1 style='color:#1a202c; margin-bottom:0;'>{obra}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtext' style='margin-bottom:15px;'>{len(obra_info['apartamentos'])} apartamento(s)</div>", unsafe_allow_html=True)
        
        col_ap_in, col_ap_btn = st.columns([4, 1])
        with col_ap_in:
            novo_ap = st.text_input("Nome do apartamento (ex: Bloco A · 3ºD)", key="new_ap_input", label_visibility="collapsed", placeholder="Nome do apartamento (ex: Bloco A · 3ºD)")
        with col_ap_btn:
            if st.button("＋ Novo", use_container_width=True):
                if novo_ap and novo_ap not in obra_info["apartamentos"]:
                    st.session_state.obras_data[obra]["apartamentos"][novo_ap] = {
                        "estado": "Em curso", "modificado_por": user_clean, "data": data_hoje, "tarefas": []
                    }
                    st.rerun()
                    
        st.write(" ")
        for ap_nome, ap_detalhes in obra_info["apartamentos"].items():
            st.markdown(f'<div class="card-box">', unsafe_allow_html=True)
            col_icon, col_info, col_status, col_go = st.columns([1, 4, 2, 1])
            with col_icon:
                st.markdown("<h3 style='margin:0;'>🏢</h3>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"<b style='color:#1a202c;'>{ap_nome}</b>", unsafe_allow_html=True)
                st.markdown(f"<div class='subtext'>{ap_detalhes['data']}</div>", unsafe_allow_html=True)
            with col_status:
                cor = "#006ce6" if ap_detalhes['estado'] == "Concluída" else "#e69500"
                st.markdown(f"<span style='background-color:{cor}; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:bold;'>{ap_detalhes['estado']}</span>", unsafe_allow_html=True)
            with col_go:
                if st.button("➔", key=f"go_{ap_nome}"):
                    st.session_state.ap_selecionado = ap_nome
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ECRÃ 1: LISTAGEM GERAL
    else:
        st.markdown("<h1 style='color:#1a202c; margin-bottom:0;'>Obras</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#718096; margin-bottom:20px;'>Cada obra (ex: Terramar) contém os seus apartamentos.</p>", unsafe_allow_html=True)
        
        col_in, col_btn = st.columns([4, 1])
        with col_in:
            nova_obra_nome = st.text_input("Nome da obra", key="new_obra_input", label_visibility="collapsed", placeholder="Nome da obra (ex: Terramar)")
        with col_btn:
            if st.button("＋ Nova obra", use_container_width=True):
                if nova_obra_nome and nova_obra_nome not in st.session_state.obras_data:
                    st.session_state.obras_data[nova_obra_nome] = {
                        "modificado_por": user_clean, "data_modificacao": data_hoje, "apartamentos": {}
                    }
                    st.rerun()
                    
        st.write(" ")
        for nome_obra, info_obra in st.session_state.obras_data.items():
            st.markdown(f'<div class="card-box">', unsafe_allow_html=True)
            col_icon, col_txt, col_arrow = st.columns([1, 5, 1])
            with col_icon:
                st.markdown("<h3 style='margin:0;'>🏗️</h3>", unsafe_allow_html=True)
            with col_txt:
                st.markdown(f"<b style='color:#1a202c;'>{nome_obra}</b>", unsafe_allow_html=True)
                st.markdown(f"<div class='subtext'>Modificado por {info_obra['modificado_por']} · {info_obra['data_modificacao']}</div>", unsafe_allow_html=True)
            with col_arrow:
                if st.button("➔", key=f"view_{nome_obra}"):
                    st.session_state.obra_selecionada = nome_obra
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
