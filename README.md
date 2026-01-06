# projeto-1.2-SVN

#!/usr/bin/env python3
# simulador_minimo.py
# Versão mínima: sem type hints, sem validações (assume entradas válidas). Saída no terminal.

import math

# HIPÓTESES (edite aqui)
HIPOTESES = {
    "CDI": 0.10,
    "IPCA": 0.04,
    "SELIC": 0.10,
    "USD_APP": 0.02
}
IR_PADRAO = 0.15

# Grupos de ações
ACOES_BR = ["petr4", "vale3", "itub4", "bbdc4", "abev3"]
ACOES_EX = ["aapl", "msft", "amzn", "nvda", "googl"]

# Dicionário de ativos (retornos hipotéticos)
assets = {
    "tesouro_selic": {"type":"renda_fixa","taxable":True,"return_nominal":HIPOTESES["SELIC"]},
    "tesouro_ipca_5": {"type":"renda_fixa_ipca","taxable":True,"return_nominal":HIPOTESES["IPCA"]+0.05},
    "lci_lca_95_cdi": {"type":"renda_fixa_isento","taxable":False,"return_nominal":HIPOTESES["CDI"]*0.95},
    "HGLG11": {"type":"fii","taxable":True,"return_nominal":0.10},
    "IVVB11": {"type":"etf_internacional","taxable":True,"return_nominal":0.09},
    "debentures_vale": {"type":"credito_privado","taxable":True,"return_nominal":HIPOTESES["IPCA"]+0.06},
    "petr4": {"type":"acao_brasil","taxable":True,"return_nominal":0.12},
    "vale3": {"type":"acao_brasil","taxable":True,"return_nominal":0.11},
    "itub4": {"type":"acao_brasil","taxable":True,"return_nominal":0.09},
    "bbdc4": {"type":"acao_brasil","taxable":True,"return_nominal":0.085},
    "abev3": {"type":"acao_brasil","taxable":True,"return_nominal":0.08},
    "aapl": {"type":"acao_exterior","taxable":True,"return_nominal":0.11},
    "msft": {"type":"acao_exterior","taxable":True,"return_nominal":0.11},
    "amzn": {"type":"acao_exterior","taxable":True,"return_nominal":0.12},
    "nvda": {"type":"acao_exterior","taxable":True,"return_nominal":0.15},
    "googl": {"type":"acao_exterior","taxable":True,"return_nominal":0.10},
    "BOVA11": {"type":"etf_brasil","taxable":True,"return_nominal":0.08},
    "dolar": {"type":"cambio","taxable":True,"return_nominal":HIPOTESES["USD_APP"]},
    "ouro": {"type":"commodity","taxable":True,"return_nominal":0.03},
    "bitcoin": {"type":"crypto","taxable":True,"return_nominal":0.30},
    "CDB_100_CDI": {"type":"renda_fixa","taxable":True,"return_nominal":HIPOTESES["CDI"]},
    "cdb_prefixado": {"type":"renda_fixa","taxable":True,"return_nominal":0.085},
    "fundo_investimento": {"type":"fundo","taxable":True,"return_nominal":0.095},
    "carteira_administrada": {"type":"carteira_administrada","taxable":True,"return_nominal":0.075}
}

# converter retornos USD -> BRL aproximado
for k in list(assets.keys()):
    if assets[k]["type"] in ("acao_exterior","etf_internacional"):
        r = assets[k]["return_nominal"]
        u = HIPOTESES["USD_APP"]
        assets[k]["return_brl"] = (1+r)*(1+u)-1
    else:
        assets[k]["return_brl"] = assets[k]["return_nominal"]

# gross-up simples
def gross_up_for_ir(target_net_return, ir=IR_PADRAO):
    return target_net_return / (1 - ir)

# expande acoes_br e acoes_ex
def expand_special(port):
    out = {}
    for k,w in port.items():
        key = k.lower()
        if key == "acoes_br":
            per = w / len(ACOES_BR)
            for a in ACOES_BR:
                out[a] = out.get(a,0.0) + per
        elif key == "acoes_ex":
            per = w / len(ACOES_EX)
            for a in ACOES_EX:
                out[a] = out.get(a,0.0) + per
        else:
            out[key] = out.get(key,0.0) + w
    return out

# normaliza alocacao
def normalize(port):
    s = sum(port.values())
    return {k: v/s for k,v in port.items()}

# calcula retorno esperado e breakdown
def portfolio_expected_return(port):
    expanded = expand_special(port)
    alloc = normalize(expanded)
    expected = 0.0
    breakdown = {}
    for k,w in alloc.items():
        r = assets[k]["return_brl"]
        c = w * r
        breakdown[k] = {"weight": w, "return": r, "contribution": c, "taxable": assets[k]["taxable"]}
        expected += c
    return expected, breakdown

