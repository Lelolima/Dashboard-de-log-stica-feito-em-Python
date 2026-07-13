"""
Configurações da aplicação usando Pydantic Settings.

Centraliza todas as configurações do dashboard com validação de tipos.
"""

from typing import Literal, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """
    Configurações do Dashboard Logística.

    Attributes:
        app_name: Nome da aplicação
        version: Versão da aplicação
        debug: Modo debug (development)
        host: Host do servidor
        port: Porta do servidor
        log_level: Nível de logging (DEBUG, INFO, WARNING, ERROR)
        log_format: Formato dos logs (json, console)
        mapbox_token: Token da API Mapbox para mapas
        cache_type: Tipo de cache (diskcache, redis, memory)
        redis_url: URL de conexão Redis (para cache redis)
        data_source: Fonte de dados (local, api, database)
        secret_key: Chave secreta para sessões
    """

    model_config = SettingsConfigDict(
        env_prefix="DASH_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App settings
    app_name: str = Field(default="Dashboard Logística Loggi", description="Nome da aplicação")
    version: str = Field(default="2.0.0", description="Versão da aplicação")
    debug: bool = Field(default=False, description="Modo debug")

    # Server settings
    host: str = Field(default="127.0.0.1", description="Host do servidor")
    port: int = Field(default=8050, ge=1, le=65535, description="Porta do servidor")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Nível de logging"
    )
    log_format: Literal["json", "console"] = Field(default="json", description="Formato dos logs")

    # External services
    mapbox_token: Optional[str] = Field(default=None, description="Token API Mapbox")

    # Cache
    cache_type: Literal["diskcache", "redis", "memory"] = Field(
        default="diskcache", description="Tipo de cache"
    )
    redis_url: Optional[str] = Field(default=None, description="URL Redis para cache")
    cache_dir: str = Field(default=".cache", description="Diretório para diskcache")

    # Data
    data_source: Literal["local", "api", "database"] = Field(
        default="local", description="Fonte de dados"
    )
    data_api_url: Optional[str] = Field(default=None, description="URL da API de dados")

    # Security
    secret_key: str = Field(
        default="change-me-in-production",
        description="Chave secreta para sessões",
        min_length=16,
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Valida se a porta está no range válido."""
        if not (1 <= v <= 65535):
            raise ValueError("Porta deve estar entre 1 e 65535")
        return v

    @property
    def is_production(self) -> bool:
        """Retorna True se estiver em produção."""
        return not self.debug

    @property
    def use_redis_cache(self) -> bool:
        """Retorna True se cache Redis está configurado."""
        return self.cache_type == "redis" and self.redis_url is not None


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """
    Factory para obter instância das configurações.

    Returns:
        Settings: Instância das configurações validadas
    """
    return settings