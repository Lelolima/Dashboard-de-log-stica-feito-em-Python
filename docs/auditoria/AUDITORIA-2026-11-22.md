# Auditoria — 2026-11-22

**Repositório:** Lelolima/Dashboard-de-log-stica-feito-em-Python
**Finalidade real:** dashboard Dash/Plotly de entregas (KPIs, mapa, gráficos e filtros). Sem `data/deliveries.json`, gera 500 entregas **simuladas** (seed 42). Não existe integração com a Loggi; o nome é só tema.
**Stack:** Python 3.11+, Dash, dash-bootstrap-components, Plotly, pandas, pydantic-settings, structlog, diskcache, waitress; pytest; Docker.

## Estado anterior
- CI (run 29378503297) falhando nos jobs **Lint** e **Tests**. Os logs expiraram (HTTP 410), então reproduzi localmente:
  - Lint: `ruff` com 249 erros (incluindo `F821` real) e `black` querendo reformatar 26 arquivos.
  - Tests: `ImportError: cannot import name 'create_heatmap'` na coleta. Depois disso, `test_get_dados_mapa` falhava porque a fixture não tinha coordenadas.
- **O app não funcionava:** `GET /` → HTTP 500 (`DuplicateIdError: metrics-container`).
- Imagem Docker quebrada: `CMD gunicorn ... src.app:server`, mas o gunicorn não está instalado e `src.app.server` não existe.

## Problemas encontrados

| # | Sev. | Problema | Evidência | Correção |
|---|------|----------|-----------|----------|
| 1 | P0 | Página inicial com HTTP 500 | `DuplicateIdError` (id repetido em `metrics_cards.py` e `app.py`) | id removido do componente filho; `tests/test_app.py` |
| 2 | P0 | Todos os filtros e o download quebravam no pandas 3 (`pd.read_json(str)`) | `FileNotFoundError` com o JSON no lugar do caminho | `StringIO`; `tests/test_callbacks.py` |
| 3 | P1 | Filtros de estado/cidade usavam só o 1º item marcado. Com todos marcados (padrão), o dashboard mostrava 1 estado | `states[0]` em `update_dashboard` | `isin(states)` / `isin(cities)` |
| 4 | P1 | Hover do gráfico de barras: f-string com nome indefinido `text` (NameError com `orientation="h"`), e o modo "v" perdia o valor | ruff F821, novo teste | Parênteses/escape corretos |
| 5 | P1 | `create_heatmap` importado pelos testes, mas inexistente | ImportError | Implementado com `go.Densitymap` (sem token). Plotly mínimo passou para 5.24 |
| 6 | P1 | Docker não iniciava | Dockerfile / `src.app:server` | `src/wsgi.py` + `waitress-serve`; imagem simplificada |
| 7 | P1 | `.env.example` e `docker-compose.yml` usavam nomes sem o prefixo `DASH_`, então as variáveis eram ignoradas | `env_prefix="DASH_"` em `src/config.py` | Arquivos corrigidos; `tests/test_config.py` |
| 8 | P1 | Dados simulados exibidos como operação real ("Dashboard Logística Loggi", sem aviso) | `_load_sample_data` | Alerta visível no layout quando os dados são de exemplo; nota no README |
| 9 | P2 | Exceções engolidas sem log no validador; variáveis mortas | ruff F841/SIM105 | `logger.warning`; código morto removido |
| 10 | P2 | Lint/format quebrados | 249 erros ruff, 26 arquivos black | `ruff --fix` + `black`. `C408` (`dict()`, estilo Plotly) ignorado no `ruff.toml` |
| 11 | P3 | README com URL de clone, comando de produção e variáveis errados | — | Corrigido |

**Segredos:** nada encontrado. Busquei padrões de chave (AWS, GitHub, OpenAI, Slack, Google, Mapbox `pk.eyJ`, chaves privadas) na árvore atual e no histórico (`git log -p --all`); gitleaks não está instalado. O `.env.example` tinha um placeholder `SECRET_KEY=sua-secret-key-aqui-mude-em-producao`, que não é segredo real; ficou só como comentário.

**Dependências (`pip-audit -r requirements.txt`):** `diskcache 5.6.3` — PYSEC-2026-2447, **sem versão corrigida disponível**. Ver riscos residuais.

## Testes executados (local, Windows, Python 3.13.15, pandas 3.1.1, plotly 7.1.0)
- `pytest` → **36 passed**.
- `ruff check src tests main.py` → All checks passed; `black --check` → ok.
- App executado de verdade: `waitress` servindo `src.wsgi:server` → `GET /` 200 e `GET /_dash-layout` 200. Antes da correção: 500.
- Os testes de callbacks foram executados contra o código antigo e falharam (3 failed), confirmando que reproduzem os defeitos.
- Docker build e smoke test do container: não rodei localmente; são validados pelo job `build` do CI.

## CI novo
`.github/workflows/ci.yml`: `permissions: contents: read`, actions fixadas por SHA, ruff/black com versão fixa, pytest e `docker build` com smoke test (`curl /`). Jobs de push no GHCR e de deploy removidos.

## Riscos residuais / decisões do dono
- **diskcache (PYSEC-2026-2447) sem correção upstream.** O backend padrão é `diskcache`. Se o diretório de cache puder ser escrito por terceiros, o risco é relevante. Alternativa sem mudar código: `DASH_CACHE_TYPE=memory`. Trocar a biblioteca é decisão do dono.
- Mudança de semântica no filtro: agora vale a seleção completa do checklist. Antes só o 1º item era considerado, o que tratei como bug; confirme se essa é a regra desejada.
- O mapa no callback não repassa `mapbox_token` (só o layout inicial usa). Não alterei.
- A cobertura total segue baixa (~50%): páginas e cache_manager quase sem testes.
