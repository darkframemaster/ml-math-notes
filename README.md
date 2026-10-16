# ml-math-notes

机器学习与数学的学习记录与分享。

## Docker 环境

`docker/` 下是 Jupyter + Transformers 环境（含 PyTorch、TensorFlow）：

```bash
cd docker
docker build -t jupyter/transformer -f Dockerfile .
# 或使用带 vim 的版本
# docker build -t jupyter/transformer -f DockerfileV2 .
```

默认将 notebook 目录挂载到容器内 `/home/jovyan/work`，端口映射见 `build.sh`。
