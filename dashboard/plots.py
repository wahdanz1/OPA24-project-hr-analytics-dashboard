import plotly.express as px
import plotly.graph_objects as go

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "")
    y_value = kwargs.pop("y_value", "")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "")
    title = kwargs.pop("title", "")
    color_column = kwargs.pop("color_column", "")
    margin = kwargs.pop("margin", dict(l=0, r=0, t=0, b=0))
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
        uniformtext_minsize=16,
        uniformtext_mode='hide'
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
        uniformtext_minsize=16,
        uniformtext_mode='hide'
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



# Create a pie chart using Plotly
def create_pie_chart(data,**kwargs):
    values = kwargs.pop("values", "")
    names = kwargs.pop("names", "")
    title = kwargs.pop("title", "")

    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title,
        **kwargs
    )

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        title=title,
        uniformtext_minsize=16,
        uniformtext_mode='hide'
        )

    return fig

# Create a marimekko chart using plotly (graph objects)
def create_marimekko_chart(data, municipality_labels):
    fig = go.Figure()

    for _, row in data.iterrows():
        fig.add_trace(go.Bar(
            x=[row['x_base']],
            y=[row['height']],
            width=[row['width']],
            name=row['occupation_group'],
            legendgroup=row['occupation_group'],
            showlegend=not any(
                (trace.name == row['occupation_group']) for trace in fig.data
            ),
            marker=dict(line=dict(width=0)),
            hovertemplate=(
                f"<b>{row['occupation_group']}</b><br>"
                f"Municipality: {row['workplace_municipality']}<br>"
                f"Vacancies: {row['total_vacancies']}<extra></extra>"
            )
        ))

    fig.update_layout(
        barmode='stack',
        title='Top Occupation Groups per Municipality (Marimekko-style)',
        xaxis=dict(
            title='Municipality (Width = Total Vacancies)',
            tickmode='array',
            tickvals=municipality_labels['x_center'],
            ticktext=municipality_labels['workplace_municipality'],
            tickangle=-45
        ),
        yaxis=dict(title='Share of Municipality Vacancies'),
        height=500,
        margin=dict(l=40, r=40, t=60, b=80)
    )

    return fig