"""FigureWidget helpers.

Plotly's incremental restyle messages often never reach the JupyterLab frontend
(the slider moves, the figure stays on the first frame). Rebuild the figure and
put it in an Output so each interaction sends a complete widget.
"""

from __future__ import annotations

import plotly.graph_objects as go
from IPython.display import clear_output, display
from ipywidgets import Output


def make_figure(*args, **kwargs):
    """Return a FigureWidget. Data should already be JSON-friendly lists."""
    return go.FigureWidget(*args, **kwargs)


def show_figure(out: Output, fig) -> None:
    """Replace the contents of an Output with one complete figure."""
    with out:
        clear_output(wait=True)
        display(fig)


def is_figure_widget(fig) -> bool:
    return fig.__class__.__name__ == "FigureWidget"
