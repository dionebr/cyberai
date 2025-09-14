#!/bin/bash

echo "Instalando CyberAI Offensive Suite..."

# Instalar dependências do sistema
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm base-devel git python python-pip nodejs npm docker docker-compose go cmake protobuf curl

## Removido: instalação Ollama (não é necessária para GGUF via llama-cpp)

# Criar ambiente virtual Python
python -m venv venv
source venv/bin/activate

echo "[+] Instalando dependências Python..."
pip install -r requirements.txt

echo "[+] Baixando modelo Mistral GGUF..."
bash src/scripts/download-model.sh || {
    echo "[!] Falha ao baixar o modelo. Tente novamente mais tarde."; exit 1; }

echo "Instalação concluída!"
echo "Execute: bash src/scripts/start.sh"