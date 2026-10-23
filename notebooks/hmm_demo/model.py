"""Supervised first-order HMM: train (π, A, E), generate, Viterbi decode."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

import numpy as np


@dataclass
class HiddenMarkovModel:
    tags: list[str]
    vocab: list[str]
    pi: np.ndarray  # (K,)
    A: np.ndarray  # (K, K)
    E: np.ndarray  # (K, V)
    unk_index: int

    @property
    def tag2i(self) -> dict[str, int]:
        return {t: i for i, t in enumerate(self.tags)}

    @property
    def word2i(self) -> dict[str, int]:
        return {w: i for i, w in enumerate(self.vocab)}

    @classmethod
    def train(
        cls,
        tagged_sents: list[list[tuple[str, str]]],
        *,
        alpha: float = 0.1,
        unk_token: str = "<unk>",
        min_word_count: int = 2,
    ) -> "HiddenMarkovModel":
        """Estimate π, A, E by counting with add-α smoothing."""
        tag_counts: Counter[str] = Counter()
        start_counts: Counter[str] = Counter()
        trans_counts: Counter[tuple[str, str]] = Counter()
        emit_counts: Counter[tuple[str, str]] = Counter()
        word_counts: Counter[str] = Counter()

        for sent in tagged_sents:
            if not sent:
                continue
            start_counts[sent[0][1]] += 1
            for word, tag in sent:
                tag_counts[tag] += 1
                word_counts[word] += 1
                emit_counts[(tag, word)] += 1
            for (w0, t0), (w1, t1) in zip(sent, sent[1:]):
                trans_counts[(t0, t1)] += 1

        tags = sorted(tag_counts)
        kept_words = {w for w, c in word_counts.items() if c >= min_word_count}
        vocab = sorted(kept_words) + [unk_token]
        tag2i = {t: i for i, t in enumerate(tags)}
        word2i = {w: i for i, w in enumerate(vocab)}
        unk_i = word2i[unk_token]
        K, V = len(tags), len(vocab)

        pi = np.full(K, alpha, dtype=float)
        for t, c in start_counts.items():
            pi[tag2i[t]] += c
        pi /= pi.sum()

        A = np.full((K, K), alpha, dtype=float)
        for (t0, t1), c in trans_counts.items():
            A[tag2i[t0], tag2i[t1]] += c
        A /= A.sum(axis=1, keepdims=True)

        E = np.full((K, V), alpha, dtype=float)
        for (tag, word), c in emit_counts.items():
            wi = word2i.get(word, unk_i)
            E[tag2i[tag], wi] += c
        E /= E.sum(axis=1, keepdims=True)

        return cls(tags=tags, vocab=vocab, pi=pi, A=A, E=E, unk_index=unk_i)

    def _word_index(self, word: str) -> int:
        return self.word2i.get(word, self.unk_index)

    def _sample_word(self, z: int, rng: np.random.Generator, *, avoid_unk: bool) -> int:
        probs = self.E[z].copy()
        if avoid_unk:
            probs[self.unk_index] = 0.0
            s = probs.sum()
            if s <= 0:
                probs = self.E[z].copy()
            else:
                probs /= s
        return int(rng.choice(len(self.vocab), p=probs))

    def generate(
        self,
        n_words: int,
        rng: np.random.Generator | None = None,
        *,
        avoid_unk: bool = True,
    ) -> list[tuple[str, str]]:
        """Sample hidden tags from the Markov chain, then emit words."""
        rng = rng or np.random.default_rng()
        if n_words <= 0:
            return []
        z = int(rng.choice(len(self.tags), p=self.pi))
        out: list[tuple[str, str]] = []
        for _ in range(n_words):
            w = self._sample_word(z, rng, avoid_unk=avoid_unk)
            out.append((self.vocab[w], self.tags[z]))
            z = int(rng.choice(len(self.tags), p=self.A[z]))
        return out

    def generate_from_prefix(
        self,
        prefix: list[str] | str,
        *,
        length: int,
        rng: np.random.Generator | None = None,
        avoid_unk: bool = True,
    ) -> list[tuple[str, str]]:
        """Keep ``prefix`` words fixed, then sample until total ``length`` words.

        Prefix tags come from Viterbi; continuation samples tag transitions and
        emissions from the last prefix tag.
        """
        rng = rng or np.random.default_rng()
        if isinstance(prefix, str):
            prefix = [w for w in prefix.strip().split() if w]
        prefix = [w.lower() for w in prefix]

        if length < len(prefix):
            raise ValueError(f"length={length} 不能短于前缀词数 {len(prefix)}")

        if not prefix:
            return self.generate(length, rng=rng, avoid_unk=avoid_unk)

        tags = self.tag(prefix)
        out = list(zip(prefix, tags))
        z = self.tag2i[tags[-1]]
        for _ in range(length - len(prefix)):
            z = int(rng.choice(len(self.tags), p=self.A[z]))
            w = self._sample_word(z, rng, avoid_unk=avoid_unk)
            out.append((self.vocab[w], self.tags[z]))
        return out

    def generate_batch(
        self,
        *,
        prefix: list[str] | str = "",
        length: int = 12,
        n: int = 5,
        seed: int | None = 0,
        avoid_unk: bool = True,
    ) -> list[list[tuple[str, str]]]:
        """Generate ``n`` sequences with shared prefix / length controls."""
        if n <= 0:
            return []
        base = np.random.default_rng(seed)
        seeds = base.integers(0, 2**31 - 1, size=n)
        return [
            self.generate_from_prefix(
                prefix,
                length=length,
                rng=np.random.default_rng(int(s)),
                avoid_unk=avoid_unk,
            )
            for s in seeds
        ]

    def viterbi(self, words: list[str]) -> tuple[list[str], np.ndarray]:
        """Return best tag path and log-joint δ table."""
        if not words:
            return [], np.zeros((0, len(self.tags)))

        obs = [self._word_index(w) for w in words]
        K = len(self.tags)
        T = len(obs)
        with np.errstate(divide="ignore"):
            log_pi, log_a, log_e = np.log(self.pi), np.log(self.A), np.log(self.E)

        delta = np.full((T, K), -np.inf)
        bp = np.full((T, K), -1, dtype=int)
        delta[0] = log_pi + log_e[:, obs[0]]
        for t in range(1, T):
            cand = delta[t - 1][:, None] + log_a
            bp[t] = np.argmax(cand, axis=0)
            delta[t] = cand[bp[t], np.arange(K)] + log_e[:, obs[t]]

        path_i = [int(np.argmax(delta[-1]))]
        for t in range(T - 1, 0, -1):
            path_i.append(int(bp[t, path_i[-1]]))
        path_i.reverse()
        return [self.tags[i] for i in path_i], delta

    def tag(self, words: list[str]) -> list[str]:
        path, _ = self.viterbi(words)
        return path

    def accuracy(self, tagged_sents: list[list[tuple[str, str]]]) -> float:
        correct = total = 0
        for sent in tagged_sents:
            words = [w for w, _ in sent]
            gold = [t for _, t in sent]
            pred = self.tag(words)
            correct += sum(p == g for p, g in zip(pred, gold))
            total += len(gold)
        return correct / total if total else 0.0
