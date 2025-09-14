# Guia de Uso

## API

Ative o ambiente virtual antes de iniciar a API:
```bash
source .venv/bin/activate
python -m src.api.main
```

Principais endpoints:
- `POST /generate` — Gera resposta LLM para contexto técnico
- `POST /generate_exploit` — Gera exploit customizado
- `GET /techniques` — Lista técnicas de pentest disponíveis

Exemplo de requisição via `curl`:
```bash
curl -X POST http://localhost:8000/generate \
	-H 'Content-Type: application/json' \
	-d '{"prompt": "Explique buffer overflow em C"}'
```

## Interface Web

Abra `src/web/templates/index.html` no navegador.

- Preencha contexto, técnica e alvo
- Envie comandos ou perguntas técnicas
- Gere exploits informando CVE, aplicação e SO
