#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="$(cd "$(dirname "$0")/../../models" && pwd)"
FILE="mistral-7b-instruct-v0.2.Q4_K_M.gguf"
URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/${FILE}"
SHA256_EXPECTED="3e0039fd0273fcbebb49228943b17831aadd55cbcbf56f0af00499be2040ccf9"

mkdir -p "${MODEL_DIR}"
cd "${MODEL_DIR}"

echo "[+] Baixando modelo ${FILE} em ${MODEL_DIR}"
echo "[i] URL: ${URL}"

if ! command -v curl >/dev/null 2>&1; then
  echo "[!] curl não encontrado. Instale curl e tente novamente." >&2
  exit 1
fi

# Download com retomada (-C -)
curl -L --retry 3 --fail --progress-bar -C - -o "${FILE}" "${URL}"

echo "[+] Verificando checksum SHA256..."
if command -v sha256sum >/dev/null 2>&1; then
  SHA256_ACTUAL="$(sha256sum "${FILE}" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  SHA256_ACTUAL="$(shasum -a 256 "${FILE}" | awk '{print $1}')"
else
  echo "[!] sha256sum/shasum não encontrado. Pulei verificação de integridade." >&2
  exit 0
fi

if [[ "${SHA256_ACTUAL}" != "${SHA256_EXPECTED}" ]]; then
  echo "[!] Checksum inválido! Esperado: ${SHA256_EXPECTED} | Obtido: ${SHA256_ACTUAL}" >&2
  echo "[!] Removendo arquivo corrompido..."
  rm -f "${FILE}"
  exit 1
fi

echo "[+] Modelo baixado e verificado com sucesso: ${MODEL_DIR}/${FILE}"