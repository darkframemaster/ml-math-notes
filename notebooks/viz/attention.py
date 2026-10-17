"""Interactive attention explorers: token picker, QK heatmap, softmax temp."""

from __future__ import annotations

import numpy as np
import torch
from ipywidgets import HTML, VBox

from ._live import live_view

# Re-export softmax interactive for notebook convenience
from .softmax import interactive_softmax_temperature  # noqa: F401


def _toy_attention_weights(tokens: list[str], seed: int = 0) -> np.ndarray:
    """Build a plausible educational attention matrix for a short sentence."""
    rng = np.random.default_rng(seed)
    n = len(tokens)
    scores = rng.normal(0, 0.4, size=(n, n))
    for i in range(n):
        for j in range(n):
            scores[i, j] += 1.2 * np.exp(-0.35 * abs(i - j))
            if tokens[j].lower() in {"the", "a", "an", ",", ".", "of", "to"}:
                scores[i, j] -= 0.6
            if tokens[i].lower() == tokens[j].lower() and i != j:
                scores[i, j] += 0.5
    scores = scores - scores.max(axis=1, keepdims=True)
    weights = np.exp(scores)
    weights = weights / weights.sum(axis=1, keepdims=True)
    return weights


def interactive_attention_explorer(
    sentence: str = "The cat sat on the mat",
    tokens: list[str] | None = None,
    weights: np.ndarray | None = None,
) -> VBox:
    """Pick a query token; show attention bars over keys."""
    if tokens is None:
        tokens = sentence.split()
    if weights is None:
        weights = _toy_attention_weights(tokens)
    weights = np.asarray(weights, dtype=float)
    view = live_view(
        "attention",
        {"tokens": list(tokens), "weights": weights.tolist()},
        [
            {
                "type": "select",
                "name": "query",
                "label": "Query",
                "value": 0,
                "options": [{"label": f"{i}: {tok}", "value": i} for i, tok in enumerate(tokens)],
            }
        ],
    )
    hint = HTML(
        value=(
            "<b>点什么：</b> 下拉选择 query &nbsp;|&nbsp; "
            "<b>看什么：</b> 柱状图是“软查找”结果；热力图是所有 query 的汇总。"
            "真正的 Transformer 里这些权重由 Q·K 算出来。"
        )
    )
    return VBox([hint, view])


def interactive_qk_heatmap(
    tokens: list[str] | None = None,
    d_k: int = 8,
    seed: int = 2,
) -> VBox:
    """Show QK^T / sqrt(d_k) heatmap with optional causal mask."""
    if tokens is None:
        tokens = ["The", "cat", "sat", "on", "mat"]
    rng = np.random.default_rng(seed)
    n = len(tokens)
    q = rng.normal(0, 1, size=(n, d_k))
    k = rng.normal(0, 1, size=(n, d_k))
    scores = (q @ k.T) / np.sqrt(d_k)
    view = live_view(
        "qk",
        {"tokens": list(tokens), "scores": scores.tolist()},
        [{"type": "checkbox", "name": "causal", "label": "因果 mask", "value": False}],
    )
    hint = HTML(
        value=(
            "<b>勾什么：</b> 因果 mask（decoder 用）&nbsp;|&nbsp; "
            "<b>看什么：</b> mask 后未来位置变成空，softmax 后权重为 0——"
            "模型不能偷看未来词。"
        )
    )
    return VBox([hint, view])


@torch.no_grad()
def attention_from_hf_model(
    text: str = "The cat sat on the mat",
    model_name: str = "distilbert-base-uncased",
    layer: int = 0,
    head: int = 0,
) -> tuple[list[str], np.ndarray]:
    """Extract one head's attention from a small HF encoder model."""
    from transformers import AutoModel, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, output_attentions=True)
    model.eval()
    encoded = tok(text, return_tensors="pt")
    outputs = model(**encoded)
    att = outputs.attentions[layer][0, head].cpu().numpy()
    tokens = tok.convert_ids_to_tokens(encoded["input_ids"][0])
    return tokens, att
