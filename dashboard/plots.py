import plotly.express as px
import plotly.graph_objects as go
import textwrap

COLOR_PALETTE = px.colors.qualitative.Plotly

# Create a horizontal bar chart using Plotly
def create_horizontal_bar_chart(data,**kwargs):
    x_value = kwargs.pop("x_value", "")
    y_value = kwargs.pop("y_value", "")
    x_label = kwargs.pop("x_label", "")
    y_label = kwargs.pop("y_label", "")
    title = kwargs.pop("title", "")
    color_column = kwargs.pop("color_column", y_value)
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
        color_discrete_sequence=COLOR_PALETTE,
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
        uniformtext_mode='hide',
        showlegend=False,
    )

    fig.update_traces(
        textposition="auto",
        insidetextanchor="end",
        textfont=dict(size=14),
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
    color_column = kwargs.pop("color_column", y_value)
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
        color_discrete_sequence=COLOR_PALETTE,
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
        uniformtext_mode='hide',
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
    color_column = kwargs.pop("color_column", y_value)

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
        color_discrete_sequence=COLOR_PALETTE,
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
    color = kwargs.pop("color", names)

    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title,
        color=color,
        color_discrete_sequence=COLOR_PALETTE,
        **kwargs
    )

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        title=title,
        uniformtext_minsize=16,
        uniformtext_mode='hide',
        )

    return fig

# Create a marimekko chart using plotly (graph objects)
def create_marimekko_chart(data, municipality_labels):
    import numpy as np

    # 1. Generate consistent color map
    occupation_groups = (
        data.groupby("occupation_group")["total_vacancies"]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    color_map = {
        group: COLOR_PALETTE[i % len(COLOR_PALETTE)]
        for i, group in enumerate(occupation_groups)
    }

    # 2. Get unique municipalities with their widths and x positions
    x_positions = data[['workplace_municipality', 'x_base', 'width']].drop_duplicates()
    x_lookup = x_positions.set_index('workplace_municipality')[['x_base', 'width']].to_dict(orient='index')

    # 3. Build dictionary of y values per occupation group, per municipality
    plot_data = {group: [] for group in occupation_groups}
    for municipality in municipality_labels['workplace_municipality']:
        group_heights = data[data['workplace_municipality'] == municipality].set_index('occupation_group')['height'].to_dict()
        for group in occupation_groups:
            plot_data[group].append(group_heights.get(group, 0))

    # 4. Plot one trace per occupation group
    fig = go.Figure()
    for group in occupation_groups:
        fig.add_trace(go.Bar(
            name=group,
            y=plot_data[group],
            x=[x_lookup[muni]['x_base'] for muni in municipality_labels['workplace_municipality']],
            width=[x_lookup[muni]['width'] for muni in municipality_labels['workplace_municipality']],
            offset=0,
            marker=dict(
                color=color_map[group],
                line=dict(width=0.5, color='rgb(38, 39, 48)')
            ),
            marker_color=color_map[group],
            texttemplate="%{y:.1%}",
            textposition="inside",
            textangle=0,
            hovertemplate="<b>%{text}</b><extra></extra>",
            text=[group]*len(municipality_labels),
            legendgroup=group,
        ))

    fig.update_layout(
        barmode='stack',
        title='Top Occupation Groups per Municipality',
        xaxis=dict(
            title='Municipality (Width = Total Vacancies)',
            tickmode='array',
            tickvals=municipality_labels['x_center'],
            ticktext=municipality_labels['workplace_municipality'],
            tickangle=-45
        ),
        yaxis=dict(title='Share of Municipality Vacancies', tickformat=".0%"),
        height=500,
        margin=dict(l=40, r=40, t=60, b=80),
        uniformtext=dict(mode="hide", minsize=10),
    )

    return fig
