"""Gradient descent playground and mini-GPT training plot helpers."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import torch
import torch.nn as nn
from IPython.display import display
from ipywidgets import HTML, Output, VBox

from ._live import live_view
from ._plotly_widget import show_figure


def interactive_gradient_descent() -> VBox:
    """2D bowl loss; step / autoplay a point downhill with adjustable LR."""

    def loss_fn(x: float, y: float) -> float:
        return (x - 1.2) ** 2 + 0.4 * (y + 0.8) ** 2 + 0.15 * np.sin(3 * x) * np.cos(2 * y)

    grid = np.linspace(-2.5, 3.5, 80)
    xx, yy = np.meshgrid(grid, grid)
    zz = loss_fn(xx, yy)
    view = live_view(
        "descent",
        {"grid": grid.tolist(), "zz": zz.tolist()},
        [
            {"name": "lr", "label": "学习率", "min": 0.01, "max": 0.5, "step": 0.01, "value": 0.15},
            {"type": "button", "name": "step", "label": "单步"},
            {"type": "button", "name": "play", "label": "自动播放"},
            {"type": "button", "name": "stop", "label": "停止"},
            {"type": "button", "name": "reset", "label": "重置"},
        ],
    )

    hint = HTML(
        value=(
            "<b>拖什么：</b> 学习率 &nbsp;|&nbsp; "
            "<b>点什么：</b> 单步 / 自动播放 &nbsp;|&nbsp; "
            "<b>看什么：</b> 红点沿梯度反方向走向低谷；学习率过大可能震荡。"
        )
    )
    return VBox([hint, view])


class MiniGPT(nn.Module):
    """Tiny character-level GPT for teaching (decoder-only)."""

    def __init__(
        self,
        vocab_size: int,
        n_embd: int = 64,
        n_head: int = 4,
        n_layer: int = 2,
        block_size: int = 32,
    ) -> None:
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.blocks = nn.ModuleList(
            [_DecoderBlock(n_embd, n_head, block_size) for _ in range(n_layer)]
        )
        self.ln_f = nn.LayerNorm(n_embd)
        self.head = nn.Linear(n_embd, vocab_size, bias=False)

    def forward(self, idx: torch.Tensor) -> torch.Tensor:
        _b, t = idx.shape
        pos = torch.arange(t, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.head(x)

    @torch.no_grad()
    def generate(self, idx: torch.Tensor, max_new_tokens: int) -> torch.Tensor:
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size :]
            logits = self(idx_cond)
            logits = logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_id], dim=1)
        return idx


class _DecoderBlock(nn.Module):
    def __init__(self, n_embd: int, n_head: int, block_size: int) -> None:
        super().__init__()
        assert n_embd % n_head == 0
        self.n_head = n_head
        self.head_dim = n_embd // n_head
        self.qkv = nn.Linear(n_embd, 3 * n_embd)
        self.proj = nn.Linear(n_embd, n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)
        self.ffn = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.GELU(),
            nn.Linear(4 * n_embd, n_embd),
        )
        mask = torch.tril(torch.ones(block_size, block_size))
        self.register_buffer("mask", mask.view(1, 1, block_size, block_size))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, c = x.shape
        h = self.ln1(x)
        qkv = self.qkv(h)
        q, k, v = qkv.split(c, dim=-1)
        q = q.view(b, t, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(b, t, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(b, t, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / (self.head_dim**0.5)
        att = att.masked_fill(self.mask[:, :, :t, :t] == 0, float("-inf"))
        att = torch.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(b, t, c)
        x = x + self.proj(y)
        x = x + self.ffn(self.ln2(x))
        return x


def train_mini_gpt_with_plot(
    text: str | None = None,
    steps: int = 300,
    block_size: int = 32,
    batch_size: int = 32,
    lr: float = 3e-3,
    sample_prompt: str = "The ",
) -> tuple[MiniGPT, dict]:
    """Train a tiny char-GPT and show a live loss + sample panel."""
    if text is None:
        text = (
            "The quick brown fox jumps over the lazy dog. "
            "Transformers learn context by attending to previous tokens. "
            "Attention is a soft lookup over a sequence of vectors. "
            "Small models can still demonstrate next-token prediction. "
        ) * 20

    chars = sorted(set(text))
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for ch, i in stoi.items()}
    data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

    def get_batch() -> tuple[torch.Tensor, torch.Tensor]:
        ix = torch.randint(len(data) - block_size - 1, (batch_size,))
        x = torch.stack([data[i : i + block_size] for i in ix])
        y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
        return x, y

    model = MiniGPT(vocab_size=len(chars), block_size=block_size)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    losses: list[float] = []

    plot_out = Output()
    sample_html = HTML(value="<i>训练开始后这里会显示续写样例…</i>")
    display(VBox([plot_out, sample_html]))

    def _draw_loss(step: int) -> None:
        fig = go.FigureWidget(
            data=[
                go.Scatter(
                    y=list(losses),
                    mode="lines",
                    line=dict(color="#4C78A8"),
                    name="loss",
                )
            ],
            layout=dict(
                title=f"迷你 GPT 训练：step={step}, loss={losses[-1]:.3f}",
                xaxis_title="step",
                yaxis_title="cross-entropy",
                width=720,
                height=360,
                template="plotly_white",
            ),
        )
        show_figure(plot_out, fig)

    model.train()
    for step in range(1, steps + 1):
        xb, yb = get_batch()
        logits = model(xb)
        loss = nn.functional.cross_entropy(logits.view(-1, logits.size(-1)), yb.view(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        losses.append(float(loss.item()))

        if step % 20 == 0 or step == 1:
            _draw_loss(step)
            # sample
            model.eval()
            prompt_ids = torch.tensor(
                [[stoi.get(c, 0) for c in sample_prompt]], dtype=torch.long
            )
            out = model.generate(prompt_ids, max_new_tokens=60)[0].tolist()
            gen = "".join(itos[i] for i in out)
            sample_html.value = f"<b>续写样例</b>（prompt=<code>{sample_prompt}</code>）:<br><pre>{gen}</pre>"
            model.train()

    meta = {"stoi": stoi, "itos": itos, "losses": losses, "chars": chars}
    return model, meta
