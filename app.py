import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Family Wealth Dashboard", layout="wide", initial_sidebar_state="expanded")

# 2. Mock dos Dados Extraídos das Suas Planilhas
# Em produção, o app lerá isso automaticamente do seu banco de dados ou Google Sheets
dados_kpis = {
    "Patrimônio Total": 353045.57,
    "Imóveis": 100000.00,
    "Renda Fixa": 31282.00,
    "Renda Variável": 221763.57 # (Small Caps + Própria + Cripto)
}

dados_fluxo_mensal = {
    "Receita (Bernardo + Cintia)": 47000.00,
    "Gastos": 33000.00,
    "Aportes (Investimentos)": 14000.00
}

# 3. Construindo a Interface
st.title("🏛️ Family Wealth - Painel Consolidado")
st.markdown("Bem-vindo, Bernardo e Cintia. Aqui está o resumo atualizado do ecossistema financeiro.")

# Filtro de Titularidade (Sidebar)
visao = st.sidebar.radio("Selecione a Visão:", ["Consolidado Familiar", "Apenas Bernardo", "Apenas Cintia"])

st.divider()

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
    # Preparando dados para o gráfico
    df_alocacao = pd.DataFrame({
        "Classe": ["Imóveis", "Renda Fixa", "Renda Variável"],
        "Valor": [100000, 31282, 221763]
    })
    # Gráfico interativo com Plotly
    fig = px.pie(df_alocacao, values="Valor", names="Classe", hole=0.4, 
                 color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col_metas:
    st.subheader("Aportes Mensais (Orçamento)")
    st.metric("Poder de Fogo Mensal", f"R$ 14.000,00")
    
    # Progresso Visual das metas mensais
    st.write("🎯 Previdência (R$ 9.000)")
    st.progress(9000 / 14000)
    
    st.write("🏠 Novo Imóvel (R$ 2.800)")
    st.progress(2800 / 14000)
    
    st.write("✈️ Viagem (R$ 1.500)")
    st.progress(1500 / 14000)
    
    st.write("🚗 Troca de Carro (R$ 700)")
    st.progress(700 / 14000)

st.markdown("---")
st.caption("Última atualização com base nos dados mais recentes processados pelo sistema.")
