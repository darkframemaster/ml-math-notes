# ml-math-notes

机器学习与数学的学习记录与分享。

## Notebooks

| Notebook | 说明 |
|----------|------|
| [notebooks/01_transformer_deep_dive.ipynb](notebooks/01_transformer_deep_dive.ipynb) | Transformer 深入理解（零基础）：Demo → 神经网络/词向量铺垫 → Attention 原理 → 迷你 GPT；含 3b1b 风格交互可视化（`ipywidgets` + `plotly`） |
| [notebooks/02_gpt_step_by_step.ipynb](notebooks/02_gpt_step_by_step.ipynb) | 从规则/概率到 GPT 的方法演进（含 HMM 词性算例） |
| [notebooks/03_hmm_pos_demo.ipynb](notebooks/03_hmm_pos_demo.ipynb) | 仅用《爱丽丝》全文：HMM 词性/生成 vs N-gram 续写对照（可控前缀/长度/条数） |

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

> 交互图需要 `plotly` + `anywidget`。HMM demo 需要 `nltk` / `kagglehub`。旧镜像缺包时请重新 `./build.sh`（或对已有容器 `docker exec ml-math-notes-jupyter pip install nltk kagglehub`）。
>
> HMM demo 使用 NLTK 的 `punkt` / `punkt_tab` 分句模型和 `averaged_perceptron_tagger_eng` 词性模型。重建 Docker 镜像时会自动装入；已有容器可执行：
>
> ```bash
> docker exec ml-math-notes-jupyter python -m nltk.downloader \
>   -d /home/jovyan/work/.cache/nltk_data \
>   punkt punkt_tab averaged_perceptron_tagger averaged_perceptron_tagger_eng
> ```
>
> Brown 语料（与 [Kaggle nltkdata/brown-corpus](https://www.kaggle.com/datasets/nltkdata/brown-corpus) 同源）若要运行扩展算例，放在仓库 `.cache/nltk_data/`。若缺失可：
>
> ```bash
> mkdir -p .cache/nltk_data/corpora
> curl -L -o .cache/nltk_data/corpora/brown.zip \
>   https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/brown.zip
> unzip -qo .cache/nltk_data/corpora/brown.zip -d .cache/nltk_data/corpora
> ```
