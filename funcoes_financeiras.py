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