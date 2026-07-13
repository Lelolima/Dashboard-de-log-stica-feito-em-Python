"""
Módulo de carregamento de dados.

Responsável por carregar dados de múltiplas fontes:
- API externa
- Arquivos locais (JSON, CSV)
- Banco de dados
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pandas as pd
import requests

from src.config import settings
from src.utils.logger import get_logger
from src.utils.cache_manager import cache
from src.utils.data_validator import DataValidator

logger = get_logger(__name__)


class DataLoader:
    """
    Carregador de dados para o dashboard.

    Suporta múltiplas fontes e cache automático.

    Attributes:
        data_source: Fonte de dados (local, api, database)
        cache_enabled: Se cache está habilitado
        validator: Validador de dados
    """

    def __init__(
        self,
        data_source: Optional[str] = None,
        cache_enabled: bool = True,
    ):
        """
        Inicializa o DataLoader.

        Args:
            data_source: Fonte de dados (default: do settings)
            cache_enabled: Habilitar cache
        """
        self.data_source = data_source or settings.data_source
        self.cache_enabled = cache_enabled
        self.validator = DataValidator()
        self._cache = cache  # Usa instância global diretamente

        logger.info(
            "DataLoader inicializado",
            data_source=self.data_source,
            cache_enabled=cache_enabled,
        )

    def load_deliveries(self) -> pd.DataFrame:
        """
        Carrega dados de entregas.

        Returns:
            DataFrame com dados de entregas

        Raises:
            FileNotFoundError: Se arquivo local não encontrado
            requests.RequestException: Se falha na API
        """
        logger.info("Carregando dados de entregas", source=self.data_source)

        if self.data_source == "local":
            return self._load_from_local()
        elif self.data_source == "api":
            return self._load_from_api()
        else:
            # Dados de exemplo para demonstração
            return self._load_sample_data()

    def _load_from_local(self) -> pd.DataFrame:
        """Carrega de arquivo JSON local."""
        data_dir = Path(__file__).parent / "data"
        files = [
            data_dir / "deliveries.json",
            data_dir / "entregas.json",
            Path.cwd() / "data" / "deliveries.json",
        ]

        for file_path in files:
            if file_path.exists():
                logger.info(f"Carregando arquivo local: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    df = pd.DataFrame(data)
                    logger.info("Dados carregados com sucesso", rows=len(df))
                    return self._process_dataframe(df)

                except json.JSONDecodeError as e:
                    logger.error("Erro ao parsear JSON", path=str(file_path), error=str(e))
                    raise
                except Exception as e:
                    logger.error("Erro ao carregar arquivo", path=str(file_path), error=str(e))
                    raise

        logger.warning("Nenhum arquivo local encontrado, usando dados de exemplo")
        return self._load_sample_data()

    def _load_from_api(self) -> pd.DataFrame:
        """Carrega dados de API externa."""
        api_url = settings.data_api_url

        if not api_url:
            logger.warning("API URL não configurada, fallback para local")
            return self._load_from_local()

        logger.info(f"Carregando dados da API: {api_url}")

        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data)
            logger.info("Dados da API carregados", rows=len(df))
            return self._process_dataframe(df)

        except requests.RequestException as e:
            logger.error("Falha ao carregar da API", url=api_url, error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Resposta API inválida", url=api_url, error=str(e))
            raise

    def _load_sample_data(self) -> pd.DataFrame:
        """
        Gera dados de exemplo para demonstração.

        Dícnica de logística urbana com hubs e entregas simuladas.
        """
        logger.info("Gerando dados de exemplo para demonstração")

        # Hubs de distribuição (baseado em cidades reais do Brasil)
        hubs = [
            {"id": "hub_sp_centro", "name": "São Paulo - Centro", "city": "São Paulo", "state": "SP", "lat": -23.5505, "lng": -46.6333},
            {"id": "hub_sp_zsul", "name": "São Paulo - Zona Sul", "city": "São Paulo", "state": "SP", "lat": -23.7000, "lng": -46.6800},
            {"id": "hub_rj_centro", "name": "Rio de Janeiro - Centro", "city": "Rio de Janeiro", "state": "RJ", "lat": -22.9068, "lng": -43.1729},
            {"id": "hub_mg_centro", "name": "Belo Horizonte - Centro", "city": "Belo Horizonte", "state": "MG", "lat": -19.9167, "lng": -43.9345},
        ]

        # Gerar entregas simuladas
        import random
        random.seed(42)  # Reprodutibilidade

        deliveries = []
        statuses = ["pending", "in_transit", "delivered", "delivered", "delivered", "cancelled"]

        for i in range(500):
            hub = random.choice(hubs)

            # Variação de coordenadas ao redor do hub
            lat_var = random.uniform(-0.1, 0.1)
            lng_var = random.uniform(-0.1, 0.1)

            delivery = {
                "id": f"ENT-{i+1:05d}",
                "name": f"Cliente {i+1}",
                "address": f"Rua {random.randint(1, 999)}, {random.choice(['Centro', 'Jardins', 'Vila', 'Bairro'])}",
                "latitude": hub["lat"] + lat_var,
                "longitude": hub["lng"] + lng_var,
                "city": hub["city"],
                "state": hub["state"],
                "status": random.choice(statuses),
                "hub_id": hub["id"],
                "hub_name": hub["name"],
                "weight": round(random.uniform(0.5, 50), 2),
                "value": round(random.uniform(10, 500), 2),
            }
            deliveries.append(delivery)

        df = pd.DataFrame(deliveries)
        logger.info("Dados de exemplo gerados", count=len(df))

        return self._process_dataframe(df)

    def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa e limpa o DataFrame.

        Args:
            df: DataFrame bruto

        Returns:
            DataFrame processado
        """
        logger.info("Processando dados", rows=len(df))

        # Normalizar colunas
        df.columns = df.columns.str.lower().str.strip()

        # Colunas obrigatórias
        required = ["id", "latitude", "longitude", "city", "state", "hub_id"]
        missing = [col for col in required if col not in df.columns]

        if missing:
            logger.warning("Colunas faltantes", columns=missing)

        # Tratar valores nulos
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Tratar duplicatas
        before_dedup = len(df)
        if "id" in df.columns:
            df = df.drop_duplicates(subset=["id"])
            dupes = before_dedup - len(df)
            if dupes > 0:
                logger.info(f"Removidas {dupes} duplicatas")

        logger.info("Dados processados", rows=len(df))
        return df

    def load_hubs(self) -> pd.DataFrame:
        """
        Carrega dados de hubs.

        Returns:
            DataFrame com dados de hubs
        """
        logger.info("Carregando dados de hubs")

        # Dados padrão de hubs
        hubs_data = [
            {"id": "hub_sp_centro", "name": "São Paulo - Centro", "city": "São Paulo", "state": "SP", "lat": -23.5505, "lng": -46.6333, "capacity": 1000},
            {"id": "hub_sp_zsul", "name": "São Paulo - Zona Sul", "city": "São Paulo", "state": "SP", "lat": -23.7000, "lng": -46.6800, "capacity": 800},
            {"id": "hub_rj_centro", "name": "Rio de Janeiro - Centro", "city": "Rio de Janeiro", "state": "RJ", "lat": -22.9068, "lng": -43.1729, "capacity": 600},
            {"id": "hub_mg_centro", "name": "Belo Horizonte - Centro", "city": "Belo Horizonte", "state": "MG", "lat": -19.9167, "lng": -43.9345, "capacity": 500},
        ]

        return pd.DataFrame(hubs_data)

    def get_unique_values(self, df: pd.DataFrame, column: str) -> List[Any]:
        """
        Obtém valores únicos de uma coluna.

        Args:
            df: DataFrame
            column: Nome da coluna

        Returns:
            Lista de valores únicos
        """
        if column not in df.columns:
            return []
        return sorted(df[column].dropna().unique().tolist())


def load_data() -> pd.DataFrame:
    """
    Função utilitária para carregar dados.

    Returns:
        DataFrame com dados de entregas

    Example:
        >>> df = load_data()
    """
    loader = DataLoader()
    return loader.load_deliveries()