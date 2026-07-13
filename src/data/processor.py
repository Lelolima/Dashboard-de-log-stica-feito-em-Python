"""
Processamento de dados para o dashboard.

Transforma dados brutos em métricas e aggregações para visualização.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """
    Processador de dados para extração de métricas e filtragem.

    Example:
        >>> processor = DataProcessor(df)
        >>> metrics = processor.calcular_metricas()
    """

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o processador.

        Args:
            df: DataFrame com dados de entregas
        """
        self.df = df.copy()
        logger.info("DataProcessor inicializado", rows=len(self.df))

    def calcular_metricas(self) -> Dict[str, Any]:
        """
        Calcula métricas principais do dashboard.

        Returns:
            Dicionário com métricas calculadas
        """
        total = len(self.df)

        if total == 0:
            return self._metricas_vazias()

        # Contar por status
        status_counts = self.df["status"].value_counts().to_dict() if "status" in self.df.columns else {}

        entregas_pendentes = status_counts.get("pending", 0)
        entregas_em_transito = status_counts.get("in_transit", 0)
        entregas_entregues = status_counts.get("delivered", 0)
        entregas_canceladas = status_counts.get("cancelled", 0)

        # Taxa de sucesso
        taxa_sucesso = (entregas_entregues / total * 100) if total > 0 else 0

        # Peso total e médio
        peso_total = self.df["weight"].sum() if "weight" in self.df.columns else 0
        peso_medio = self.df["weight"].mean() if "weight" in self.df.columns else 0

        # Valor total e médio
        valor_total = self.df.get("value", pd.Series([0] * len(self.df))).sum()
        valor_medio = self.df.get("value", pd.Series([0] * len(self.df))).mean()

        metricas = {
            "total_entregas": total,
            "entregas_pendentes": entregas_pendentes,
            "entregas_em_transito": entregas_em_transito,
            "entregas_entregues": entregas_entregues,
            "entregas_canceladas": entregas_canceladas,
            "taxa_sucesso": round(taxa_sucesso, 2),
            "peso_total": round(peso_total, 2),
            "peso_medio": round(peso_medio, 2),
            "valor_total": round(valor_total, 2),
            "valor_medio": round(valor_medio, 2),
        }

        logger.info("Métricas calculadas", total=total, taxa_sucesso=taxa_sucesso)
        return metricas

    def _metricas_vazias(self) -> Dict[str, Any]:
        """Retorna métricas vazias para DataFrame vazio."""
        return {
            "total_entregas": 0,
            "entregas_pendentes": 0,
            "entregas_em_transito": 0,
            "entregas_entregues": 0,
            "entregas_canceladas": 0,
            "taxa_sucesso": 0.0,
            "peso_total": 0.0,
            "peso_medio": 0.0,
            "valor_total": 0.0,
            "valor_medio": 0.0,
        }

    def filtrar_por_regiao(self, estado: Optional[str] = None, cidade: Optional[str] = None) -> "DataProcessor":
        """
        Filtra dados por região.

        Args:
            estado: UF do estado
            cidade: Nome da cidade

        Returns:
            Self para chaining
        """
        if estado:
            self.df = self.df[self.df["state"] == estado.upper()]
            logger.info(f"Filtrado por estado: {estado}", rows=len(self.df))

        if cidade:
            self.df = self.df[self.df["city"].str.lower() == cidade.lower()]
            logger.info(f"Filtrado por cidade: {cidade}", rows=len(self.df))

        return self

    def filtrar_por_status(self, statuses: List[str]) -> "DataProcessor":
        """
        Filtra dados por status.

        Args:
            statuses: Lista de statuses para filtrar

        Returns:
            Self para chaining
        """
        if "status" in self.df.columns:
            self.df = self.df[self.df["status"].isin(statuses)]
            logger.info(f"Filtrado por status: {statuses}", rows=len(self.df))

        return self

    def filtrar_por_hub(self, hub_ids: List[str]) -> "DataProcessor":
        """
        Filtra dados por hub.

        Args:
            hub_ids: Lista de IDs de hubs

        Returns:
            Self para chaining
        """
        if "hub_id" in self.df.columns:
            self.df = self.df[self.df["hub_id"].isin(hub_ids)]
            logger.info(f"Filtrado por hubs: {hub_ids}", rows=len(self.df))

        return self

    def agrupar_por_cidade(self) -> pd.DataFrame:
        """
        Agrega dados por cidade.

        Returns:
            DataFrame agrupado por cidade
        """
        if "city" not in self.df.columns:
            return pd.DataFrame()

        grouped = self.df.groupby("city").agg({
            "id": "count",
            "weight": ["sum", "mean"],
            "value": ["sum", "mean"],
        }).reset_index()

        grouped.columns = ["cidade", "total_entregas", "peso_total", "peso_medio", "valor_total", "valor_medio"]
        grouped = grouped.sort_values("total_entregas", ascending=False)

        logger.info("Agrupamento por cidade realizado", cities=len(grouped))
        return grouped

    def agrupar_por_hub(self) -> pd.DataFrame:
        """
        Agrega dados por hub.

        Returns:
            DataFrame agrupado por hub
        """
        if "hub_id" not in self.df.columns:
            return pd.DataFrame()

        grouped = self.df.groupby("hub_id").agg({
            "id": "count",
            "hub_name": "first",
            "weight": "sum",
            "value": "sum",
        }).reset_index()

        grouped.columns = ["hub_id", "hub_name", "total_entregas", "peso_total", "valor_total"]
        grouped = grouped.sort_values("total_entregas", ascending=False)

        logger.info("Agrupamento por hub realizado", hubs=len(grouped))
        return grouped

    def agrupar_por_status(self) -> pd.DataFrame:
        """
        Agrega dados por status.

        Returns:
            DataFrame agrupado por status
        """
        if "status" not in self.df.columns:
            return pd.DataFrame()

        grouped = self.df.groupby("status").agg({
            "id": "count",
            "weight": "sum",
            "value": "sum",
        }).reset_index()

        grouped.columns = ["status", "total_entregas", "peso_total", "valor_total"]
        grouped = grouped.sort_values("total_entregas", ascending=False)

        logger.info("Agrupamento por status realizado")
        return grouped

    def get_dados_mapa(self) -> pd.DataFrame:
        """
        Prepara dados para visualização no mapa.

        Returns:
            DataFrame com colunas necessárias para o mapa
        """
        required_cols = ["id", "latitude", "longitude", "city", "state", "status"]
        available_cols = [col for col in required_cols if col in self.df.columns]

        if "latitude" not in self.df.columns or "longitude" not in self.df.columns:
            logger.warning("Dados de latitude/longitude não encontrados")
            return pd.DataFrame()

        return self.df[available_cols].copy()

    def get_unique_cities(self) -> List[str]:
        """Retorna lista de cidades únicas."""
        if "city" not in self.df.columns:
            return []
        return sorted(self.df["city"].dropna().unique().tolist())

    def get_unique_states(self) -> List[str]:
        """Retorna lista de estados únicos."""
        if "state" not in self.df.columns:
            return []
        return sorted(self.df["state"].dropna().unique().tolist())

    def get_unique_hubs(self) -> List[Dict[str, str]]:
        """Retorna lista de hubs únicos com id e nome."""
        if "hub_id" not in self.df.columns:
            return []

        hubs = self.df[["hub_id", "hub_name"]].drop_duplicates()
        return hubs.to_dict("records")

    def get_unique_statuses(self) -> List[str]:
        """Retorna lista de statuses únicos."""
        if "status" not in self.df.columns:
            return []
        return sorted(self.df["status"].dropna().unique().tolist())