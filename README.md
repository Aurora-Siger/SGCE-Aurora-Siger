<div align="center">

# ⚡ SGCE — Sistema de Gestão da Colônia Espacial
### *Gerenciamento Energético Automatizado — Missão Aurora Siger*

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/Persistência-JSON-F7DF1E?style=for-the-badge&logo=json&logoColor=black)
![Status](https://img.shields.io/badge/Status-Operacional-28a745?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-PBL%20Fase%203-ED1C24?style=for-the-badge)

<br/>

> Sistema de monitoramento e tomada de decisão energética da **Colônia Aurora Siger**.  
> Processa geração solar e eólica, balanceia consumo por setor e emite alertas automáticos  
> com base em regras operacionais — com **previsão adaptativa via regressão linear**.

</div>

---

## 👨‍🚀 Equipe

| Nome | RM |
|---|---|
| Isabelle Caroline de Camargo Francisco | 572096 |
| Matheus Lyncoln Souza Dias | 570765 |
| Mirela Aparecida Bispo Miguel | 70830 |
| Rodrigo Abrantes Mizerani | 571808 |

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Módulos do Sistema](#-módulos-do-sistema)
- [Algoritmo de Decisão](#-algoritmo-de-decisão)
- [Regressão Linear](#-regressão-linear)
- [Dataset](#-dataset)
- [Como Executar](#-como-executar)
- [Exemplo de Saída](#-exemplo-de-saída)

---

## 🌌 Sobre o Projeto

O **SGCE** (Sistema de Gestão da Colônia Espacial) é desenvolvido como parte do **PBL (Project-Based Learning) da FIAP**, Fase 3 da missão Aurora Siger.

O sistema simula o núcleo de controle energético de uma colônia marciana: a cada turno ele lê os dados gerados pelo simulador, avalia o estado atual da colônia e emite decisões automáticas de operação, além de projetar tendências futuras de geração e consumo.

As fases anteriores da Missão Aurora Siger produziram dois sistemas complementares. A Fase 1 desenvolveu o sistema de verificação pré-decolagem, responsável por validar as condições de segurança antes da partida. A Fase 2 implementou o MGPEB, que coordenou o pouso sequencial dos seis módulos em Arcadia Planitia utilizando filas, pilhas e validação dos três estágios de descida.

Os módulos pousados na Fase 2 agora operam. O SGCE, da fase 3, gerencia a energia da colônia: organiza os dados, toma decisões automáticas, prevê geração e analisa consumo. Os módulos utilizados foram definidos na Fase 2 e estão documentados no repositório do MGPEB: https://github.com/Aurora-Siger/MGPEB-Aurora-aproxima-Marte


---

## 🗂 Estrutura do Projeto

```
SGCE-Aurora-Siger/
├── README.md
├── main.py          # Motor principal — decisão, análise e previsão
├── dataset.py       # Gerador de dados simulados e persistência JSON
└── historico.json   # Gerado automaticamente ao executar dataset.py
```

---

## 🔧 Módulos do Sistema

O SGCE é composto por dois arquivos Python com responsabilidades bem definidas:

### `dataset.py` — Simulador e Persistência

| Função | Responsabilidade |
|---|---|
| `gerar_energia()` | Gera dados de geração solar, eólica e carga da bateria |
| `gerar_consumo()` | Gera o consumo de cada setor operacional da colônia |
| `gerar_clima()` | Gera condições climáticas: vento, temperatura e tempestade |
| `gerar_colonia()` | Agrupa energia, consumo e clima em um único registro de turno |
| `gerar_historico(n)` | Gera `n` turnos e salva tudo no `historico.json` |
| `carregar_historico()` | Lê e retorna o histórico salvo do `historico.json` |

### `main.py` — Motor de Decisão

| Função | Responsabilidade |
|---|---|
| `decisao_automatica()` | Avalia o estado e emite o modo de operação da colônia |
| `analisar_energia()` | Calcula cobertura de geração, autonomia da bateria e eficiência por setor |
| `regressao_linear()` | Implementação dos mínimos quadrados do zero — sem bibliotecas externas |
| `prever_geracao_eolica()` | Projeta a geração eólica esperada dado um valor de vento |
| `prever_consumo_turno()` | Projeta o consumo total esperado para um turno futuro |
| `executar_sgce()` | Orquestra todas as funções acima para o turno mais recente |
| `exibir_historico()` | Exibe o resumo dos últimos N turnos registrados |

---

## 🧠 Algoritmo de Decisão

O `decisao_automatica()` avalia quatro condições em ordem de prioridade a cada turno:

```
┌──────────────────────────────────────────────┐
│              INÍCIO DO TURNO                 │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
      ┌────────────────────────────┐
      │  reserva_pct < 20%         │
      │         E                  │── SIM ──► 🔴 EMERGÊNCIA: RESERVA CRÍTICA
      │  consumo > geração?        │           Mineração: DESLIGADA
      └────────────┬───────────────┘           Ciência: DESLIGADA
                   │ NÃO                       Suporte à vida: mantido
                   ▼
      ┌────────────────────────────┐
      │  tempestade_areia == True? │── SIM ──► 🟠 EMERGÊNCIA: TEMPESTADE
      └────────────┬───────────────┘           Painéis solares: DESLIGADOS
                   │ NÃO                       Opera na reserva da bateria
                   ▼                           Suporte à vida: mantido
      ┌────────────────────────────┐
      │  consumo > geração?        │── SIM ──► 🟡 ALERTA
      └────────────┬───────────────┘           Reduzir consumo não essencial
                   │ NÃO                       Suporte à vida: mantido
                   ▼
      ┌────────────────────────────┐
      │  geração > consumo × 1.2?  │── SIM ──► 🟢 OTIMIZAÇÃO
      └────────────┬───────────────┘           Armazenar excedente na bateria
                   │ NÃO
                   ▼
              🔵 NORMAL — operação padrão
```

### Modos de Operação

| Modo | Condição | Ação |
|---|---|---|
| 🔴 **EMERGÊNCIA — Reserva Crítica** | `reserva_pct < 20` **e** `consumo > geração` | Desliga mineração e ciência. Suporte à vida mantido. |
| 🟠 **EMERGÊNCIA — Tempestade** | `tempestade_areia == True` | Desliga painéis solares. Opera 100% na bateria. |
| 🟡 **ALERTA** | `consumo > geração` | Reduz consumo não essencial. |
| 🟢 **OTIMIZAÇÃO** | `geração > consumo × 1.2` | Armazena excedente na bateria. |
| 🔵 **NORMAL** | Nenhuma das anteriores | Todos os sistemas operando normalmente. |

> O **suporte à vida** jamais é cortado em nenhum modo de operação — é a única variável com prioridade absoluta e incondicional no sistema.

---

## 📈 Regressão Linear

O SGCE implementa regressão linear dos **mínimos quadrados completamente do zero**, sem nenhuma biblioteca externa, dentro da função `regressao_linear()`.

Ela é chamada por duas funções especializadas:

- **`prever_geracao_eolica(vento_novo)`** — usa os 6 turnos do histórico para correlacionar `velocidade_vento` → `geracao_kw` eólica e prever a geração esperada para um vento informado.
- **`prever_consumo_turno(turno_novo)`** — usa os 6 turnos para ajustar uma reta ao consumo total ao longo do tempo e projetar o consumo de qualquer turno futuro.

### Fórmulas aplicadas

```
       n · Σ(xᵢ · yᵢ)  −  Σxᵢ · Σyᵢ
  a = ────────────────────────────────    (coeficiente angular)
          n · Σ(xᵢ²)  −  (Σxᵢ)²

  b = ( Σyᵢ  −  a · Σxᵢ ) / n           (intercepto)

  ŷ = a · x_novo + b                     (valor previsto)
```

A regressão é **recalculada a cada execução** com os dados mais recentes do `historico.json`, tornando as previsões adaptativas ao comportamento real registrado da colônia.

---

## 📦 Dataset

O `historico.json` é gerado automaticamente ao rodar `dataset.py`. Cada execução **substitui completamente** o arquivo anterior com 6 novos turnos simulados.

### Campos de cada turno

| Campo | Tipo | Faixa simulada | Descrição |
|---|---|---|---|
| `turno` | int | 1 – 6 | Número sequencial do turno |
| `energia.solar.geracao_kw` | int | 20 – 80 kW | Geração pelos painéis fotovoltaicos |
| `energia.solar.paineis_ativos` | int | 1 – 8 | Painéis em operação |
| `energia.eolico.geracao_kw` | int | 10 – 50 kW | Geração pelas turbinas eólicas |
| `energia.eolico.velocidade_vento` | int | 5 – 20 km/h | Velocidade do vento medida |
| `energia.bateria.carga_atual` | int | 10 – 100 kWh | Nível atual da bateria |
| `energia.bateria.capacidade_max` | int | 100 kWh (fixo) | Capacidade nominal instalada |
| `consumo.suporte_vida` | int | 20 – 30 kW | Consumo do suporte à vida |
| `consumo.habitacao` | int | 10 – 25 kW | Consumo dos módulos habitacionais |
| `consumo.logistica` | int | 5 – 15 kW | Consumo da logística |
| `consumo.ciencia` | int | 10 – 30 kW | Consumo dos laboratórios |
| `consumo.mineracao` | int | 15 – 40 kW | Consumo da mineração / ISRU |
| `clima.vento_kmh` | int | 5 – 20 km/h | Vento climático geral |
| `clima.temperatura` | int | −60 a −20 °C | Temperatura ambiente em Marte |
| `clima.tempestade_areia` | bool | 20% de chance | Presença de tempestade de areia |

### Exemplo fixo de `historico.json` (seed=42)

O exemplo abaixo foi gerado com semente fixa para garantir reprodutibilidade na demonstração:

<details>
<summary><b>🔽 Clique para expandir o historico.json completo</b></summary>

```json
[
  {
    "turno": 1,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 60, "paineis_ativos": 2 },
        "eolico":  { "geracao_kw": 11, "velocidade_vento": 13 },
        "bateria": { "carga_atual": 41, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 23, "habitacao": 14,
        "logistica": 6, "ciencia": 27, "mineracao": 17
      },
      "clima": { "vento_kmh": 18, "temperatura": -58, "tempestade_areia": true }
    }
  },
  {
    "turno": 2,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 33, "paineis_ativos": 4 },
        "eolico":  { "geracao_kw": 42, "velocidade_vento": 5 },
        "bateria": { "carga_atual": 81, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 23, "habitacao": 23,
        "logistica": 8, "ciencia": 24, "mineracao": 33
      },
      "clima": { "vento_kmh": 13, "temperatura": -60, "tempestade_areia": false }
    }
  },
  {
    "turno": 3,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 30, "paineis_ativos": 7 },
        "eolico":  { "geracao_kw": 31, "velocidade_vento": 13 },
        "bateria": { "carga_atual": 29, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 23, "habitacao": 20,
        "logistica": 6, "ciencia": 12, "mineracao": 27
      },
      "clima": { "vento_kmh": 8, "temperatura": -38, "tempestade_areia": false }
    }
  },
  {
    "turno": 4,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 58, "paineis_ativos": 5 },
        "eolico":  { "geracao_kw": 12, "velocidade_vento": 19 },
        "bateria": { "carga_atual": 78, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 21, "habitacao": 22,
        "logistica": 6, "ciencia": 27, "mineracao": 24
      },
      "clima": { "vento_kmh": 16, "temperatura": -24, "tempestade_areia": true }
    }
  },
  {
    "turno": 5,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 24, "paineis_ativos": 1 },
        "eolico":  { "geracao_kw": 24, "velocidade_vento": 14 },
        "bateria": { "carga_atual": 20, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 23, "habitacao": 13,
        "logistica": 11, "ciencia": 18, "mineracao": 29
      },
      "clima": { "vento_kmh": 16, "temperatura": -50, "tempestade_areia": false }
    }
  },
  {
    "turno": 6,
    "dados": {
      "energia": {
        "solar":   { "geracao_kw": 33, "paineis_ativos": 5 },
        "eolico":  { "geracao_kw": 14, "velocidade_vento": 10 },
        "bateria": { "carga_atual": 78, "capacidade_max": 100 }
      },
      "consumo": {
        "suporte_vida": 23, "habitacao": 15,
        "logistica": 12, "ciencia": 22, "mineracao": 23
      },
      "clima": { "vento_kmh": 12, "temperatura": -40, "tempestade_areia": false }
    }
  }
]
```

</details>

---

## ▶ Como Executar

**Pré-requisito:** Python 3.10 ou superior — sem dependências externas.

**1. Clone o repositório**
```bash
git clone hhttps://github.com/Aurora-Siger/SGCE-Aurora-Siger.git
cd SGCE-Aurora-Siger
```

**2. Gere o histórico de dados**
```bash
python dataset.py
```
> Cria o `historico.json` com 6 turnos simulados. Execute sempre antes de rodar o `main.py`.

**3. Rode o sistema**
```bash
python main.py
```

---

## 🖥 Exemplo de Saída

Saída do `main.py` com o `historico.json` de exemplo acima — **turno 6** como estado atual:

```
========================================
 SGCE — COLÔNIA AURORA SIGER
========================================
  Geração total  : 47 kW
  Painéis ativos : 5
  Consumo total  : 95 kW
  Bateria        : 78% (78 / 100 kWh)
  Vento (eólico) : 10 km/h
  Tempestade     : False

=== DECISÃO AUTOMÁTICA ===
ALERTA: Consumo maior que geração.
  -> Reduzir consumo não essencial.
  -> Suporte à vida mantido (prioridade máxima).

=== ANÁLISE DE ENERGIA ===
ALERTA: consumo maior que geração.
  A geração cobre 49.5% do consumo atual.
  Reserva sustenta a colônia por 0.8 hora(s).

  Eficiência por sistema:
    suporte_vida: 24.2% do consumo total
    habitacao: 15.8% do consumo total
    logistica: 12.6% do consumo total
    ciencia: 23.2% do consumo total
    mineracao: 24.2% do consumo total

=== PREVISÃO: GERAÇÃO EÓLICA ===
  Vento informado: 10 km/h
  Energia eólica prevista: 26.5 kW

=== PREVISÃO: CONSUMO POR TURNO ===
  Turno informado: 3
  Consumo previsto: 95.8 kW

========================================

========================================
 HISTÓRICO — últimas 5 de 6 execuções
========================================
  [Turno   2]  Geração: 75 kW | Consumo: 111 kW | Bateria: 81% | Tempestade: NÃO
  [Turno   3]  Geração: 61 kW | Consumo:  88 kW | Bateria: 29% | Tempestade: NÃO
  [Turno   4]  Geração: 70 kW | Consumo: 100 kW | Bateria: 78% | Tempestade: SIM
  [Turno   5]  Geração: 48 kW | Consumo:  94 kW | Bateria: 20% | Tempestade: NÃO
  [Turno   6]  Geração: 47 kW | Consumo:  95 kW | Bateria: 78% | Tempestade: NÃO
========================================
```

---

<div align="center">

*Desenvolvido com ☕ e Python · FIAP 2026*

</div>
