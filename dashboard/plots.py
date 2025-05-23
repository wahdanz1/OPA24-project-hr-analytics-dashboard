import plotly.express as px

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "")
    y_value = kwargs.pop("y_value", "")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "")
    title = kwargs.pop("title", "")
    color_column = kwargs.pop("color_column", "")
    margin = kwargs.pop("margin", dict(l=0, r=0, t=0, b=0))
    color_gradient = kwargs.pop("color_gradient", px.colors.diverging.Spectral)
    hover_template = kwargs.pop("hover_template", "")

    fig = px.bar(
        data,
        x=x_value,
        y=y_value,
        orientation="h",
        labels={
            x_value: x_label,
            y_value: y_label
        },
        title=title,
        color=color_column,
        **kwargs
    )

    fig.update_layout(
        margin=margin,
        yaxis_title=None,
        title_x=0.0,
            title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=20)
        ),
    )

    fig.update_traces(
        textposition="auto",
        insidetextanchor="end",
        textfont=dict(size=14),
        hovertemplate=hover_template,
    )

    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)

    return fig

# Create a vertical bar chart using Plotly
def create_vertical_bar_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "")
    y_value = kwargs.pop("y_value", "")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "")
    title = kwargs.pop("title", "")
    color_column = kwargs.pop("color_column", "")
    margin = kwargs.pop("margin", dict(l=50, r=50, t=50, b=40))
    showticklabels = kwargs.pop("showticklabels", True)
    barmode = kwargs.pop("barmode", "stack")
    textangle = kwargs.pop("textangle", 0)
    hover_template = kwargs.pop("hover_template", "")

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
        barmode=barmode,
        **kwargs
    )

    fig.update_layout(
        margin=margin,
        title_x=0.0,
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=20)
        ),
    )

    fig.update_yaxes(
        showticklabels=showticklabels,
        )
    
    fig.update_traces(
        textangle = textangle,
    )

    return fig

# Create a line chart using Plotly
def create_line_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "")
    y_value = kwargs.pop("y_value", "")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "")
    title = kwargs.pop("title", "")
    color_column = kwargs.pop("color_column", "")
    

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
        **kwargs
    )

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=20)
        ),
    )

    return fig
