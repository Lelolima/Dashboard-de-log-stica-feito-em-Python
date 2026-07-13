"""
Componente de Sidebar para o Dashboard.

Inclui filtros por região, hub, status e controles.
"""

from typing import List, Dict, Any, Optional
import dash_bootstrap_components as dbc
from dash import html


def render_sidebar(
    cities: Optional[List[str]] = None,
    states: Optional[List[str]] = None,
    hubs: Optional[List[Dict[str, str]]] = None,
    statuses: Optional[List[str]] = None,
) -> dbc.Card:
    """
    Renderiza a sidebar com filtros.

    Args:
        cities: Lista de cidades disponíveis
        states: Lista de estados disponíveis
        hubs: Lista de hubs disponíveis
        statuses: Lista de statuses disponíveis

    Returns:
        Card com controles de filtro
    """
    cities = cities or []
    states = states or []
    hubs = hubs or []
    statuses = statuses or []

    sidebar = dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.I(className="bi bi-funnel-fill me-2"),
                    "Filtros",
                ],
                className="bg-primary text-white",
            ),
            dbc.CardBody(
                [
                    # Filtro por Estado
                    html.Label("Estado (UF)", className="form-label fw-semibold"),
                    dbc.Checklist(
                        options=[{"label": s, "value": s} for s in states],
                        value=states,
                        id="filter-state",
                        className="mb-3",
                        switch=True,
                    ),

                    # Filtro por Cidade
                    html.Label("Cidade", className="form-label fw-semibold"),
                    dbc.Checklist(
                        options=[{"label": c, "value": c} for c in cities],
                        value=cities,
                        id="filter-city",
                        className="mb-3",
                        switch=True,
                    ),

                    # Filtro por Hub
                    html.Label("Hub", className="form-label fw-semibold"),
                    dbc.Checklist(
                        options=[{"label": h.get("hub_name", h.get("id", "")), "value": h.get("id", "")} for h in hubs],
                        value=[h.get("id", "") for h in hubs],
                        id="filter-hub",
                        className="mb-3",
                        switch=True,
                    ),

                    # Filtro por Status
                    html.Label("Status", className="form-label fw-semibold"),
                    dbc.Checklist(
                        options=[
                            {"label": "✅ Entregue", "value": "delivered"},
                            {"label": "🚚 Em Trânsito", "value": "in_transit"},
                            {"label": "⏳ Pendente", "value": "pending"},
                            {"label": "❌ Cancelada", "value": "cancelled"},
                        ],
                        value=["delivered", "in_transit", "pending"],
                        id="filter-status",
                        className="mb-3",
                        switch=True,
                    ),

                    # Botões de ação
                    html.Hr(className="my-3"),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Aplicar",
                                    id="btn-apply-filters",
                                    color="primary",
                                    size="sm",
                                    className="w-100",
                                ),
                                xs=6,
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Limpar",
                                    id="btn-clear-filters",
                                    color="outline-danger",
                                    size="sm",
                                    className="w-100",
                                ),
                                xs=6,
                            ),
                        ],
                        className="g-2",
                    ),

                    # Info
                    html.Div(
                        [
                            html.I(className="bi bi-info-circle me-1"),
                            html.Small(
                                "Os gráficos atualizam automaticamente.",
                                className="text-muted",
                            ),
                        ],
                        className="d-flex align-items-center mt-3",
                    ),
                ]
            ),
        ],
        className="shadow-sm h-100",
        style={"borderRadius": "12px"},
    )

    return sidebar