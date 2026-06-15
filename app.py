import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração inicial da página
st.set_page_config(
    page_title="Domotics Pro Hub",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (OPCIONAL) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SIMULAÇÃO DE BASE DE DADOS ---
# Nota: Mais tarde, ligamos isto diretamente ao seu Supabase do Lovable
if 'obras' not in st.session_state:
    st.session_state.obras = [
        {
            "id": 1,
            "cliente": "Marta Silva",
            "localidade": "Porto",
            "tipo": "Domótica (Shelly/Home Assistant)",
            "estado": "Em Progresso",
            "data_inicio": "2026-05-10",
            "orcamento": 1250.00
        },
        {
            "id": 2,
            "cliente": "Carlos Santos",
            "localidade": "Valongo",
            "tipo": "CCTV & Alarme",
            "estado": "Concluído",
            "data_inicio": "2026-04-15",
            "orcamento": 850.00
        }
    ]

# --- NAVEGAÇÃO LATERAL ---
st.sidebar.title("🏠 Domotics Pro Hub")
st.sidebar.subheader("Gestão de Projetos")
menu = st.sidebar.radio("Ir para:", ["Dashboard", "Listagem de Obras", "Registar Nova Obra"])

st.sidebar.info("💡 Dica: Esta interface substitui o ecrã do Lovable rodando totalmente em Python.")

# --- ABA 1: DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Painel de Controlo")
    st.markdown("Visão geral dos projetos de domótica e instalações em curso.")
    st.write("---")
    
    # Métricas Rápidas
    df = pd.DataFrame(st.session_state.obras)
    total_obras = len(df)
    em_progresso = len(df[df['estado'] == 'Em Progresso'])
    total_faturado = df['orcamento'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Obras", total_obras)
    col2.metric("Obras Ativas", em_progresso, delta="Técnicos na rua")
    col3.metric("Volume de Orçamentos", f"{total_faturado:.2f} €")
    
    st.write("---")
    st.subheader("Cronograma de Intervenções Recentes")
    st.dataframe(df[['cliente', 'localidade', 'tipo', 'estado']], use_container_width=True)

# --- ABA 2: LISTAGEM DE OBRAS ---
elif menu == "Listagem de Obras":
    st.title("📋 Gestão e Estado das Obras")
    st.markdown("Consulte, filtre e edite o estado de cada projeto.")
    st.write("---")
    
    df = pd.DataFrame(st.session_state.obras)
    
    # Filtros rápidos
    filtro_estado = st.selectbox("Filtrar por Estado:", ["Todos", "Planeado", "Em Progresso", "Concluído"])
    if filtro_estado != "Todos":
        df = df[df['estado'] == filtro_estado]
        
    # Tabela Editável (Permite mudar valores diretamente no ecrã como no Excel/Lovable)
    st.subheader("Clique em qualquer célula para atualizar os dados:")
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.button("Guardar Alterações"):
        st.session_state.obras = edited_df.to_dict('records')
        st.success("Base de dados atualizada com sucesso!")

# --- ABA 3: REGISTAR NOVA OBRA ---
elif menu == "Registar Nova Obra":
    st.title("📝 Ficha de Nova Instalação")
    st.markdown("Insira os dados do cliente e os requisitos técnicos do sistema de domótica/segurança.")
    st.write("---")
    
    with st.form("form_nova_obra", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            cliente = st.text_input("Nome do Cliente:")
            localidade = st.text_input("Localidade / Concelho:")
            tipo = st.selectbox("Tipo de Sistema:", [
                "Domótica Completa (Home Assistant)", 
                "Redes Estruturadas / FTTH", 
                "Segurança (CCTV & Alarmes)",
                "Automatismos / Shelly"
            ])
            
        with col2:
            estado = st.selectbox("Estado Inicial:", ["Planeado", "Em Progresso"])
            orcamento = st.number_input("Valor do Orçamento (€):", min_value=0.0, step=50.0)
            data_inicio = st.date_input("Data de Início do Projeto:", datetime.now())
            
        detalhes = st.text_area("Notas Técnicas / Equipamento Necessário (ex: Switches, Réguas, Sensores):")
        
        submetido = st.form_submit_form_button("Gravar Projeto")
        
        if submetido:
            if cliente and localidade:
                nova_obra = {
                    "id": len(st.session_state.obras) + 1,
                    "cliente": cliente,
                    "localidade": localidade,
                    "tipo": tipo,
                    "estado": estado,
                    "data_inicio": str(data_inicio),
                    "orcamento": orcamento
                }
                st.session_state.obras.append(nova_obra)
                st.success(f"Obra para {cliente} registada com sucesso!")
            else:
                st.error("Por favor, preencha o Nome do Cliente e a Localidade.")
