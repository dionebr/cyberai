# Solução de Problemas - CyberAI

## 🔧 Problemas Comuns do Sistema Híbrido

### ⚡ Modelo TinyLlama Não Encontrado
**Erro:** `Modelo GGUF não encontrado em [...]/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf`

**Soluções:**
```bash
# Método 1: Download direto
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf

# Método 2: Via huggingface-cli
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False

# Verificar se foi baixado
ls -la models/*.gguf
```

### 🐌 Respostas Muito Lentas (>30s)
**Causa:** Sistema tentando usar Mistral em máquina limitada

**Soluções:**
```bash
# Opção 1: Remover Mistral (forçar apenas TinyLlama)
cd models
mv mistral-7b-instruct-v0.2.Q4_K_M.gguf mistral-7b-instruct-v0.2.Q4_K_M.gguf.backup

# Opção 2: Verificar qual modelo está sendo usado
curl http://localhost/api/models

# Opção 3: Usar apenas técnicas rápidas (TinyLlama)
# recon, payloads, xss, sql_injection, buffer_overflow, etc.
```

### 🔄 Sistema Não Seleciona Modelo Correto
**Problema:** Sempre usa o mesmo modelo

**Diagnóstico:**
```bash
# Verificar modelos disponíveis
curl http://localhost/api/models

# Teste com técnica rápida (deve usar TinyLlama)
curl -X POST http://localhost/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"nmap scan","technique":"recon","max_tokens":50}'

# Verificar resposta - deve conter: "model_used":"Modelo rápido para tarefas simples"
```

---

## 🐳 Problemas Docker

### Container API Não Inicia
**Erro:** `Container cyberai-api-1 exited with code 1`

**Diagnóstico:**
```bash
# Ver logs detalhados
docker-compose logs api

# Possíveis causas e soluções:
# 1. Modelo não encontrado
docker exec -it cyberai-api-1 ls -la /app/models/

# 2. Dependências não instaladas
docker-compose build --no-cache api

# 3. Porta ocupada
fuser -k 8000/tcp
docker-compose restart api
```

### Erro de Permissão nos Modelos
**Erro:** `Permission denied` ao acessar modelo

**Solução:**
```bash
# Corrigir permissões
sudo chown -R $USER:$USER models/
chmod 644 models/*.gguf

# Recriar containers
docker-compose down
docker-compose up --build -d
```

---

## 💻 Problemas Instalação Local

### llama-cpp-python Não Funciona
**Erro:** `ImportError: cannot import name 'Llama'`

**Soluções por Plataforma:**
```bash
# Linux CPU (genérico)
pip install llama-cpp-python

# Linux com NVIDIA GPU
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python

# Linux com AMD GPU
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python

# macOS Apple Silicon
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python

# Windows
# Use: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu118
```

### Ambiente Virtual Não Funciona
**Problema:** Dependências não encontradas

**Solução Completa:**
```bash
# Remover ambiente existente
rm -rf .venv

# Criar novo ambiente
python3 -m venv .venv
source .venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências na ordem correta
pip install wheel setuptools
pip install -r requirements.txt

# Verificar instalação
python -c "from llama_cpp import Llama; print('OK')"
```

---

## 🌐 Problemas Interface Web

### API 404 Not Found
**Erro:** `GET http://localhost/api/techniques 404 (Not Found)`

**Verificações:**
```bash
# 1. Verificar se nginx está proxy correto
docker exec -it cyberai-web-1 cat /etc/nginx/conf.d/default.conf

# 2. Testar API diretamente
curl http://localhost:8000/api/techniques

# 3. Verificar containers rodando
docker-compose ps

# 4. Reiniciar nginx
docker-compose restart web
```

### JavaScript Errors
**Erro:** `Uncaught ReferenceError: detectApiBase is not defined`

**Solução:**
```bash
# Verificar se utils.js está carregando
curl http://localhost/static/js/utils.js

# Verificar no browser DevTools:
# F12 → Console → deve mostrar erros específicos

# Se necessário, recriar containers
docker-compose down
docker-compose up --build -d
```

### Timeout nas Requisições Frontend
**Erro:** Request timeout após 30 segundos

**Soluções:**
1. **Para máquinas limitadas:**
   ```bash
   # Remover Mistral, manter apenas TinyLlama
   cd models && mv mistral*.gguf mistral.backup
   docker-compose restart api
   ```

2. **Aumentar timeout no frontend:**
   ```javascript
   // Em cada página HTML, aumentar max-time
   fetch(url, { signal: AbortSignal.timeout(60000) }) // 60s
   ```

---

## ⚡ Otimizações de Performance

### Máquina com Pouca RAM (<4GB)
```bash
# Usar apenas TinyLlama
cd models
mkdir backup && mv mistral*.gguf backup/

# Verificar uso apenas do modelo rápido
curl http://localhost/api/models
# Deve mostrar apenas TinyLlama
```

### Máquina com Boa Performance (>8GB RAM)
```bash
# Manter ambos os modelos para sistema híbrido
ls models/
# Deve ter: tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf E mistral-7b-instruct-v0.2.Q4_K_M.gguf

# Verificar seleção automática
curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{"prompt":"teste","technique":"recon"}'
# Deve usar TinyLlama (~5s)

curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{"prompt":"análise complexa","technique":"advanced_analysis"}'  
# Deve usar Mistral (~30s)
```

---

## 🔍 Ferramentas de Diagnóstico

### Script de Diagnóstico Rápido
```bash
#!/bin/bash
echo "=== CyberAI System Check ==="
echo "1. Modelos disponíveis:"
ls -la models/*.gguf

echo "2. API Status:"
curl -s http://localhost:8000/api/models || echo "API não responde"

echo "3. Containers Docker:"
docker-compose ps

echo "4. Logs recentes da API:"
docker-compose logs --tail=5 api

echo "5. Teste rápido TinyLlama:"
curl -s -X POST http://localhost/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","technique":"recon","max_tokens":10}' \
  | grep -o '"model_used":"[^"]*"'
```

### Verificação Manual Completa
```bash
# 1. Verificar modelos
ls -la models/
# Esperado: 2 arquivos .gguf (tinyllama + mistral) OU apenas tinyllama

# 2. Testar API
curl http://localhost/api/models
# Esperado: JSON com informações dos modelos

# 3. Teste funcional
curl -X POST http://localhost/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"nmap","technique":"recon","max_tokens":20}'
# Esperado: Resposta em ~5-10 segundos

# 4. Verificar frontend
curl http://localhost/
# Esperado: HTML da página inicial
```

---

## 🆘 Suporte e Recursos

### Logs Importantes
```bash
# API logs (Docker)
docker-compose logs -f api

# Web logs (Docker)  
docker-compose logs -f web

# Sistema local
tail -f ~/.local/share/cyberai/logs/api.log
```

### Restaurar Estado Limpo
```bash
# Parar tudo
docker-compose down

# Limpar containers e imagens
docker system prune -a

# Recriar do zero
git pull origin main
docker-compose up --build -d
```

### Community & Issues
- **GitHub Issues:** https://github.com/dionebr/cyberai/issues
- **Documentação:** https://github.com/dionebr/cyberai/tree/main/docs
- **Discord:** [Em breve]
