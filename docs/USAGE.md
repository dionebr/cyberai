# Guia de Uso

Importante: os arquivos de modelo (.gguf) NÃO são versionados. O modelo será baixado localmente durante a instalação e mantido em `models/`.

## Opção A — Docker (recomendado)

1) Suba os serviços
```bash
docker-compose up --build -d
```

2) Acesse a interface web
- Navegador: http://localhost
- A API é acessada via proxy em `/api` (ex: http://localhost/api/generate)

3) Logs (opcional)
```bash
docker-compose logs -f --tail=200
```

## Opção B — Execução local (sem Docker)

1) Instale dependências e baixe o modelo
```bash
bash src/scripts/install.sh
```

2) Inicie a API e verificação
```bash
bash src/scripts/start.sh
```

3) Interface Web
- Via Nginx (Docker): http://localhost
- Ou abra diretamente o arquivo: `src/web/templates/index.html`

## Endpoints principais
- POST /api/generate — Gera resposta técnica do LLM
- POST /api/generate_exploit — Gera exploit customizado
- GET /api/techniques — Lista técnicas suportadas
- GET /api/models — Lista modelos disponíveis (nome do GGUF)

Exemplo via curl
```bash
curl -X POST http://localhost/api/generate \
	-H 'Content-Type: application/json' \
	-d '{"prompt": "Explique buffer overflow em C"}'
```

## Erros comuns
- 503 Modelo indisponível
	- Rode o download do modelo: `bash src/scripts/download-model.sh`
	- Verifique se `llama-cpp-python` está instalado (requirements.txt)
- CORS/Portas
	- A interface usa `/api`. Certifique-se de acessar via http://localhost com o Nginx do Docker.
