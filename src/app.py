"""
Dashboard Logística Loggi - App Principal v2.0 BI Enterprise.

Aplicação Dash enterprise para análise de dados de logística.
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from src.components.footer import render_footer
from src.components.header import render_header
from src.components.metrics_cards import render_metrics_cards
from src.components.sidebar import render_sidebar
from src.config import settings
from src.data.loader import DataLoader
from src.data.processor import DataProcessor
from src.utils.logger import get_logger, setup_logging
from src.visualizations import create_bar_chart, create_map_chart, create_pie_chart

logger = get_logger(__name__)


def create_app(testing: bool = False) -> dash.Dash:  # noqa: ARG001 (contrato público)
    """
    Cria e configura a aplicação Dash.
    """
    # Setup logging
    setup_logging()

    logger.info("Criando aplicação Dash BI Enterprise", version="2.0.0")

    # Inicializar Dash com Bootstrap
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP,
        ],
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
            {"name": "description", "content": "Dashboard de logística para análise de entregas"},
            {"name": "theme-color", "content": "#2563eb"},
        ],
        title="Dashboard Logística Loggi",
    )
    app.title = "📊 Dashboard Logística Loggi"

    # Carregar dados iniciais
    logger.info("Carregando dados iniciais")
    loader = DataLoader()
    df = loader.load_deliveries()
    processor = DataProcessor(df)

    # Obter opções para filtros
    cities = processor.get_unique_cities()
    states = processor.get_unique_states()
    hubs = processor.get_unique_hubs()
    statuses = processor.get_unique_statuses()

    # Calcular métricas iniciais
    metrics = processor.calcular_metricas()

    # Criar gráficos iniciais
    logger.info("Criando gráficos enterprise")
    initial_map = create_map_chart(processor.get_dados_mapa(), mapbox_token=settings.mapbox_token)
    initial_bar_city = create_bar_chart(df, group_by="city", height=350)
    initial_pie_status = create_pie_chart(df, group_by="status", height=350)

    # Gráfico de hubs
    if len(df) > 0 and "hub_id" in df.columns:
        initial_hub_capacity = create_bar_chart(df, group_by="hub_id", height=350)
    else:
        initial_hub_capacity = create_pie_chart(df, group_by="status", height=350)

    # Layout principal
    app.layout = html.Div(
        [
            # Stores
            dcc.Store(id="store-data", data={"df_json": df.to_json(), "metrics": metrics}),
            dcc.Store(
                id="store-options",
                data={
                    "cities": cities,
                    "states": states,
                    "hubs": [
                        {"id": h.get("id", ""), "hub_name": h.get("hub_name", "")} for h in hubs
                    ],
                    "statuses": statuses,
                },
            ),
            dcc.Location(id="url", refresh=False),
            dcc.Download(id="download-data"),
            # Corpo do Dashboard
            html.Div(
                id="body",
                children=[
                    render_header(),
                    *(
                        [
                            dbc.Alert(
                                "Dados de exemplo gerados automaticamente (simulados): "
                                "não representam operações reais.",
                                id="sample-data-alert",
                                color="warning",
                                className="m-3 mb-0",
                            )
                        ]
                        if loader.using_sample_data
                        else []
                    ),
                    dbc.Container(
                        [
                            # Cards de métricas
                            html.Div(
                                id="metrics-container",
                                children=render_metrics_cards(metrics),
                            ),
                            # Conteúdo principal
                            dbc.Row(
                                [
                                    # Sidebar (filtros)
                                    dbc.Col(
                                        render_sidebar(
                                            cities=cities,
                                            states=states,
                                            hubs=hubs,
                                            statuses=statuses,
                                        ),
                                        md=3,
                                        lg=2,
                                        className="p-0 border-end mb-3",
                                    ),
                                    # Gráficos
                                    dbc.Col(
                                        [
                                            # Mapa
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="map-chart",
                                                            figure=initial_map,
                                                            config={"responsive": True},
                                                        )
                                                    ]
                                                ),
                                                className="mb-3 border-0 shadow-sm",
                                                style={"borderRadius": "12px"},
                                            ),
                                            # Gráficos lado a lado
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                [
                                                                    dcc.Graph(
                                                                        id="bar-chart-city",
                                                                        figure=initial_bar_city,
                                                                        config={"responsive": True},
                                                                    )
                                                                ]
                                                            ),
                                                            className="border-0 shadow-sm",
                                                            style={"borderRadius": "12px"},
                                                        ),
                                                        md=6,
                                                    ),
                                                    dbc.Col(
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                [
                                                                    dcc.Graph(
                                                                        id="pie-chart-status",
                                                                        figure=initial_pie_status,
                                                                        config={"responsive": True},
                                                                    )
                                                                ]
                                                            ),
                                                            className="border-0 shadow-sm",
                                                            style={"borderRadius": "12px"},
                                                        ),
                                                        md=6,
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            # Capacidade por hub
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="hub-capacity-chart",
                                                            figure=initial_hub_capacity,
                                                            config={"responsive": True},
                                                        )
                                                    ]
                                                ),
                                                className="border-0 shadow-sm",
                                                style={"borderRadius": "12px"},
                                            ),
                                        ],
                                        md=9,
                                        lg=10,
                                    ),
                                ],
                                className="g-0",
                            ),
                        ],
                        fluid=True,
                        className="py-4",
                    ),
                    render_footer(),
                ],
                style={
                    "minHeight": "100vh",
                    "display": "flex",
                    "flexDirection": "column",
                    "backgroundColor": "var(--bg-body)",
                },
            ),
        ],
        style={"minHeight": "100vh", "display": "flex", "flexDirection": "column"},
    )

    # Registrar callbacks após layout
    logger.info("Registrando callbacks")

    logger.info("Aplicação BI Enterprise criada com sucesso")
    return app


def main() -> None:
    """
    Ponto de entrada principal para desenvolvimento.
    """
    app = create_app()

    logger.info(
        "Iniciando servidor de desenvolvimento",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )

    app.run(
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )


if __name__ == "__main__":
    main()
