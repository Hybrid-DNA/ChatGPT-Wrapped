DATA_COLORS = [
    "#2563EB",
    "#0EA5E9",
    "#22C55E",
    "#111827",
    "#F59E0B",
    "#F97316",
    "#7C3AED",
    "#14B8A6",
]
# Used for time-of-day heatmaps to provide a single-color gradient from white to deep blue.
HEATMAP_BLUE_SCALE = ["#FFFFFF", "#E8F0FB", "#D7E5FA", "#B6CFF6", "#8FB5EF", "#5E90E6", "#1D4ED8"]

PRIMARY_FONT = "'Lato', system-ui, -apple-system, sans-serif"
SECONDARY_FONT = "'Inter', system-ui, -apple-system, sans-serif"
BACKGROUND_COLOR = "#f8fbff"
TEXT_COLOR = "#0f172a"
MUTED_TEXT_COLOR = "#4b5563"
ACCENT_COLOR = DATA_COLORS[0]


def apply_plotly_theme():
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio

    base_layout = go.Layout(
        font=dict(family=PRIMARY_FONT, color=TEXT_COLOR),
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
    )

    template = go.layout.Template(layout=base_layout)
    pio.templates["chatgpt-wrapped"] = template
    px.defaults.template = "chatgpt-wrapped"
    px.defaults.color_discrete_sequence = DATA_COLORS
    px.defaults.color_continuous_scale = DATA_COLORS
