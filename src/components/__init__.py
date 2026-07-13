"""
Módulo de componentes UI do Dashboard.
"""

from src.components.header import render_header  # noqa: F401
from src.components.sidebar import render_sidebar  # noqa: F401
from src.components.metrics_cards import render_metrics_cards  # noqa: F401
from src.components.footer import render_footer  # noqa: F401

__all__ = [
    "render_header",
    "render_sidebar",
    "render_metrics_cards",
    "render_footer",
]