#!/bin/bash

echo "[+] Iniciando CyberAI Offensive Suite"
echo "[+] Verificando dependências..."


# Verificar versão do Python e ambiente virtual
PYVER=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYVER" != "3.12" && "$PYVER" != "3.11" ]]; then
	echo "[!] Atenção: Recomenda-se Python 3.12 ou 3.11 para compatibilidade total. Versão detectada: $PYVER"
	if ! command -v python3.12 &> /dev/null && ! command -v python3.11 &> /dev/null; then
		echo "[!] Python 3.12 ou 3.11 não encontrado no sistema. Instale antes de continuar."
		exit 1
	fi
	if [ ! -d "venv" ]; then
		if command -v python3.12 &> /dev/null; then
			echo "[+] Criando ambiente virtual com Python 3.12..."
			python3.12 -m venv venv
		else
			echo "[+] Criando ambiente virtual com Python 3.11..."
			python3.11 -m venv venv
		fi
		source venv/bin/activate
		pip install -r requirements.txt
	fi
fi

if [ ! -f "venv/bin/activate" ]; then
	echo "[!] Ambiente virtual não encontrado. Crie com: python3.12 -m venv venv"
	exit 1
fi


echo "[+] Verificando modelo GGUF..."
MODEL_PATH="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if [ ! -f "$MODEL_PATH" ]; then
	echo "[!] Modelo não encontrado em $MODEL_PATH. Rode: bash src/scripts/download-model.sh"
	exit 1
fi


# Iniciar a API
echo "[+] Iniciando API FastAPI..."
source venv/bin/activate
python src/api/main.py &


# Aguardar a API inicializar
sleep 5

# Verificar se a API está respondendo
if curl -s http://localhost:8000/techniques > /dev/null; then
    echo "[+] API inicializada com sucesso!"
	echo "[+] URL da API: http://localhost:8000"
	echo "[+] Interface web: http://localhost (via Nginx/docker-compose)"
else
    echo "[!] Erro ao inicializar API. Verifique as portas ou dependências."
    exit 1
fi


# Manter o script rodando
wait
