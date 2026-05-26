import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from dataset import carregar_historico


# ============================================================
#  1. DATASET — COLÔNIA AURORA SIGER  (fonte: historico.json)
# ============================================================

historico = carregar_historico()
if not historico:
    raise RuntimeError("historico.json não encontrado. Execute dataset.py primeiro.")

colonia = historico[-1]["dados"]   

amostras = [r["dados"] for r in historico]
turnos   = [r["turno"] for r in historico]

vento   = [a["energia"]["eolico"]["velocidade_vento"] for a in amostras]
energia = [a["energia"]["eolico"]["geracao_kw"]        for a in amostras]
turno   = turnos
consumo = [sum(a["consumo"].values())                  for a in amostras]


# ============================================================
#  2. LÓGICA DE DECISÃO AUTOMÁTICA
# ============================================================

def decisao_automatica(geracao, consumo, reserva_pct, tempestade_areia):
    print("\n=== DECISÃO AUTOMÁTICA ===")

    if reserva_pct < 20 and consumo > geracao:
        print("EMERGÊNCIA: Reserva crítica e consumo acima da geração.")
        print("  -> Mineração: DESLIGADA.")
        print("  -> Ciência: DESLIGADA.")
        print("  -> Suporte à vida mantido (prioridade máxima).")

    elif tempestade_areia:
        print("EMERGÊNCIA: Tempestade de areia detectada.")
        print("  -> Painéis solares desligados.")
        print("  -> Sistema operando com reserva da bateria.")
        print("  -> Suporte à vida mantido (prioridade máxima).")

    elif consumo > geracao:
        print("ALERTA: Consumo maior que geração.")
        print("  -> Reduzir consumo não essencial.")
        print("  -> Suporte à vida mantido (prioridade máxima).")

    elif geracao > consumo * 1.2:
        print("OTIMIZAÇÃO: Geração excede consumo em 20%.")
        print("  -> Sugestão: armazenar energia excedente na bateria.")

    else:
        print("OK: Operação normal.")
        print("  -> Todos os sistemas funcionando dentro do esperado.")


# ============================================================
#  3. ANÁLISE DE ENERGIA
# ============================================================

def analisar_energia(geracao, consumo, reserva_kwh, consumo_por_sistema):
    print("\n=== ANÁLISE DE ENERGIA ===")

    if consumo > geracao:
        print("ALERTA: consumo maior que geração.")
    elif geracao > consumo:
        print("SUGESTÃO: armazenar energia excedente.")
    else:
        print("Geração igual ao consumo.")

    cobertura = (geracao / consumo) * 100
    print(f"  A geração cobre {cobertura:.1f}% do consumo atual.")

    autonomia = reserva_kwh / consumo
    print(f"  Reserva sustenta a colônia por {autonomia:.1f} hora(s).")

    print("\n  Eficiência por sistema:")
    for sistema, valor in consumo_por_sistema.items():
        percentual = (valor / consumo) * 100
        print(f"    {sistema}: {percentual:.1f}% do consumo total")


# ============================================================
#  4. PREVISÃO POR REGRESSÃO LINEAR
# ============================================================

def regressao_linear(x_lista, y_lista, x_novo):
    n   = len(x_lista)
    sx  = sum(x_lista)
    sy  = sum(y_lista)
    sxy = sum(x_lista[i] * y_lista[i] for i in range(n))
    sx2 = sum(x_lista[i] ** 2 for i in range(n))

    a = (n * sxy - sx * sy) / (n * sx2 - sx ** 2)
    b = (sy - a * sx) / n

    return round(a * x_novo + b, 1)


def prever_geracao_eolica(vento_novo):
    resultado = regressao_linear(vento, energia, vento_novo)
    print(f"\n=== PREVISÃO: GERAÇÃO EÓLICA ===")
    print(f"  Vento informado: {vento_novo} km/h")
    print(f"  Energia eólica prevista: {resultado} kW")
    return resultado


def prever_consumo_turno(turno_novo):
    resultado = regressao_linear(turno, consumo, turno_novo)
    print(f"\n=== PREVISÃO: CONSUMO POR TURNO ===")
    print(f"  Turno informado: {turno_novo}")
    print(f"  Consumo previsto: {resultado} kW")
    return resultado


# ============================================================
#  5. EXECUÇÃO DO SISTEMA
# ============================================================

def executar_sgce(colonia):
    geracao_solar    = colonia["energia"]["solar"]["geracao_kw"]
    paineis_ativos   = colonia["energia"]["solar"]["paineis_ativos"]
    geracao_eolica   = colonia["energia"]["eolico"]["geracao_kw"]
    velocidade_vento = colonia["energia"]["eolico"]["velocidade_vento"]
    carga_bateria    = colonia["energia"]["bateria"]["carga_atual"]
    capacidade_max   = colonia["energia"]["bateria"]["capacidade_max"]

    consumo_por_sistema = colonia["consumo"]
    consumo_total = sum(consumo_por_sistema.values())
    geracao_total = geracao_solar + geracao_eolica
    reserva_pct   = (carga_bateria / capacidade_max) * 100

    tempestade_areia = colonia["clima"]["tempestade_areia"]

    print("========================================")
    print(" SGCE — COLÔNIA AURORA SIGER")
    print("========================================")
    print(f"  Geração total  : {geracao_total} kW")
    print(f"  Painéis ativos : {paineis_ativos}")
    print(f"  Consumo total  : {consumo_total} kW")
    print(f"  Bateria        : {reserva_pct:.0f}% ({carga_bateria} / {capacidade_max} kWh)")
    print(f"  Vento (eólico) : {velocidade_vento} km/h")
    print(f"  Tempestade     : {tempestade_areia}")

    decisao_automatica(geracao_total, consumo_total, reserva_pct, tempestade_areia)
    analisar_energia(geracao_total, consumo_total, carga_bateria, consumo_por_sistema)
    prever_geracao_eolica(velocidade_vento)
    prever_consumo_turno(3)

    print("\n========================================")


executar_sgce(colonia)


# ============================================================
#  6. HISTÓRICO DE EXECUÇÕES
# ============================================================

def exibir_historico(ultimos: int = 5) -> None:
    historico = carregar_historico()
    total = len(historico)
    if total == 0:
        print("\n[HISTÓRICO] Nenhum registro encontrado.")
        return

    print(f"\n========================================")
    print(f" HISTÓRICO — últimas {min(ultimos, total)} de {total} execuções")
    print(f"========================================")

    for registro in historico[-ultimos:]:
        turno = registro["turno"]
        d     = registro["dados"]
        gen   = d["energia"]["solar"]["geracao_kw"] + d["energia"]["eolico"]["geracao_kw"]
        cons  = sum(d["consumo"].values())
        bat   = d["energia"]["bateria"]["carga_atual"]
        temp  = "SIM" if d["clima"]["tempestade_areia"] else "NÃO"
        print(f"  [Turno {turno:>3}]  Geração: {gen} kW | Consumo: {cons} kW | "
              f"Bateria: {bat}% | Tempestade: {temp}")

    print("========================================")


exibir_historico()
