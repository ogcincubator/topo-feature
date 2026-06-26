#!/bin/bash
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

to_host_path() {
  local path="$1"

  if command -v cygpath >/dev/null 2>&1; then
    cygpath -m "${path}"
  else
    echo "${path}"
  fi
}

HOST_ROOT_DIR="$(to_host_path "${ROOT_DIR}")"

# Process building blocks
VOLUMES=()
if [ -f '.volumes' ]; then
  while read -r line; do
    [ -n "${line}" ] || continue

    if [[ "${line}" != /* ]]; then
      VOLUMES+=("-v" "$(to_host_path "${ROOT_DIR}/${line}")")
    else
      VOLUMES+=("-v" "$(to_host_path "${line}")")
    fi
  done < .volumes
fi

PERMISSION_ARGS=()
if [ "${ALLOW_TRANSFORMS:-false}" = "true" ]; then
  PERMISSION_ARGS+=("--skip-permissions" "true")
fi

MSYS_NO_PATHCONV=1 docker run --pull=always --rm --workdir /workspace \
  -v "${HOST_ROOT_DIR}:/workspace" "${VOLUMES[@]}" \
  ghcr.io/opengeospatial/bblocks-postprocess \
  --clean true --base-url http://localhost:9090/register/ \
  "${PERMISSION_ARGS[@]}" "$@"