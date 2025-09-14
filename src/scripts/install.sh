#!/bin/bash

echo "Instalando CyberAI Offensive Assistant..."

# Instalar dependências do sistema
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm base-devel git python python-pip nodejs npm docker go cmake protobuf

# Instalar Ollama
if ! command -v ollama &> /dev/null; then
    git clone https://aur.archlinux.org/ollama.git
    cd ollama
    makepkg -si --noconfirm
    cd ..
    rm -rf ollama
fi

# Configurar serviços
sudo systemctl enable ollama
sudo systemctl start ollama

# Criar ambiente virtual Python
python -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt

# Baixar modelos
echo "Baixando modelos..."
ollama pull codellama:7b-code-q4_0
ollama pull llama2-uncensored:7b-chat-q4_0

# Criar modelo personalizado
if [ -f models/cyberhack-modellama.modelfile ]; then
    ollama create cyberhack -f models/cyberhack-modellama.modelfile
fi

echo "Instalação concluída!"
echo "Execute: bash src/scripts/start.sh"