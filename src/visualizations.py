"""
Módulo de visualizações com Plotly - Versão BI Enterprise.

Cria gráficos profissionais com cores enterprise, tooltips customizados e interatividade.
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.styles_bi import (
    CATEGORICAL_COLORS,
    SEQUENTIAL_COLORS,
    STATUS_COLORS,
    get_categorical_scale,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_map_chart(
    df: pd.DataFrame,
    mapbox_token: Optional[str] = None,
    height: int = 500,
) -> go.Figure:
    """
    Cria mapa interativo com entregas - Versão Enterprise.

    Features:
    - Hover tooltips customizados
    - Cluster de markers
    - Zoom automático
    - Cores por status
    """
    if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return _create_empty_map(height)

    # Mapear cores e ícones por status
    df = df.copy()
    df["status_color"] = df.get("status", "pending").map({
        "delivered": STATUS_COLORS["delivered"]["bg"],
        "in_transit": STATUS_COLORS["in_transit"]["bg"],
        "pending": STATUS_COLORS["pending"]["bg"],
        "cancelled": STATUS_COLORS["cancelled"]["bg"],
    }).fillna(STATUS_COLORS["pending"]["bg"])

    df["status_label"] = df.get("status", "pending").map({
        "delivered": STATUS_COLORS["delivered"]["label"],
        "in_transit": STATUS_COLORS["in_transit"]["label"],
        "pending": STATUS_COLORS["pending"]["label"],
        "cancelled": STATUS_COLORS["cancelled"]["label"],
    }).fillna("Pendente")

    # Criar hover template customizado
    hover_template = (
        "<b>📦 %{text}</b><br>"
        "📍 %{customdata[0]}, %{customdata[1]}<br>"
        "🚚 Status: %{customdata[2]}<br>"
        "<extra></extra>"
    )

    # Mapa com Scatter Geo (fallback sem Mapbox)
    if mapbox_token:
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="status",
            color_discrete_map=dict(zip(df["status"], df["status_color"])),
            hover_name="id",
            hover_data=["city", "state", "status_label"],
            zoom=8,
            center={"lat": df["latitude"].mean(), "lon": df["longitude"].mean()},
            height=height,
        )
        fig.update_layout(
            mapbox_style="mapbox://styles/mapbox/light-v11",
            mapbox_accesstoken=mapbox_token,
        )
    else:
        # Scatter geo com cores customizadas
        fig = go.Figure()

        for status in df["status"].unique():
            status_df = df[df["status"] == status]
            status_info = STATUS_COLORS.get(status, STATUS_COLORS["pending"])

            fig.add_trace(
                go.Scattergeo(
                    lat=status_df["latitude"],
                    lon=status_df["longitude"],
                    mode="markers",
                    name=f"{status_info['icon']} {status_info['label']}",
                    marker=dict(
                        size=8,
                        color=status_info["bg"],
                        opacity=0.8,
                        line=dict(width=1, color="white"),
                    ),
                    text=status_df["id"],
                    customdata=status_df[["city", "state", "status_label"]].values,
                    hovertemplate=hover_template,
                )
            )

        fig.update_layout(
            geo=dict(
                scope="south america",
                center={"lat": -15.0, "lon": -52.0},
                landcolor="#f1f5f9",
                lakecolor="#dbeafe",
                showcoastlines=True,
                coastlinecolor="#cbd5e1",
                countrycolor="#94a3b8",
            ),
        )

    # Layout enterprise
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
        ),
        hovermode="closest",
        dragmode="pan",
    )

    logger.info("Mapa enterprise criado", points=len(df))
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    group_by: str = "city",
    metric: str = "total",
    height: int = 400,
    orientation: str = "v",
) -> go.Figure:
    """
    Cria gráfico de barras enterprise.

    Features:
    - Gradiente de cores
    - Hover tooltips formatados
    - Animação de entrada
    - Ordenação inteligente
    """
    if df.empty or group_by not in df.columns:
        return _create_empty_chart("Gráfico de Barras", height)

    # Agrupar dados
    if metric == "total":
        grouped = df.groupby(group_by).size().reset_index(name="total")
        grouped = grouped.sort_values("total", ascending=False)
        title = f"📊 Entregas por {group_by.title()}"
        y_label = "Quantidade"
    elif metric == "weight":
        grouped = df.groupby(group_by)["weight"].sum().reset_index(name="total")
        grouped = grouped.sort_values("total", ascending=False)
        title = f"⚖️ Peso Total por {group_by.title()}"
        y_label = "Peso (kg)"
    elif metric == "value":
        grouped = df.groupby(group_by)["value"].sum().reset_index(name="total")
        grouped = grouped.sort_values("total", ascending=False)
        title = f"💰 Valor Total por {group_by.title()}"
        y_label = "Valor (R$)"
    else:
        grouped = df.groupby(group_by).size().reset_index(name="total")
        title = f"📊 Entregas por {group_by.title()}"
        y_label = "Quantidade"

    # Limitar a top 15
    if len(grouped) > 15:
        grouped = grouped.head(15)

    # Cores com gradiente
    colors = get_categorical_scale(len(grouped))

    # Hover template formatado
    hover_template = (
        "<b>%{x}</b><br>" if orientation == "v" else "<b>%{y}</b><br>"
        f"{y_label}: %{text:,}<br>"
        "<extra></extra>"
    )

    fig = px.bar(
        grouped,
        x=group_by if orientation == "v" else "total",
        y="total" if orientation == "v" else group_by,
        text="total",
        orientation=orientation,
        color="total",
        color_discrete_sequence=colors,
        height=height,
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=hover_template.replace("%{text:,}", "%{y:,}") if orientation == "v" else hover_template.replace("%{text:,}", "%{x:,}"),
        marker=dict(
            line=dict(width=1, color="white"),
            opacity=0.9,
        ),
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, weight="bold")),
        height=height,
        margin=dict(l=60, r=20, t=60, b=60),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified" if orientation == "v" else "y unified",
        font=dict(family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=13),
    )

    # Grid lines sutis
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title_text=group_by.title() if orientation == "v" else y_label)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title_text=y_label if orientation == "v" else group_by.title())

    logger.info(f"Gráfico de barras enterprise criado: {title}")
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    group_by: str = "status",
    height: int = 350,
) -> go.Figure:
    """
    Cria gráfico de pizza/rosca enterprise.

    Features:
    - Donut chart moderno
    - Cores por status
    - Percentuais formatados
    - Legendas interativas
    """
    if df.empty or group_by not in df.columns:
        return _create_empty_chart("Distribuição", height)

    grouped = df.groupby(group_by).size().reset_index(name="count")
    grouped = grouped[grouped["count"] > 0]

    if grouped.empty:
        return _create_empty_chart("Distribuição", height)

    # Labels com ícones
    label_map = {k: f"{v['icon']} {v['label']}" for k, v in STATUS_COLORS.items()}
    grouped["label"] = grouped[group_by].map(label_map).fillna(grouped[group_by])

    # Cores dos status
    color_map = {k: v["bg"] for k, v in STATUS_COLORS.items()}

    fig = px.pie(
        grouped,
        values="count",
        names="label",
        hole=0.5,  # Donut chart
        color="label",
        color_discrete_map=color_map,
        height=height,
    )

    # Hover template customizado
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=12, weight="bold"),
        hovertemplate="<b>%{label}</b><br>📦 %{value:,} entregas<br>%{percent}<br><extra></extra>",
        marker=dict(line=dict(width=2, color="white")),
        sort=True,
    )

    fig.update_layout(
        title=dict(text=f"🥧 Distribuição por {group_by.title()}", font=dict(size=16, weight="bold")),
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.8)",
        ),
        hovermode="closest",
        font=dict(family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=13),
    )

    logger.info(f"Gráfico de pizza enterprise criado: {group_by}")
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    height: int = 350,
) -> go.Figure:
    """
    Cria gráfico de linha enterprise.

    Features:
    - Spline interpolation
    - Gradient fill
    - Markers interativos
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        return _create_empty_chart(title, height)

    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        line_shape="spline",
        height=height,
    )

    # Adicionar gradient fill
    fig.update_traces(
        line=dict(width=3, shape="spline"),
        marker=dict(size=8, line=dict(width=2, color="white")),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.1)",
        hovertemplate=f"<b>%{{x}}</b><br>{y_col.replace('_', ' ').title()}: %{{y:,.0f}}<br><extra></extra>",
    )

    fig.update_layout(
        title=dict(text=f"📈 {title}", font=dict(size=16, weight="bold")),
        height=height,
        margin=dict(l=60, r=20, t=60, b=60),
        hovermode="x unified",
        font=dict(family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=13),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title_text=y_col.replace("_", " ").title())

    logger.info(f"Gráfico de linha enterprise criado: {title}")
    return fig


