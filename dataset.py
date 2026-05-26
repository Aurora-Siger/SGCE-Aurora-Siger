import random
import json
import os

HISTORICO_PATH = os.path.join(os.path.dirname(__file__), "historico.json")


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


def gerar_colonia():
    return {
        "energia": gerar_energia(),
        "consumo": gerar_consumo(),
        "clima":   gerar_clima()
    }


# ============================================================
#  PERSISTÊNCIA DE HISTÓRICO
# ============================================================

def gerar_historico(n: int = 6) -> None:
    """Gera n turnos e salva no JSON, substituindo completamente o anterior."""
    registros = [
        {"turno": turno, "dados": gerar_colonia()}
        for turno in range(1, n + 1)
    ]
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)


def carregar_historico() -> list:
    if not os.path.exists(HISTORICO_PATH):
        return []
    with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    gerar_historico(6)
    print(f"Histórico de 6 turnos gerado em: {HISTORICO_PATH}")
