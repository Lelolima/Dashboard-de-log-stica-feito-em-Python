"""Garante que o .env.example é compatível com src/config.py (prefixo DASH_)."""

from pathlib import Path

from src.config import Settings

ENV_EXAMPLE = Path(__file__).resolve().parents[1] / ".env.example"


def test_env_example_carrega_e_usa_prefixo(monkeypatch):
    s = Settings(_env_file=str(ENV_EXAMPLE))
    assert s.port == 8050
    assert s.cache_type == "diskcache"
    for linha in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            assert linha.startswith("DASH_"), linha
