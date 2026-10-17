#!/usr/bin/env bash
# 在容器内完整执行主教程 notebook（保留 steps=300 等原文参数）
set -euo pipefail
cd /home/jovyan/work

python -c "import anywidget" 2>/dev/null || pip install --quiet --no-cache-dir anywidget

python <<'PY'
import nbformat
from nbformat.validator import normalize

nb = nbformat.read("notebooks/01_transformer_deep_dive.ipynb", as_version=4)
normalize(nb)
src = nb.cells[1].source
if isinstance(src, list):
    src = "".join(src)
# headless 执行时用 json renderer，避免依赖前端 CDN
nb.cells[1].source = src.replace("notebook_connected", "json")
nbformat.write(nb, "notebooks/01_transformer_deep_dive.runtmp.ipynb")
print("prepared (full notebook)")
PY

# 优先走本地缓存，减少 Hub 重试噪音（缓存没有时仍会失败，可去掉 OFFLINE）
export HF_HOME="${HF_HOME:-/home/jovyan/work/.cache/huggingface}"
export TRANSFORMERS_VERBOSITY="${TRANSFORMERS_VERBOSITY:-error}"

jupyter nbconvert \
  --to notebook \
  --execute \
  --ExecutePreprocessor.timeout=1800 \
  --ExecutePreprocessor.kernel_name=python3 \
  notebooks/01_transformer_deep_dive.runtmp.ipynb \
  --output 01_transformer_deep_dive.executed.ipynb \
  --output-dir notebooks

python <<'PY'
import nbformat
from pathlib import Path

path = Path("notebooks/01_transformer_deep_dive.executed.ipynb")
nb = nbformat.read(path, as_version=4)
errors = 0
code_cells = 0
markers = [
    'print("numpy"',
    "one_hot_vs_embedding_demo",
    "convert_ids_to_tokens",
    "last_hidden_state",
    "scaled_dot_product_attention",
    "MultiHeadSelfAttention",
    "train_mini_gpt_with_plot",
    "attention_from_hf_model",
]
for i, cell in enumerate(nb.cells):
    if cell.cell_type != "code":
        continue
    code_cells += 1
    texts = []
    for o in cell.get("outputs", []):
        if o.get("output_type") == "error":
            errors += 1
            print("ERROR", i, o.get("ename"), o.get("evalue"))
        elif o.get("output_type") == "stream":
            t = o.get("text", "")
            texts.append("".join(t) if isinstance(t, list) else t)
        elif o.get("output_type") == "execute_result":
            t = o.get("data", {}).get("text/plain", "")
            texts.append("".join(t) if isinstance(t, list) else t)
    src = cell.source if isinstance(cell.source, str) else "".join(cell.source)
    if any(k in src for k in markers) and texts:
        print(f"\n=== cell {i} ===")
        print("".join(texts)[:1200])

print(
    f"\nSUMMARY code_cells={code_cells} errors={errors} "
    f"size_mb={path.stat().st_size / 1e6:.1f}"
)
if errors:
    raise SystemExit(1)
PY

rm -f notebooks/01_transformer_deep_dive.runtmp.ipynb \
      notebooks/01_transformer_deep_dive.executed.ipynb
echo DONE
