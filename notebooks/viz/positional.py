"""Interactive sinusoidal positional encoding explorer."""

from __future__ import annotations

import numpy as np
from ipywidgets import HTML, VBox

from ._live import live_view


def sinusoidal_pe(seq_len: int, d_model: int) -> np.ndarray:
    """Classic Attention-Is-All-You-Need sinusoidal positional encoding."""
    position = np.arange(seq_len)[:, None]
    div_term = np.exp(np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return pe


def interactive_positional_encoding(d_model: int = 32, max_len: int = 64) -> VBox:
    """Sliders for position / dimension; show PE heatmap and a single wave."""
    view = live_view(
        "positional",
        {"maxLen": int(max_len), "dModel": int(d_model)},
        [
            {"name": "pos", "label": "位置", "min": 0, "max": max_len - 1, "step": 1, "value": 0, "digits": 0},
            {"name": "dim", "label": "维度", "min": 0, "max": d_model - 1, "step": 1, "value": 0, "digits": 0},
        ],
    )
    hint = HTML(
        value=(
            "<b>拖什么：</b> 位置 / 维度 &nbsp;|&nbsp; "
            "<b>看什么：</b> 不同位置有独特“指纹”；相邻位置编码更相似。"
            "真正模型里 PE 会加到词向量上。"
        )
    )
    return VBox([hint, view])
