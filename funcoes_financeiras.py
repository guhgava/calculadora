import numpy as np
import numpy_financial as npf

def calcular_juros_compostos(capital, taxa, tempo):
    return capital * (1 + taxa) ** tempo

def calcular_vpl(fluxos, taxa):
    return npf.npv(taxa, fluxos)

def calcular_tir(fluxos):
    return npf.irr(fluxos) 