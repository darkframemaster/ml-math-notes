"""Softmax temperature interactive bar chart."""

from __future__ import annotations

from ipywidgets import HTML, VBox

from ._live import live_view


def interactive_softmax_temperature(logits: list[float] | None = None) -> VBox:
    """Temperature slider: probabilities sharpen (cold) or flatten (hot)."""
    if logits is None:
        logits = [2.0, 1.0, 0.2, -0.5, -1.2]
    view = live_view(
        "softmax",
        {
            "logits": [float(v) for v in logits],
            "labels": [f"选项 {i}" for i in range(len(logits))],
        },
        [
            {
                "name": "temperature",
                "label": "温度 T",
                "min": 0.15,
                "max": 5,
                "step": 0.05,
                "value": 1,
            }
        ],
    )
    hint = HTML(
        value=(
            "<b>拖什么：</b> 温度 T &nbsp;|&nbsp; "
            "<b>看什么：</b> T 越小分布越“自信”（尖）；T 越大越平均。"
            "注意力权重就是对分数做 softmax。"
        )
    )
    return VBox([hint, view])
