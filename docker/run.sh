#!/usr/bin/env bash
# 持久 Jupyter 环境（不加 --rm）：容器停了还在，下次 start 即可复用。
#
# 用法:
#   ./run.sh           # 同 start
#   ./run.sh start     # 创建（若不存在）并后台启动
#   ./run.sh stop      # 停止，保留容器与缓存
#   ./run.sh restart   # 重启
#   ./run.sh status    # 状态 + 访问链接
#   ./run.sh logs      # 看日志
#   ./run.sh destroy   # 删除容器（下次 start 会按当前镜像重建）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_NAME="${IMAGE_NAME:-jupyter/transformer}"
CONTAINER_NAME="${CONTAINER_NAME:-ml-math-notes-jupyter}"
PORT="${PORT:-8888}"

cmd="${1:-start}"

container_exists() {
  docker container inspect "${CONTAINER_NAME}" >/dev/null 2>&1
}

container_running() {
  [[ "$(docker container inspect -f '{{.State.Running}}' "${CONTAINER_NAME}" 2>/dev/null || echo false)" == "true" ]]
}

print_url() {
  echo "Mount : ${REPO_ROOT}  ->  /home/jovyan/work"
  echo "Notebook: notebooks/01_transformer_deep_dive.ipynb"
  echo
  # 官方镜像会在日志里打带 token 的 URL；等几秒再抓
  local url
  # 日志里常见 http://127.0.0.1:8888/lab?token=...
  local token
  token="$(docker logs "${CONTAINER_NAME}" 2>&1 | grep -Eo 'token=[0-9a-f]+' | tail -n 1 | cut -d= -f2 || true)"
  if [[ -n "${token}" ]]; then
    echo "Open  : http://127.0.0.1:${PORT}/lab?token=${token}"
  else
    echo "Open  : http://127.0.0.1:${PORT}  （若需 token: ./run.sh logs | grep token）"
  fi
}

create_container() {
  echo "Creating container ${CONTAINER_NAME} (persistent, no --rm)..."
  docker create \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:8888" \
    -v "${REPO_ROOT}:/home/jovyan/work" \
    -e HOME=/home/jovyan \
    -e HF_HOME=/home/jovyan/work/.cache/huggingface \
    -e TRANSFORMERS_VERBOSITY=error \
    -e HF_HUB_DISABLE_PROGRESS_BARS=1 \
    "${IMAGE_NAME}" >/dev/null
}

start_container() {
  if container_exists; then
    if container_running; then
      echo "Already running: ${CONTAINER_NAME}"
    else
      echo "Starting existing container: ${CONTAINER_NAME}"
      docker start "${CONTAINER_NAME}" >/dev/null
    fi
  else
    create_container
    docker start "${CONTAINER_NAME}" >/dev/null
  fi
  # 等 Jupyter 写出 URL
  for _ in $(seq 1 20); do
    if docker logs "${CONTAINER_NAME}" 2>&1 | grep -q 'http://127.0.0.1:8888/'; then
      break
    fi
    sleep 0.5
  done
  print_url
}

case "${cmd}" in
  start)
    start_container
    ;;
  stop)
    if container_running; then
      docker stop "${CONTAINER_NAME}" >/dev/null
      echo "Stopped ${CONTAINER_NAME}（容器仍保留，下次 ./run.sh start）"
    else
      echo "Not running: ${CONTAINER_NAME}"
    fi
    ;;
  restart)
    if container_exists; then
      docker restart "${CONTAINER_NAME}" >/dev/null
      sleep 1
      print_url
    else
      start_container
    fi
    ;;
  status)
    if ! container_exists; then
      echo "No container. Run: ./run.sh start"
      exit 0
    fi
    docker ps -a --filter "name=^${CONTAINER_NAME}$" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
    if container_running; then
      echo
      print_url
    fi
    ;;
  logs)
    docker logs -f "${CONTAINER_NAME}"
    ;;
  destroy)
    if container_exists; then
      docker rm -f "${CONTAINER_NAME}" >/dev/null
      echo "Removed ${CONTAINER_NAME}. 下次 ./run.sh start 会新建。"
    else
      echo "Nothing to destroy."
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs|destroy}"
    exit 1
    ;;
esac
