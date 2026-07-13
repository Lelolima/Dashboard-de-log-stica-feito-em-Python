"""
Relatório Executivo para Dashboard de Logística.

Gera relatório profissional com insights automáticos e análise detalhada.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import html


def render_executive_report(df: pd.DataFrame, metrics: Dict[str, Any]) -> html.Div:
    """
    Renderiza página de relatório executivo.

    Args:
        df: DataFrame com dados de entregas
        metrics: Dict com métricas calculadas

    Returns:
        Div com layout do relatório
    """
    # Gerar insights automáticos
    insights = generate_insights(df, metrics)

    # Gerar tabela de performance por hub
    hub_performance = generate_hub_performance(df)

    # Gerar ranking de cidades
    city_ranking = generate_city_ranking(df)

    report = html.Div(
        [
            # Header do Relatório
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H1(
                                            "📊 Relatório Executivo de Logística",
                                            className="mb-1",
                                            style={"fontSize": "1.75rem", "fontWeight": "700"},
                                        ),
                                        html.P(
                                            f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
                                            className="text-muted mb-0",
                                        ),
                                    ],
                                    md=8,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-download me-2"),
                                                "Exportar PDF",
                                            ],
                                            id="btn-export-pdf",
                                            color="primary",
                                            size="sm",
                                        ),
                                    ],
                                    md=4,
                                    className="text-end",
                                ),
                            ],
                            align="center",
                        ),
                    ]
                ),
                className="border-0 shadow-sm mb-4",
                style={"borderRadius": "12px", "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
            ),

            # Seção 1: Resumo Executivo
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-box-seam me-2"),
                            "Resumo Executivo",
                        ],
                        className="bg-transparent border-bottom fw-semibold",
                    ),
                    dbc.CardBody(
                        [
                            # KPIs em Cards
                            dbc.Row(
                                [
                                    create_kpi_card("Total de Entregas", f"{metrics.get('total_entregas', 0):,}", "📦", "blue"),
                                    create_kpi_card("Taxa de Sucesso", f"{metrics.get('taxa_sucesso', 0):.1f}%", "✅", "green"),
                                    create_kpi_card("Entregues", f"{metrics.get('entregas_entregues', 0):,}", "🎯", "emerald"),
                                    create_kpi_card("Pendentes", f"{metrics.get('entregas_pendentes', 0) + metrics.get('entregas_em_transito', 0):,}", "⏳", "amber"),
                                ],
                                className="mb-4",
                            ),

                            # Insights Automáticos
                            html.H5("🔍 Insights Automáticos", className="fw-semibold mb-3"),
                            dbc.Alert(
                                [
                                    html.I(className="bi bi-lightbulb me-2"),
                                    insights["main_insight"],
                                ],
                                color="info",
                                className="mb-2",
                            ),
                            dbc.Alert(
                                [
                                    html.I(className="bi bi-trend-up me-2"),
                                    insights["performance_insight"],
                                ],
                                color="success",
                                className="mb-2",
                            ),
                            dbc.Alert(
                                [
                                    html.I(className="bi bi-exclamation-triangle me-2"),
                                    insights["attention_insight"],
                                ],
                                color="warning",
                                className="mb-0",
                            ),
                        ]
                    ),
                ],
                className="border-0 shadow-sm mb-4",
                style={"borderRadius": "12px"},
            ),

            # Seção 2: Performance por Hub
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-building me-2"),
                            "Análise de Performance por Hub",
                        ],
                        className="bg-transparent border-bottom fw-semibold",
                    ),
                    dbc.CardBody(
                        [
                            # Tabela de Performance
                            dbc.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [
                                                html.Th("Hub"),
                                                html.Th("Total Entregas"),
                                                html.Th("Entregues"),
                                                html.Th("Taxa Sucesso"),
                                                html.Th("Status"),
                                            ]
                                        )
                                    ),
                                    html.Tbody(
                                        [
                                            html.Tr(
                                                [
                                                    html.Td(hub.get("hub_name", hub.get("hub_id", "N/A"))),
                                                    html.Td(f"{hub.get('total_entregas', 0):,}"),
                                                    html.Td(f"{hub.get('entregues', 0):,}"),
                                                    html.Td(
                                                        html.Span(
                                                            f"{hub.get('taxa_sucesso', 0):.1f}%",
                                                            className=f"badge bg-{get_badge_color(hub.get('taxa_sucesso', 0))}",
                                                        )
                                                    ),
                                                    html.Td(get_status_icon(hub.get("taxa_sucesso", 0))),
                                                ]
                                            )
                                            for hub in hub_performance
                                        ]
                                    ),
                                ],
                                hover=True,
                                responsive=True,
                                className="mb-0",
                            ),
                        ]
                    ),
                ],
                className="border-0 shadow-sm mb-4",
                style={"borderRadius": "12px"},
            ),

            # Seção 3: Ranking de Cidades
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-geo-alt me-2"),
                            "Ranking de Cidades por Volume",
                        ],
                        className="bg-transparent border-bottom fw-semibold",
                    ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            create_city_rank_card(city, idx)
                                            for idx, city in enumerate(city_ranking[:6])
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            create_city_rank_card(city, idx + 6)
                                            for idx, city in enumerate(city_ranking[6:12])
                                        ],
                                        md=6,
                                    ),
                                ],
                            ),
                        ]
                    ),
                ],
                className="border-0 shadow-sm mb-4",
                style={"borderRadius": "12px"},
            ),

            # Seção 4: Recomendações
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-chat-dots me-2"),
                            "Recomendações & Ações",
                        ],
                        className="bg-transparent border-bottom fw-semibold",
                    ),
                    dbc.CardBody(
                        [
                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem(
                                        [
                                            html.I(className="bi bi-check-circle-fill text-success me-2"),
                                            "Manter foco nos hubs com alta taxa de sucesso para replicar melhores práticas.",
                                        ],
                                        className="border-0",
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            html.I(className="bi bi-exclamation-circle-fill text-warning me-2"),
                                            "Investigar causas de cancelamentos nos hubs com taxa abaixo de 80%.",
                                        ],
                                        className="border-0",
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            html.I(className="bi bi-arrow-right-circle-fill text-primary me-2"),
                                            "Otimizar rotas das cidades com maior volume para reduzir tempo de entrega.",
                                        ],
                                        className="border-0",
                                    ),
                                ],
                                flush=True,
                            ),
                        ]
                    ),
                ],
                className="border-0 shadow-sm",
                style={"borderRadius": "12px"},
            ),
        ],
        className="py-4",
    )

    return report


def generate_insights(df: pd.DataFrame, metrics: Dict[str, Any]) -> Dict[str, str]:
    """
    Gera insights automáticos baseados nos dados.

    Returns:
        Dict com insights principais
    """
    total = metrics.get("total_entregas", 0)
    success_rate = metrics.get("taxa_sucesso", 0)
    delivered = metrics.get("entregas_entregues", 0)
    pending = metrics.get("entregas_pendentes", 0)
    in_transit = metrics.get("entregas_em_transito", 0)

    # Insight principal
    if success_rate >= 90:
        main_insight = f"Excelente performance! Taxa de sucesso de {success_rate:.1f}% está acima da meta de 90%."
    elif success_rate >= 75:
        main_insight = f"Performance adequada. Taxa de sucesso de {success_rate:.1f}% está dentro da faixa aceitável."
    else:
        main_insight = f"Atenção necessária. Taxa de sucesso de {success_rate:.1f}% está abaixo da meta de 75%."

    # Insight de performance
    performance_ratio = delivered / total if total > 0 else 0
    performance_insight = f"{delivered} de {total} entregas realizadas ({performance_ratio:.1%}). "
    if performance_ratio >= 0.8:
        performance_insight += "Operação está fluindo normalmente."
    else:
        performance_insight += f"Ainda há {pending + in_transit} entregas em andamento para concluir."

    # Insight de atenção
    cancelled = metrics.get("entregas_canceladas", 0)
    cancel_rate = (cancelled / total * 100) if total > 0 else 0
    if cancel_rate > 5:
        attention_insight = f"Taxa de cancelamento de {cancel_rate:.1f}% requer investigação. {cancelled} entregas canceladas."
    elif pending + in_transit > total * 0.3:
        attention_insight = f"{pending + in_transit} entregas pendentes/em trânsito ({(pending + in_transit) / total * 100:.1f}%). Acelerar processo."
    else:
        attention_insight = "Sem alertas críticos no momento."

    return {
        "main_insight": main_insight,
        "performance_insight": performance_insight,
        "attention_insight": attention_insight,
    }


def generate_hub_performance(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Gera tabela de performance por hub.
    """
    if df.empty or "hub_id" not in df.columns:
        return []

    hub_stats = df.groupby("hub_id").agg({
        "id": "count",
        "status": lambda x: (x == "delivered").sum(),
        "hub_name": "first" if "hub_name" in df.columns else lambda x: x.iloc[0],
    }).reset_index()

    hub_stats.columns = ["hub_id", "total_entregas", "entregues", "hub_name"]
    hub_stats["taxa_sucesso"] = (hub_stats["entregues"] / hub_stats["total_entregas"] * 100).round(1)
    hub_stats = hub_stats.sort_values("taxa_sucesso", ascending=False)

    return hub_stats.to_dict("records")


