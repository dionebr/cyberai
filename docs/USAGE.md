# Guia de Uso - CyberAI

## 🧠 Sistema Híbrido de IA

O CyberAI usa **dois modelos de IA** que trabalham juntos para otimizar velocidade e qualidade:

### ⚡ Seleção Automática Inteligente
- **TinyLlama (668MB):** Tarefas simples = respostas em 5-10 segundos
- **Mistral (4GB):** Tarefas complexas = análises detalhadas
- **Automático:** O sistema escolhe o modelo ideal baseado na técnica

### 📊 Mapeamento de Técnicas
**TinyLlama (Rápido):**
- `recon`, `payloads`, `xss`, `sql_injection`, `buffer_overflow`
- `post`, `binarios`, `exploit`, `relatorios`, `gestao` 
- `ferramentas`, `intelligence`, `lab`, `treinamento`

**Mistral (Completo):**
- Técnicas não listadas acima (análises muito complexas)

---

## 🐳 Opção A — Docker (Recomendado)

### 1. Subir os Serviços
```bash
git clone https://github.com/dionebr/cyberai.git
cd cyberai
docker compose up --build -d
```

### 2. Acessar Interface Web
- **Principal:** http://localhost
- **API Direta:** http://localhost/api/models

### 3. Módulos Disponíveis
| URL | Módulo | Modelo | Velocidade |
|-----|--------|--------|------------|
| `/recon.html` | Reconhecimento | TinyLlama | ⚡ Ultra-rápido |
| `/payloads.html` | Payloads | TinyLlama | ⚡ Ultra-rápido |
| `/binarios.html` | Análise Binários | TinyLlama | ⚡ Ultra-rápido |
| `/exploit.html` | Exploração | TinyLlama | ⚡ Ultra-rápido |
| `/post.html` | Pós-Exploração | TinyLlama | ⚡ Ultra-rápido |
| `/treinamento.html` | Treinamento | TinyLlama | ⚡ Ultra-rápido |
| `/relatorios.html` | Relatórios | TinyLlama | ⚡ Ultra-rápido |
| `/gestao.html` | Gestão | TinyLlama | ⚡ Ultra-rápido |
| `/ferramentas.html` | Dev Tools | TinyLlama | ⚡ Ultra-rápido |
| `/intelligence.html` | Threat Intel | TinyLlama | ⚡ Ultra-rápido |
| `/lab.html` | Laboratório | TinyLlama | ⚡ Ultra-rápido |
| `/community.html` | Comunidade | Automático | 🔄 Híbrido |

### 4. Comandos Úteis
```bash
# Ver logs em tempo real
docker compose logs -f

# Reiniciar API (após mudanças)
docker compose restart api

# Parar tudo
docker compose down
```

---

## 💻 Opção B — Execução Local

### 1. Setup Completo
```bash
git clone https://github.com/dionebr/cyberai.git
cd cyberai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Baixar TinyLlama (essencial)
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf
```

### 2. Iniciar Serviços
```bash
# Terminal 1: API
source .venv/bin/activate
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Web
cd src/web && python -m http.server 8080
```

### 3. Acesso
- **URL:** http://localhost:8080/templates/index.html
- **API:** http://localhost:8000/api/models

---

## 🚀 Endpoints da API

### Principais
- `POST /api/generate` — Gera resposta (seleção automática de modelo)
- `POST /api/generate_exploit` — Exploits (usa Mistral para qualidade)
- `GET /api/techniques` — Lista técnicas suportadas
- `GET /api/models` — Informações dos modelos disponíveis

### Novo: Endpoint de Modelos
```bash
curl http://localhost/api/models
```
**Resposta:**
```json
{
  "models": [
    {
      "name": "TinyLlama (Rápido)",
      "description": "Modelo rápido para tarefas simples (600MB)",
      "techniques": ["recon", "payloads", ...],
      "max_tokens": 128
    },
    {
      "name": "Mistral (Completo)", 
      "description": "Modelo completo para tarefas complexas (4GB)",
      "max_tokens": 256
    }
  ]
}
```

---

## 💡 Exemplos Práticos

### Teste Rápido (TinyLlama)
```bash
curl -X POST http://localhost/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "nmap scan básico", "technique": "recon"}'
```
**Resultado:** Resposta em ~5-10 segundos ⚡

### Análise Complexa (Mistral)
```bash
curl -X POST http://localhost/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Desenvolver exploit buffer overflow avançado", "technique": "advanced_exploit"}'
```
**Resultado:** Análise detalhada (~30 segundos, alta qualidade)

### Interface Web - Chat Flutuante
1. Acesse http://localhost
2. Clique no botão de chat (canto inferior direito)
3. Digite: *"Gere reverse shell para Linux"*
4. **Resultado:** TinyLlama responde instantaneamente! ⚡

---

## 🔧 Configurações Avançadas

### Forçar Modelo Específico
```bash
# Sempre usar TinyLlama (ultra-rápido)
curl -X POST http://localhost/api/generate \
  -d '{"prompt": "...", "technique": "recon"}'

# Usar Mistral (mais lento, melhor qualidade)
curl -X POST http://localhost/api/generate \
  -d '{"prompt": "...", "technique": "complex_analysis"}'
```

### Otimizar para Máquina Limitada
1. Use apenas TinyLlama (remova/renomeie o arquivo Mistral)
2. Sistema detecta automaticamente e usa só o modelo rápido
3. **Benefício:** Todas as respostas em ~5-10 segundos

---

## ❗ Solução de Problemas

### Modelo Indisponível (503)
```bash
# Verificar se modelos existem
ls -la models/

# Re-baixar TinyLlama se necessário
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf
```

### Respostas Muito Lentas
- **Causa:** Tentando usar Mistral em máquina limitada
- **Solução:** Remova o arquivo `mistral-7b-instruct-v0.2.Q4_K_M.gguf` para forçar apenas TinyLlama

### Interface Não Carrega
- **Causa:** Conflito de CORS/portas
- **Solução:** Use Docker (`http://localhost`) em vez de acesso direto aos arquivos
