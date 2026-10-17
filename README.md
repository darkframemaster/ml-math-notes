# ml-math-notes

机器学习与数学的学习记录与分享。

## Notebooks

| Notebook | 说明 |
|----------|------|
| [notebooks/01_transformer_deep_dive.ipynb](notebooks/01_transformer_deep_dive.ipynb) | Transformer 深入理解（零基础）：Demo → 神经网络/词向量铺垫 → Attention 原理 → 迷你 GPT；含 3b1b 风格交互可视化（`ipywidgets` + `plotly`） |

交互控件说明：

1. 用下面的 Docker 打开 Jupyter 后，打开该 notebook 并 **Trust**
2. 建议按 Part 顺序运行；`notebooks/viz/` 提供可复用的交互组件
3. Part 1 / 3 首次运行需联网下载小模型（DistilBERT、GPT-2 等）

## Docker 环境

`docker/` 下是 Jupyter + Transformers 环境（含 PyTorch、TensorFlow、plotly、anywidget、ipywidgets）：

```bash
cd docker
./build.sh          # 构建镜像（改过 Dockerfile 后要重建）
./run.sh start      # 创建/启动持久容器（无 --rm，可反复用）
./run.sh stop       # 停掉，容器保留
./run.sh status     # 看状态和访问链接
./run.sh destroy    # 真要删容器时再用（下次 start 会重建）
```

`run.sh` 把**仓库根目录**挂到 `/home/jovyan/work`，容器名固定为 `ml-math-notes-jupyter`，后台运行，关掉终端也不丢：

| 宿主机 | 容器内 |
|--------|--------|
| `.../ml-math-notes/` | `/home/jovyan/work/` |
| `.../ml-math-notes/notebooks/...` | `/home/jovyan/work/notebooks/...` |
| `.../ml-math-notes/.cache/huggingface/` | 模型缓存（下次不用重下） |

浏览器打开 `./run.sh start` / `status` 打印的链接，进入 `notebooks/01_transformer_deep_dive.ipynb`，**Trust** 后按 Part 跑。

> 交互图需要 `plotly` + `anywidget`。旧镜像缺包时请重新 `./build.sh`。
