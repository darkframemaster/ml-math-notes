"""3b1b-style interactive single-neuron decision boundary."""

from __future__ import annotations

import numpy as np
from ipywidgets import HTML, VBox

from ._live import live_view


def interactive_neuron_boundary() -> VBox:
    """Drag weights/bias and watch a linear decision boundary move in 2D."""
    rng = np.random.default_rng(0)
    class0 = rng.normal([-1.2, -0.8], 0.55, size=(80, 2))
    class1 = rng.normal([1.1, 0.9], 0.55, size=(80, 2))
    xs = np.concatenate([class0, class1], axis=0)
    ys = np.array([0] * len(class0) + [1] * len(class1))
    view = live_view(
        "neuron",
        {
            "x0": xs[ys == 0, 0].tolist(),
            "y0": xs[ys == 0, 1].tolist(),
            "x1": xs[ys == 1, 0].tolist(),
            "y1": xs[ys == 1, 1].tolist(),
        },
        [
            {"name": "w1", "label": "w1", "min": -3, "max": 3, "step": 0.05, "value": 1.2},
            {"name": "w2", "label": "w2", "min": -3, "max": 3, "step": 0.05, "value": 1.0},
            {"name": "bias", "label": "bias", "min": -3, "max": 3, "step": 0.05, "value": 0.0},
        ],
    )
    hint = HTML(
        value=(
            "<b>拖什么：</b> w1 / w2 / bias，拖动时图会跟着动 &nbsp;|&nbsp; "
            "<b>看什么：</b> 红线是 <code>w·x + b = 0</code>；"
            "改变权重相当于旋转/平移这把“刀”。"
        )
    )
    return VBox([hint, view])
