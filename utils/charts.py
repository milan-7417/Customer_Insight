import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Diverse Professional Colors
INDIGO_COLOR = '#4F46E5'
EMERALD_COLOR = '#10B981'
AMBER_COLOR = '#F59E0B'
ROSE_COLOR = '#F43F5E'
SKY_COLOR = '#0EA5E9'
VIOLET_COLOR = '#7C3AED'
ORANGE_COLOR = '#F97316'

COLOR_PALETTE = [INDIGO_COLOR, EMERALD_COLOR, AMBER_COLOR, ROSE_COLOR, SKY_COLOR, ORANGE_COLOR, VIOLET_COLOR, '#9333EA', '#64748B']


def apply_layout_styles(fig, title=None, show_legend=True):
    """Applies common premium styling to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Outfit, sans-serif", size=16, color="#0F172A"),
            x=0.0,
            y=0.98,
            xanchor='left',
            yanchor='top'
        ) if title else None,
        font=dict(family="Outfit, sans-serif", color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50 if title else 15, b=10),
        hovermode="closest",
        legend=dict(
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ) if show_legend else dict(visible=False),
        clickmode='event+select'
    )
    
    # Update axes if they exist in the figure type
    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E8F0",
        tickfont=dict(size=11, family="Outfit, sans-serif"),
        title_font=dict(size=12, color="#64748B", family="Outfit, sans-serif")
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F1F5F9",
        linecolor="#E2E8F0",
        tickfont=dict(size=11, family="Outfit, sans-serif"),
        title_font=dict(size=12, color="#64748B", family="Outfit, sans-serif")
    )
    return fig

def bar_chart(df, x, y, title=None, color=None, barmode='group'):
    """Generates a styled vertical bar chart."""
    if color is None:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=[INDIGO_COLOR], barmode=barmode)
    else:
        fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=COLOR_PALETTE, barmode=barmode)
    
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return apply_layout_styles(fig, title)

def horizontal_bar_chart(df, x, y, title=None, color=None):
    """Generates a styled horizontal bar chart."""
    if color is None:
        fig = px.bar(df, x=x, y=y, orientation='h', color_discrete_sequence=[EMERALD_COLOR])
    else:
        fig = px.bar(df, x=x, y=y, orientation='h', color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(marker_line_width=0, opacity=0.9)
    # Hide the y-grid lines as it's a horizontal bar
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
    return apply_layout_styles(fig, title)

def line_chart(df, x, y, title=None, color=None):
    """Generates a styled line chart."""
    if color is None:
        fig = px.line(df, x=x, y=y, color_discrete_sequence=[VIOLET_COLOR])
    else:
        fig = px.line(df, x=x, y=y, color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(line=dict(width=3.5), marker=dict(size=6, line=dict(width=1)))
    return apply_layout_styles(fig, title)

def area_chart(df, x, y, title=None, color=None):
    """Generates a styled area chart."""
    if color is None:
        fig = px.area(df, x=x, y=y, color_discrete_sequence=[SKY_COLOR])
    else:
        fig = px.area(df, x=x, y=y, color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(line=dict(width=2.5), opacity=0.6)
    return apply_layout_styles(fig, title)

def donut_chart(df, names, values, title=None):
    """Generates a styled donut chart."""
    fig = px.pie(df, names=names, values=values, hole=0.55, color_discrete_sequence=COLOR_PALETTE)
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    return apply_layout_styles(fig, title, show_legend=True)

def pie_chart(df, names, values, title=None):
    """Generates a styled pie chart."""
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=COLOR_PALETTE)
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    return apply_layout_styles(fig, title, show_legend=True)

def scatter_chart(df, x, y, color=None, size=None, title=None):
    """Generates a styled scatter plot."""
    if color is None:
        fig = px.scatter(df, x=x, y=y, size=size, color_discrete_sequence=[INDIGO_COLOR])
    else:
        fig = px.scatter(df, x=x, y=y, size=size, color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(marker=dict(line=dict(width=0.5, color='#FFFFFF'), opacity=0.8))
    return apply_layout_styles(fig, title)

def histogram_chart(df, x, title=None, color=None, nbins=30):
    """Generates a styled histogram chart."""
    if color is None:
        fig = px.histogram(df, x=x, nbins=nbins, color_discrete_sequence=[AMBER_COLOR])
    else:
        fig = px.histogram(df, x=x, nbins=nbins, color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(marker_line_width=0, opacity=0.85)
    return apply_layout_styles(fig, title, show_legend=color is not None)

def box_plot(df, x, y=None, color=None, title=None):
    """Generates a styled box plot."""
    if color is None:
        fig = px.box(df, x=x, y=y, color_discrete_sequence=[ROSE_COLOR])
    else:
        fig = px.box(df, x=x, y=y, color=color, color_discrete_sequence=COLOR_PALETTE)
        
    fig.update_traces(marker_line_width=1, opacity=0.9)
    return apply_layout_styles(fig, title, show_legend=color is not None)

def heatmap_chart(matrix_df, title=None):
    """Generates a styled correlation matrix heatmap."""
    # Drop non-numeric cols if necessary
    numeric_df = matrix_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="Purples",
        labels=dict(color="Correlation")
    )
    
    fig.update_layout(coloraxis_showscale=False)
    # Hide grid for heatmap
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return apply_layout_styles(fig, title, show_legend=False)

def treemap_chart(df, path, values, title=None):
    """Generates a styled treemap chart."""
    fig = px.treemap(
        df,
        path=path,
        values=values,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=2.5)))
    return apply_layout_styles(fig, title, show_legend=False)

def sunburst_chart(df, path, values, title=None):
    """Generates a styled sunburst chart."""
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=1.5)))
    return apply_layout_styles(fig, title, show_legend=False)
