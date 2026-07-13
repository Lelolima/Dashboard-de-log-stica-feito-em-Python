"""
Testes do módulo de Visualizações.
"""

import pytest
import pandas as pd
import plotly.graph_objects as go
from src.visualizations import (
    create_map_chart,
    create_bar_chart,
    create_pie_chart,
    create_heatmap,
    _create_empty_chart,
)


class TestCreateMapChart:
    """Testes para create_map_chart."""

    @pytest.fixture
    def sample_df(self):
        """Fixture com dados de exemplo."""
        return pd.DataFrame({
            "id": ["ENT-001", "ENT-002"],
            "latitude": [-23.5505, -22.9068],
            "longitude": [-46.6333, -43.1729],
            "city": ["São Paulo", "Rio de Janeiro"],
            "state": ["SP", "RJ"],
            "status": ["delivered", "pending"],
        })

    def test_create_map_with_data(self, sample_df):
        """Testa criação de mapa com dados."""
        fig = create_map_chart(sample_df)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_create_map_empty(self):
        """Testa criação de mapa vazio."""
        empty_df = pd.DataFrame()
        fig = create_map_chart(empty_df)

        assert isinstance(fig, go.Figure)
        # Deve ter annotation de "nenhum dado"

    def test_create_map_missing_columns(self):
        """Testa mapa sem colunas necessárias."""
        df = pd.DataFrame({"city": ["SP"], "status": ["delivered"]})
        fig = create_map_chart(df)

        assert isinstance(fig, go.Figure)
        # Deve retornar mapa vazio


class TestCreateBarChart:
    """Testes para create_bar_chart."""

    @pytest.fixture
    def sample_df(self):
        """Fixture com dados."""
        return pd.DataFrame({
            "city": ["SP", "SP", "RJ", "BH", "SP"],
            "status": ["delivered", "pending", "delivered", "pending", "delivered"],
            "weight": [10, 5, 8, 12, 7],
        })

    def test_bar_chart_by_city(self, sample_df):
        """Testa gráfico de barras por cidade."""
        fig = create_bar_chart(sample_df, group_by="city")

        assert isinstance(fig, go.Figure)

    def test_bar_chart_by_status(self, sample_df):
        """Testa gráfico de barras por status."""
        fig = create_bar_chart(sample_df, group_by="status")

        assert isinstance(fig, go.Figure)

    def test_bar_chart_empty(self):
        """Testa gráfico vazio."""
        fig = create_bar_chart(pd.DataFrame(), group_by="city")
        assert isinstance(fig, go.Figure)


class TestCreatePieChart:
    """Testes para create_pie_chart."""

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "status": ["delivered", "pending", "delivered", "cancelled"],
        })

    def test_pie_chart_with_data(self, sample_df):
        """Testa gráfico de pizza com dados."""
        fig = create_pie_chart(sample_df, group_by="status")

        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0


class TestCreateHeatmap:
    """Testes para create_heatmap."""

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "latitude": [-23.5505, -23.5600, -23.5700],
            "longitude": [-46.6333, -46.6400, -46.6500],
        })

    def test_heatmap_with_data(self, sample_df):
        """Testa heatmap com dados."""
        fig = create_heatmap(sample_df)
        assert isinstance(fig, go.Figure)


class TestEmptyChart:
    """Testes para gráfico vazio."""

    def test_create_empty_chart(self):
        """Testa criação de chart vazio."""
        fig = _create_empty_chart("Teste", height=300)

        assert isinstance(fig, go.Figure)
        assert fig.layout.height == 300