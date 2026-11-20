# Projeto de Portfólio: Pipeline de Ponta a Ponta

Material gratuito do QG da Engenharia de Dados. Você recebeu porque comentou **PORTFOLIO**.

Um pipeline completo com dados reais do Banco Central: inflação (IPCA) e juros (Selic) caindo num dashboard.

## Como usar este material

1. Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/) e o Python
2. Suba o PostgreSQL e instale as dependências:

```bash
docker compose up -d
pip install -r requirements.txt
```

No Windows, se o `pip install` der erro de caminho longo → crie o ambiente numa pasta curta (ex: `python -m venv C:
env`) ou ative o Long Paths do Windows.

3. Rode as 3 etapas na ordem:

```bash
python extract/extrair.py                       # API → tabela raw
cd transform && dbt build --profiles-dir . && cd ..   # raw → staging → marts
streamlit run dashboard/app.py                  # marts → dashboard
```

4. O dashboard abre em [http://localhost:8501](http://localhost:8501)

## A arquitetura

```
API do Banco Central → extrair.py → PostgreSQL (raw) → dbt (staging → marts) → Streamlit
```

## Estrutura

```
extract/extrair.py              → busca IPCA e Selic na API e grava em raw.indicadores
transform/                      → projeto dbt
  models/staging/stg_indicadores.sql  → converte data e valor
  models/marts/indicadores_mensais.sql → IPCA, Selic, IPCA 12 meses e juro real
dashboard/app.py                → gráficos e números do mês
docker-compose.yml              → PostgreSQL
```

## Os dados

| Série | Código no Banco Central | O que é |
|---|---|---|
| IPCA | 433 | Inflação do mês (%) |
| Selic | 4390 | Juros acumulados no mês (%) |

Fonte → [API SGS do Banco Central](https://dadosabertos.bcb.gov.br), pública e sem cadastro.

## Como apresentar no portfólio

1. Coloque um print do dashboard no topo do README
2. Explique o problema → "acompanhar inflação e juros num lugar só"
3. Mostre a arquitetura com setas, como acima
4. Liste as decisões → por que dbt, por que camadas, por que carga idempotente
5. Diga o que faria a seguir → agendar com Airflow, subir na nuvem, adicionar testes de frescor

## Próximos passos para evoluir

→ Agendar com Airflow (material: comente **AIRFLOW**)
→ Trocar o PostgreSQL local por um banco na nuvem
→ Adicionar mais séries (dólar é a 1, desemprego é a 24369)

## QG da Engenharia de Dados

Este material é uma amostra do que você encontra no QG.

→ Trilha completa do zero ao sênior
→ Projetos reais para o portfólio
→ Comunidade para tirar dúvidas

Acesse → [qg-engenharia-de-dados.com.br](https://qg-engenharia-de-dados.com.br)
YouTube → [@gonzagadosdados](https://www.youtube.com/@gonzagadosdados)
