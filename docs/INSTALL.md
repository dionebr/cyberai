# Guia de Instalação - CyberAI

## 🔧 Requisitos do Sistema

### Mínimos (com TinyLlama)
- **OS:** Linux, macOS ou Windows com WSL
- **RAM:** 2GB disponível
- **Armazenamento:** 2GB livre
- **CPU:** Qualquer processador moderno

### Recomendados (com sistema híbrido)
- **OS:** Linux (Arch, Ubuntu, Debian, etc.)
- **RAM:** 8GB+ (para usar ambos os modelos)
- **Armazenamento:** 10GB livre
- **CPU:** 4+ cores
- **GPU:** Opcional (melhora performance)

---

## 🐳 Instalação com Docker (Recomendada)

### Método Mais Simples - Um Comando
```bash
git clone https://github.com/dionebr/cyberai.git
cd cyberai
docker compose up --build -d
```

### Acesso
- **URL:** `http://localhost`
- **API:** `http://localhost/api/models` (para ver modelos disponíveis)

### Comandos Úteis
```bash
# Ver logs em tempo real
docker compose logs -f

# Parar os serviços
docker compose down

# Reiniciar apenas a API
docker compose restart api
```

---

## 💻 Instalação Manual (Avançada)

### 1. Clone e Setup Inicial
```bash
git clone https://github.com/dionebr/cyberai.git
cd cyberai
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Download dos Modelos

**TinyLlama (Rápido - 668MB):**
```bash
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf
```

**Mistral (Opcional - Completo - 4GB):**
```bash
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
```

### 3. Iniciar Serviços
```bash
# Terminal 1: API
source .venv/bin/activate
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Web Server (em outra aba)
cd src/web && python -m http.server 8080
```

### 4. Acesso
- **URL:** `http://localhost:8080/templates/index.html`

---

## ⚡ Configuração de Performance

### Para Máquinas Limitadas
O sistema automaticamente usa apenas TinyLlama para todas as tarefas. Para forçar isto:

1. Remova ou renomeie o arquivo `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
2. O sistema usará apenas TinyLlama (ultra-rápido)

### Para Máquinas Potentes
Mantenha ambos os modelos para aproveitar o sistema híbrido inteligente.

### Otimizações de GPU (Opcional)
```bash
# Para NVIDIA GPU
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python

# Para AMD GPU  
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python

# Para Apple Silicon
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python
```

---

## 🔧 Verificação da Instalação

### Teste da API
```bash
curl http://localhost:8000/api/techniques
curl http://localhost:8000/api/models
```

### Teste Rápido
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"nmap básico","technique":"recon","max_tokens":50}'
```

---

## 🆘 Solução de Problemas

### Erro: "Modelo indisponível"
- **Causa:** Arquivo GGUF não encontrado
- **Solução:** Verifique se os arquivos estão na pasta `models/`

### Erro: Timeout nas respostas
- **Causa:** Modelo muito pesado para a máquina
- **Solução:** Use apenas TinyLlama (remova o Mistral)

### Erro: "llama-cpp-python" não funciona
- **Solução:** Reinstale com flags específicas da sua arquitetura (ver seção GPU acima)

### Interface não carrega
- **Causa:** Servidor web não está rodando corretamente
- **Solução:** Verifique se está servindo a pasta `src/web/templates`
