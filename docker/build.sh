# docker build --platform=linux/arm64/v8 . -t jupyter/transformer
docker run -ti -d \
    -p 0.0.0.0:9001:8888 \
    -v /Users/darkframexue/Documents/jupyter:/home/jovyan/work \
    --platform=linux/arm64/v8 \
    --name jupyter-transformer \
    jupyter/transformer
