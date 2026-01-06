# simulador_interativo_minimo.py
# Simulador de carteiras 100% interativo (sem portfolio padrão)

# HIPÓTESES
HIPOTESES = {
    "CDI": 0.10,
    "IPCA": 0.04,
    "SELIC": 0.10,
    "USD_APP": 0.02
}

# Grupos de ações
ACOES_BR = ["petr4", "vale3", "itub4", "bbdc4", "abev3"]
ACOES_EX = ["aapl", "msft", "amzn", "nvda", "googl"]

# Ativos e retornos hipotéticos
assets = {
    "tesouro_selic": {"return": HIPOTESES["SELIC"]},
    "tesouro_ipca_5": {"return": HIPOTESES["IPCA"] + 0.05},
    "lci_lca_95_cdi": {"return": HIPOTESES["CDI"] * 0.95},
    "HGLG11": {"return": 0.10},
    "IVVB11": {"return": (1 + 0.09) * (1 + HIPOTESES["USD_APP"]) - 1},
    "debentures_vale": {"return": HIPOTESES["IPCA"] + 0.06},
    "petr4": {"return": 0.12},
    "vale3": {"return": 0.11},
    "itub4": {"return": 0.09},
    "bbdc4": {"return": 0.085},
    "abev3": {"return": 0.08},
    "aapl": {"return": (1 + 0.11) * (1 + HIPOTESES["USD_APP"]) - 1},
    "msft": {"return": (1 + 0.11) * (1 + HIPOTESES["USD_APP"]) - 1},
    "amzn": {"return": (1 + 0.12) * (1 + HIPOTESES["USD_APP"]) - 1},
    "nvda": {"return": (1 + 0.15) * (1 + HIPOTESES["USD_APP"]) - 1},
    "googl": {"return": (1 + 0.10) * (1 + HIPOTESES["USD_APP"]) - 1},
    "BOVA11": {"return": 0.08},
    "dolar": {"return": HIPOTESES["USD_APP"]},
    "ouro": {"return": 0.03},
    "bitcoin": {"return": 0.30},
    "CDB_100_CDI": {"return": HIPOTESES["CDI"]},
    "cdb_prefixado": {"return": 0.085},
    "fundo_investimento": {"return": 0.095},
    "carteira_administrada": {"return": 0.075}
}

# Expande acoes_br e acoes_ex
def expandir(port):
    novo = {}
    for k, w in port.items():
        if k == "acoes_br":
            for a in ACOES_BR:
                novo[a] = novo.get(a, 0) + w / len(ACOES_BR)
        elif k == "acoes_ex":
            for a in ACOES_EX:
                novo[a] = novo.get(a, 0) + w / len(ACOES_EX)
        else:
            novo[k] = novo.get(k, 0) + w
    return novo

# Normaliza pesos
def normalizar(port):
    s = sum(port.values())
    return {k: v / s for k, v in port.items()}

# Input da carteira
print("Digite os ativos no formato: ativo peso  (ex: acoes_br 0.3)")
print("Use 'acoes_br' ou 'acoes_ex' para ações. Digite 'pronto' ao final.\n")

portfolio = {}
while True:
    entrada = input(">>> ").strip().lower()
    if entrada == "pronto":
        break
    ativo, peso = entrada.split()
    portfolio[ativo] = portfolio.get(ativo, 0) + float(peso)

portfolio = normalizar(expandir(portfolio))

# Inputs financeiros
capital = float(input("\nCapital inicial (R$): "))
aporte = float(input("Contribuição anual (R$): "))
anos = int(input("Horizonte (anos): "))

# Retorno esperado
retorno = 0
for k, w in portfolio.items():
    retorno += w * assets[k]["return"]

# Impressão da carteira
print("\n=== COMPOSIÇÃO DA CARTEIRA ===")
for k, w in portfolio.items():
    print(f"{k:12s} | Peso: {w:.2%} | Retorno: {assets[k]['return']:.2%}")

print(f"\nRetorno anual esperado da carteira: {retorno:.2%}\n")

# Projeção
print("=== PROJEÇÃO ===")
valor = capital
for ano in range(1, anos + 1):
    valor += aporte
    valor *= (1 + retorno)
    print(f"Ano {ano:2d} → R$ {valor:,.2f}")

print("\nSimulação finalizada.")
