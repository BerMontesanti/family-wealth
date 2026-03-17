import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Family Wealth Dashboard", layout="wide", initial_sidebar_state="expanded")

# 2. MOTOR DE DADOS: Função para ler do Google Sheets
@st.cache_data(ttl=600) # Atualiza a cada 10 minutos
def carregar_dados_sheets(gid):
    sheet_id = "1-XY6i7XdFOU26esEsZyfGtvmKPOrVluv1y38CJzGJCI"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# Tentativa de carregar o banco de dados (Substitua os GIDs depois)
try:
    # Coloque aqui o GID real da sua aba de Aportes_Mensais
    df_aportes = carregar_dados_sheets("1426534025") 
    dados_conectados = True
except Exception as e:
    dados_conectados = False


# 3. INTERFACE VISUAL (A "Lataria")
st.title("🏛️ Family Wealth - Painel Consolidado")
st.markdown("Bem-vindo, Bernardo e Cintia. Aqui está o resumo atualizado do ecossistema financeiro.")

if dados_conectados:
    st.success("🟢 Conectado ao banco de dados em nuvem (Google Sheets).")
else:
    st.warning("🟡 Aguardando conexão ou preenchimento da planilha inicial...")

st.sidebar.header("Filtros")
visao = st.sidebar.radio("Selecione a Visão:", ["Consolidado Familiar", "Apenas Bernardo", "Apenas Cintia"])

st.divider()

# -- Valores Fixos Iniciais (Em breve serão substituídos pelas somas do df_aportes, df_rf, etc) --
dados_kpis = {
    "Patrimônio Total": 353045.57,
    "Imóveis": 100000.00,
    "Renda Fixa": 31282.00,
    "Renda Variável": 221763.57 
}

# 4. Primeira Linha: KPIs (Indicadores Principais)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Patrimônio Total", f"R$ {dados_kpis['Patrimônio Total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Imóveis", f"R$ {dados_kpis['Imóveis']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Renda Fixa", f"R$ {dados_kpis['Renda Fixa']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col4.metric("Renda Variável", f"R$ {dados_kpis['Renda Variável']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# 5. Segunda Linha: Gráficos e Alocação
col_grafico, col_metas = st.columns([1.5, 1])

with col_grafico:
    st.subheader("Asset Allocation Atual (%)")
    df_alocacao = pd.DataFrame({
        "Classe": ["Imóveis", "Renda Fixa", "Renda Variável"],
        "Valor": [dados_kpis['Imóveis'], dados_kpis['Renda Fixa'], dados_kpis['Renda Variável']]
    })
    
    fig = px.pie(df_alocacao, values="Valor", names="Classe", hole=0.4, 
                 color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col_metas:
    st.subheader("Aportes e Orçamento Mensal")
    st.metric("Poder de Fogo Mensal", "R$ 14.000,00")
    
    st.write("🎯 Previdência (R$ 9.000)")
    st.progress(9000 / 14000)
    
    st.write("🏠 Novo Imóvel (R$ 2.800)")
    st.progress(2800 / 14000)
    
    st.write("✈️ Viagem (R$ 1.500)")
    st.progress(1500 / 14000)
    
    st.write("🚗 Troca de Carro (R$ 700)")
    st.progress(700 / 14000)

st.markdown("---")

# 6. Área de Debug/Visualização dos Dados da Nuvem
if dados_conectados:
    with st.expander("🔍 Ver Dados Brutos da Planilha (Nuvem)"):
        st.dataframe(df_aportes, use_container_width=True)
