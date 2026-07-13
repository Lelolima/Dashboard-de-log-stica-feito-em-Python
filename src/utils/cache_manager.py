"""
Gerenciador de cache para otimização de performance.

Suporta múltiplos backends: diskcache, redis, memory.
"""

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional
from datetime import timedelta

import diskcache

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CacheManager:
    """
    Gerenciador de cache unificado com múltiplos backends.

    Attributes:
        backend: Backend de cache (diskcache, redis, memory)
        default_ttl: Tempo padrão de expiração em segundos
    """

    def __init__(
        self,
        cache_type: Optional[str] = None,
        redis_url: Optional[str] = None,
        cache_dir: Optional[str] = None,
        default_ttl: int = 300,
    ):
        """
        Inicializa o CacheManager.

        Args:
            cache_type: Tipo de cache (diskcache, redis, memory)
            redis_url: URL do Redis (para cache redis)
            cache_dir: Diretório para diskcache
            default_ttl: TTL padrão em segundos (default: 300)
        """
        self.cache_type = cache_type or settings.cache_type
        self.redis_url = redis_url or settings.redis_url
        self.cache_dir = cache_dir or settings.cache_dir
        self.default_ttl = default_ttl
        self._cache = None
        self._redis_client = None

        self._initialize_backend()

    def _initialize_backend(self) -> None:
        """Inicializa o backend de cache configurado."""
        if self.cache_type == "diskcache":
            try:
                self._cache = diskcache.Cache(self.cache_dir, size_limit=1e9)
                logger.info("Cache diskcache inicializado", path=self.cache_dir)
            except Exception as e:
                logger.warning("Falha ao inicializar diskcache, usando memory", error=str(e))
                self._cache = {}
        elif self.cache_type == "redis" and self.redis_url:
            try:
                import redis
                self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
                self._redis_client.ping()
                logger.info("Cache redis inicializado", url=self.redis_url)
            except Exception as e:
                logger.warning("Falha ao conectar Redis, fallback para diskcache", error=str(e))
                self._cache = diskcache.Cache(self.cache_dir, size_limit=1e9)
        else:
            self._cache = {}
            logger.info("Cache memory inicializado")

    def _generate_key(self, func_name: str, *args, **kwargs) -> str:
        """Gera chave de cache única baseada nos argumentos."""
        key_data = f"{func_name}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache.

        Args:
            key: Chave do cache

        Returns:
            Valor em cache ou None
        """
        if self._redis_client:
            try:
                value = self._redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            except Exception as e:
                logger.warning("Erro ao ler cache redis", error=str(e), key=key)
                return None
        elif isinstance(self._cache, diskcache.Cache):
            return self._cache.get(key)
        else:
            return self._cache.get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Armazena valor no cache.

        Args:
            key: Chave do cache
            value: Valor a armazenar
            ttl: Tempo de vida em segundos (usa default_ttl se None)

        Returns:
            True se sucesso, False se erro
        """
        ttl = ttl or self.default_ttl

        if self._redis_client:
            try:
                import redis
                self._redis_client.setex(key, ttl, json.dumps(value))
                return True
            except Exception as e:
                logger.warning("Erro ao escrever cache redis", error=str(e), key=key)
                return False
        elif isinstance(self._cache, diskcache.Cache):
            self._cache.set(key, value, expire=ttl)
            return True
        else:
            self._cache[key] = value
            return True

    def delete(self, key: str) -> bool:
        """Remove valor do cache."""
        if self._redis_client:
            try:
                self._redis_client.delete(key)
                return True
            except Exception as e:
                logger.warning("Erro ao deletar cache redis", error=str(e), key=key)
                return False
        elif isinstance(self._cache, diskcache.Cache):
            self._cache.delete(key)
            return True
        else:
            self._cache.pop(key, None)
            return True

    def clear(self) -> bool:
        """Limpa todo o cache."""
        if self._redis_client:
            try:
                self._redis_client.flushdb()
                return True
            except Exception as e:
                logger.warning("Erro ao limpar cache redis", error=str(e))
                return False
        elif isinstance(self._cache, diskcache.Cache):
            self._cache.clear()
            return True
        else:
            self._cache.clear()
            return True

    def cached(self, ttl: Optional[int] = None, key_prefix: str = ""):
        """
        Decorator para cache de funções.

        Args:
            ttl: Tempo de vida em segundos
            key_prefix: Prefixo para a chave de cache

        Example:
            >>> cache = CacheManager()
            >>> @cache.cached(ttl=600)
            ... def get_expensive_data(query: str) -> dict:
            ...     return fetch_data(query)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self._generate_key(f"{key_prefix}{func.__name__}", *args, **kwargs)

                # Tentar obter do cache
                cached_value = self.get(key)
                if cached_value is not None:
                    logger.debug(f"Cache hit: {func.__name__}", key=key)
                    return cached_value

                # Executar função e armazenar resultado
                logger.debug(f"Cache miss: {func.__name__}", key=key)
                result = func(*args, **kwargs)
                self.set(key, result, ttl=ttl or self.default_ttl)
                return result

            return wrapper
        return decorator

    def close(self) -> None:
        """Fecha conexões e limpa recursos."""
        if self._redis_client:
            self._redis_client.close()
        elif isinstance(self._cache, diskcache.Cache):
            self._cache.close()


# Instância global de cache
cache = CacheManager()


def get_cache() -> CacheManager:
    """Factory para obter instância do cache."""
    return cache