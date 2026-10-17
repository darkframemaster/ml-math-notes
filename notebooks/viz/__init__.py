"""Interactive visualization helpers for the Transformer deep-dive notebook."""

from .attention import (
    attention_from_hf_model,
    interactive_attention_explorer,
    interactive_qk_heatmap,
)
from .embedding import interactive_embedding_space, one_hot_vs_embedding_demo
from .neuron import interactive_neuron_boundary
from .pipeline_ui import interactive_pipeline_playground
from .positional import interactive_positional_encoding, sinusoidal_pe
from .softmax import interactive_softmax_temperature
from .training import MiniGPT, interactive_gradient_descent, train_mini_gpt_with_plot

__all__ = [
    "interactive_neuron_boundary",
    "interactive_softmax_temperature",
    "interactive_gradient_descent",
    "interactive_embedding_space",
    "one_hot_vs_embedding_demo",
    "interactive_attention_explorer",
    "interactive_qk_heatmap",
    "attention_from_hf_model",
    "interactive_positional_encoding",
    "sinusoidal_pe",
    "interactive_pipeline_playground",
    "train_mini_gpt_with_plot",
    "MiniGPT",
]
