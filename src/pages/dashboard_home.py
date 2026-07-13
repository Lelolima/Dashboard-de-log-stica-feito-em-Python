"""
Dashboard Home Page - Versão BI Enterprise.
"""

from typing import Dict, Any, List, Optional
import dash_bootstrap_components as dbc
from dash import html, dcc


def render_dashboard_home(metrics: Dict[str, Any], df_info: Dict[str, Any]) -> html.Div:
    """
    Renderiza página home do dashboard.

    Args:
        metrics: Dict com métricas calculadas
        df_info: Info do DataFrame (total rows, last update)

    Returns:
        Div com layout do dashboard home
    """
    return html.Div(
        [
            # Barra de Navegação Superior
            dbc.Navbar(
                dbc.Container(
                    [
                        # Logo e Brand
                        dbc.NavbarBrand(
                            [
                                html.Img(src="/assets/logo.svg", height="40", className="me-2"),
                                html.Span("Dashboard Logística", className="ms-2 fw-bold"),
                            ],
                            href="/",
                        ),

                        # Navegação
                        dbc.Nav(
                            [
                                dbc.NavLink("📊 Dashboard", href="/", active="exact"),
                                dbc.NavLink("📑 Relatório Executivo", href="/report", active="exact"),
                                dbc.NavLink("⚙️ Configurações", href="/settings", active="exact"),
                            ],
                            className="me-auto",
                            navbar=True,
                        ),

                        # User Menu
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-moon-stars-fill me-1", id="theme-icon"),
                                        ],
                                        id="btn-toggle-theme",
                                        variant="outline-secondary",
                                        size="sm",
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.DropdownMenu(
                                        [
                                            dbc.DropdownMenuItem("👤 Perfil"),
                                            dbc.DropdownMenuItem("🔑 API Keys"),
                                            dbc.DropdownMenuItem(divider=True),
                                            dbc.DropdownMenuItem("🚪 Sair"),
                                        ],
                                        nav=True,
                                        inNavbar=True,
                                        label="👤 Admin",
                                    )
                                ),
                            ],
                            navbar=True,
                        ),
                    ]
                ),
                color="primary",
                dark=True,
                className="mb-4",
            ),

            # Stats em Tempo Real
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Small("📦 Total Entregas", className="text-muted mb-1"),
                                                            html.H3(
                                                                f"{metrics.get('total_entregas', 0):,}",
                                                                className="mb-0 fw-bold",
                                                                style={"fontSize": "2rem"},
                                                            ),
                                                        ],
                                                        xs=8,
                                                    ),
                                                    dbc.Col(
                                                        html.Span(
                                                            "📈 +12%",
                                                            className="badge bg-success",
                                                            style={"fontSize": "0.75rem"},
                                                        ),
                                                        xs=4,
                                                        className="text-end",
                                                    ),
                                                ],
                                                align="center",
                                            ),
                                            html.Div(
                                                className="sparkline-container",
                                                style={"height": "30px", "marginTop": "0.5rem"},
                                            ),
                                        ]
                                    ),
                                    className="border-0 shadow-sm",
                                    style={"borderRadius": "12px"},
                                ),
                                md=3,
                                className="mb-3",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Small("✅ Taxa Sucesso", className="text-muted mb-1"),
                                                            html.H3(
                                                                f"{metrics.get('taxa_sucesso', 0):.1f}%",
                                                                className="mb-0 fw-bold",
                                                                style={"fontSize": "2rem", "color": "#10b981"},
                                                            ),
                                                        ],
                                                        xs=8,
                                                    ),
                                                    dbc.Col(
                                                        html.Span(
                                                            "📈 +2.5%",
                                                            className="badge bg-success",
                                                            style={"fontSize": "0.75rem"},
                                                        ),
                                                        xs=4,
                                                        className="text-end",
                                                    ),
                                                ],
                                                align="center",
                                            ),
                                        ]
                                    ),
                                    className="border-0 shadow-sm",
                                    style={
                                        "borderRadius": "12px",
                                        "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                                        "color": "white",
                                    },
                                ),
                                md=3,
                                className="mb-3",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Small("⏳ Em Andamento", className="text-muted mb-1"),
                                                            html.H3(
                                                                f"{metrics.get('entregas_pendentes', 0) + metrics.get('entregas_em_transito', 0):,}",
                                                                className="mb-0 fw-bold",
                                                                style={"fontSize": "2rem", "color": "#f59e0b"},
                                                            ),
                                                        ],
                                                        xs=8,
                                                    ),
                                                    dbc.Col(
                                                        html.Span(
                                                            "📊 Pendentes",
                                                            className="badge bg-warning text-dark",
                                                            style={"fontSize": "0.75rem"},
                                                        ),
                                                        xs=4,
                                                        className="text-end",
                                                    ),
                                                ],
                                                align="center",
                                            ),
                                        ]
                                    ),
                                    className="border-0 shadow-sm",
                                    style={"borderRadius": "12px"},
                                ),
                                md=3,
                                className="mb-3",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Small("🕐 Última Atualização", className="text-muted mb-1"),
                                                            html.P(
                                                                df_info.get("last_update", "Agora"),
                                                                className="mb-0 fw-semibold",
                                                                style={"fontSize": "1rem"},
                                                            ),
                                                        ],
                                                        xs=12,
                                                    ),
                                                ],
                                                align="center",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span(
                                                        className="badge bg-success me-1",
                                                        style={
                                                            "width": "8px",
                                                            "height": "8px",
                                                            "borderRadius": "50%",
                                                            "display": "inline-block",
                                                        },
                                                    ),
                                                    html.Small("Dados sincronizados", className="text-muted"),
                                                ],
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="border-0 shadow-sm",
                                    style={"borderRadius": "12px"},
                                ),
                                md=3,
                                className="mb-3",
                            ),
                        ]
                    ),
                ],
                fluid=True,
            ),
        ]
    )