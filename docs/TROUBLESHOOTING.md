# Solução de Problemas

## API não inicia
- Verifique se o ambiente virtual está ativado: `source .venv/bin/activate`
- Instale dependências: `pip install fastapi pydantic uvicorn llama-cpp-python huggingface-hub`
- Verifique se o modelo GGUF está presente em `models/`
- Confira o caminho do modelo em `src/api/core/llama_client.py`

## Modelo GGUF não disponível
- Baixe novamente via huggingface-cli:
	```bash
	huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
	```

## Interface web não carrega
- Verifique se a API está rodando: `python -m src.api.main`
- Abra `src/web/templates/index.html` diretamente no navegador
- Para servir via nginx, confira configurações em `config/nginx/`
