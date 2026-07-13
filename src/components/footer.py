"""
Componente de Footer para o Dashboard.
"""

import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime

from src import __version__


def render_footer() -> html.Footer:
    """
    Renderiza o footer do dashboard.

    Returns:
        Footer com créditos, links e versão
    """
    current_year = datetime.now().year

    footer = html.Footer(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            # Créditos
                            dbc.Col(
                                [
                                    html.P(
                                        f"© {current_year} Dashboard Logística Loggi",
                                        className="mb-1 text-muted small",
                                    ),
                                    html.P(
                                        "Desenvolvido com Dash + Plotly",
                                        className="mb-0 text-muted small",
                                    ),
                                ],
                                md=6,
                                className="text-center text-md-start mb-2 mb-md-0",
                            ),
                            # Links
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.A(
                                                "Documentação",
                                                href="/docs",
                                                className="text-muted small text-decoration-none me-3",
                                            ),
                                            html.A(
                                                "GitHub",
                                                href="https://github.com/Lelolima/dashboard-logistica-loggi",
                                                target="_blank",
                                                rel="noopener noreferrer",
                                                className="text-muted small text-decoration-none me-3",
                                            ),
                                            html.A(
                                                f"v{__version__}",
                                                href="https://github.com/Lelolima/dashboard-logistica-loggi/releases",
                                                target="_blank",
                                                rel="noopener noreferrer",
                                                className="text-muted small text-decoration-none",
                                            ),
                                        ],
                                        className="text-center text-md-end",
                                    )
                                ],
                                md=6,
                            ),
                        ],
                        align="center",
                    ),
                    # Separator
                    html.Hr(className="mt-3 border-secondary"),
                    # Tech badges
                    dbc.Row(
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Badge("Python 3.11+", color="info", className="me-2"),
                                        dbc.Badge("Dash 2.18", color="info", className="me-2"),
                                        dbc.Badge("Plotly 5.22", color="info", className="me-2"),
                                        dbc.Badge("Bootstrap 5", color="info", className="me-2"),
                                        dbc.Badge("Pandas 2.2", color="info", className="me-2"),
                                    ],
                                    className="text-center",
                                )
                            ],
                            className="text-center",
                        )
                    ),
                ],
                className="py-4",
            )
        ],
        className="bg-body-tertiary mt-auto border-top",
        style={"marginTop": "auto"},
    )

    return footer