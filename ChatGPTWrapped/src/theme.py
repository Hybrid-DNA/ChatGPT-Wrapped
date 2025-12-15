DATA_COLORS = ["#418AB3", "#A6B727", "#F69200", "#123552", "#FEC306", "#DF5327", "#9D44B5", "#6E0D25"]

PRIMARY_FONT = "Georgia, 'Times New Roman', Times, serif"
SECONDARY_FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
BACKGROUND_COLOR = "#ffffff"
TEXT_COLOR = "#0b0b0b"
MUTED_TEXT_COLOR = "#2f3640"
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
