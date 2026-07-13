"""
Testes do módulo DataProcessor.
"""

import pytest
import pandas as pd
from src.data.processor import DataProcessor


class TestDataProcessor:
    """Testes unitários para DataProcessor."""

    @pytest.fixture
    def sample_df(self):
        """Fixture com dados de exemplo."""
        return pd.DataFrame({
            "id": ["ENT-001", "ENT-002", "ENT-003", "ENT-004"],
            "city": ["SP", "SP", "RJ", "BH"],
            "state": ["SP", "SP", "RJ", "MG"],
            "status": ["delivered", "pending", "delivered", "cancelled"],
            "hub_id": ["hub_sp", "hub_sp", "hub_rj", "hub_bh"],
            "hub_name": ["SP Centro", "SP Centro", "RJ Centro", "BH Centro"],
            "weight": [10.5, 5.0, 8.0, 12.0],
            "value": [100.0, 50.0, 80.0, 120.0],
        })

    def test_calcular_metricas(self, sample_df):
        """Testa cálculo de métricas."""
        processor = DataProcessor(sample_df)
        metrics = processor.calcular_metricas()

        assert metrics["total_entregas"] == 4
        assert metrics["entregas_pendentes"] == 1
        assert metrics["entregas_entregues"] == 2
        assert metrics["entregas_canceladas"] == 1
        assert metrics["taxa_sucesso"] == 50.0  # 2/4 = 50%
        assert metrics["peso_total"] == 35.5

    def test_calcular_metricas_vazio(self):
        """Testa métricas com DataFrame vazio."""
        processor = DataProcessor(pd.DataFrame())
        metrics = processor.calcular_metricas()

        assert metrics["total_entregas"] == 0
        assert metrics["taxa_sucesso"] == 0.0

    def test_filtrar_por_regiao(self, sample_df):
        """Testa filtro por estado."""
        processor = DataProcessor(sample_df)
        processor.filtrar_por_regiao(estado="SP")

        assert len(processor.df) == 2
        assert all(processor.df["state"] == "SP")

    def test_filtrar_por_status(self, sample_df):
        """Testa filtro por status."""
        processor = DataProcessor(sample_df)
        processor.filtrar_por_status(["delivered"])

        assert len(processor.df) == 2
        assert all(processor.df["status"] == "delivered")

    def test_filtrar_por_hub(self, sample_df):
        """Testa filtro por hub."""
        processor = DataProcessor(sample_df)
        processor.filtrar_por_hub(["hub_sp"])

        assert len(processor.df) == 2
        assert all(processor.df["hub_id"] == "hub_sp")

    def test_agrupar_por_cidade(self, sample_df):
        """Testa agrupamento por cidade."""
        processor = DataProcessor(sample_df)
        grouped = processor.agrupar_por_cidade()

        assert len(grouped) == 3  # SP, RJ, BH
        assert grouped.iloc[0]["cidade"] == "SP"
        assert grouped.iloc[0]["total_entregas"] == 2

    def test_agrupar_por_status(self, sample_df):
        """Testa agrupamento por status."""
        processor = DataProcessor(sample_df)
        grouped = processor.agrupar_por_status()

        assert len(grouped) == 3  # delivered, pending, cancelled
        assert grouped[grouped["status"] == "delivered"]["total_entregas"].values[0] == 2

    def test_get_unique_cities(self, sample_df):
        """Testa obtenção de cidades únicas."""
        processor = DataProcessor(sample_df)
        cities = processor.get_unique_cities()

        assert cities == ["BH", "RJ", "SP"]

    def test_get_unique_statuses(self, sample_df):
        """Testa obtenção de statuses únicos."""
        processor = DataProcessor(sample_df)
        statuses = processor.get_unique_statuses()

        assert statuses == ["cancelled", "delivered", "pending"]

    def test_get_dados_mapa(self, sample_df):
        """Testa preparação de dados para mapa."""
        processor = DataProcessor(sample_df)
        map_data = processor.get_dados_mapa()

        assert "latitude" in map_data.columns
        assert "longitude" in map_data.columns
        assert "city" in map_data.columns
        assert "state" in map_data.columns