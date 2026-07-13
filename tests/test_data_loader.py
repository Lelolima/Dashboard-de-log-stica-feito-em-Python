"""
Testes do módulo DataLoader.
"""

import pytest
import pandas as pd
from src.data.loader import DataLoader
from src.config import settings


class TestDataLoader:
    """Testes unitários para DataLoader."""

    @pytest.fixture
    def loader(self):
        """Fixture que cria DataLoader com dados locais."""
        return DataLoader(data_source="local", cache_enabled=False)

    def test_load_sample_data(self):
        """Testa carregamento de dados de exemplo."""
        loader = DataLoader(data_source="local", cache_enabled=False)
        df = loader.load_deliveries()

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "id" in df.columns
        assert "latitude" in df.columns
        assert "longitude" in df.columns
        assert "city" in df.columns
        assert "state" in df.columns
        assert "status" in df.columns

    def test_process_dataframe(self):
        """Testa processamento de DataFrame."""
        loader = DataLoader()

        # Criar dados brutos
        raw_data = pd.DataFrame({
            "ID": ["ENT-001", "ENT-002", "ENT-001"],  # duplicata
            "Latitude": [-23.5505, -22.9068, None],  # nulo
            "Longitude": [-46.6333, -43.1729, -46.6333],
            "City": ["São Paulo", "Rio de Janeiro", "São Paulo"],
            "State": ["SP", "RJ", "SP"],
            "Status": ["delivered", "pending", "delivered"],
        })

        processed = loader._process_dataframe(raw_data)

        # Verificardeduplicação
        assert len(processed) == 2  # removal uma duplicata

        # Verificar tratamento de nulos
        assert processed["longitude"].isna().sum() == 0

        # Verificar colunas normalizadas
        assert "id" in processed.columns
        assert "latitude" in processed.columns

    def test_get_unique_values(self):
        """Testa obtenção de valores únicos."""
        loader = DataLoader()
        df = pd.DataFrame({
            "city": ["SP", "RJ", "SP", "BH"],
            "state": ["SP", "RJ", "SP", "MG"],
        })

        cities = loader.get_unique_values(df, "city")
        states = loader.get_unique_values(df, "state")

        assert cities == ["BH", "RJ", "SP"]
        assert states == ["MG", "RJ", "SP"]

    def test_get_unique_values_missing_column(self):
        """Testa coluna inexistente."""
        loader = DataLoader()
        df = pd.DataFrame({"city": ["SP", "RJ"]})

        result = loader.get_unique_values(df, "nonexistent")
        assert result == []

    def test_load_data_utility_function(self):
        """Testa função utilitária load_data()."""
        from src.data.loader import load_data

        df = load_data()

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


class TestDataLoaderIntegration:
    """Testes de integração para DataLoader."""

    def test_full_pipeline(self):
        """Testa pipeline completo: load → process → filter."""
        loader = DataLoader(data_source="local", cache_enabled=False)
        df = loader.load_deliveries()

        # Verificar estrutura
        assert len(df) >= 100  # dados de exemplo têm 500 entregas

        # Verificar statuses válidos
        valid_statuses = ["pending", "in_transit", "delivered", "cancelled"]
        assert all(s in valid_statuses for s in df["status"].unique())

        # Verificar coordenadas válidas
        assert df["latitude"].between(-90, 90).all()
        assert df["longitude"].between(-180, 180).all()