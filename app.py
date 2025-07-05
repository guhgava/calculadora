import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from funcoes_financeiras import (
    calcular_juros_compostos, calcular_vpl, calcular_tir, 
    calcular_amortizacao_sac, calcular_amortizacao_price, calcular_amortizacao_sac_american,
    calcular_retorno_acao, calcular_volatilidade, calcular_beta, calcular_sharpe_ratio,
    calcular_max_drawdown, calcular_roi_fundo, calcular_volatilidade_cripto,
    calcular_correlacao_ativos, calcular_alocacao_otima
)

# Configuração da página
st.set_page_config(
    page_title="Calculadora Financeira Interativa",
    page_icon="💰",
    layout="wide"
)

# Título principal
st.title("💰 Calculadora Financeira Interativa")
st.markdown("---")

# Sidebar para navegação
st.sidebar.title("📊 Tipos de Cálculo")
opcao = st.sidebar.selectbox(
    "Escolha o tipo de cálculo:",
    ["Juros Compostos", "Valor Presente Líquido (VPL)", "Taxa Interna de Retorno (TIR)", "Sistema de Amortização", "Análise de Investimentos"]
)

# Função para juros compostos
def juros_compostos():
    st.header("📈 Cálculo de Juros Compostos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        capital = st.number_input("Capital Inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
        taxa = st.number_input("Taxa de Juros (% ao mês)", min_value=0.0, max_value=100.0, value=1.0, step=0.1) / 100
    
    with col2:
        tempo = st.number_input("Período (meses)", min_value=1, value=12, step=1)
        tipo_tempo = st.selectbox("Tipo de período:", ["Mensal", "Anual"])
        
        if tipo_tempo == "Anual":
            tempo = tempo * 12
            taxa = (1 + taxa) ** 12 - 1
    
    # Cálculo
    montante = calcular_juros_compostos(capital, taxa, tempo)
    juros = montante - capital
    
    # Resultados
    st.markdown("### 📊 Resultados")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Capital Inicial", f"R$ {capital:,.2f}")
    with col2:
        st.metric("Montante Final", f"R$ {montante:,.2f}")
    with col3:
        st.metric("Juros Ganhos", f"R$ {juros:,.2f}")
    
    # Gráfico
    st.markdown("### 📈 Evolução do Investimento")
    periodos = list(range(tempo + 1))
    valores = [calcular_juros_compostos(capital, taxa, t) for t in periodos]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=periodos, 
        y=valores, 
        mode='lines+markers',
        name='Montante',
        line=dict(color='#1f77b4', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=periodos, 
        y=[capital] * len(periodos),
        mode='lines',
        name='Capital Inicial',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Evolução do Investimento ao Longo do Tempo",
        xaxis_title="Períodos",
        yaxis_title="Valor (R$)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Função para VPL
def valor_presente_liquido():
    st.header("💼 Cálculo do Valor Presente Líquido (VPL)")
    
    st.markdown("### 📝 Entrada de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        taxa_desconto = st.number_input("Taxa de Desconto (% ao ano)", min_value=0.0, max_value=100.0, value=10.0, step=0.1) / 100
    
    with col2:
        st.markdown("**Fluxo de Caixa:**")
        st.markdown("Digite os valores do fluxo de caixa (negativo para saída, positivo para entrada)")
    
    # Entrada do fluxo de caixa
    st.markdown("### 💰 Fluxo de Caixa")
    
    # Interface para entrada dos fluxos
    num_periodos = st.number_input("Número de períodos:", min_value=1, value=5, step=1)
    
    fluxos = []
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Período 0 (Investimento Inicial):**")
        fluxo_inicial = st.number_input("Valor (R$)", value=-10000.0, step=1000.0, key="fluxo_0")
        fluxos.append(fluxo_inicial)
    
    with col2:
        st.markdown("**Períodos Futuros:**")
        for i in range(1, num_periodos + 1):
            fluxo = st.number_input(f"Período {i} (R$)", value=3000.0, step=500.0, key=f"fluxo_{i}")
            fluxos.append(fluxo)
    
    # Cálculo do VPL
    try:
        vpl = calcular_vpl(fluxos, taxa_desconto)
        
        # Resultados
        st.markdown("### 📊 Resultados")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("VPL", f"R$ {vpl:,.2f}")
        with col2:
            st.metric("Taxa de Desconto", f"{taxa_desconto*100:.1f}%")
        with col3:
            if vpl > 0:
                st.metric("Decisão", "✅ Viável", delta="Aceitar")
            else:
                st.metric("Decisão", "❌ Não Viável", delta="Rejeitar")
        
        # Tabela do fluxo de caixa
        st.markdown("### 📋 Resumo do Fluxo de Caixa")
        df_fluxos = pd.DataFrame({
            'Período': range(len(fluxos)),
            'Fluxo (R$)': fluxos,
            'Tipo': ['Investimento' if f < 0 else 'Retorno' for f in fluxos]
        })
        st.dataframe(df_fluxos, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro no cálculo: {str(e)}")

# Função para TIR
def taxa_interna_retorno():
    st.header("🎯 Cálculo da Taxa Interna de Retorno (TIR)")
    
    st.markdown("### 📝 Entrada de Dados")
    st.markdown("Digite os valores do fluxo de caixa para calcular a TIR")
    
    # Entrada do fluxo de caixa
    st.markdown("### 💰 Fluxo de Caixa")
    
    num_periodos = st.number_input("Número de períodos:", min_value=1, value=5, step=1, key="tir_periodos")
    
    fluxos = []
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Período 0 (Investimento Inicial):**")
        fluxo_inicial = st.number_input("Valor (R$)", value=-10000.0, step=1000.0, key="tir_fluxo_0")
        fluxos.append(fluxo_inicial)
    
    with col2:
        st.markdown("**Períodos Futuros:**")
        for i in range(1, num_periodos + 1):
            fluxo = st.number_input(f"Período {i} (R$)", value=3000.0, step=500.0, key=f"tir_fluxo_{i}")
            fluxos.append(fluxo)
    
    # Cálculo da TIR
    try:
        tir = calcular_tir(fluxos)
        
        # Resultados
        st.markdown("### 📊 Resultados")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("TIR", f"{tir*100:.2f}%")
        with col2:
            st.metric("TIR (decimal)", f"{tir:.4f}")
        with col3:
            if tir > 0.1:  # 10% como referência
                st.metric("Avaliação", "✅ Boa", delta="Acima de 10%")
            else:
                st.metric("Avaliação", "⚠️ Baixa", delta="Abaixo de 10%")
        
        # Tabela do fluxo de caixa
        st.markdown("### 📋 Resumo do Fluxo de Caixa")
        df_fluxos = pd.DataFrame({
            'Período': range(len(fluxos)),
            'Fluxo (R$)': fluxos,
            'Tipo': ['Investimento' if f < 0 else 'Retorno' for f in fluxos]
        })
        st.dataframe(df_fluxos, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro no cálculo: {str(e)}")

# Função para sistema de amortização
def sistema_amortizacao():
    st.header("🏦 Sistema de Amortização")
    
    st.markdown("### 📝 Dados do Financiamento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valor_principal = st.number_input("Valor Principal (R$)", min_value=0.0, value=100000.0, step=1000.0)
    
    with col2:
        taxa_anual = st.number_input("Taxa de Juros (% ao ano)", min_value=0.0, max_value=100.0, value=12.0, step=0.1)
        taxa_mensal = taxa_anual / 12 / 100
    
    with col3:
        num_parcelas = st.number_input("Número de Parcelas", min_value=1, value=60, step=1)
    
    # Seleção do sistema de amortização
    st.markdown("### 🎯 Sistema de Amortização")
    sistema = st.selectbox(
        "Escolha o sistema de amortização:",
        ["SAC (Sistema de Amortização Constante)", "Price (Prestações Fixas)", "SAC Americano", "Comparação dos Sistemas"]
    )
    
    if sistema == "SAC (Sistema de Amortização Constante)":
        st.markdown("#### 📊 SAC - Sistema de Amortização Constante")
        st.markdown("**Características:** Prestações decrescentes, amortização constante")
        
        df_sac = calcular_amortizacao_sac(valor_principal, taxa_mensal, num_parcelas)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valor Total Pago", f"R$ {df_sac['Prestacao'].sum():,.2f}")
        with col2:
            st.metric("Total de Juros", f"R$ {df_sac['Juros'].sum():,.2f}")
        with col3:
            st.metric("1ª Prestação", f"R$ {df_sac.iloc[0]['Prestacao']:,.2f}")
        with col4:
            st.metric("Última Prestação", f"R$ {df_sac.iloc[-1]['Prestacao']:,.2f}")
        
        # Tabela
        st.markdown("### 📋 Tabela de Amortização SAC")
        st.dataframe(df_sac, use_container_width=True)
        
        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sac['Periodo'], y=df_sac['Prestacao'], 
                                mode='lines+markers', name='Prestação', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_sac['Periodo'], y=df_sac['Juros'], 
                                mode='lines+markers', name='Juros', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df_sac['Periodo'], y=df_sac['Amortizacao'], 
                                mode='lines+markers', name='Amortização', line=dict(color='green')))
        
        fig.update_layout(title="Evolução das Prestações - SAC", xaxis_title="Período", yaxis_title="Valor (R$)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif sistema == "Price (Prestações Fixas)":
        st.markdown("#### 📊 Price - Prestações Fixas")
        st.markdown("**Características:** Prestações constantes, amortização crescente")
        
        df_price = calcular_amortizacao_price(valor_principal, taxa_mensal, num_parcelas)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valor Total Pago", f"R$ {df_price['Prestacao'].sum():,.2f}")
        with col2:
            st.metric("Total de Juros", f"R$ {df_price['Juros'].sum():,.2f}")
        with col3:
            st.metric("Prestação Fixa", f"R$ {df_price.iloc[0]['Prestacao']:,.2f}")
        with col4:
            st.metric("Valor Principal", f"R$ {valor_principal:,.2f}")
        
        # Tabela
        st.markdown("### 📋 Tabela de Amortização Price")
        st.dataframe(df_price, use_container_width=True)
        
        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_price['Periodo'], y=df_price['Prestacao'], 
                                mode='lines+markers', name='Prestação', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_price['Periodo'], y=df_price['Juros'], 
                                mode='lines+markers', name='Juros', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df_price['Periodo'], y=df_price['Amortizacao'], 
                                mode='lines+markers', name='Amortização', line=dict(color='green')))
        
        fig.update_layout(title="Evolução das Prestações - Price", xaxis_title="Período", yaxis_title="Valor (R$)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif sistema == "SAC Americano":
        st.markdown("#### 📊 SAC Americano")
        st.markdown("**Características:** Juros pagos mensalmente, principal no final")
        
        df_american = calcular_amortizacao_sac_american(valor_principal, taxa_mensal, num_parcelas)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valor Total Pago", f"R$ {df_american['Prestacao'].sum():,.2f}")
        with col2:
            st.metric("Total de Juros", f"R$ {df_american['Juros'].sum():,.2f}")
        with col3:
            st.metric("Prestação Mensal", f"R$ {df_american.iloc[0]['Prestacao']:,.2f}")
        with col4:
            st.metric("Última Prestação", f"R$ {df_american.iloc[-1]['Prestacao']:,.2f}")
        
        # Tabela
        st.markdown("### 📋 Tabela de Amortização SAC Americano")
        st.dataframe(df_american, use_container_width=True)
        
        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_american['Periodo'], y=df_american['Prestacao'], 
                                mode='lines+markers', name='Prestação', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_american['Periodo'], y=df_american['Juros'], 
                                mode='lines+markers', name='Juros', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df_american['Periodo'], y=df_american['Amortizacao'], 
                                mode='lines+markers', name='Amortização', line=dict(color='green')))
        
        fig.update_layout(title="Evolução das Prestações - SAC Americano", xaxis_title="Período", yaxis_title="Valor (R$)")
        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Comparação dos Sistemas
        st.markdown("#### 📊 Comparação dos Sistemas de Amortização")
        
        df_sac = calcular_amortizacao_sac(valor_principal, taxa_mensal, num_parcelas)
        df_price = calcular_amortizacao_price(valor_principal, taxa_mensal, num_parcelas)
        df_american = calcular_amortizacao_sac_american(valor_principal, taxa_mensal, num_parcelas)
        
        # Métricas comparativas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("SAC - Total Pago", f"R$ {df_sac['Prestacao'].sum():,.2f}")
            st.metric("SAC - Total Juros", f"R$ {df_sac['Juros'].sum():,.2f}")
        with col2:
            st.metric("Price - Total Pago", f"R$ {df_price['Prestacao'].sum():,.2f}")
            st.metric("Price - Total Juros", f"R$ {df_price['Juros'].sum():,.2f}")
        with col3:
            st.metric("SAC Americano - Total Pago", f"R$ {df_american['Prestacao'].sum():,.2f}")
            st.metric("SAC Americano - Total Juros", f"R$ {df_american['Juros'].sum():,.2f}")
        
        # Gráfico comparativo
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sac['Periodo'], y=df_sac['Prestacao'], 
                                mode='lines', name='SAC', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_price['Periodo'], y=df_price['Prestacao'], 
                                mode='lines', name='Price', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df_american['Periodo'], y=df_american['Prestacao'], 
                                mode='lines', name='SAC Americano', line=dict(color='green')))
        
        fig.update_layout(title="Comparação das Prestações", xaxis_title="Período", yaxis_title="Prestação (R$)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela comparativa
        st.markdown("### 📋 Resumo Comparativo")
        comparacao = pd.DataFrame({
            'Sistema': ['SAC', 'Price', 'SAC Americano'],
            'Total Pago (R$)': [df_sac['Prestacao'].sum(), df_price['Prestacao'].sum(), df_american['Prestacao'].sum()],
            'Total Juros (R$)': [df_sac['Juros'].sum(), df_price['Juros'].sum(), df_american['Juros'].sum()],
            '1ª Prestação (R$)': [df_sac.iloc[0]['Prestacao'], df_price.iloc[0]['Prestacao'], df_american.iloc[0]['Prestacao']],
            'Última Prestação (R$)': [df_sac.iloc[-1]['Prestacao'], df_price.iloc[-1]['Prestacao'], df_american.iloc[-1]['Prestacao']]
        })
        st.dataframe(comparacao, use_container_width=True)

# Função para análise de investimentos
def analise_investimentos():
    st.header("📈 Análise de Investimentos")
    
    # Submenu para tipos de investimento
    tipo_investimento = st.sidebar.selectbox(
        "Tipo de Análise:",
        ["Análise de Ações", "Fundos de Investimento", "Criptomoedas", "Correlação de Ativos"]
    )
    
    if tipo_investimento == "Análise de Ações":
        st.markdown("### 📊 Análise de Ações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Dados da Ação")
            preco_inicial = st.number_input("Preço Inicial (R$)", min_value=0.0, value=50.0, step=1.0)
            preco_final = st.number_input("Preço Final (R$)", min_value=0.0, value=60.0, step=1.0)
            dividendos = st.number_input("Dividendos Recebidos (R$)", min_value=0.0, value=2.0, step=0.5)
        
        with col2:
            st.markdown("#### 📊 Dados de Mercado")
            taxa_livre_risco = st.number_input("Taxa Livre de Risco (% ao ano)", min_value=0.0, max_value=20.0, value=6.0, step=0.1) / 100
            
            # Simulação de retornos históricos
            st.markdown("**Retornos Históricos (últimos 12 meses):**")
            retornos_acao = st.text_input("Retornos mensais (separados por vírgula)", value="0.05, -0.02, 0.08, -0.03, 0.06, 0.01, -0.04, 0.07, 0.02, -0.01, 0.09, 0.03")
            retornos_mercado = st.text_input("Retornos do mercado (separados por vírgula)", value="0.03, -0.01, 0.05, -0.02, 0.04, 0.01, -0.02, 0.05, 0.01, -0.01, 0.06, 0.02")
        
        # Cálculos
        try:
            # Converter strings em arrays
            retornos_acao_array = np.array([float(x.strip()) for x in retornos_acao.split(',')])
            retornos_mercado_array = np.array([float(x.strip()) for x in retornos_mercado.split(',')])
            
            # Calcular métricas
            retorno_total = calcular_retorno_acao(preco_inicial, preco_final, dividendos)
            volatilidade = calcular_volatilidade(retornos_acao_array)
            beta = calcular_beta(retornos_acao_array, retornos_mercado_array)
            sharpe = calcular_sharpe_ratio(retornos_acao_array, taxa_livre_risco)
            
            # Resultados
            st.markdown("### 📊 Resultados da Análise")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Retorno Total", f"{retorno_total*100:.2f}%")
            with col2:
                st.metric("Volatilidade", f"{volatilidade*100:.2f}%")
            with col3:
                st.metric("Beta", f"{beta:.3f}")
            with col4:
                st.metric("Sharpe Ratio", f"{sharpe:.3f}")
            
            # Interpretação
            st.markdown("### 📋 Interpretação")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Beta:**")
                if beta < 1:
                    st.success("Ação defensiva (menos volátil que o mercado)")
                elif beta > 1:
                    st.warning("Ação agressiva (mais volátil que o mercado)")
                else:
                    st.info("Ação neutra (volatilidade similar ao mercado)")
            
            with col2:
                st.markdown("**Sharpe Ratio:**")
                if sharpe > 1:
                    st.success("Excelente retorno ajustado ao risco")
                elif sharpe > 0.5:
                    st.info("Bom retorno ajustado ao risco")
                else:
                    st.warning("Baixo retorno ajustado ao risco")
            
            # Gráfico de retornos
            st.markdown("### 📈 Evolução dos Retornos")
            periodos = list(range(1, len(retornos_acao_array) + 1))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=periodos, y=retornos_acao_array*100, 
                                    mode='lines+markers', name='Ação', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=periodos, y=retornos_mercado_array*100, 
                                    mode='lines+markers', name='Mercado', line=dict(color='red')))
            
            fig.update_layout(title="Retornos Mensais", xaxis_title="Mês", yaxis_title="Retorno (%)")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro nos cálculos: {str(e)}")
    
    elif tipo_investimento == "Fundos de Investimento":
        st.markdown("### 🏦 Análise de Fundos de Investimento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Dados do Fundo")
            valor_inicial = st.number_input("Valor Inicial (R$)", min_value=0.0, value=10000.0, step=1000.0)
            valor_final = st.number_input("Valor Final (R$)", min_value=0.0, value=11500.0, step=1000.0)
            taxas = st.number_input("Taxas Totais (% ao ano)", min_value=0.0, max_value=5.0, value=1.5, step=0.1) / 100
        
        with col2:
            st.markdown("#### 📊 Comparação")
            st.markdown("**Fundos para Comparação:**")
            fundo1_nome = st.text_input("Nome do Fundo 1", value="Fundo A")
            fundo1_retorno = st.number_input("Retorno Fundo 1 (%)", value=12.0, step=0.1) / 100
            fundo2_nome = st.text_input("Nome do Fundo 2", value="Fundo B")
            fundo2_retorno = st.number_input("Retorno Fundo 2 (%)", value=10.0, step=0.1) / 100
        
        # Cálculos
        roi_bruto, roi_liquido = calcular_roi_fundo(valor_inicial, valor_final, taxas)
        
        # Resultados
        st.markdown("### 📊 Resultados")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("ROI Bruto", f"{roi_bruto*100:.2f}%")
        with col2:
            st.metric("ROI Líquido", f"{roi_liquido*100:.2f}%")
        with col3:
            st.metric("Taxas", f"{taxas*100:.2f}%")
        with col4:
            st.metric("Valor Final", f"R$ {valor_final:,.2f}")
        
        # Comparação
        st.markdown("### 📋 Comparação de Fundos")
        comparacao_fundos = pd.DataFrame({
            'Fundo': ['Seu Fundo', fundo1_nome, fundo2_nome],
            'ROI Bruto (%)': [roi_bruto*100, fundo1_retorno*100, fundo2_retorno*100],
            'ROI Líquido (%)': [roi_liquido*100, fundo1_retorno*100*0.985, fundo2_retorno*100*0.985]
        })
        st.dataframe(comparacao_fundos, use_container_width=True)
        
        # Gráfico comparativo
        fig = go.Figure()
        fig.add_trace(go.Bar(x=comparacao_fundos['Fundo'], y=comparacao_fundos['ROI Líquido (%)'],
                            name='ROI Líquido', marker_color=['green', 'blue', 'orange']))
        
        fig.update_layout(title="Comparação de Retornos", xaxis_title="Fundo", yaxis_title="ROI Líquido (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif tipo_investimento == "Criptomoedas":
        st.markdown("### 🪙 Análise de Criptomoedas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Dados da Criptomoeda")
            preco_atual = st.number_input("Preço Atual (US$)", min_value=0.0, value=50000.0, step=1000.0)
            preco_anterior = st.number_input("Preço Anterior (US$)", min_value=0.0, value=45000.0, step=1000.0)
            
            # Simulação de preços históricos
            st.markdown("**Preços Históricos (últimos 30 dias):**")
            precos_hist = st.text_input("Preços diários (separados por vírgula)", 
                                       value="45000, 46000, 47000, 46500, 48000, 47500, 49000, 48500, 50000, 49500, 51000, 50500, 52000, 51500, 53000, 52500, 54000, 53500, 55000, 54500, 56000, 55500, 57000, 56500, 58000, 57500, 59000, 58500, 60000, 59500, 50000")
        
        with col2:
            st.markdown("#### 📊 Análise de Risco")
            periodo_analise = st.selectbox("Período de Análise", ["7 dias", "30 dias", "90 dias"])
            
            # Métricas de risco
            st.markdown("**Limites de Risco:**")
            stop_loss = st.number_input("Stop Loss (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0) / 100
            take_profit = st.number_input("Take Profit (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0) / 100
        
        # Cálculos
        try:
            precos_array = np.array([float(x.strip()) for x in precos_hist.split(',')])
            volatilidade = calcular_volatilidade_cripto(precos_array)
            max_dd = calcular_max_drawdown(precos_array)
            retorno_periodo = (preco_atual - preco_anterior) / preco_anterior
            
            # Resultados
            st.markdown("### 📊 Resultados da Análise")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Retorno do Período", f"{retorno_periodo*100:.2f}%")
            with col2:
                st.metric("Volatilidade Anualizada", f"{volatilidade*100:.2f}%")
            with col3:
                st.metric("Máximo Drawdown", f"{max_dd*100:.2f}%")
            with col4:
                st.metric("Preço Atual", f"US$ {preco_atual:,.0f}")
            
            # Análise de risco
            st.markdown("### ⚠️ Análise de Risco")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Stop Loss:**")
                preco_stop = preco_atual * (1 - stop_loss)
                st.metric("Preço Stop Loss", f"US$ {preco_stop:,.0f}")
                
                st.markdown("**Take Profit:**")
                preco_take = preco_atual * (1 + take_profit)
                st.metric("Preço Take Profit", f"US$ {preco_take:,.0f}")
            
            with col2:
                st.markdown("**Classificação de Risco:**")
                if volatilidade > 0.8:
                    st.error("Alto Risco - Muito volátil")
                elif volatilidade > 0.5:
                    st.warning("Risco Moderado")
                else:
                    st.success("Baixo Risco - Relativamente estável")
                
                st.markdown("**Recomendação:**")
                if retorno_periodo > 0.1 and volatilidade < 0.6:
                    st.success("Considerar compra")
                elif retorno_periodo < -0.05:
                    st.error("Considerar venda")
                else:
                    st.info("Manter posição")
            
            # Gráfico de preços
            st.markdown("### 📈 Evolução dos Preços")
            dias = list(range(1, len(precos_array) + 1))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dias, y=precos_array, 
                                    mode='lines', name='Preço', line=dict(color='orange')))
            
            fig.update_layout(title="Evolução dos Preços", xaxis_title="Dia", yaxis_title="Preço (US$)")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro nos cálculos: {str(e)}")
    
    else:  # Correlação de Ativos
        st.markdown("### 🔗 Análise de Correlação entre Ativos")
        
        st.markdown("#### 📝 Dados dos Ativos")
        st.markdown("Insira os preços históricos dos ativos (últimos 30 dias):")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ativo1_nome = st.text_input("Nome do Ativo 1", value="Ação A")
            precos_ativo1 = st.text_input("Preços Ativo 1 (separados por vírgula)", 
                                         value="100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110, 112, 111, 113, 115, 114, 116, 118, 117, 119, 120, 122, 121, 123, 125, 124, 126, 128, 127, 129, 130")
            
            ativo2_nome = st.text_input("Nome do Ativo 2", value="Ação B")
            precos_ativo2 = st.text_input("Preços Ativo 2 (separados por vírgula)", 
                                         value="50, 51, 50.5, 51.5, 52.5, 52, 53, 54, 53.5, 54.5, 55, 56, 55.5, 56.5, 57.5, 57, 58, 59, 58.5, 59.5, 60, 61, 60.5, 61.5, 62.5, 62, 63, 64, 63.5, 64.5, 65")
        
        with col2:
            ativo3_nome = st.text_input("Nome do Ativo 3", value="Cripto C")
            precos_ativo3 = st.text_input("Preços Ativo 3 (separados por vírgula)", 
                                         value="1000, 1100, 1050, 1150, 1200, 1180, 1250, 1300, 1280, 1350, 1400, 1450, 1420, 1480, 1500, 1470, 1520, 1550, 1530, 1580, 1600, 1650, 1620, 1680, 1700, 1670, 1720, 1750, 1730, 1780, 1800")
            
            st.markdown("#### 📊 Análise de Diversificação")
            st.markdown("**Objetivo:** Identificar ativos com baixa correlação para diversificação")
        
        # Cálculos
        try:
            precos1 = np.array([float(x.strip()) for x in precos_ativo1.split(',')])
            precos2 = np.array([float(x.strip()) for x in precos_ativo2.split(',')])
            precos3 = np.array([float(x.strip()) for x in precos_ativo3.split(',')])
            
            # Matriz de correlação
            precos_ativos = np.column_stack((precos1, precos2, precos3))
            correlacao = calcular_correlacao_ativos(precos_ativos)
            
            # Resultados
            st.markdown("### 📊 Matriz de Correlação")
            df_correlacao = pd.DataFrame(
                correlacao,
                columns=[ativo1_nome, ativo2_nome, ativo3_nome],
                index=[ativo1_nome, ativo2_nome, ativo3_nome]
            )
            st.dataframe(df_correlacao, use_container_width=True)
            
            # Heatmap
            fig = go.Figure(data=go.Heatmap(
                z=correlacao,
                x=[ativo1_nome, ativo2_nome, ativo3_nome],
                y=[ativo1_nome, ativo2_nome, ativo3_nome],
                colorscale='RdBu',
                zmid=0
            ))
            fig.update_layout(title="Mapa de Correlação entre Ativos")
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendações
            st.markdown("### 💡 Recomendações de Diversificação")
            
            corr_12 = correlacao[0, 1]
            corr_13 = correlacao[0, 2]
            corr_23 = correlacao[1, 2]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Análise de Correlação:**")
                if abs(corr_12) < 0.3:
                    st.success(f"{ativo1_nome} e {ativo2_nome}: Baixa correlação ✅")
                else:
                    st.warning(f"{ativo1_nome} e {ativo2_nome}: Alta correlação ⚠️")
                
                if abs(corr_13) < 0.3:
                    st.success(f"{ativo1_nome} e {ativo3_nome}: Baixa correlação ✅")
                else:
                    st.warning(f"{ativo1_nome} e {ativo3_nome}: Alta correlação ⚠️")
            
            with col2:
                if abs(corr_23) < 0.3:
                    st.success(f"{ativo2_nome} e {ativo3_nome}: Baixa correlação ✅")
                else:
                    st.warning(f"{ativo2_nome} e {ativo3_nome}: Alta correlação ⚠️")
                
                st.markdown("**Recomendação Geral:**")
                if all(abs(corr) < 0.5 for corr in [corr_12, corr_13, corr_23]):
                    st.success("Portfólio bem diversificado!")
                else:
                    st.warning("Considere adicionar ativos menos correlacionados")
            
        except Exception as e:
            st.error(f"Erro nos cálculos: {str(e)}")

# Navegação principal
if opcao == "Juros Compostos":
    juros_compostos()
elif opcao == "Valor Presente Líquido (VPL)":
    valor_presente_liquido()
elif opcao == "Taxa Interna de Retorno (TIR)":
    taxa_interna_retorno()
elif opcao == "Sistema de Amortização":
    sistema_amortizacao()
elif opcao == "Análise de Investimentos":
    analise_investimentos()

# Footer
st.markdown("---")
st.markdown("### 📚 Sobre os Cálculos")
with st.expander("ℹ️ Informações sobre os métodos financeiros"):
    st.markdown("""
    **Juros Compostos:** Calcula o montante final considerando juros sobre juros.
    
    **VPL (Valor Presente Líquido):** Calcula o valor presente de todos os fluxos de caixa futuros.
    - VPL > 0: Projeto viável
    - VPL < 0: Projeto não viável
    
    **TIR (Taxa Interna de Retorno):** Taxa que torna o VPL igual a zero.
    - TIR > Taxa de oportunidade: Projeto viável
    - TIR < Taxa de oportunidade: Projeto não viável
    
    **Sistemas de Amortização:**
    - **SAC:** Prestações decrescentes, amortização constante
    - **Price:** Prestações fixas, amortização crescente
    - **SAC Americano:** Juros mensais, principal no final
    
    **Análise de Investimentos:**
    - **Ações:** Beta, Sharpe Ratio, volatilidade
    - **Fundos:** ROI bruto/líquido, comparação
    - **Criptomoedas:** Volatilidade, drawdown, análise de risco
    - **Correlação:** Diversificação de portfólio
    """)

# Adicionar plotly ao requirements.txt
st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvido com:**")
st.sidebar.markdown("- Streamlit")
st.sidebar.markdown("- NumPy Financial")
st.sidebar.markdown("- Plotly") 