DATA_COLORS = ["#7BD3EA", "#F6C7FF", "#F9E795", "#7E5DEB", "#2E8B9C", "#FF9F66", "#E25C84", "#2F4550"]
# Used for time-of-day heatmaps to provide a single-color gradient from white to deep blue.
HEATMAP_BLUE_SCALE = ["#FFFFFF", "#E5EDFB", "#C7D8F4", "#9DBBEA", "#6B92DC", "#3B5DB7", "#1F2F70"]

PRIMARY_FONT = "'Space Grotesk', 'Inter', system-ui, -apple-system, sans-serif"
SECONDARY_FONT = "'Inter', system-ui, -apple-system, sans-serif"
BACKGROUND_COLOR = "#f7f8fb"
TEXT_COLOR = "#0f172a"
MUTED_TEXT_COLOR = "#525f78"
ACCENT_COLOR = DATA_COLORS[3]


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
