import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Smarthome SPNOS", page_icon="📱", layout="centered")

# --- DESIGN E ESTILIZAÇÃO CUSTOMIZADA (Fundo Azul + Card de Login) ---
st.markdown("""
    <style>
    /* Estilo Geral */
    .stApp {
        background-color: #0084d6;
    }
    .main-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
        color: #333333;
    }
    .card-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e6e9ef;
        margin-bottom: 10px;
        color: #333333;
    }
    .subtext {
        color: #6c757d;
        font-size: 12px;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: inherit;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA BASE DE DADOS EM MEMÓRIA ---
if 'usuarios' not in st.session_state:
    # Utilizador padrão sugerido na imagem
    st.session_state.usuarios = {
        "marco.a.ramires@parceiros.nos.pt": "1234" 
    }

if 'obras_data' not in st.session_state:
    st.session_state.obras_data = {
        "Terramar": {
            "modificado_por": "marco.a.ramires@parceiros.nos.pt",
            "data_modificacao": "12/05/2026",
            "apartamentos": {
                "A1": {"estado": "Concluída", "modificado_por": "marco.a.ramires@parceiros.nos.pt", "data": "15/06/2026", "tarefas": [{"texto": "Falta instalar cilindro e a fechadura", "feita": True, "autor": "marco.a.ramires@parceiros.nos.pt", "data": "15/06/2026"}]},
                "F1": {"estado": "Concluída", "modificado_por": "marco.a.ramires@parceiros.nos.pt", "data": "12/05/2026", "tarefas": []},
                "B1": {"estado": "Concluída", "modificado_por": "marco.a.ramires@parceiros.nos.pt", "data": "12/05/2026", "tarefas": []}
            }
        },
        "Lidador": {
            "modificado_por": "marco.a.ramires@parceiros.nos.pt",
            "data_modificacao": "12/05/2026",
            "apartamentos": {}
        }
    }

# Estados de sessão para Login e Navegação
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None
if 'obra_selecionada' not in st.session_state:
    st.session_state.obra_selecionada = None
if 'ap_selecionado' not in st.session_state:
    st.session_state.ap_selecionado = None


# ==========================================
# ECRÃ DE LOGIN (image_76abe1.png)
# ==========================================
if st.session_state.usuario_logado is None:
    
    # Centralizar o card de login verticalmente de forma simples
    st.write("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Ícone e Título
    col_logo, _ = st.columns([1, 4])
    with col_logo:
        st.markdown("<div style='background-color:#0066cc; padding:12px; border-radius:12px; text-align:center; color:white; font-size:24px; font-weight:bold;'>📱</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-top:-10px;'>Smarthome SPNOS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d;'>Acede à tua área de obras e checklists</p>", unsafe_allow_html=True)
    
    # Abas Entrar / Registar igual à imagem
    aba_login, aba_registro = st.tabs(["Entrar", "Registar"])
    
    with aba_login:
        email_input = st.text_input("Email", placeholder="Insira o seu email", key="login_email")
        pass_input = st.text_input("Palavra-passe", type="password", placeholder="Insira a sua password", key="login_pass")
        
        if st.button("Entrar", use_container_width=True, type="primary"):
            if email_input in st.session_state.usuarios and st.session_state.usuarios[email_input] == pass_input:
                st.session_state.usuario_logado = email_input
                st.rerun()
            else:
                st.error("Email ou Palavra-passe incorretos.")
                
        st.markdown("<p style='text-align:center; font-size:13px; color:#6c757d; margin-top:15px; cursor:pointer;'>Esqueci a password</p>", unsafe_allow_html=True)
        
    with aba_registro:
        novo_email = st.text_input("Email", placeholder="exemplo@parceiros.nos.pt", key="reg_email")
        nova_pass = st.text_input("Criar Palavra-passe", type="password", placeholder="Mínimo 4 caracteres", key="reg_pass")
        conf_pass = st.text_input("Confirmar Palavra-passe", type="password", placeholder="Repita a password", key="reg_conf_pass")
        
        if st.button("Criar Conta", use_container_width=True):
            if not novo_email or not nova_pass:
                st.error("Preencha todos os campos.")
            elif nova_pass != conf_pass:
                st.error("As passwords não coincidem.")
            elif novo_email in st.session_state.usuarios:
                st.error("Este email já está registado.")
            else:
                st.session_state.usuarios[novo_email] = nova_pass
                st.success("Conta criada com sucesso! Mude para a aba 'Entrar'.")
                
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ÁREA LOGADA (SISTEMA DE GESTÃO DE OBRAS)
# ==========================================
else:
    # Resetar o fundo azul para a área de trabalho ficar limpa e profissional
    st.markdown("<style>.stApp { background-color: #f8f9fa; color: #333333; }</style>", unsafe_allow_html=True)
    
    # --- HEADER ---
    col_logo, col_user = st.columns([2, 1.5])
    with col_logo:
        st.subheader("🔷 Smarthome SPNOS")
    with col_user:
        user_email = st.session_state.usuario_logado
        st.write(f"<div style='text-align: right; font-size: 13px; color: #6c757d; margin-bottom:5px;'>{user_email}</div>", unsafe_allow_html=True)
        if st.button("Sair ➔", key="logout_btn", use_container_width=True):
            st.session_state.usuario_logado = None
            st.session_state.obra_selecionada = None
            st.session_state.ap_selecionado = None
            st.rerun()
            
    st.write("---")
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    # ==========================================
    # ECRÃ 3: CHECKLIST DO APARTAMENTO
    # ==========================================
    if st.session_state.obra_selecionada and st.session_state.ap_selecionado:
        obra = st.session_state.obra_selecionada
        ap = st.session_state.ap_selecionado
        ap_info = st.session_state.obras_data[obra]["apartamentos"][ap]
        
        if st.button("← Voltar à obra"):
            st.session_state.ap_selecionado = None
            st.rerun()
            
        st.title(ap)
        
        total_t = len(ap_info["tarefas"])
        concluidas_t = sum(1 for t in ap_info["tarefas"] if t["feita"])
        st.caption(f"{concluidas_t} / {total_t} tarefas concluídas")
        st.caption(f"Última alteração por: **{ap_info['modificado_por']}** em {ap_info['data']}")
        
        # Alterar estado do apartamento (Quem altera fica registado)
        novo_estado = st.selectbox("Estado:", ["Planeado", "Em curso", "Concluída"], index=["Planeado", "Em curso", "Concluída"].index(ap_info["estado"]))
        if novo_estado != ap_info["estado"]:
            st.session_state.obras_data[obra]["apartamentos"][ap]["estado"] = novo_estado
            st.session_state.obras_data[obra]["apartamentos"][ap]["modificado_por"] = user_email
            st.session_state.obras_data[obra]["apartamentos"][ap]["data"] = data_hoje
            st.rerun()

        # Caixa de Checklist
        st.markdown("<div class='card-box'><h4>Checklist</h4>", unsafe_allow_html=True)
        
        col_t_in, col_t_btn = st.columns([5, 1])
        with col_t_in:
            nova_tarefa_txt = st.text_input("Adicionar tarefa...", key="input_nova_tarefa", label_visibility="collapsed", placeholder="Adicionar tarefa...")
        with col_t_btn:
            if st.button("＋", key="btn_add_tarefa", use_container_width=True):
                if nova_tarefa_txt:
                    st.session_state.obras_data[obra]["apartamentos"][ap]["tarefas"].append({
                        "texto": nova_tarefa_txt,
                        "feita": False,
                        "autor": user_email,
                        "data": data_hoje
                    })
                    st.rerun()
                        
        for idx, t in enumerate(ap_info["tarefas"]):
            col_chk, col_txt = st.columns([1, 10])
            with col_chk:
                status_chk = st.checkbox("", value=t["feita"], key=f"chk_{idx}")
                if status_chk != t["feita"]:
                    st.session_state.obras_data[obra]["apartamentos"][ap]["tarefas"][idx]["feita"] = status_chk
                    st.session_state.obras_data[obra]["apartamentos"][ap]["modificado_por"] = user_email
                    st.session_state.obras_data[obra]["apartamentos"][ap]["data"] = data_hoje
                    st.rerun()
            with col_txt:
                if t["feita"]:
                    st.markdown(f"~~{t['texto']}~~ <span class='subtext'>— {t['autor']} · {t['data']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{t['texto']} <span class='subtext'>— {t['autor']} · {t['data']}</span>", unsafe_allow_html=True)
                    
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # ECRÃ 2: APARTAMENTOS DA OBRA
    # ==========================================
    elif st.session_state.obra_selecionada:
        obra = st.session_state.obra_selecionada
        obra_info = st.session_state.obras_data[obra]
        
        if st.button("← Todas as obras"):
            st.session_state.obra_selecionada = None
            st.rerun()
            
        st.title(obra)
        st.caption(f"{len(obra_info['apartamentos'])} apartamento(s) cadastrado(s)")
        
        col_ap_in, col_ap_btn = st.columns([4, 1])
        with col_ap_in:
            novo_ap = st.text_input("Nome do apartamento (ex: Bloco A · 3ºD)", key="new_ap_input", label_visibility="collapsed", placeholder="Nome do apartamento (ex: Bloco A · 3ºD)")
        with col_ap_btn:
            if st.button("＋ Novo apartamento", use_container_width=True):
                if novo_ap and novo_ap not in obra_info["apartamentos"]:
                    st.session_state.obras_data[obra]["apartamentos"][novo_ap] = {
                        "estado": "Em curso", "modificado_por": user_email, "data": data_hoje, "tarefas": []
                    }
                    st.rerun()
                    
        st.write(" ")
        
        for ap_nome, ap_detalhes in obra_info["apartamentos"].items():
            st.markdown(f'<div class="card-box">', unsafe_allow_html=True)
            col_icon, col_info, col_status, col_go = st.columns([1, 4, 2, 1])
            with col_icon:
                st.markdown("<h3>🏢</h3>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"**{ap_nome}**")
                st.markdown(f"<div class='subtext'>Modificado por {ap_detalhes['modificado_por']} · {ap_detalhes['data']}</div>", unsafe_allow_html=True)
            with col_status:
                cor = "#007bff" if ap_detalhes['estado'] == "Concluída" else "#ffc107"
                st.markdown(f"<span style='background-color:{cor}; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:bold;'>{ap_detalhes['estado']}</span>", unsafe_allow_html=True)
            with col_go:
                if st.button("➔", key=f"go_{ap_nome}"):
                    st.session_state.ap_selecionado = ap_nome
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ECRÃ 1: LISTAGEM GERAL DE OBRAS
    # ==========================================
    else:
        st.title("Obras")
        st.markdown("Cada obra (ex: Terramar) contém os seus apartamentos.")
        
        col_in, col_btn = st.columns([4, 1])
        with col_in:
            nova_obra_nome = st.text_input("Nome da obra (ex: Terramar)", key="new_obra_input", label_visibility="collapsed", placeholder="Nome da obra (ex: Terramar)")
        with col_btn:
            if st.button("＋ Nova obra", use_container_width=True):
                if nova_obra_nome and nova_obra_nome not in st.session_state.obras_data:
                    st.session_state.obras_data[nova_obra_nome] = {
                        "modificado_por": user_email, "data_modificacao": data_hoje, "apartamentos": {}
                    }
                    st.rerun()
                    
        st.write(" ")
        
        for nome_obra, info_obra in st.session_state.obras_data.items():
            st.markdown(f'<div class="card-box">', unsafe_allow_html=True)
            col_icon, col_txt, col_arrow = st.columns([1, 5, 1])
            with col_icon:
                st.markdown("<h3>🏗️</h3>", unsafe_allow_html=True)
            with col_txt:
                st.markdown(f"**{nome_obra}**")
                st.markdown(f"<div class='subtext'>Modificado por {info_obra['modificado_por']} · {info_obra['data_modificacao']}</div>", unsafe_allow_html=True)
            with col_arrow:
                if st.button("➔", key=f"view_{nome_obra}"):
                    st.session_state.obra_selecionada = nome_obra
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
