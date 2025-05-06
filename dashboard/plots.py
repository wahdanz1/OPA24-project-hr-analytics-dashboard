import plotly.express as px

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data,**kwargs ):
                                
    x_value = kwargs.pop("x_value", "distinct_occupations")
    y_value = kwargs.pop("y_value", "workplace_municipality")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "Distinct Occupations per Municipality")
    is_horizontal = kwargs.pop("is_horizontal", True)
    title = kwargs.pop("title", "Distinct Occupations per Municipality")
    color_collumn = kwargs.pop("color_collumn", "distinct_occupations")
    margin = kwargs.pop("margin", dict(l=50, r=50, t=50, b=40))
    color_gradient = kwargs.pop("color_gradient", px.colors.diverging.Spectral)

    fig = px.bar(
        data,
        x=x_value,
        y=y_value,
        orientation="h" if is_horizontal else "v",
        labels={
            x_value: x_label,
            y_value: y_label
        },
        title=title,
        color=color_collumn,
        color_continuous_scale=color_gradient,
        **kwargs
    )

    fig.update_layout(
        margin=margin,
        yaxis_title=None,
        title_x=0.0,
    )

    fig.update_traces(
        text=data[x_value],
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