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
HEATMAP_BLUE_SCALE = ["#FFFFFF", "#E6EEF5", "#D0DFEC", "#ABC6DD", "#7CA6C9", "#4D83AE", "#123552"]

PRIMARY_FONT = "'Space Grotesk', 'Inter', system-ui, -apple-system, sans-serif"
SECONDARY_FONT = "'Inter', system-ui, -apple-system, sans-serif"
BACKGROUND_COLOR = "#f5f8fb"
TEXT_COLOR = "#123552"
MUTED_TEXT_COLOR = "#5b6e80"
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
