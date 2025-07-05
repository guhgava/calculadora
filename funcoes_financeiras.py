import numpy as np
import numpy_financial as npf
import pandas as pd

def calcular_juros_compostos(capital, taxa, tempo):
    return capital * (1 + taxa) ** tempo

def calcular_vpl(fluxos, taxa):
    return npf.npv(taxa, fluxos)

def calcular_tir(fluxos):
    return npf.irr(fluxos)

def calcular_amortizacao_sac(valor_principal, taxa_mensal, num_parcelas):
    """
    Calcula a amortização pelo sistema SAC (Sistema de Amortização Constante)
    """
    amortizacao = valor_principal / num_parcelas
    tabela = []
    
    saldo_devedor = valor_principal
    
    for periodo in range(1, num_parcelas + 1):
        juros = saldo_devedor * taxa_mensal
        prestacao = amortizacao + juros
        saldo_devedor -= amortizacao
        
        tabela.append({
            'Periodo': periodo,
            'Prestacao': prestacao,
            'Amortizacao': amortizacao,
            'Juros': juros,
            'Saldo_Devedor': max(0, saldo_devedor)
        })
    
    return pd.DataFrame(tabela)

def calcular_amortizacao_price(valor_principal, taxa_mensal, num_parcelas):
    """
    Calcula a amortização pelo sistema Price (Prestações Fixas)
    """
    prestacao = npf.pmt(taxa_mensal, num_parcelas, -valor_principal)
    tabela = []
    
    saldo_devedor = valor_principal
    
    for periodo in range(1, num_parcelas + 1):
        juros = saldo_devedor * taxa_mensal
        amortizacao = prestacao - juros
        saldo_devedor -= amortizacao
        
        tabela.append({
            'Periodo': periodo,
            'Prestacao': prestacao,
            'Amortizacao': amortizacao,
            'Juros': juros,
            'Saldo_Devedor': max(0, saldo_devedor)
        })
    
    return pd.DataFrame(tabela)

def calcular_amortizacao_sac_american(valor_principal, taxa_mensal, num_parcelas):
    """
    Calcula a amortização pelo sistema SAC Americano (juros pagos mensalmente, principal no final)
    """
    juros_mensal = valor_principal * taxa_mensal
    tabela = []
    
    for periodo in range(1, num_parcelas + 1):
        if periodo == num_parcelas:
            # Última parcela: juros + principal
            prestacao = juros_mensal + valor_principal
            amortizacao = valor_principal
            saldo_devedor = 0
        else:
            # Parcelas intermediárias: apenas juros
            prestacao = juros_mensal
            amortizacao = 0
            saldo_devedor = valor_principal
        
        tabela.append({
            'Periodo': periodo,
            'Prestacao': prestacao,
            'Amortizacao': amortizacao,
            'Juros': juros_mensal,
            'Saldo_Devedor': saldo_devedor
        })
    
    return pd.DataFrame(tabela)

def calcular_retorno_acao(preco_inicial, preco_final, dividendos=0):
    """
    Calcula o retorno total de uma ação
    """
    retorno_capital = (preco_final - preco_inicial) / preco_inicial
    retorno_dividendos = dividendos / preco_inicial
    retorno_total = retorno_capital + retorno_dividendos
    return retorno_total

def calcular_volatilidade(retornos):
    """
    Calcula a volatilidade (desvio padrão) dos retornos
    """
    return np.std(retornos)

def calcular_beta(retornos_acao, retornos_mercado):
    """
    Calcula o Beta de uma ação em relação ao mercado
    """
    covariancia = np.cov(retornos_acao, retornos_mercado)[0, 1]
    variancia_mercado = np.var(retornos_mercado)
    return covariancia / variancia_mercado

def calcular_sharpe_ratio(retornos, taxa_livre_risco=0.06):
    """
    Calcula o Sharpe Ratio (retorno ajustado ao risco)
    """
    retorno_medio = np.mean(retornos)
    volatilidade = np.std(retornos)
    if volatilidade == 0:
        return 0
    return (retorno_medio - taxa_livre_risco) / volatilidade

def calcular_max_drawdown(precos):
    """
    Calcula o máximo drawdown (maior queda) de uma série de preços
    """
    picos = np.maximum.accumulate(precos)
    drawdowns = (precos - picos) / picos
    return np.min(drawdowns)

def calcular_roi_fundo(valor_inicial, valor_final, taxas=0):
    """
    Calcula o ROI de um fundo de investimento
    """
    roi_bruto = (valor_final - valor_inicial) / valor_inicial
    roi_liquido = roi_bruto - taxas
    return roi_bruto, roi_liquido

