"""
Configuração de logging estruturado com structlog.

Fornece logging consistente em formato JSON para produção
e formato legível para desenvolvimento.
"""

import logging
import sys
from typing import Optional

import structlog
from src.config import settings


def setup_logging() -> None:
    """
    Configura o logging estruturado da aplicação.

    Em produção: formato JSON para integração com ELK/Datadog
    Em desenvolvimento: formato console colorido e legível
    """
    log_level = getattr(logging, settings.log_level, logging.INFO)

    # Configurar logging padrão
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    if settings.is_production:
        # Formato JSON para produção
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Formato console para desenvolvimento
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """
    Obtém um logger estruturado nomeado.

    Args:
        name: Nome do logger (geralmente __name__ do módulo)

    Returns:
        BoundLogger: Logger configurado com contexto

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processando dados", count=100, status="success")
    """
    logger = structlog.get_logger(name or "dashboard")
    return logger