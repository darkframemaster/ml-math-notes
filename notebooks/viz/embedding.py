"""Interactive word embedding space visualization."""

from __future__ import annotations

import numpy as np
from ipywidgets import HTML, VBox

from ._live import live_view


def interactive_embedding_space() -> VBox:
    """Hand-crafted 3D word vectors with analogy button (king - man + woman)."""
    words = {
        "king": [0.9, 0.85, 0.2],
        "queen": [0.88, 0.2, 0.82],
        "man": [0.75, 0.8, 0.15],
        "woman": [0.72, 0.18, 0.78],
        "prince": [0.7, 0.75, 0.25],
        "princess": [0.68, 0.22, 0.72],
        "apple": [-0.7, -0.2, 0.1],
        "orange": [-0.65, -0.15, 0.25],
        "car": [-0.2, 0.7, -0.6],
        "bus": [-0.15, 0.65, -0.55],
    }
    view = live_view(
        "embedding",
        {"labels": list(words), "points": list(words.values())},
        [
            {"type": "button", "name": "analogy", "label": "运行 king−man+woman"},
            {"type": "button", "name": "clear", "label": "清除"},
        ],
    )
    hint = HTML(
        value=(
            "<b>做什么：</b> 拖动旋转散点；点按钮看向量加减。&nbsp;|&nbsp; "
            "<b>看什么：</b> 皇室词聚在一起，水果和交通工具是另一簇。"
        )
    )
    return VBox([hint, view])


def one_hot_vs_embedding_demo(vocab: list[str] | None = None) -> None:
    """Print a tiny comparison table for one-hot vs dense embedding."""
    if vocab is None:
        vocab = ["cat", "dog", "car"]
    n = len(vocab)
    print("One-hot（稀疏、任意两词正交，看不出相似性）：")
    eye = np.eye(n)
    for word, row in zip(vocab, eye):
        print(f"  {word:4s} -> {row.astype(int).tolist()}")
    print("\nEmbedding（稠密、可学习；相似词可有相近方向）：")
    rng = np.random.default_rng(1)
    emb = rng.normal(0, 0.5, size=(n, 4)).round(2)
    for word, row in zip(vocab, emb):
        print(f"  {word:4s} -> {row.tolist()}")
