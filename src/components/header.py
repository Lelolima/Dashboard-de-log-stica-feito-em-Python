"""
Componente de Header para o Dashboard.

Inclui logo, título, controles de tema e download.
"""

from typing import Dict, Any
import dash_bootstrap_components as dbc
from dash import html, dcc


def render_header() -> html.Div:
    """
    Renderiza o header do dashboard.

    Returns:
        Componente dbc.Card com header completo
    """
    header = dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Logo e Título
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            # Logo SVG
                                            html.Img(
                                                src="/assets/logo.svg",
                                                alt="Logo",
                                                style={"height": "48px", "marginRight": "16px"},
                                            ),
                                            html.Div(
                                                [
                                                    html.H1(
                                                        "Dashboard Logística",
                                                        className="mb-0 fw-bold",
                                                        style={"fontSize": "1.75rem", "color": "var(--bs-primary)"},
                                                    ),
                                                    html.P(
                                                        "Análise de Entregas Loggi",
                                                        className="mb-0 text-muted",
                                                        style={"fontSize": "0.875rem"},
                                                    ),
                                                ],
                                                style={"display": "flex", "flexDirection": "column"},
                                            ),
                                        ],
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "gap": "16px",
                                        },
                                    )
                                ],
                                md=6,
                                className="d-flex align-items-center",
                            ),
                            # Controles
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            # Toggle Dark Mode
                                            dbc.Button(
                                                [
                                                    html.I(className="bi bi-moon-stars-fill", id="theme-icon"),
                                                ],
                                                id="btn-toggle-theme",
                                                color="outline-secondary",
                                                size="sm",
                                                className="me-2",
                                                title="Alternar tema (Dark/Light)",
                                            ),
                                            # Botão de Download
                                            dbc.Button(
                                                [
                                                    html.I(className="bi bi-download me-1"),
                                                    "Exportar CSV",
                                                ],
                                                id="btn-download",
                                                color="outline-success",
                                                size="sm",
                                                className="me-2",
                                                title="Baixar dados em CSV",
                                            ),
                                            # Status indicator
                                            html.Span(
                                                [
                                                    html.Span(
                                                        className="badge bg-success me-1",
                                                        style={"width": "8px", "height": "8px", "borderRadius": "50%"},
                                                    ),
                                                    "Dados atualizados",
                                                ],
                                                className="text-muted small",
                                            ),
                                        ],
                                        style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
                                    )
                                ],
                                md=6,
                                className="d-flex align-items-center justify-content-end",
                            ),
                        ],
                        align="center",
                    )
                ],
                className="py-3",
            )
        ],
        className="shadow-sm border-0 mb-4",
        style={"borderRadius": "12px"},
    )

    return header


def get_header_callbacks(app):
    """
    Registra callbacks do header.

    Args:
        app: Instância do Dash app
    """
    from dash import Output, Input, State
    import dash

    @app.callback(
        Output("body", "data-bs-theme"),
        Input("btn-toggle-theme", "n_clicks"),
        State("body", "data-bs-theme"),
        prevent_initial_call=True,
    )
    def toggle_theme(n_clicks, current_theme):
        """Alterna entre tema claro e escuro."""
        return "dark" if current_theme == "light" else "light"

    @app.callback(
        Output("download-data", "data"),
        Input("btn-download", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_data(n_clicks):
        """Gera arquivo CSV para download."""
        return dcc.send_data_frame(
            lambda: None,  # Será preenchido com dados reais no callback principal
            filename="dashboard_export.csv",
        )