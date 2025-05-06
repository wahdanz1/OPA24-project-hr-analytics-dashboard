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
        textfont=dict(size=14),
        hovertemplate="%{y} has %{x} distinct occupations",
    )

    return fig

# Create a line chart using Plotly
def create_line_chart(data):
    fig = px.line(
        data,
        x="week",
        y="distinct_occupations",
        labels={
            "week": "Week",
            "workplace_municipality": "Municipality",
            "distinct_occupations": "Distinct occupations"
        },
        title="Distinct Occupations per Municipality (Over Time)",
        color="workplace_municipality",
    )

    return fig