# projeção determinística ano a ano
def project_portfolio(initial, contrib, years, expected_return):
    rows = []
    capital = initial
    for y in range(0, years+1):
        rows.append({"year": y, "start": capital})
        if y == years:
            break
        capital += contrib
        capital = capital * (1 + expected_return)
        rows[-1]["contribution"] = contrib
        rows[-1]["end"] = capital
        rows[-1]["annual_return"] = expected_return
    return rows

# métricas simples
def metrics_from_rows(rows, initial):
    final = rows[-1]["start"]
    years = rows[-1]["year"]
    total_contrib = initial + sum(r.get("contribution",0.0) for r in rows)
    cagr = (final / initial) ** (1/years) - 1 if years>0 else 0
    ret_val = final - total_contrib
    ret_pct = (final / total_contrib - 1) if total_contrib>0 else 0
    return {"final": final, "years": years, "initial": initial, "total_contrib": total_contrib, "cagr": cagr, "ret_val": ret_val, "ret_pct": ret_pct}

# prints
def print_breakdown(expected, breakdown):
    print("\nComposição e contribuição:")
    print(f"{'Ativo':12s} | {'Peso':>6s} | {'Ret.Ann':>8s} | {'Contrib':>8s} | {'IR?':>4s}")
    print("-"*60)
    for k,v in sorted(breakdown.items(), key=lambda x: x[1]["contribution"], reverse=True):
        print(f"{k:12s} | {v['weight']:6.2%} | {v['return']:8.2%} | {v['contribution']:8.2%} | {str(v['taxable']):>4s}")
    print(f"\nRetorno anual esperado (média ponderada): {expected:.4%} a.a.")

def print_projection(rows):
    print("\nProjeção ano a ano:")
    print(f"{'Ano':>3s} | {'Capital Início':>15s} | {'Contrib.':>10s} | {'Ret.anual':>8s} | {'Capital Final':>15s}")
    print("-"*80)
    for r in rows:
        year = r["year"]
        start = r["start"]
        if "end" in r:
            print(f"{year:3d} | R${start:13,.2f} | R${r['contribution']:8,.2f} | {r['annual_return']:8.2%} | R${r['end']:13,.2f}")
        else:
            print(f"{year:3d} | R${start:13,.2f} | {'-':>10s} | {'-':>8s} | {'-':>15s}")

def print_metrics(m):
    print("\nMétricas:")
    print(f"Valor final (R$): R${m['final']:,.2f}")
    print(f"Total contribuições (inclui inicial) (R$): R${m['total_contrib']:,.2f}")
    print(f"CAGR aproximado: {m['cagr']:.2%}")
    print(f"Retorno total (R$): R${m['ret_val']:,.2f} ({m['ret_pct']:.2%})")

# Construção da carteira via input (assume entradas válidas)
def build_portfolio_input():
    print("Digite pares 'ativo peso' (ex: BOVA11 0.3). Digite 'pronto' quando terminar.")
    port = {}
    while True:
        line = input().strip()
        if line.lower() == "pronto":
            break
        parts = line.split()
        key = parts[0]
        weight = float(parts[1])
        port[key] = port.get(key,0.0) + weight
    return port

# Ponto de entrada mínimo
if __name__ == "__main__":
    print("Simulador mínimo (digite carteira via input ou edite o dicionário 'portfolio' no código).")
    modo = input("Usar input interativo? (s/n) ").strip().lower()
    if modo == "s":
        portfolio = build_portfolio_input()
    else:
        portfolio = {
            "tesouro_ipca_5": 0.25,
            "lci_lca_95_cdi": 0.15,
            "HGLG11": 0.10,
            "IVVB11": 0.10,
            "debentures_vale": 0.05,
            "acoes_br": 0.10,
            "acoes_ex": 0.05,
            "CDB_100_CDI": 0.05,
            "ouro": 0.05,
            "bitcoin": 0.03,
            "fundo_investimento": 0.07
        }

    initial = float(input("Capital inicial (ex: 100000): "))
    contrib = float(input("Contribuição anual (ex: 10000): "))
    years = int(input("Horizonte (anos): "))

    expected, breakdown = portfolio_expected_return(portfolio)
    print_breakdown(expected, breakdown)

    rows = project_portfolio(initial, contrib, years, expected)
    print_projection(rows)

    m = metrics_from_rows(rows, initial)
    print_metrics(m)

    print("\nFim.")
