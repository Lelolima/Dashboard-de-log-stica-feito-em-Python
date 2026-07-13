"""
Módulo de estilos do Dashboard.

Define cores, temas e estilos para componentes.
"""

from typing import Dict, Any


# ============================================
# Cores do Design System
# ============================================

COLORS = {
    "primary": "#0d6efd",
    "secondary": "#6c757d",
    "success": "#198754",
    "info": "#0dcaf0",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "light": "#f8f9fa",
    "dark": "#212529",
}

# Status colors para entregas
STATUS_COLORS = {
    "delivered": "#198754",  # Verde
    "in_transit": "#0d6efd",  # Azul
    "pending": "#ffc107",  # Amarelo
    "cancelled": "#dc3545",  # Vermelho
}

# ============================================
# Tema Light (Bootstrap default)
# ============================================

THEME_LIGHT: Dict[str, Any] = {
    "bg_body": "#f8f9fa",
    "bg_card": "#ffffff",
    "bg_header": "#ffffff",
    "text_primary": "#212529",
    "text_secondary": "#6c757d",
    "text_muted": "#6c757d",
    "border_color": "#dee2e6",
    "shadow": "0 2px 12px rgba(0, 0, 0, 0.08)",
    "shadow_sm": "0 1px 4px rgba(0, 0, 0, 0.06)",
    "shadow_lg": "0 4px 24px rgba(0, 0, 0, 0.12)",
    "border_radius": "12px",
    "border_radius_sm": "8px",
    "border_radius_lg": "16px",
    "transition": "all 0.2s ease-in-out",
}

# ============================================
# Tema Dark
# ============================================

THEME_DARK: Dict[str, Any] = {
    "bg_body": "#1a1a2e",
    "bg_card": "#16213e",
    "bg_header": "#16213e",
    "text_primary": "#e4e4e4",
    "text_secondary": "#a0a0a0",
    "text_muted": "#6c757d",
    "border_color": "#2d3748",
    "shadow": "0 2px 12px rgba(0, 0, 0, 0.24)",
    "shadow_sm": "0 1px 4px rgba(0, 0, 0, 0.18)",
    "shadow_lg": "0 4px 24px rgba(0, 0, 0, 0.36)",
    "border_radius": "12px",
    "border_radius_sm": "8px",
    "border_radius_lg": "16px",
    "transition": "all 0.2s ease-in-out",
}

# ============================================
# Estilos de Componentes
# ============================================

CARD_STYLE = {
    "borderRadius": THEME_LIGHT["border_radius"],
    "border": "none",
    "boxShadow": THEME_LIGHT["shadow"],
    "transition": THEME_LIGHT["transition"],
}

CARD_STYLE_DARK = {
    **CARD_STYLE,
    "backgroundColor": THEME_DARK["bg_card"],
    "color": THEME_DARK["text_primary"],
}

BUTTON_STYLE = {
    "borderRadius": "8px",
    "padding": "0.5rem 1rem",
    "fontWeight": "500",
    "transition": "all 0.15s ease-in-out",
}

INPUT_STYLE = {
    "borderRadius": "8px",
    "border": "1px solid #ced4da",
    "padding": "0.5rem 0.75rem",
    "fontSize": "0.875rem",
    "transition": "border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out",
}

# ============================================
# Layout
# ============================================

LAYOUT_STYLE = {
    "minHeight": "100vh",
    "backgroundColor": THEME_LIGHT["bg_body"],
    "display": "flex",
    "flexDirection": "column",
}

LAYOUT_STYLE_DARK = {
    **LAYOUT_STYLE,
    "backgroundColor": THEME_DARK["bg_body"],
    "color": THEME_DARK["text_primary"],
}

HEADER_STYLE = {
    "backgroundColor": THEME_LIGHT["bg_header"],
    "borderBottom": f"1px solid {THEME_LIGHT['border_color']}",
    "boxShadow": THEME_LIGHT["shadow_sm"],
}

SIDEBAR_STYLE = {
    "backgroundColor": THEME_LIGHT["bg_card"],
    "borderRight": f"1px solid {THEME_LIGHT['border_color']}",
    "minHeight": "calc(100vh - 80px)",
}

# ============================================
# Responsividade
# ============================================

BREAKPOINTS = {
    "xs": 0,
    "sm": 576,
    "md": 768,
    "lg": 992,
    "xl": 1200,
    "xxl": 1400,
}

# ============================================
# Tipografia
# ============================================

FONT_FAMILY = '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

FONT_SIZES = {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
}

FONT_WEIGHTS = {
    "normal": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}

# ============================================
# Helpers
# ============================================


def get_theme_styles(dark: bool = False) -> Dict[str, Any]:
    """
    Retorna estilos do tema.

    Args:
        dark: Se True retorna tema escuro

    Returns:
        Dicionário com estilos do tema
    """
    if dark:
        return {
            "theme": "dark",
            "colors": {**THEME_DARK, **STATUS_COLORS},
            "card": CARD_STYLE_DARK,
            "layout": LAYOUT_STYLE_DARK,
        }
    return {
        "theme": "light",
        "colors": {**THEME_LIGHT, **STATUS_COLORS},
        "card": CARD_STYLE,
        "layout": LAYOUT_STYLE,
    }


def get_card_style(dark: bool = False) -> Dict[str, Any]:
    """Retorna estilo de card baseado no tema."""
    return CARD_STYLE_DARK if dark else CARD_STYLE


def get_layout_style(dark: bool = False) -> Dict[str, Any]:
    """Retorna estilo de layout baseado no tema."""
    return LAYOUT_STYLE_DARK if dark else LAYOUT_STYLE