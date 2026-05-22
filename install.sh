#!/usr/bin/env bash

set -euo pipefail

REPO_OWNER="WCRP-CORDEX"
REPO_NAME="ncrepack-cordex"
REPO_BRANCH="cordex"

RAW_BASE_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${REPO_BRANCH}/cmip7_repack"

if ! command -v cmip7repack >/dev/null 2>&1; then
    echo "Error: cmip7repack is not in PATH. Install cmip7_repack first." >&2
    exit 1
fi

CMIP7REPACK_PATH="$(command -v cmip7repack)"
INSTALL_DIR="$(dirname "${CMIP7REPACK_PATH}")"

if [[ ! -w "${INSTALL_DIR}" ]]; then
    echo "Error: install directory is not writable: ${INSTALL_DIR}" >&2
    echo "Run with elevated permissions, for example: sudo ./install.sh" >&2
    exit 1
fi

if command -v curl >/dev/null 2>&1; then
    DOWNLOADER="curl"
elif command -v wget >/dev/null 2>&1; then
    DOWNLOADER="wget"
else
    echo "Error: neither curl nor wget is available to download scripts." >&2
    exit 1
fi

echo "cmip7repack found at: ${CMIP7REPACK_PATH}"
echo "Installing scripts to: ${INSTALL_DIR}"

for script in ncrepack-cordex ncrepack-cordex-check; do
    url="${RAW_BASE_URL}/${script}"
    dest="${INSTALL_DIR}/${script}"

    if [[ "${DOWNLOADER}" == "curl" ]]; then
        curl -fsSL "${url}" -o "${dest}"
    else
        wget -q "${url}" -O "${dest}"
    fi

    chmod +x "${INSTALL_DIR}/${script}"
    echo "Installed: ${dest}"
done

echo "Installation complete."
