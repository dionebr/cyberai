# CyberAI Offensive Assistant

Assistente LLM offline especializado em cybersecurity ofensiva para treinamento em HackTheBox, TryHackMe e VulnHub.

## Arquitetura

- Backend: FastAPI + Llama2 GGUF via llama-cpp-python
- Modelo local (GGUF), sem dependência de Ollama
- Geração de exploits, payloads e técnicas avançadas
- Interface web moderna
- 100% offline e privado

## Instalação

```bash
git clone <repository-url>
cd cyberai
# Instale Python 3.12 e crie o ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi pydantic uvicorn llama-cpp-python huggingface-hub
# Baixe o modelo GGUF do Llama2 (exemplo via huggingface-cli)
huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
# Inicie a API
python -m src.api.main
```

## Uso

```bash
# Ative o ambiente virtual
source .venv/bin/activate
# Inicie a API
python -m src.api.main
# Acesse a interface web em src/web/templates/index.html
```

## Modelos

Os modelos são arquivos GGUF baixados do HuggingFace (ex: Llama2, Mistral, Gemma).
O caminho do modelo é configurado em `src/api/core/llama_client.py`.
Para adicionar novos modelos, baixe o arquivo GGUF e ajuste o caminho no client.

## Suporte

Para dúvidas, abra uma issue ou entre em contato.
