import random


# ============================================================
#  GERADORES DE DADOS ALEATÓRIOS
# ============================================================

def gerar_energia():
    return {
        "solar": {
            "geracao_kw":     random.randint(20, 80),
            "paineis_ativos": random.randint(1, 8)
        },
        "eolico": {
            "geracao_kw":       random.randint(10, 50),
            "velocidade_vento": random.randint(5, 20)
        },
        "bateria": {
            "carga_atual":    random.randint(10, 100),
            "capacidade_max": 100
        }
    }


def gerar_consumo():
    return {
        "suporte_vida": random.randint(20, 30),
        "habitacao":    random.randint(10, 25),
        "logistica":    random.randint(5, 15),
        "ciencia":      random.randint(10, 30),
        "mineracao":    random.randint(15, 40)
    }


def gerar_clima():
    return {
        "vento_kmh":        random.randint(5, 20),
        "temperatura":      random.randint(-60, -20),
        "tempestade_areia": random.random() < 0.2
    }


# ============================================================
#  GERADOR PRINCIPAL
# ============================================================

def gerar_colonia():
    return {
        "energia": gerar_energia(),
        "consumo": gerar_consumo(),
        "clima":   gerar_clima()
    }
