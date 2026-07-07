"""Design tokens shared across the app: colors, fonts, and the plotly dark template."""

BG = "#0F172A"
BG_ELEVATED = "#141C33"
CARD_BG = "rgba(255, 255, 255, 0.045)"
CARD_BORDER = "rgba(148, 163, 184, 0.14)"

PRIMARY = "#3B82F6"
SECONDARY = "#06B6D4"
ACCENT_VIOLET = "#8B5CF6"
SUCCESS = "#10B981"
DANGER = "#F87171"
WARNING = "#FBBF24"

TEXT = "#E7ECF5"
TEXT_MUTED = "#8B96AC"
GRID = "rgba(148, 163, 184, 0.09)"

FONT_DISPLAY = "'Manrope', sans-serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"

CATEGORICAL = [PRIMARY, SECONDARY, ACCENT_VIOLET, WARNING, SUCCESS, DANGER, "#F472B6", "#38BDF8"]


def apply_dark_layout(fig, height=380, legend=True):
    """Apply the shared dashboard dark theme to a plotly figure in place.

    No chart sets an actual figure title (titles are the custom HTML
    panel_title/panel_subtitle rendered above each chart) -- so title_font
    is intentionally NOT set here. Setting title_font alone creates a
    layout.title object with a font but no text, which Plotly.js renders
    as the literal word "undefined" where the title would sit. This was
    the actual, systemic cause of "undefined" showing up on every chart.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_BODY, color=TEXT_MUTED, size=12),
        height=height,
        margin=dict(l=8, r=8, t=48, b=8),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color=TEXT_MUTED, size=11),
        ) if legend else dict(visible=False),
        showlegend=legend,
        hoverlabel=dict(
            bgcolor=BG_ELEVATED,
            font=dict(family=FONT_BODY, color=TEXT, size=12),
            bordercolor=CARD_BORDER,
        ),
        colorway=CATEGORICAL,
    )
    fig.update_xaxes(
        gridcolor=GRID, zerolinecolor=GRID, showline=True,
        linecolor=CARD_BORDER, tickfont=dict(color=TEXT_MUTED, size=11),
    )
    fig.update_yaxes(
        gridcolor=GRID, zerolinecolor=GRID, showline=False,
        tickfont=dict(color=TEXT_MUTED, size=11),
    )
    return fig
