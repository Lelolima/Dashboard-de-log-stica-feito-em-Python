"""
Callbacks do Dashboard.

Todos os callbacks para interatividade do dashboard.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Output, Input, State, ctx, callback

from src.data.loader import DataLoader
from src.data.processor import DataProcessor
from src.visualizations import (
    create_map_chart,
    create_bar_chart,
    create_pie_chart,
)
from src.components.metrics_cards import render_metrics_cards
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ============================================
# Callbacks do Header
# ============================================

@callback(
    Output("body", "data-bs-theme"),
    Input("btn-toggle-theme", "n_clicks"),
    State("body", "data-bs-theme"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks: Optional[int], current_theme: str) -> str:
    """Alterna entre tema claro e escuro."""
    return "dark" if current_theme == "light" else "light"


@callback(
    Output("theme-icon", "className"),
    Input("btn-toggle-theme", "n_clicks"),
    State("body", "data-bs-theme"),
    prevent_initial_call=True,
)
def update_theme_icon(n_clicks: Optional[int], current_theme: str) -> str:
    """Atualiza o ícone do botão de tema."""
    # O tema ainda não mudou quando este callback é executado
    # Então mostramos o ícone oposto ao atual
    if current_theme == "dark":
        return "bi bi-sun-fill"  # Já está escuro, mostra sol
    return "bi bi-moon-stars-fill"  # Já está claro, mostra lua


@callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    State("store-data", "data"),
    prevent_initial_call=True,
)
def download_data(
    n_clicks: Optional[int],
    store_data: Optional[Dict[str, Any]],
):
    """Gera arquivo CSV para download."""
    if not store_data or "df_json" not in store_data:
        return None

    df = pd.read_json(store_data["df_json"])
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    return dcc.send_bytes(csv_bytes, filename="dashboard_export.csv")


# ============================================
# Callbacks Principais de Atualização (em tempo real)
# ============================================

@callback(
    [
        Output("map-chart", "figure"),
        Output("bar-chart-city", "figure"),
        Output("bar-chart-status", "figure"),
        Output("pie-chart-status", "figure"),
        Output("hub-capacity-chart", "figure"),
        Output("metrics-container", "children"),
    ],
    [
        Input("filter-state", "value"),
        Input("filter-city", "value"),
        Input("filter-hub", "value"),
        Input("filter-status", "value"),
    ],
    State("store-data", "data"),
)
def update_dashboard(
    states: Optional[List[str]] = None,
    cities: Optional[List[str]] = None,
    hubs: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
    store_data: Optional[Dict[str, Any]] = None,
) -> Tuple[go.Figure, go.Figure, go.Figure, go.Figure, go.Figure, html.Div]:
    """
    Atualiza todos os gráficos e métricas do dashboard em tempo real.

    Executa automaticamente quando qualquer filtro é alterado.
    """
    # Carregar dados
    if store_data and "df_json" in store_data:
        df = pd.read_json(store_data["df_json"])
    else:
        loader = DataLoader()
        df = loader.load_deliveries()

    # Aplicar filtros
    processor = DataProcessor(df)

    # Filtrar por estado (se selecionado)
    if states and len(states) > 0 and states != ["Todos"]:
        df_filtered = processor.filtrar_por_regiao(estado=states[0]).df
        processor = DataProcessor(df_filtered)

    # Filtrar por cidade (se selecionado)
    if cities and len(cities) > 0:
        df_filtered = processor.filtrar_por_regiao(cidade=cities[0]).df
        processor = DataProcessor(df_filtered)

    # Filtrar por hub (se selecionado)
    if hubs and len(hubs) > 0:
        df_filtered = processor.filtrar_por_hub(hubs).df
        processor = DataProcessor(df_filtered)

    # Filtrar por status (se selecionado)
    if statuses and len(statuses) > 0:
        df_filtered = processor.filtrar_por_status(statuses).df
        processor = DataProcessor(df_filtered)

    df_filtered = processor.df

    # Calcular métricas
    metrics = processor.calcular_metricas()

    # Criar visualizações
    map_fig = create_map_chart(processor.get_dados_mapa())
    bar_city_fig = create_bar_chart(df_filtered, group_by="city", height=350)
    bar_status_fig = create_bar_chart(df_filtered, group_by="status", height=350)
    pie_status_fig = create_pie_chart(df_filtered, group_by="status", height=350)

    # Gráfico de hubs
    loader = DataLoader()
    hubs_df = loader.load_hubs()

    if len(df_filtered) > 0 and "hub_id" in df_filtered.columns:
        hub_capacity_fig = create_bar_chart(df_filtered, group_by="hub_id", metric="total", height=350)
    else:
        hub_capacity_fig = go.Figure()

    # Renderizar cards de métrica
    metrics_cards = render_metrics_cards(metrics)

    logger.info(
        "Dashboard atualizado",
        rows_before=len(df),
        rows_after=len(df_filtered),
        filters={"states": states, "cities": cities, "hubs": hubs, "statuses": statuses},
    )

    return map_fig, bar_city_fig, bar_status_fig, pie_status_fig, hub_capacity_fig, metrics_cards


# ============================================
# Callback para Resetar Filtros
# ============================================

@callback(
    [
        Output("filter-state", "value"),
        Output("filter-city", "value"),
        Output("filter-hub", "value"),
        Output("filter-status", "value"),
    ],
    Input("btn-clear-filters", "n_clicks"),
    State("store-options", "data"),
    prevent_initial_call=True,
)
def clear_filters(
    n_clicks: Optional[int],
    store_options: Optional[Dict[str, Any]],
) -> Tuple[List[str], List[str], List[str], List[str]]:
    """Reseta todos os filtros para valores padrão."""
    if not store_options:
        return [], [], [], ["delivered", "in_transit", "pending"]

    # Reseta para selecionar todos os valores
    return (
        store_options.get("states", []),
        store_options.get("cities", []),
        store_options.get("hubs", []),
        ["delivered", "in_transit", "pending"],
    )


# ============================================
# Callback para Feedback Visual dos Botões
# ============================================

@callback(
    Output("btn-clear-filters", "color"),
    Input("btn-clear-filters", "n_clicks"),
    prevent_initial_call=True,
)
def clear_feedback(n_clicks: Optional[int]) -> str:
    """Feedback visual ao limpar filtros."""
    return "success"