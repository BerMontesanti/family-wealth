import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# 1. Configuração da Página
st.set_page_config(page_title="Family Wealth Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- SISTEMA DE LOGIN ---
def check_password():
    """Retorna `True` se a senha estiver correta."""
    
    # Cria a função para verificar a senha digitada
    def password_entered():
        # Compara a senha digitada com a que está no "Cofre" (Secrets)
        if st.session_state["password"] == st.secrets["passwords"]["admin"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Apaga a senha da memória por segurança
        else:
            st.session_state["password_correct"] = False

    # Se a senha já foi validada na sessão atual, permite o acesso
    if st.session_state.get("password_correct", False):
        return True

    # Se ainda não logou, mostra a tela de login
    st.title("🔒 Acesso Restrito")
    st.markdown("Por favor, insira a senha do sistema de Gestão Patrimonial.")
    st.text_input(
        "Senha:", type="password", on_change=password_entered, key="password"
    )
    
    if "password_correct" in st.session_state:
        st.error("😕 Senha incorreta. Tente novamente.")
    
    return False


# --- O APLICATIVO SÓ RODA SE O LOGIN FOR SUCESSO ---
if check_password():

    # 2. MENU DE NAVEGAÇÃO
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=50) 
    st.sidebar.title("Menu")
    st.sidebar.markdown(f"**Status:** 🟢 Logado")
    st.sidebar.divider()
    pagina = st.sidebar.radio("Navegação:", ["📊 Dashboard Consolidado", "📥 Terminal de Lançamentos"])
    st.sidebar.divider()
    
    # Botão de Logout rápido
    if st.sidebar.button("Sair (Logout)"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- PÁGINA 1: DASHBOARD ---
    if pagina == "📊 Dashboard Consolidado":
        st.title("🏛️ Family Wealth - Painel Consolidado")
        st.markdown("Bem-vindo, Bernardo e Cintia. Aqui está o resumo atualizado do ecossistema financeiro.")

        # Filtros
        visao = st.sidebar.radio("Filtrar Visão:", ["Consolidado Familiar", "Apenas Bernardo", "Apenas Cintia"])

        # Dados Fixos (Por enquanto, até conectarmos o banco para leitura automática)
        dados_kpis = {
            "Patrimônio Total": 353045.57,
            "Imóveis": 100000.00,
            "Renda Fixa": 31282.00,
            "Renda Variável": 221763.57 
        }

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Patrimônio Total", f"R$ {dados_kpis['Patrimônio Total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("Imóveis", f"R$ {dados_kpis['Imóveis']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col3.metric("Renda Fixa", f"R$ {dados_kpis['Renda Fixa']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col4.metric("Renda Variável", f"R$ {dados_kpis['Renda Variável']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.markdown("---")
        
        col_grafico, col_metas = st.columns([1.5, 1])
        with col_grafico:
            st.subheader("Asset Allocation Atual (%)")
            df_alocacao = pd.DataFrame({
                "Classe": ["Imóveis", "Renda Fixa", "Renda Variável"],
                "Valor": [dados_kpis['Imóveis'], dados_kpis['Renda Fixa'], dados_kpis['Renda Variável']]
            })
            fig = px.pie(df_alocacao, values="Valor", names="Classe", hole=0.4, color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"])
            st.plotly_chart(fig, use_container_width=True)

        with col_metas:
            st.subheader("Orçamento Mensal Consumido")
            st.metric("Poder de Fogo Mensal", "R$ 14.000,00")
            st.write("🎯 Previdência (R$ 9.000)")
            st.progress(9000 / 14000)
            st.write("🏠 Novo Imóvel (R$ 2.800)")
            st.progress(2800 / 14000)

    # --- PÁGINA 2: TERMINAL DE LANÇAMENTOS ---
    elif pagina == "📥 Terminal de Lançamentos":
        st.title("📥 Terminal de Lançamentos")
        st.markdown("Registre novas movimentações. Os dados serão salvos diretamente no banco de dados.")

        tab1, tab2, tab3 = st.tabs(["💰 Novo Aporte", "📈 Operação Renda Variável", "🛡️ Venda Coberta / PUT"])

        # Aba 1: Aportes
        with tab1:
            st.subheader("Registrar Novo Aporte")
            with st.form(key="form_aporte", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                data_aporte = col_a.date_input("Data do Aporte", value=date.today())
                titular = col_b.selectbox("Titular", ["Bernardo", "Cintia", "Conjunto"])
                
                col_c, col_d = st.columns(2)
                valor = col_c.number_input("Valor (R$)", min_value=0.0, step=100.0, format="%.2f")
                destino = col_d.selectbox("Destino (Caixa/Meta)", ["Previdência", "Novo Imóvel", "Viagem", "Troca de Carro", "Caixa Livre"])
                
                submit_aporte = st.form_submit_button(label="Gravar Aporte")
                if submit_aporte:
                    # Aqui entrará o código de salvar no banco invisível
                    st.success(f"✅ Aporte de R$ {valor} para {destino} ({titular}) registrado com sucesso!")

        # Aba 2: Renda Variável (Compra/Venda de Ações)
        with tab2:
            st.subheader("Registrar Compra/Venda de Ações")
            with st.form(key="form_rv", clear_on_submit=True):
                col_a, col_b, col_c = st.columns(3)
                data_rv = col_a.date_input("Data da Operação", value=date.today())
                tipo_op = col_b.selectbox("Tipo", ["Compra", "Venda"])
                estrategia = col_c.selectbox("Estratégia", ["Carteira Própria", "Small Caps - Nord"])
                
                col_d, col_e, col_f = st.columns(3)
                ticker = col_d.text_input("Ticker (Ex: ITUB4)").upper()
                quantidade = col_e.number_input("Quantidade", min_value=1, step=1)
                preco = col_f.number_input("Preço Executado (R$)", min_value=0.01, step=0.10, format="%.2f")
                
                submit_rv = st.form_submit_button(label="Gravar Operação")
                if submit_rv:
                    st.success(f"✅ {tipo_op} de {quantidade}x {ticker} a R$ {preco} registrada!")

        # Aba 3: Derivativos (Opções)
        with tab3:
            st.subheader("Registrar Venda Coberta ou PUT")
            with st.form(key="form_opcoes", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                ticker_opcao = col_a.text_input("Ticker da Opção (Ex: ITUBM166)").upper()
                tipo_derivativo = col_b.selectbox("Estratégia", ["Venda de PUT", "Venda Coberta (CALL)"])
                
                col_c, col_d, col_e = st.columns(3)
                qtd_opcao = col_c.number_input("Qtd Vendida", min_value=100, step=100)
                premio_recebido = col_d.number_input("Prêmio Recebido Total (R$)", min_value=0.0, step=10.0)
                strike = col_e.number_input("Strike (Preço Alvo)", min_value=0.0, step=0.10)
                
                submit_derivativo = st.form_submit_button(label="Gravar Derivativo")
                if submit_derivativo:
                    st.success(f"✅ Operação de {tipo_derivativo} ({ticker_opcao}) registrada! Prêmio de R$ {premio_recebido} lançado.")
