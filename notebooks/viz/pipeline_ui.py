"""Lightweight interactive playground for Hugging Face pipelines."""

from __future__ import annotations

from IPython.display import display
from ipywidgets import Button, Dropdown, HTML, Textarea, VBox, Output


_PIPELINES: dict[str, dict] = {
    "情感分析 (Encoder 分类)": {
        "task": "sentiment-analysis",
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
        "default_text": "I love learning about transformers!",
        "note": "把整句映射成一个标签（正面/负面）。",
    },
    "填空 fill-mask (Encoder / MLM)": {
        "task": "fill-mask",
        "model": "distilbert-base-uncased",
        "default_text": "Paris is the [MASK] of France.",
        "note": "根据双向上下文预测被遮住的词。",
    },
    "命名实体 NER (Encoder token 分类)": {
        "task": "ner",
        "model": "dslim/bert-base-NER",
        "default_text": "My name is Ada and I work at OpenAI in San Francisco.",
        "kwargs": {"aggregation_strategy": "simple"},
        "note": "给每个词打上人名/组织/地点等标签。",
    },
    "文本生成 (Decoder / CLM)": {
        "task": "text-generation",
        "model": "gpt2",
        "default_text": "Once upon a time in a small village,",
        "kwargs": {"max_new_tokens": 40, "do_sample": True, "top_k": 50},
        "note": "从左到右预测下一个词，循环生成。",
    },
    "摘要 (Encoder-Decoder)": {
        "task": "summarization",
        "model": "sshleifer/distilbart-cnn-12-6",
        "default_text": (
            "Transformers are neural network architectures that rely on attention "
            "mechanisms to process sequences. They power modern translation, "
            "summarization, and large language models."
        ),
        "kwargs": {"max_length": 40, "min_length": 10},
        "note": "编码器读全文，解码器生成更短的摘要。",
    },
}


def interactive_pipeline_playground() -> VBox:
    """Text box + task dropdown + run button for several HF pipelines."""
    task = Dropdown(options=list(_PIPELINES.keys()), description="任务")
    text = Textarea(value=_PIPELINES[task.value]["default_text"], layout={"width": "90%", "height": "100px"})
    note = HTML(value=f"<i>{_PIPELINES[task.value]['note']}</i>")
    out = Output()
    cache: dict = {}

    def on_task_change(change) -> None:
        cfg = _PIPELINES[change["new"]]
        text.value = cfg["default_text"]
        note.value = f"<i>{cfg['note']}</i>"

    task.observe(on_task_change, names="value")

    def run(_: Button) -> None:
        cfg = _PIPELINES[task.value]
        key = (cfg["task"], cfg["model"])
        with out:
            out.clear_output()
            print("加载模型中（首次需联网下载）…")
            try:
                from transformers import pipeline

                if key not in cache:
                    kwargs = dict(cfg.get("kwargs", {}))
                    # kwargs for pipeline construction vs call: split carefully
                    call_kwargs = {}
                    init_kwargs = {}
                    if cfg["task"] == "ner":
                        init_kwargs["aggregation_strategy"] = kwargs.pop(
                            "aggregation_strategy", "simple"
                        )
                    else:
                        call_kwargs = kwargs
                    cache[key] = (
                        pipeline(cfg["task"], model=cfg["model"], **init_kwargs),
                        call_kwargs,
                    )
                pipe, call_kwargs = cache[key]
                result = pipe(text.value, **call_kwargs)
                print("结果：")
                print(result)
            except Exception as exc:  # noqa: BLE001 - educational notebook
                print(f"运行失败：{exc}")
                print("若在离线环境，请先联网下载模型，或跳过本 Part。")

    btn = Button(description="运行 Demo", button_style="primary")
    btn.on_click(run)

    hint = HTML(
        value=(
            "<b>做什么：</b> 选任务、改输入文本、点运行。&nbsp;|&nbsp; "
            "<b>看什么：</b> 同样是 Transformer，不同“头”解决不同问题。"
            "此时先当魔术看，后面再拆。"
        )
    )
    ui = VBox([hint, task, note, text, btn, out])
    display(ui)
    return ui