def create_hub_capacity_chart(
    df: pd.DataFrame,
    hubs_df: pd.DataFrame,
    height: int = 350,
) -> go.Figure:
    """
    Cria gráfico de utilização de capacidade por hub.
    """
    if df.empty or hubs_df.empty:
        return _create_empty_chart("Utilização por Hub", height)

    # Calcular utilização
    usage = df.groupby("hub_id").size().reset_index(name="utilizacao")
    merged = usage.merge(hubs_df[["id", "name", "capacity"]], left_on="hub_id", right_on="id")
    merged["percentual"] = (merged["utilizacao"] / merged["capacity"] * 100).round(1)
    merged = merged.sort_values("percentual", ascending=False)

    # Cores baseadas na utilização
    merged["cor"] = merged["percentual"].apply(
        lambda x: "#10b981" if x < 50 else ("#f59e0b" if x < 80 else "#ef4444")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=merged["name"],
            x=merged["utilizacao"],
            name="Utilização",
            orientation="h",
            marker=dict(color=merged["cor"], opacity=0.8),
            hovertemplate="<b>%{y}</b><br>📦 %{x:,} entregas<br>💡 %{customdata:.1f}% da capacidade<br><extra></extra>",
            customdata=merged["percentual"],
        )
    )

    # Linha de capacidade
    fig.add_trace(
        go.Scatter(
            y=merged["name"],
            x=merged["capacity"],
            mode="lines",
            line=dict(width=2, color="#64748b", dash="dash"),
            name="Capacidade",
            hovertemplate="<b>%{y}</b><br>🎯 Capacidade: %{x:,}<br><extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="🏢 Utilização de Capacidade por Hub", font=dict(size=16, weight="bold")),
        height=height,
        barmode="overlay",
        margin=dict(l=150, r=20, t=60, b=40),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="y unified",
        font=dict(family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=13),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(title_text="📦 Quantidade de Entregas", showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    fig.update_yaxes(title_text="🏢 Hub")

    logger.info(f"Gráfico de capacidade criado: {len(merged)} hubs")
    return fig


def _create_empty_map(height: int = 500) -> go.Figure:
    """Cria mapa vazio com mensagem elegante."""
    fig = go.Figure()
    fig.add_annotation(
        text="📍 Nenhum dado para exibir no mapa",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#64748b"),
    )
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _create_empty_chart(title: str, height: int = 350) -> go.Figure:
    """Cria gráfico vazio com mensagem elegante."""
    fig = go.Figure()
    fig.add_annotation(
        text=f"📊 Nenhum dado: {title}",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color="#64748b"),
    )
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig