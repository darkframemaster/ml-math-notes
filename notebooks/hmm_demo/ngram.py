"""Add-α smoothed n-gram LM for Alice-only generation demos."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np


@dataclass
class NgramLM:
    order: int  # n in n-gram; context length is n-1
    vocab: list[str]
    counts: dict[tuple[str, ...], Counter]
    context_totals: dict[tuple[str, ...], int]
    unigram: np.ndarray
    alpha: float
    unk_token: str
    bos: str
    eos: str

    @property
    def word2i(self) -> dict[str, int]:
        return {w: i for i, w in enumerate(self.vocab)}

    @classmethod
    def train(
        cls,
        sentences: list[list[str]],
        *,
        order: int = 3,
        alpha: float = 0.1,
        min_word_count: int = 2,
        unk_token: str = "<unk>",
        bos: str = "<s>",
        eos: str = "</s>",
    ) -> "NgramLM":
        if order < 1:
            raise ValueError("order must be >= 1")
        word_counts: Counter[str] = Counter()
        for sent in sentences:
            word_counts.update(sent)

        kept = {w for w, c in word_counts.items() if c >= min_word_count}
        vocab = sorted(kept) + [unk_token, bos, eos]
        word2i = {w: i for i, w in enumerate(vocab)}

        def norm(w: str) -> str:
            return w if w in word2i else unk_token

        ctx_len = order - 1
        counts: dict[tuple[str, ...], Counter] = {}
        context_totals: Counter[tuple[str, ...]] = Counter()
        uni = np.zeros(len(vocab), dtype=float)

        for sent in sentences:
            padded = [bos] * ctx_len + [norm(w) for w in sent] + [eos]
            for w in padded[ctx_len:]:
                uni[word2i[w]] += 1
            if order == 1:
                continue
            for i in range(ctx_len, len(padded)):
                w = padded[i]
                # Keep every suffix context so distribution() can really
                # back off from N-1 words to N-2, ..., one word.
                for k in range(1, ctx_len + 1):
                    ctx = tuple(padded[i - k : i])
                    bucket = counts.setdefault(ctx, Counter())
                    bucket[w] += 1
                    context_totals[ctx] += 1

        uni += alpha
        uni /= uni.sum()

        return cls(
            order=order,
            vocab=vocab,
            counts={k: Counter(v) for k, v in counts.items()},
            context_totals=dict(context_totals),
            unigram=uni,
            alpha=alpha,
            unk_token=unk_token,
            bos=bos,
            eos=eos,
        )

    def _norm_word(self, w: str) -> str:
        return w if w in self.word2i else self.unk_token

    def distribution(self, context: list[str]) -> np.ndarray:
        """P(w | context) with add-α; backs off to shorter context then unigram."""
        V = len(self.vocab)
        word2i = self.word2i
        ctx_len = self.order - 1
        ctx = [self._norm_word(w) for w in context[-ctx_len:]] if ctx_len else []

        for k in range(len(ctx), -1, -1):
            if k == 0:
                return self.unigram.copy()
            key = tuple(ctx[-k:])
            total = self.context_totals.get(key, 0)
            bucket = self.counts.get(key)
            if total > 0 and bucket:
                probs = np.full(V, self.alpha, dtype=float)
                for w, c in bucket.items():
                    probs[word2i[w]] += c
                probs /= probs.sum()
                return probs
        return self.unigram.copy()

    def generate_from_prefix(
        self,
        prefix: list[str] | str,
        *,
        length: int,
        rng: np.random.Generator | None = None,
        stop_at_eos: bool = True,
        avoid_special: bool = True,
    ) -> list[str]:
        rng = rng or np.random.default_rng()
        if isinstance(prefix, str):
            prefix = [w for w in prefix.strip().split() if w]
        prefix = [w.lower() for w in prefix]
        if length < len(prefix):
            raise ValueError(f"length={length} 不能短于前缀词数 {len(prefix)}")

        out = list(prefix)
        ctx_len = self.order - 1
        history = ([self.bos] * ctx_len + out)[-max(ctx_len, 1) :] if ctx_len else out

        block = {self.unk_token, self.bos}
        if not stop_at_eos:
            block.add(self.eos)

        while len(out) < length:
            probs = self.distribution(history)
            if avoid_special:
                for tok in block:
                    probs[self.word2i[tok]] = 0.0
                s = probs.sum()
                if s <= 0:
                    probs = self.distribution(history)
                else:
                    probs /= s
            wi = int(rng.choice(len(self.vocab), p=probs))
            w = self.vocab[wi]
            if w == self.eos:
                break
            out.append(w)
            if ctx_len:
                history = (history + [w])[-ctx_len:]
        return out

    def generate_batch(
        self,
        *,
        prefix: list[str] | str = "",
        length: int = 12,
        n: int = 5,
        seed: int | None = 0,
        stop_at_eos: bool = True,
        order_note: bool = False,
    ) -> list[list[str]]:
        del order_note  # API symmetry with callers
        if n <= 0:
            return []
        base = np.random.default_rng(seed)
        seeds = base.integers(0, 2**31 - 1, size=n)
        return [
            self.generate_from_prefix(
                prefix,
                length=length,
                rng=np.random.default_rng(int(s)),
                stop_at_eos=stop_at_eos,
            )
            for s in seeds
        ]
