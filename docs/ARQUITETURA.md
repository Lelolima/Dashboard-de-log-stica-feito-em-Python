# Arquitetura do Dashboard

## Visão Geral

O Dashboard Logística Loggi segue uma arquitetura **modular e em camadas**, inspirada em **Clean Architecture** e **12 Factor App**.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         Camada de Apresentação                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐  │
│  │   Header    │ │   Sidebar   │ │   Cards     │ │  Footer   │  │
│  │ Component   │ │  Component  │ │  Component  │ │ Component │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Visualizações (Plotly)                    │ │
│  │  • Mapa           • Gráficos        • KPIs                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕_callbacks
┌─────────────────────────────────────────────────────────────────┐
│                      Camada de Aplicação                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐   │
│  │   DataProcessor     │  │   Callbacks (Dash)              │   │
│  │   • Filtrar         │  │   • Atualizar gráficos          │   │
│  │   • Calcular        │  │   • Toggle theme                │   │
│  │   • Agrupar         │  │   • Download data               │   │
│  └─────────────────────┘  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                        Camada de Dados                          │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐   │
│  │   DataLoader        │  │   Utils                         │   │
│  │   • API Local API   │  │   • Cache Manager               │   │
│  │   • Sample Data     │  │   • Logger                      │   │
│  │   • Validação       │  │   • Data Validator (Pydantic)   │   │
│  └─────────────────────┘  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Configurações (Settings)                   │
│              • Pydantic Settings • Variáveis de Ambiente        │
└─────────────────────────────────────────────────────────────────┘
```

## Módulos Principais

### 1. `src/app.py` - App Principal
**Responsabilidade**: bootstrap da aplicação, layout inicial, registro de callbacks.

**Dependências**:
- `config.settings`
- `data.loader`
- `components.*`
- `callbacks.*`

### 2. `src/config.py` - Configurações
**Responsabilidade**: centralizar configurações com validação Pydantic.

**Variáveis**:
- `DASH_HOST`, `DASH_PORT`, `DASH_DEBUG`
- `DASH_LOG_LEVEL`, `DASH_LOG_FORMAT`
- `MAPBOX_TOKEN`, `REDIS_URL`
- `DATA_SOURCE`, `DATA_API_URL`

### 3. `src/data/loader.py` - Carregamento de Dados
**Responsabilidade**: carregar dados de múltiplas fontes.

**Fontes suportadas**:
- Arquivos locais (JSON, CSV)
- API externa via HTTP
- Dados de exemplo (fallback)

**Cache**: Resultados cacheados via `CacheManager` (diskcache ou Redis).

### 4. `src/data/processor.py` - Processamento
**Responsabilidade**: transformar dados brutos em métricas.

**Operações**:
- `calcular_metricas()` → retorna KPIs
- `filtrar_por_regiao()` → estado, cidade
- `filtrar_por_status()` → status da entrega
- `filtrar_por_hub()` → hub específico
- `agrupar_por_cidade()` → aggregação por cidade
- `agrupar_por_hub()` → utilização por hub

### 5. `src/visualizations.py` - Gráficos
**Responsabilidade**: criar figuras Plotly.

**Gráficos**:
- `create_map_chart()` → mapa com entregas
- `create_bar_chart()` → barras verticais/horizontais
- `create_pie_chart()` → pizza/rosca
- `create_heatmap()` → densidade geográfica
- `create_hub_capacity_chart()` → capacidade por hub

### 6. `src/components/*` - Componentes UI
**Responsabilidade**: componentes Dash reutilizáveis.

**Componentes**:
- `header.py` → logo, título, toggle theme, download
- `sidebar.py` → filtros (accordion, checklist)
- `metrics_cards.py` → 4 KPI cards
- `footer.py` → créditos, links, versão

### 7. `src/callbacks.py` - Callbacks
**Responsabilidade**: interatividade do dashboard.

**Callbacks**:
- `toggle_theme()` → dark/light mode
- `download_data()` → exportar CSV
- `toggle_sidebar()` → mobile sidebar
- `update_dashboard()` → atualizar gráficos ao filtrar
- `clear_filters()` → resetar filtros

### 8. `src/utils/*` - Utilitários

#### `logger.py`
Logging estruturado com structlog:
- JSON em produção
- Console colorido em desenvolvimento

#### `cache_manager.py`
Gerenciador de cache multi-backend:
- diskcache (default)
- Redis (opcional)
- Memory (fallback)

#### `data_validator.py`
Schemas Pydantic para validação:
- `DeliverySchema`
- `HubSchema`
- `DeliveryMetrics`

## Fluxo de Dados

```
1. Usuário abre dashboard
         ↓
2. DataLoader carrega dados (cache ou fonte)
         ↓
3. DataProcessor calcula métricas iniciais
         ↓
4. Visualizations cria gráficos iniciais
         ↓
5. Components renderizam layout
         ↓
6. Usuário aplica filtro
         ↓
7. Callback update_dashboard() é disparado
         ↓
8. DataProcessor filtra dados
         ↓
9. Visualizations recria gráficos
         ↓
10. Frontend atualiza (sem reload)
```

## Decisões de Design

### Por que Dash?
- **React sem JavaScript**: componentes em Python puro
- **Interatividade nativa**: callbacks automáticos
- **Plotly integrado**: melhores gráficos do mercado
- **Enterprise-ready**: usado por Uber, Amazon, Google

### Por que Pydantic?
- Validação automática de dados
- Type hints com runtime checking
- Settings management com variáveis de ambiente
- Melhor DX (Developer Experience)

### Por que structlog?
- Logs estruturados (JSON) fáceis de parsear
- Contexto automático em cada log
- Performance melhor que logging padrão
- Integração com ELK/Datadog/Splunk

### Por que Cache?
- Evita recarregar dados a cada filtro
- diskcache: zero configuração, file-based
- Redis: opcional para produção com múltiplas instâncias

## Extensibilidade

### Adicionar Novo Gráfico

```python
# src/visualizations.py
def create_new_chart(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="city", y="count")
    fig.update_layout(title="Novo Gráfico")
    return fig

# src/app.py
dcc.Graph(id="new-chart", figure=create_new_chart(df))

# src/callbacks.py
@callback(Output("new-chart", "figure"), Input("filter", "value"))
def update_new_chart(value):
    return create_new_chart(filtered_df)
```

### Adicionar Nova Fonte de Dados

```python
# src/data/loader.py
def _load_from_database(self) -> pd.DataFrame:
    import psycopg2
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return pd.read_sql("SELECT * FROM deliveries", conn)
```

## Segurança

- **Variáveis de ambiente**: credenciais fora do código
- **Usuário não-root** no Docker
- **Health checks** para monitoramento
- **Rate limiting** (via gunicorn/proxy reverso)

## Performance

- **Cache de dados**: 300s TTL default
- **Lazy loading**: dados carregados sob demanda
- **Filtering no backend**: evita transferir dados desnecessários
- **Gunicorn workers**: 4 workers default em produção