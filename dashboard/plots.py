import plotly.express as px

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data):
    fig = px.bar(
        data,
        x="distinct_occupations",
        y="workplace_municipality",
        orientation="h",
        labels={
            "workplace_municipality": "",
            "distinct_occupations": "Number of distinct occupations"
        },
        title="Distinct Occupations per Municipality",
        color="distinct_occupations",
        color_continuous_scale=px.colors.diverging.Spectral,
    )

    fig.update_layout(
        margin=dict(l=50, r=50, t=50, b=40),
        yaxis_title=None,
        title_x=0.0,
    )

    fig.update_traces(
        text=data["distinct_occupations"],
        textposition="auto",
        insidetextanchor="end",
        textfont=dict(size=12),
        hovertemplate="%{y} has %{x} distinct occupations",
    )

    return fig