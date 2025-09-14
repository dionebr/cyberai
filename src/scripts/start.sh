#!/bin/bash

echo "[+] Iniciando CyberAI Offensive Assistant"
echo "[+] Verificando dependências..."


# Verificar se Ollama está rodando
if systemctl list-units --type=service | grep -q ollama; then
	if ! systemctl is-active --quiet ollama; then
		echo "[+] Iniciando serviço Ollama..."
		sudo systemctl start ollama
		sleep 3
	fi
else
	if ! pgrep -f "ollama serve" > /dev/null; then
		echo "[+] Iniciando Ollama manualmente..."
		nohup ollama serve > /dev/null 2>&1 &
		sleep 3
	fi
fi


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


# Verificar se os modelos estão disponíveis
echo "[+] Verificando modelos..."
if ! ollama list | grep -q "cyberhack"; then
    echo "[!] Modelo cyberhack não encontrado. Criando..."
    ollama create cyberhack -f models/cyberhack-modellama.modelfile
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
    echo "[+] Interface web: abra src/web/templates/index.html no navegador"
else
    echo "[!] Erro ao inicializar API. Verifique as portas ou dependências."
    exit 1
fi


# Manter o script rodando
wait
