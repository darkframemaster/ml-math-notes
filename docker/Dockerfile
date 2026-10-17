FROM quay.io/jupyter/scipy-notebook:latest

# scipy-notebook 已含 pandas / matplotlib / scikit-learn / scipy / numpy 等
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# 先装 CPU 版 PyTorch，避免 accelerate 等依赖从 PyPI 拉下 CUDA 巨包
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir \
    transformers \
    tensorflow \
    plotly \
    anywidget \
    ipywidgets \
    openai \
    tiktoken \
    datasets \
    accelerate
