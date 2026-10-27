# ml-math-notes

统一学习笔记仓库。本仓库原为 **ml-math-notes**（机器学习与数学笔记），现已并入其它笔记仓，作为单一学习笔记项目。

Unified study-notes hub. This repository started as **ml-math-notes** (machine-learning and math notes) and now also holds the other note repos imported below.

既有的 `notebooks/` 与 `docker/` 保持原样。`docker/run.sh` 仍把**仓库根目录**挂到容器内 `/home/jovyan/work`。

Existing `notebooks/` and `docker/` are unchanged. `docker/run.sh` still mounts the **repository root** at `/home/jovyan/work`.

## ML / Math notebooks

| Notebook | 说明 |
|----------|------|
| [notebooks/01_transformer_deep_dive.ipynb](notebooks/01_transformer_deep_dive.ipynb) | Transformer 深入理解（零基础）：Demo → 神经网络/词向量铺垫 → Attention 原理 → 迷你 GPT；含 3b1b 风格交互可视化（`ipywidgets` + `plotly`） |
| [notebooks/02_gpt_step_by_step.ipynb](notebooks/02_gpt_step_by_step.ipynb) | 从规则/概率到 GPT 的方法演进（含 HMM 词性算例） |
| [notebooks/03_hmm_pos_demo.ipynb](notebooks/03_hmm_pos_demo.ipynb) | 仅用《爱丽丝》全文：HMM 词性/生成 vs N-gram 续写对照（可控前缀/长度/条数） |

交互控件说明：

1. 用下面的 Docker 打开 Jupyter 后，打开该 notebook 并 **Trust**
2. 建议按 Part 顺序运行；`notebooks/viz/` 提供可复用的交互组件
3. Part 1 / 3 首次运行需联网下载小模型（DistilBERT、GPT-2 等）

## Docker

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

## topics/compute-networking

来自 [dfx-note](https://github.com/darkframemaster/dfx-note) 的 `compute-networking/`（分支 `master`）。文件名按原样保留。

Imported from [dfx-note](https://github.com/darkframemaster/dfx-note) `compute-networking/` (branch `master`). Original filenames are unchanged.

| 文件 | 说明 |
|------|------|
| [ComputerNetwoking.md](topics/compute-networking/ComputerNetwoking.md) | 计算机网络笔记（考试、面试，以及工作中遇到的网络问题；文件名保留原文拼写） |
| [HTTP.md](topics/compute-networking/HTTP.md) | HTTP：非持续/持续连接，以及请求报文格式 |

## topics/sklearn

来自 [notes](https://github.com/darkframemaster/notes) 的 `sklearn_tutorial/`（分支 `master`），放到 `topics/sklearn/`。

Imported from [notes](https://github.com/darkframemaster/notes) `sklearn_tutorial/` (branch `master`), placed at `topics/sklearn/`.

| 文件 | 说明 |
|------|------|
| [intro.ipynb](topics/sklearn/intro.ipynb) | scikit-learn 入门：加载 iris 与 digits（笔记本原标题为「数据加载」「监督学习：从高维观察预测输出变量」） |

## archive/here-and-there

2016–2019 年的历史笔记合集（源仓库创建于 2016-04，最后推送于 2019-11）。来自 [here-and-there](https://github.com/darkframemaster/here-and-there)（分支 `master`）。总说明见 [README.mkd](archive/here-and-there/README.mkd)。

Historical dump from 2016–2019 (source repo created 2016-04, last push 2019-11), from [here-and-there](https://github.com/darkframemaster/here-and-there) (branch `master`). Overview: [README.mkd](archive/here-and-there/README.mkd).

下面只列顶层主题目录，不展开到每个文件。

Top-level topic folders only:

- [bash](archive/here-and-there/bash)
- [c](archive/here-and-there/c)
- [c++](<archive/here-and-there/c++>)
- [docker](archive/here-and-there/docker)
- [etcd](archive/here-and-there/etcd)
- [git](archive/here-and-there/git)
- [go](archive/here-and-there/go)
- [html&css](<archive/here-and-there/html&css>)
- [js](archive/here-and-there/js)
- [just-for-fun](archive/here-and-there/just-for-fun)
- [linux](archive/here-and-there/linux)
- [mongo](archive/here-and-there/mongo)
- [nginx](archive/here-and-there/nginx)
- [php](archive/here-and-there/php)
- [python](archive/here-and-there/python)
- [reading_note](archive/here-and-there/reading_note)
- [redis](archive/here-and-there/redis)
- [ruby](archive/here-and-there/ruby)
- [scala](archive/here-and-there/scala)
- [SQL](archive/here-and-there/SQL)
- [svn](archive/here-and-there/svn)
- [tensorflow](archive/here-and-there/tensorflow)
- [tools](archive/here-and-there/tools)
- [university](archive/here-and-there/university)
- [web_roadmap](archive/here-and-there/web_roadmap)

未并入的是操作系统元数据、编辑器交换文件、编译出来的 ELF 二进制，以及检出后为空的 gitlink 占位目录 `ruby/rails/blog`（源仓库没有 `.gitmodules`）。笔记正文、图片、字体、课件和示例源码都保留。

Left out: OS metadata, editor swap files, compiled ELF binaries, and the empty gitlink placeholder `ruby/rails/blog` (the source repo has no `.gitmodules`). Notes, images, fonts, course files, and example sources are kept.

## 来源 / Sources

这些源仓库之后会归档。并入的文件按原内容复制，没有改写。

These source repositories will be archived later. Imported files were copied as-is and were not rewritten.

- [darkframemaster/dfx-note](https://github.com/darkframemaster/dfx-note)（`master`）→ `topics/compute-networking/`
- [darkframemaster/notes](https://github.com/darkframemaster/notes)（`master`）→ `topics/sklearn/`
- [darkframemaster/here-and-there](https://github.com/darkframemaster/here-and-there)（`master`）→ `archive/here-and-there/`
