import plotly.express as px

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data,**kwargs):
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

# Create a vertical bar chart using Plotly
def create_vertical_bar_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "workplace_city")
    y_value = kwargs.pop("y_value", "job_ad_count")
    x_label = kwargs.pop("x_label", "City")
    y_label = kwargs.pop("y_label", "Number of job ads")
    title = kwargs.pop("title", "Top 3 Occupations per City")
    color_column = kwargs.pop("color_column", "occupation")
    margin = kwargs.pop("margin", dict(l=50, r=50, t=50, b=40))

    fig = px.bar(
        data,
        x=x_value,
        y=y_value,
        labels={
            x_value: x_label,
            y_value: y_label
        },
        title=title,
        color=color_column,
        **kwargs
    )

    fig.update_layout(
        height=max(300, len(data[x_value].unique()) * 40),
        margin=margin,
        yaxis_title=None,
        xaxis_tickangle=-45,
        title_x=0.0,
    )

    fig.update_yaxes(
        autorange=True,
        range=[-4,4],
        )

    return fig

# Create a line chart using Plotly
def create_line_chart(data ,**kwargs):
    x_value = kwargs.pop("x_value", "week")
    y_value = kwargs.pop("y_value", "distinct_occupations")
    x_label = kwargs.pop("x_label", "Week")
    y_label = kwargs.pop("y_label", "Distinct Occupations")
    title = kwargs.pop("title", "Distinct Occupations per Municipality (Over Time)")
    color_column = kwargs.pop("color_column", "workplace_municipality")
    

    fig = px.line(
        data,
        x=x_value,
        y=y_value,
        labels={
            x_value: x_label,
            y_value: y_label

        },
        title=title,
        color=color_column,
    )

    return fig
