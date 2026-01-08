TAXAS = {
    "CDI": 0.10,
    "IPCA": 0.05,
    "SELIC": 0.10,
    "USD": 0.02
}

ACOES_BR = ["petr4", "vale3", "itub4", "bbdc4", "abev3"]
ACOES_EUA = ["aapl", "msft", "amzn", "nvda", "googl"]

assets = {
    "tesouro_direto": {"return": TAXAS["SELIC"]},
    "tesouro_ipca": {"return": TAXAS["IPCA"] + 0.05},
    "lci": {"return": TAXAS["CDI"] * 0.95},
    "lca": {"return": TAXAS["CDI"] * 0.95},
    "fundos_imobiliarios": {"return": 0.10},
    "debentures": {"return": TAXAS["IPCA"] + 0.06},
    "etf_eua": {"return": (1 + 0.09) * (1 + TAXAS["USD"]) - 1},
    "etf_br": {"return": 0.08},
    "dolar": {"return": TAXAS["USD"]},
    "ouro": {"return": 0.03},
    "bitcoin": {"return": 0.20},
    "cdb": {"return": TAXAS["CDI"]},
    "cdb_pre_fixado": {"return": 0.105},
    "fundos_de_investimento": {"return": 0.095},
    "carteira_administrada": {"return": 0.12},

    "petr4": {"return": 0.14},
    "vale3": {"return": 0.13},
    "itub4": {"return": 0.12},
    "bbdc4": {"return": 0.12},
    "abev3": {"return": 0.11},
    "aapl": {"return": 0.13},
    "msft": {"return": 0.13},
    "amzn": {"return": 0.15},
    "nvda": {"return": 0.18},
    "googl": {"return": 0.13}
}

def expandir(port):
    novo = {}
    for k, w in port.items():
        if k == "acoes_br":
            for a in ACOES_BR:
                novo[a] = novo.get(a, 0) + w / len(ACOES_BR)
        elif k == "acoes_eua":
            for a in ACOES_EUA:
                novo[a] = novo.get(a, 0) + w / len(ACOES_EUA)
        else:
            novo[k] = novo.get(k, 0) + w
    return novo

def normalizar(port):
    s = sum(port.values())
    return {k: v / s for k, v in port.items()}

print("Digite os ativos no formato: nome_meio_sobrenome porcentagem(sem %)")
print("Exemplo: acoes_br 30 | etf_eua 15")
print("Digite 'pronto' quando finalizar.\n")

portfolio = {}
while True:
    entrada = input(">>> ").strip().lower()
    if entrada == "pronto":
        break
    ativo, peso = entrada.split()
    portfolio[ativo] = portfolio.get(ativo, 0) + float(peso) / 100

portfolio = normalizar(expandir(portfolio))

capital = float(input("\nCapital inicial (R$): "))
aporte = float(input("Contribuição anual (R$): "))
anos = int(input("Tempo investido (anos): "))
VTI = capital+(aporte*anos)

retorno = 0
print("\n=== COMPOSIÇÃO DA CARTEIRA ===")
for k, w in portfolio.items():
    r = assets[k]["return"]
    retorno += w * r
    print(f"{k:20s} | Peso: {w*100:.2f}% | Retorno: {r*100:.2f}%")

print(f"\nRetorno anual esperado da carteira: {retorno*100:.2f}%\n")

print("=== PROJEÇÃO ===")
valor = capital
for ano in range(1, anos + 1):
    valor += aporte
    valor *= (1 + retorno)
    print(f"Ano {ano:2d} → R$ {valor:,.2f}")


print("\n" + "-" * 40)
print(f"{'Resumo do Investimento':^40}")
print("-" * 40)

print(f"{'Valor total investido (R$):':<30} {VTI:>10,.2f}")
print(f"{'Lucro obtido (R$):':<30} {(valor - VTI):>10,.2f}")
print(f"{'Valorização (%):':<30} {((valor / VTI) * 100):>10.2f}")

print("-" * 40)

print("\nSimulação finalizada.")
