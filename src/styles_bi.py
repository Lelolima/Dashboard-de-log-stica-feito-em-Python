"""
Design System para Dashboard BI Enterprise.

Paleta de cores profissional, gradients e estilos para visualizações enterprise.
"""

from typing import Dict, Any, List


# ============================================
# PALETA DE CORES PROFISSIONAL PARA BI
# ============================================

COLORS = {
    # Cores Primárias
    "primary": "#2563eb",       # Azul enterprise
    "primary_dark": "#1d4ed8",
    "primary_light": "#3b82f6",

    "secondary": "#64748b",     # Slate
    "secondary_dark": "#475569",
    "secondary_light": "#94a3b8",

    # Cores de Status
    "success": "#10b981",       # Emerald
    "success_dark": "#059669",
    "success_light": "#34d399",

    "warning": "#f59e0b",       # Amber
    "warning_dark": "#d97706",
    "warning_light": "#fbbf24",

    "danger": "#ef4444",        # Red
    "danger_dark": "#dc2626",
    "danger_light": "#f87171",

    "info": "#06b6d4",          # Cyan
    "info_dark": "#0891b2",
    "info_light": "#22d3ee",

    # Cores Neutras
    "neutral_50": "#f8fafc",
    "neutral_100": "#f1f5f9",
    "neutral_200": "#e2e8f0",
    "neutral_300": "#cbd5e1",
    "neutral_400": "#94a3b8",
    "neutral_500": "#64748b",
    "neutral_600": "#475569",
    "neutral_700": "#334155",
    "neutral_800": "#1e293b",
    "neutral_900": "#0f172a",
}

# ============================================
# CORES CATEGÓRICAS PARA GRÁFICOS
# ============================================

CATEGORICAL_COLORS = [
    "#2563eb",  # Azul
    "#10b981",  # Verde
    "#f59e0b",  # Âmbar
    "#ef4444",  # Vermelho
    "#8b5cf6",  # Violeta
    "#06b6d4",  # Cyan
    "#ec4899",  # Rosa
    "#14b8a6",  # Teal
]

# ============================================
# CORES SEQUENCIAIS (Heatmaps, Densidade)
# ============================================

SEQUENTIAL_COLORS = [
    "#dbeafe",  # Azul muito claro
    "#93c5fd",  # Azul claro
    "#60a5fa",  # Azul médio
    "#3b82f6",  # Azul
    "#2563eb",  # Azul escuro
    "#1d4ed8",  # Azul mais escuro
]

# ============================================
# CORES DIVERGING (Variação positiva/negativa)
# ============================================

DIVERGING_COLORS = [
    "#ef4444",  # Vermelho (negativo)
    "#f87171",
    "#fca5a5",
    "#ffffff",  # Neutro
    "#93c5fd",
    "#60a5fa",
    "#3b82f6",  # Azul (positivo)
]

# ============================================
# GRADIENTS MODERNOS
# ============================================

GRADIENTS = {
    "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "success": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
    "warning": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
    "danger": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
    "dark": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
    "ocean": "linear-gradient(135deg, #2563eb 0%, #06b6d4 100%)",
    "sunset": "linear-gradient(135deg, #f59e0b 0%, #ec4899 100%)",
}

# ============================================
# SOMBRAS EMPRESARIAIS
# ============================================

SHADOWS = {
    "xs": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "sm": "0 1px 3px rgba(0, 0, 0, 0.1)",
    "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px rgba(0, 0, 0, 0.15)",
    "xl": "0 20px 25px rgba(0, 0, 0, 0.2)",
    "inner": "inset 0 2px 4px rgba(0, 0, 0, 0.05)",
}

# ============================================
# STATUS CORES (Entregas)
# ============================================

STATUS_COLORS = {
    "delivered": {
        "bg": "#10b981",
        "bg_light": "#d1fae5",
        "text": "#065f46",
        "icon": "✅",
        "label": "Entregue",
    },
    "in_transit": {
        "bg": "#3b82f6",
        "bg_light": "#dbeafe",
        "text": "#1e40af",
        "icon": "🚚",
        "label": "Em Trânsito",
    },
    "pending": {
        "bg": "#f59e0b",
        "bg_light": "#fef3c7",
        "text": "#92400e",
        "icon": "⏳",
        "label": "Pendente",
    },
    "cancelled": {
        "bg": "#ef4444",
        "bg_light": "#fee2e2",
        "text": "#991b1b",
        "icon": "❌",
        "label": "Cancelada",
    },
}

# ============================================
# CONFIGURAÇÃO DE GRÁFICOS PLOTLY
# ============================================

PLOTLY_LAYOUT = {
    "font": {
        "family": '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        "size": 13,
        "color": COLORS["neutral_700"],
    },
    "title": {
        "font": {
            "size": 16,
            "weight": "600",
            "color": COLORS["neutral_900"],
        },
        "x": 0.05,
        "y": 0.95,
    },
    "plot_bgcolor": "#ffffff",
    "paper_bgcolor": "#ffffff",
    "hovermode": "closest",
    "showlegend": True,
    "legend": {
        "orientation": "h",
        "y": -0.15,
        "x": 0,
        "font": {
            "size": 11,
        },
    },
    "margin": {
        "l": 60,
        "r": 30,
        "t": 60,
        "b": 60,
    },
}

# ============================================
# CONFIGURAÇÃO DARK MODE
# ============================================

DARK_COLORS = {
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_card": "#1e293b",
    "text_primary": "#f1f5f9",
    "text_secondary": "#cbd5e1",
    "border": "#334155",
}

DARK_PLOTLY_LAYOUT = {
    "font": {
        "color": DARK_COLORS["text_primary"],
    },
    "title": {
        "font": {
            "color": DARK_COLORS["text_primary"],
        },
    },
    "plot_bgcolor": DARK_COLORS["bg_secondary"],
    "paper_bgcolor": DARK_COLORS["bg_primary"],
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_status_color(status: str, dark: bool = False) -> Dict[str, str]:
    """
    Retorna cores para um status específico.

    Args:
        status: Status da entrega
        dark: Se True, ajusta para dark mode

    Returns:
        Dict com bg, bg_light, text, icon, label
    """
    color = STATUS_COLORS.get(status.lower(), STATUS_COLORS["pending"])
    if dark:
        # Ajustar contraste para dark mode
        return {
            **color,
            "bg_light": color["bg"],
        }
    return color


def get_categorical_scale(num_colors: int = None) -> List[str]:
    """
    Retorna escala categórica com número específico de cores.

    Args:
        num_colors: Número de cores necessárias

    Returns:
        Lista de cores hex
    """
    if num_colors is None or num_colors >= len(CATEGORICAL_COLORS):
        return CATEGORICAL_COLORS

    # Distribuir cores uniformemente
    step = len(CATEGORICAL_COLORS) / num_colors
    return [CATEGORICAL_COLORS[int(i * step) % len(CATEGORICAL_COLORS)] for i in range(num_colors)]


def get_gradient(gradient_name: str) -> str:
    """
    Retorna definição de gradiente por nome.

    Args:
        gradient_name: Nome do gradiente

    Returns:
        String CSS do gradiente
    """
    return GRADIENTS.get(gradient_name.lower(), GRADIENTS["primary"])


def get_shadow(shadow_size: str) -> str:
    """
    Retorna definição de sombra por tamanho.

    Args:
        shadow_size: xs, sm, md, lg, xl, inner

    Returns:
        String CSS da shadow
    """
    return SHADOWS.get(shadow_size.lower(), SHADOWS["md"])