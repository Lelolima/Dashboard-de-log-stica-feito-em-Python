"""
Componente de Cards de Métricas (KPIs).

Exibe 4 cards com métricas principais do dashboard.
"""

from typing import Dict, Any, Optional
import dash_bootstrap_components as dbc
from dash import html


def render_metrics_cards(metrics: Optional[Dict[str, Any]] = None) -> html.Div:
    """
    Renderiza cards de métricas (KPIs).

    Args:
        metrics: Dicionário com métricas calculadas
            - total_entregas: Total de entregas
            - entregas_pendentes: Entregas pendentes
            - entregas_em_transito: Entregas em trânsito
            - entregas_entregues: Entregas entregues
            - taxa_sucesso: Taxa de sucesso (%)
            - tempo_medio_entrega: Tempo médio (opcional)

    Returns:
        Div contendo 4 cards de KPI
    """
    metrics = metrics or {
        "total_entregas": 0,
        "entregas_pendentes": 0,
        "entregas_em_transito": 0,
        "entregas_entregues": 0,
        "taxa_sucesso": 0,
        "peso_total": 0,
    }

    cards = [
        # Card 1: Total Entregas
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-box-seam-fill", style={"fontSize": "2rem"}),
                                html.Span(
                                    "Total Entregas",
                                    className="text-muted small",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "flex-start",
                                "marginBottom": "12px",
                            },
                        ),
                        html.H3(
                            f"{metrics.get('total_entregas', 0):,}".replace(",", "."),
                            className="mb-0 fw-bold",
                            style={"fontSize": "2rem"},
                        ),
                        html.Small(
                            "Todas as entregas no período",
                            className="text-muted",
                        ),
                    ]
                ),
                className="border-0 h-100",
                style={"borderRadius": "12px", "backgroundColor": "var(--bs-primary-bg-subtle)"},
            ),
            className="mb-3",
        ),
        # Card 2: Taxa de Sucesso
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-check-circle-fill", style={"fontSize": "2rem", "color": "#198754"}),
                                html.Span(
                                    "Taxa de Sucesso",
                                    className="text-muted small",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "flex-start",
                                "marginBottom": "12px",
                            },
                        ),
                        html.H3(
                            f"{metrics.get('taxa_sucesso', 0):.1f}%",
                            className="mb-0 fw-bold",
                            style={"fontSize": "2rem", "color": "#198754"},
                        ),
                        html.Small(
                            f"{metrics.get('entregas_entregues', 0):,} entregas realizadas".replace(",", "."),
                            className="text-muted",
                        ),
                    ]
                ),
                className="border-0 h-100",
                style={"borderRadius": "12px"},
            ),
            className="mb-3",
        ),
        # Card 3: Pendentes
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-clock-fill", style={"fontSize": "2rem", "color": "#ffc107"}),
                                html.Span(
                                    "Em Andamento",
                                    className="text-muted small",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "flex-start",
                                "marginBottom": "12px",
                            },
                        ),
                        html.H3(
                            f"{metrics.get('entregas_pendentes', 0) + metrics.get('entregas_em_transito', 0):,}".replace(
                                ",", "."
                            ),
                            className="mb-0 fw-bold",
                            style={"fontSize": "2rem", "color": "#ffc107"},
                        ),
                        html.Small(
                            f"{metrics.get('entregas_pendentes', 0):,} pendentes • {metrics.get('entregas_em_transito', 0):,} em trânsito".replace(
                                ",", "."
                            ),
                            className="text-muted",
                        ),
                    ]
                ),
                className="border-0 h-100",
                style={"borderRadius": "12px"},
            ),
            className="mb-3",
        ),
        # Card 4: Peso Total
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-weight-hanging-fill", style={"fontSize": "2rem", "color": "#6f42c1"}),
                                html.Span(
                                    "Peso Total",
                                    className="text-muted small",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "flex-start",
                                "marginBottom": "12px",
                            },
                        ),
                        html.H3(
                            f"{metrics.get('peso_total', 0):,.0f} kg".replace(",", "."),
                            className="mb-0 fw-bold",
                            style={"fontSize": "2rem", "color": "#6f42c1"},
                        ),
                        html.Small(
                            f"Média: {metrics.get('peso_medio', 0):.1f} kg por entrega",
                            className="text-muted",
                        ),
                    ]
                ),
                className="border-0 h-100",
                style={"borderRadius": "12px"},
            ),
            className="mb-3",
        ),
    ]

    return html.Div(
        [dbc.Row(cards, className="g-3")],
        id="metrics-container",
    )


def render_metrics_loading() -> html.Div:
    """
    Renderiza skeleton loading para cards de métricas.

    Returns:
        Div com skeletons de carregamento
    """
    skeleton = dbc.Card(
        dbc.CardBody(
            [
                dbc.Skeleton(width="40%", height="1.5rem", className="mb-3"),
                dbc.Skeleton(width="60%", height="2.5rem", className="mb-2"),
                dbc.Skeleton(width="80%", height="1rem"),
            ]
        ),
        className="border-0",
        style={"borderRadius": "12px"},
    )

    return html.Div(
        [dbc.Row([dbc.Col(skeleton, md=3, className="mb-3") for _ in range(4)], className="g-3")],
    )