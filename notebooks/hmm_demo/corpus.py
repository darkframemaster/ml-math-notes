"""Load POS-tagged corpora for the HMM demo.

Sources
-------
1. **Brown** (Kaggle ``nltkdata/brown-corpus`` / NLTK)：已有人工词性；含 news、fiction 等。
2. **完整公版故事**（如 ``notebooks/data/stories/alice_in_wonderland.txt``）：
   Project Gutenberg 全文，用 NLTK 感知机标注器自动打词性后再训 HMM。

NLTK 数据目录：仓库 ``.cache/nltk_data/``（Docker 挂载）。
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_NLTK = REPO_ROOT / ".cache" / "nltk_data"
STORIES_DIR = Path(__file__).resolve().parents[1] / "data" / "stories"

# Brown 里偏叙事的类别（仍是篇章片段，不是单部完整长篇）
BROWN_STORY_CATEGORIES = (
    "fiction",
    "adventure",
    "mystery",
    "romance",
    "science_fiction",
    "humor",
)


def _ensure_nltk_path() -> None:
    import nltk

    root = str(REPO_NLTK)
    if root not in nltk.data.path:
        nltk.data.path.insert(0, root)


def normalize_tag(tag: str) -> str:
    """Strip Brown suffix markers like ``NP-TL`` -> ``NP``."""
    return tag.split("-", 1)[0]


def load_brown_tagged_sents(
    categories: str | tuple[str, ...] = "news",
    *,
    lowercase: bool = True,
    max_sents: int | None = None,
) -> list[list[tuple[str, str]]]:
    """Return sentences as lists of ``(word, pos)`` from Brown via NLTK."""
    _ensure_nltk_path()
    from nltk.corpus import brown

    raw = brown.tagged_sents(categories=categories)
    if max_sents is not None:
        raw = raw[:max_sents]

    out: list[list[tuple[str, str]]] = []
    for sent in raw:
        pairs = []
        for word, tag in sent:
            w = word.lower() if lowercase else word
            pairs.append((w, normalize_tag(tag)))
        if pairs:
            out.append(pairs)
    return out


def load_brown_story_bundle(
    *,
    lowercase: bool = True,
    max_sents: int | None = 8000,
) -> list[list[tuple[str, str]]]:
    """Brown 叙事类拼盘（fiction / adventure / …），人工词性。"""
    return load_brown_tagged_sents(
        BROWN_STORY_CATEGORIES,
        lowercase=lowercase,
        max_sents=max_sents,
    )


_GUTENBERG_START = re.compile(
    r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
    re.I | re.S,
)
_GUTENBERG_END = re.compile(
    r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
    re.I | re.S,
)


def strip_gutenberg_boilerplate(text: str) -> str:
    start = _GUTENBERG_START.search(text)
    end = _GUTENBERG_END.search(text)
    if start and end and end.start() > start.end():
        return text[start.end() : end.start()]
    if start:
        return text[start.end() :]
    return text


def load_plain_story_tagged(
    path: str | Path | None = None,
    *,
    lowercase: bool = True,
    max_sents: int | None = None,
) -> list[list[tuple[str, str]]]:
    """Load one complete story text and auto-POS-tag with NLTK.

    Default file: ``notebooks/data/stories/alice_in_wonderland.txt``
    (Alice's Adventures in Wonderland, Project Gutenberg #11).
    """
    _ensure_nltk_path()
    from nltk import pos_tag, sent_tokenize, word_tokenize

    path = Path(path) if path else STORIES_DIR / "alice_in_wonderland.txt"
    raw = path.read_text(encoding="utf-8", errors="ignore")
    body = strip_gutenberg_boilerplate(raw)
    # Drop illustration / contents noise lines a bit
    body = re.sub(r"\[Illustration.*?\]", " ", body, flags=re.I | re.S)

    sents = sent_tokenize(body)
    if max_sents is not None:
        sents = sents[:max_sents]

    out: list[list[tuple[str, str]]] = []
    for sent in sents:
        tokens = word_tokenize(sent)
        if not tokens:
            continue
        tagged = pos_tag(tokens)
        pairs = []
        for word, tag in tagged:
            w = word.lower() if lowercase else word
            pairs.append((w, normalize_tag(tag)))
        if pairs:
            out.append(pairs)
    return out


def list_local_stories() -> list[Path]:
    if not STORIES_DIR.is_dir():
        return []
    return sorted(STORIES_DIR.glob("*.txt"))


def try_kagglehub_brown() -> Path | None:
    """Optional: download Brown via kagglehub if credentials are configured."""
    try:
        import kagglehub

        return Path(kagglehub.dataset_download("nltkdata/brown-corpus"))
    except Exception:
        return None
