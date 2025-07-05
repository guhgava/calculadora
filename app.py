import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from funcoes_financeiras import calcular_juros_compostos, calcular_vpl, calcular_tir

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
    ["Juros Compostos", "Valor Presente Líquido (VPL)", "Taxa Interna de Retorno (TIR)"]
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

# Navegação principal
if opcao == "Juros Compostos":
    juros_compostos()
elif opcao == "Valor Presente Líquido (VPL)":
    valor_presente_liquido()
elif opcao == "Taxa Interna de Retorno (TIR)":
    taxa_interna_retorno()

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
    """)

# Adicionar plotly ao requirements.txt
st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvido com:**")
st.sidebar.markdown("- Streamlit")
st.sidebar.markdown("- NumPy Financial")
st.sidebar.markdown("- Plotly") 