def generate_city_ranking(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Gera ranking de cidades por volume.
    """
    if df.empty or "city" not in df.columns:
        return []

    city_stats = df.groupby("city").size().reset_index(name="total")
    city_stats = city_stats.sort_values("total", ascending=False)

    return city_stats.to_dict("records")


def create_kpi_card(title: str, value: str, icon: str, color: str) -> dbc.Col:
    """
    Cria card de KPI para o relatório.
    """
    color_map = {
        "blue": "#3b82f6",
        "green": "#10b981",
        "emerald": "#059669",
        "amber": "#f59e0b",
        "red": "#ef4444",
    }

    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Span(icon, style={"fontSize": "2rem"}),
                            html.Span(
                                value,
                                className="d-block fw-bold",
                                style={"fontSize": "1.75rem", "color": color_map.get(color, "#3b82f6")},
                            ),
                            html.Small(title, className="text-muted"),
                        ],
                        style={"textAlign": "center"},
                    ),
                ],
                className="py-3",
            ),
            className="border-0 h-100",
            style={"borderRadius": "12px", "backgroundColor": f"{color_map.get(color, '#3b82f6')}10"},
        ),
        md=3,
        className="mb-3",
    )


def create_city_rank_card(city: Dict[str, Any], rank: int) -> dbc.Card:
    """
    Cria card de ranking de cidade.
    """
    medal = ["🥇", "🥈", "🥉"][rank] if rank < 3 else f"#{rank + 1}"

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(medal, className="me-2"),
                        html.Span(city.get("city", "N/A"), className="fw-semibold"),
                        html.Span(
                            f"{city.get('total', 0):,} entregas",
                            className="text-muted small d-block",
                        ),
                    ],
                    className="d-flex align-items-center",
                ),
            ],
            className="py-2",
        ),
        className="border-0 mb-2",
        style={"borderRadius": "8px"},
    )


def get_badge_color(taxa_sucesso: float) -> str:
    """Retorna cor do badge baseada na taxa."""
    if taxa_sucesso >= 90:
        return "success"
    elif taxa_sucesso >= 75:
        return "primary"
    elif taxa_sucesso >= 50:
        return "warning"
    return "danger"


def get_status_icon(taxa_sucesso: float) -> str:
    """Retorna ícone de status baseado na taxa."""
    if taxa_sucesso >= 90:
        return "🟢 Excelente"
    elif taxa_sucesso >= 75:
        return "🔵 Bom"
    elif taxa_sucesso >= 50:
        return "🟡 Atenção"
    return "🔴 Crítico"