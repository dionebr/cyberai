# Guia de Instalação

## Requisitos
- Linux (Arch, Ubuntu, Debian, etc.)
- Python 3.12+

## Passos
1. Clone o repositório:
	```bash
	git clone <repository-url>
	cd cyberai
	```
2. Crie o ambiente virtual e instale dependências:
	```bash
	python3.12 -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	pip install fastapi pydantic uvicorn llama-cpp-python huggingface-hub
	```
3. Baixe o modelo GGUF do Llama2:
	```bash
	huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
	```
4. Inicie a API:
	```bash
	python -m src.api.main
	```
5. Acesse a interface web:
	Abra `src/web/templates/index.html` no navegador ou configure o nginx para servir a pasta `src/web/templates`.
