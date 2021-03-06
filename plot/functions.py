"""Plotting and visualization tools."""
# stdlib
import logging
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

# external
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

LOG = logging.getLogger(__name__)


def style_to_matplotlib(fig) -> go.Figure:
    """Style a plotly figure as a matplotlib figure.

    Args:
        fig: Plotly figure object to be styled.

    """
    fig_styled = go.Figure(fig)

    # choose the figure font
    font_dict = dict(family="Arial", size=26, color="black")

    # general figure formatting
    fig_styled.update_layout(
        font=font_dict,  # font formatting
        plot_bgcolor="white",  # background color
        width=850,  # figure width
        height=700,  # figure height
        margin=dict(r=20, t=20, b=10),  # remove white space
    )

    # x and y-axis formatting
    fig_styled.update_yaxes(
        showline=True,  # add line at x=0
        linecolor="black",  # line color
        linewidth=2.4,  # line size
        ticks="outside",  # ticks outside axis
        tickfont=font_dict,  # tick label font
        mirror="allticks",  # add ticks to top/right axes
        tickwidth=2.4,  # tick width
        tickcolor="black",  # tick color
    )

    fig_styled.update_xaxes(
        showline=True,
        showticklabels=True,
        linecolor="black",
        linewidth=2.4,
        ticks="outside",
        tickfont=font_dict,
        mirror="allticks",
        tickwidth=2.4,
        tickcolor="black",
    )

    return fig_styled


def line(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    fc: str = None,
    fr: str = None,
    x_error: str = None,
    y_error: str = None,
    markers: bool = False,
    title: str = None,
    show: bool = False,
    dark: bool = False,
):
    """Plots a line plot.

    Supports up to 4D data.
    Will show plot in browser window when called. Supports plotting of multiple traces
    on the same figure. Axis and legend labels are taken from column names. LaTeX
    directives for rendering mathematical notation are enabled by encapsulating strings
    in dollar signs: "$...$". It is recommened to avoid writing LaTeX when using facets,
    as the value of the variable at the facets will not be rendered. Only supports one
    set of error data across all traces.
    Args:
        df: dataframe containing x and y data down columns.
        x: column name to treat as x coordinates of trace(s).
        y: column name(s) to treat as y coordinates of trace(s).
        fc: column name to treat as facet column of trace(s).
        fr: column name to treat as facet row of trace(s).
        x_error: column name to treat as x error of trace(s) for plotting horizontal error bars.
        y_error: column name to treat as y error of trace(s) for plotting vertical error bars.
        markers: whether to plot markers on data points.
        title: title of plot.
        show: whether to show plot.
        dark: plot in dark mode.
    Returns:
        figure object.

    """

    template = "plotly_dark" if dark else "plotly"

    fig = px.line(
        data_frame=df,
        x=x,
        y=y,
        title=title,
        error_x=x_error,
        error_y=y_error,
        markers=markers,
        facet_col=fc,
        facet_row=fr,
        template=template,
    )

    if show:
        fig.show()

    return fig


def scatter(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    c: str = None,
    s: str = None,
    m: str = None,
    fc: str = None,
    fr: str = None,
    x_error: str = None,
    y_error: str = None,
    title: str = None,
    show: bool = False,
):
    """Plots a scatter plot. Supports up to 7D data.

    Will show plot in browser window when called. Supports plotting of multiple traces
    on the same figure. Axis and legend labels are taken from column names. LaTeX
    directives for rendering mathematical notation are enabled by encapsulating strings
    in dollar signs: "$...$". It is recommened to avoid writing LaTeX when using facets,
    as the value of the variable at the facets will not be rendered. Only supports one
    set of error data across all traces.

    Args:
        df: dataframe containing x and y data down columns.
        x: column name to treat as x coordinates of trace(s).
        y: column name(s) to treat as y coordinates of trace(s).
        c: column name to treat as color of trace(s).
        s: column name to treat as size of trace(s). Does not map negative values.
        m: column name to treat as marker symbol of trace(s).
        fc: column name to treat as facet column of trace(s).
        fr: column name to treat as facet row of trace(s).
        x_error: column name to treat as x error of trace(s) for plotting horizontal error bars.
        y_error: column name to treat as y error of trace(s) for plotting vertical error bars.
        show: whether to show plot.
        title: title of plot.

    Returns:
        figure object.

    """

    fig = px.scatter(
        data_frame=df,
        x=x,
        y=y,
        color=c,
        symbol=m,
        size=s,
        title=title,
        error_x=x_error,
        error_y=y_error,
        facet_col=fc,
        facet_row=fr,
    )

    if show:
        fig.show()

    return fig


def scatter3(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str | list[str],
    c: str = None,
    s: str = None,
    m: str = None,
    x_error: str = None,
    y_error: str = None,
    z_error: str = None,
    title: str = None,
    show: bool = False,
):
    """Plots 3D scatter plot. Supports up to 6D data.

    Args:
        df: dataframe containing x and y data down columns.
        x: column name to treat as x coordinates of trace(s).
        y: column name(s) to treat as y coordinates of trace(s).
        z: column name to treat as z coordinates of trace(s).
        c: column name to treat as color of trace(s).
        s: column name to treat as size of trace(s). Does not map negative values.
        m: column name to treat as marker symbol of trace(s).
        x_error: column name to treat as x error of trace(s).
        y_error: column name to treat as y error of trace(s).
        z_error: column name to treat as z error of trace(s).
        title: title of plot.
        show: whether to show plot.

    Returns:
        figure object.

    """
    fig = px.scatter_3d(
        data_frame=df,
        x=x,
        y=y,
        z=z,
        color=c,
        symbol=m,
        size=s,
        title=title,
        error_x=x_error,
        error_y=y_error,
        error_z=z_error,
    )

    if show:
        fig.show()

    return fig


def surface(
    x: Iterable,
    y: Iterable,
    z: Iterable[float, float],
    title: str = None,
    title_x: str = None,
    title_y: str = None,
    title_z: str = None,
    show: bool = False,
):
    """Plots surface data. Supports up to 3D data.

    Args:
        x: x-coordinate data.
        y: y-coordinate data.
        z: z-coordinate data array.
        title: title of plot.
        title_x: title of x-axis.
        title_y: title of y-axis.
        title_z: title of z-axis.
        show: whether to show plot.

    Returns:
        figure object.

    """
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    fig.update_traces(
        contours_z=dict(
            show=True, usecolormap=True, highlightcolor="limegreen", project_z=True
        )
    )
    fig.update_layout(
        title=title,
        scene=dict(xaxis_title=title_x, yaxis_title=title_y, zaxis_title=title_z),
    )

    if show:
        fig.show()

    return fig


def save(fig, name: str, path: Path):
    """Saves figure as an HTML to the output path.

    Args:
        fig: figure object.
        name: file name without extensions.
        path: directory in which to save the figure.

    Returns:
        Saved filepath.

    """
    path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    filepath = path / f"{name}_{timestamp}.html"

    fig.write_html(filepath, include_mathjax="cdn")

    LOG.info(f"Saved figure to {filepath}")

    return filepath