def calcular_volatilidade_cripto(precos, periodo=30):
    """
    Calcula a volatilidade de uma criptomoeda
    """
    retornos = np.diff(np.log(precos))
    return np.std(retornos) * np.sqrt(periodo)

def calcular_correlacao_ativos(precos_ativos):
    """
    Calcula a matriz de correlação entre ativos
    """
    retornos = np.diff(np.log(precos_ativos), axis=0)
    return np.corrcoef(retornos.T)

def calcular_alocacao_otima(retornos_ativos, risco_alvo=0.1):
    """
    Calcula alocação ótima de portfólio (simplificado)
    """
    n_ativos = len(retornos_ativos)
    # Alocação igual (1/N)
    return np.ones(n_ativos) / n_ativos

def obter_lista_acoes_b3():
    """
    Retorna uma lista das principais ações da B3
    """
    acoes_b3 = {
        'PETR4.SA': 'Petrobras PN',
        'VALE3.SA': 'Vale ON',
        'ITUB4.SA': 'Itaú PN',
        'BBDC4.SA': 'Bradesco PN',
        'ABEV3.SA': 'Ambev ON',
        'WEGE3.SA': 'WEG ON',
        'RENT3.SA': 'Localiza ON',
        'LREN3.SA': 'Lojas Renner ON',
        'MGLU3.SA': 'Magazine Luiza ON',
        'JBSS3.SA': 'JBS ON',
        'SUZB3.SA': 'Suzano ON',
        'GGBR4.SA': 'Gerdau PN',
        'USIM5.SA': 'Usiminas PN',
        'CSAN3.SA': 'Cosan ON',
        'RAIL3.SA': 'Rumo ON',
        'CCRO3.SA': 'CCR ON',
        'EMBR3.SA': 'Embraer ON',
        'GOLL4.SA': 'Gol PN',
        'CVCB3.SA': 'CVC ON',
        'HAPV3.SA': 'Hapvida ON'
    }
    return acoes_b3

def buscar_dados_acao(ticker, periodo='1y'):
    """
    Busca dados históricos de uma ação usando yfinance
    """
    try:
        import yfinance as yf
        
        # Adiciona .SA para ações brasileiras se não estiver presente
        if not ticker.endswith('.SA'):
            ticker = ticker + '.SA'
        
        acao = yf.Ticker(ticker)
        dados = acao.history(period=periodo)
        
        if dados.empty:
            return None, "Nenhum dado encontrado para este ticker"
        
        return dados, None
        
    except Exception as e:
        return None, f"Erro ao buscar dados: {str(e)}"

def calcular_metricas_acao(dados):
    """
    Calcula métricas financeiras para uma ação
    """
    if dados is None or dados.empty:
        return None
    
    # Retornos diários
    retornos = dados['Close'].pct_change().dropna()
    
    # Métricas básicas
    preco_atual = dados['Close'].iloc[-1]
    preco_inicial = dados['Close'].iloc[0]
    retorno_periodo = (preco_atual - preco_inicial) / preco_inicial
    
    # Volatilidade anualizada
    volatilidade = retornos.std() * np.sqrt(252)
    
    # Retorno médio anualizado
    retorno_medio = retornos.mean() * 252
    
    # Máximo drawdown
    picos = dados['Close'].expanding().max()
    drawdowns = (dados['Close'] - picos) / picos
    max_drawdown = drawdowns.min()
    
    # Sharpe Ratio (assumindo taxa livre de risco de 6% ao ano)
    taxa_livre_risco = 0.06
    sharpe_ratio = (retorno_medio - taxa_livre_risco) / volatilidade if volatilidade > 0 else 0
    
    return {
        'preco_atual': preco_atual,
        'preco_inicial': preco_inicial,
        'retorno_periodo': retorno_periodo,
        'volatilidade': volatilidade,
        'retorno_medio': retorno_medio,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'retornos': retornos
    }

def buscar_dados_mercado(periodo='1y'):
    """
    Busca dados do índice Bovespa (^BVSP) como referência do mercado
    """
    try:
        import yfinance as yf
        
        mercado = yf.Ticker('^BVSP')
        dados = mercado.history(period=periodo)
        
        if dados.empty:
            return None, "Nenhum dado encontrado para o mercado"
        
        return dados, None
        
    except Exception as e:
        return None, f"Erro ao buscar dados do mercado: {str(e)}" 