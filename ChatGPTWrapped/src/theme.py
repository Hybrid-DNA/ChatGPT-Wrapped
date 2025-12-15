DATA_COLORS = [
    "#418AB3",
    "#A6B727",
    "#F69200",
    "#123552",
    "#FEC306",
    "#DF5327",
    "#9D44B5",
    "#6E0D25",
]
# Used for time-of-day heatmaps to provide a single-color gradient from white to deep blue.
HEATMAP_BLUE_SCALE = ["#FFFFFF", "#E8F0FB", "#D7E5FA", "#B6CFF6", "#8FB5EF", "#5E90E6", "#1D4ED8"]

GOOD_COLOR = "#A6B727"
BAD_COLOR = "#DF5327"
NEUTRAL_COLOR = "#FEC306"

PRIMARY_FONT = "'Segoe UI', system-ui, -apple-system, sans-serif"
SECONDARY_FONT = "'Segoe UI', system-ui, -apple-system, sans-serif"
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
