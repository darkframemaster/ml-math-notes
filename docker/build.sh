#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${IMAGE_NAME:-jupyter/transformer}"
PLATFORM="${PLATFORM:-linux/arm64}"

docker build \
  --platform="${PLATFORM}" \
  -f "${SCRIPT_DIR}/Dockerfile" \
  -t "${IMAGE_NAME}" \
  "${SCRIPT_DIR}"

echo "Built ${IMAGE_NAME}"
