"""
Validação de dados com Pydantic.

Define schemas para validação de dados de entregas e hubs.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr


class DeliverySchema(BaseModel):
    """
    Schema para dados de entrega.

    Attributes:
        id: Identificador único da entrega
        name: Nome do destinatário
        address: Endereço de entrega
        latitude: Latitude do endereço
        longitude: Longitude do endereço
        city: Cidade de entrega
        state: Estado (UF)
        status: Status da entrega (pending, in_transit, delivered)
        hub_id: ID do hub responsable
        estimated_delivery: Data estimada de entrega
        actual_delivery: Data real de entrega
        weight: Peso da entrega em kg
        dimensions: Dimensões da embalagem (LxAxP em cm)
    """

    id: str = Field(..., description="Identificador único da entrega")
    name: str = Field(..., min_length=1, max_length=200, description="Nome do destinatário")
    address: str = Field(..., min_length=5, max_length=500, description="Endereço de entrega")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude do endereço")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude do endereço")
    city: str = Field(..., min_length=1, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="Estado (UF)")
    status: str = Field(default="pending", description="Status da entrega")
    hub_id: str = Field(..., description="ID do hub")
    estimated_delivery: Optional[datetime] = Field(default=None, description="Data estimada")
    actual_delivery: Optional[datetime] = Field(default=None, description="Data real")
    weight: Optional[float] = Field(default=None, ge=0, le=1000, description="Peso em kg")
    dimensions: Optional[str] = Field(default=None, description="Dimensões LxAxP")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Valida status da entrega."""
        valid_statuses = ["pending", "in_transit", "delivered", "cancelled", "returned"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {valid_statuses}")
        return v.lower()

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        """Valida UF do estado."""
        return v.upper()


class HubSchema(BaseModel):
    """
    Schema para dados de hub.

    Attributes:
        id: Identificador único do hub
        name: Nome do hub
        latitude: Latitude do hub
        longitude: Longitude do hub
        city: Cidade do hub
        state: Estado (UF)
        capacity: Capacidade máxima de entregas/dia
        active: Se o hub está ativo
    """

    id: str = Field(..., description="Identificador único do hub")
    name: str = Field(..., min_length=1, max_length=200, description="Nome do hub")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    city: str = Field(..., min_length=1, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="Estado (UF)")
    capacity: int = Field(default=1000, ge=1, le=100000, description="Capacidade diária")
    active: bool = Field(default=True, description="Hub ativo")


class DeliveryMetrics(BaseModel):
    """
    Schema para métricas de entregas.

    Attributes:
        total_entregas: Total de entregas
        entregas_pendentes: Entregas pendentes
        entregas_em_transito: Entregas em trânsito
        entregas_entregues: Entregas entregues
        entregas_canceladas: Entregas canceladas
        taxa_sucesso: Taxa de sucesso (%)
        tempo_medio_entrega: Tempo médio em horas
        peso_total: Peso total em kg
    """

    total_entregas: int = Field(..., ge=0)
    entregas_pendentes: int = Field(default=0, ge=0)
    entregas_em_transito: int = Field(default=0, ge=0)
    entregas_entregues: int = Field(default=0, ge=0)
    entregas_canceladas: int = Field(default=0, ge=0)
    taxa_sucesso: float = Field(default=0.0, ge=0, le=100)
    tempo_medio_entrega: Optional[float] = Field(default=None, ge=0)
    peso_total: float = Field(default=0.0, ge=0)


class DataValidator:
    """
    Validador de dados para entregas e hubs.

    Example:
        >>> validator = DataValidator()
        >>> delivery = validator.validate_delivery({"id": "1", "name": "João", ...})
    """

    def __init__(self):
        """Inicializa o validador."""
        self._delivery_schema = DeliverySchema
        self._hub_schema = HubSchema
        self._metrics_schema = DeliveryMetrics

    def validate_delivery(self, data: Dict[str, Any]) -> DeliverySchema:
        """
        Valida dados de entrega.

        Args:
            data: Dicionário com dados da entrega

        Returns:
            DeliverySchema: Dados validados

        Raises:
            ValueError: Se dados forem inválidos
        """
        return self._delivery_schema.model_validate(data)

    def validate_hub(self, data: Dict[str, Any]) -> HubSchema:
        """
        Valida dados de hub.

        Args:
            data: Dicionário com dados do hub

        Returns:
            HubSchema: Dados validados
        """
        return self._hub_schema.model_validate(data)

    def validate_metrics(self, data: Dict[str, Any]) -> DeliveryMetrics:
        """
        Valida métricas de entregas.

        Args:
            data: Dicionário com métricas

        Returns:
            DeliveryMetrics: Métricas validadas
        """
        return self._metrics_schema.model_validate(data)

    def validate_dataframe(
        self,
        data: List[Dict[str, Any]],
        schema_type: str = "delivery"
    ) -> List[Dict[str, Any]]:
        """
        Valida lista de dados (DataFrame-like).

        Args:
            data: Lista de dicionários
            schema_type: Tipo de schema (delivery, hub, metrics)

        Returns:
            List[Dict]: Lista de dados validados
        """
        schema_map = {
            "delivery": self._delivery_schema,
            "hub": self._hub_schema,
            "metrics": self._metrics_schema,
        }
        schema = schema_map.get(schema_type, self._delivery_schema)

        validated = []
        for item in data:
            try:
                validated.append(schema.model_validate(item).model_dump())
            except Exception as e:
                # Log erro mas continua processando
                pass

        return validated