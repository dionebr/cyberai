# CyberAI: Assistente Ofensivo de Cibersegurança ⚡

**CyberAI** é uma suíte de ferramentas acelerada por **sistema híbrido de LLMs** (TinyLlama + Mistral), projetada para apoiar profissionais e entusiastas de cibersegurança em tarefas ofensivas. A plataforma opera de forma **100% offline**, garantindo privacidade e segurança, e serve como um poderoso assistente para treinamento, pentesting e pesquisa em ambientes como HackTheBox, TryHackMe e VulnHub.

🚀 **Novo:** Sistema híbrido inteligente que seleciona automaticamente o modelo mais adequado (TinyLlama para velocidade ou Mistral para complexidade), oferecendo **respostas até 20x mais rápidas** para tarefas simples!

![CyberAI Screenshot](https://raw.githubusercontent.com/dionebr/cyberai/main/docs/images/cyberai-showcase.png)

---

## ✨ Funcionalidades Principais

-   🧠 **Sistema Híbrido Inteligente:** Dois modelos LLM trabalhando juntos:
    -   **TinyLlama 1.1B (668MB):** Respostas ultrarrápidas para tarefas simples
    -   **Mistral 7B (4GB):** Alta qualidade para análises complexas
-   ⚡ **Performance Otimizada:** Seleção automática do modelo baseada na complexidade da tarefa
-   🔒 **100% Offline:** Utilize modelos de linguagem de ponta (GGUF) sem depender de APIs externas
-   🖥️ **Interface Web Intuitiva:** Acesse todas as ferramentas através de uma interface moderna e responsiva
-   🎯 **Suíte de Módulos Especializados:** Cobertura completa do ciclo de pentesting, desde o reconhecimento até a pós-exploração
-   💾 **Economia de Recursos:** Ideal para máquinas limitadas - usa apenas 668MB para tarefas comuns
-   🐳 **Ambiente Dockerizado:** Instalação e execução simplificadas com Docker e Nginx
-   🔐 **Privacidade Total:** Seus dados e interações nunca saem da sua máquina local

---

## 🧠 Sistema Híbrido de IA

O CyberAI utiliza um **sistema híbrido inovador** que combina dois modelos de IA para otimizar performance e qualidade:

### ⚡ TinyLlama 1.1B (Modelo Rápido)
- **Tamanho:** 668MB
- **Velocidade:** Respostas em 5-10 segundos  
- **Uso:** Tarefas simples e rápidas
- **Técnicas:** recon, payloads, exploits básicos, relatórios, XSS, SQL injection, etc.

### 🎯 Mistral 7B (Modelo Completo) 
- **Tamanho:** 4GB
- **Qualidade:** Análises detalhadas e complexas
- **Uso:** Tarefas que exigem raciocínio avançado
- **Técnicas:** Análises de malware complexas, desenvolvimento de exploits avançados

### 🔄 Seleção Automática Inteligente
O sistema escolhe automaticamente o modelo mais adequado com base na técnica solicitada, garantindo:
- ⚡ **Velocidade máxima** para tarefas comuns
- 🎯 **Qualidade premium** quando necessário  
- 💾 **Economia de recursos** computacionais
- 📱 **Compatibilidade** com máquinas limitadas

---

## 🚀 Módulos Disponíveis

A plataforma é organizada em 12 módulos, cada um focado em uma área específica do pentesting:

| Módulo | Cor | Descrição |
| :--- | :--- | :--- |
| **Reconhecimento** | 🟢 | Enumeração de alvos, varredura de portas, descoberta de subdomínios e tecnologias. |
| **Payloads** | 🔵 | Geração de reverse shells, stagers e ofuscação para evasão de defesas. |
| **Análise de Binários**| 🟣 | Engenharia reversa, análise de malware e extração de IoCs. |
| **Exploração** | 🔴 | Geração de provas de conceito (PoCs) para CVEs e vulnerabilidades conhecidas. |
| **Pós-Exploração** | 🟡 | Técnicas de persistência, movimento lateral e coleta de credenciais. |
| **Treinamento** | 🌸 | Criação de trilhas de estudo com CTFs, laboratórios e guias práticos. |
| **Relatórios** | 💧 | Estruturação de relatórios técnicos, desde o sumário executivo até as recomendações. |
| **Gestão** | 🟠 | Planejamento de engajamentos, definição de escopo, alvos e métricas. |
| **Dev Tools** | 🍋 | Assistência para desenvolvimento de ferramentas, com templates e snippets seguros. |
| **Threat Intel** | 🍵 | Briefings sobre ameaças, mapeamento de TTPs no MITRE ATT&CK e análise de CVEs. |
| **Laboratório** | 🎀 | Guias para montagem de ambientes de teste seguros e isolados. |
| **Comunidade** | ⚫ | Central para plugins, integrações e recursos compartilhados. |

---

## 🐳 Instalação e Uso (Docker - Recomendado)

Este é o método mais simples e rápido para ter o ambiente completo e funcional.

### Requisitos
-   [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
-   `git`
-   Conexão com a internet (apenas para o primeiro build e download do modelo)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/dionebr/cyberai.git
    cd cyberai
    ```

2.  **Construa e inicie os serviços:**
    O comando a seguir irá construir a imagem da API, baixar o Nginx e iniciar ambos os contêineres em background.
    ```bash
    docker compose up --build -d
    ```

3.  **Acesse a plataforma:**
    Abra seu navegador e acesse:
    -   **URL:** `http://localhost`

4.  **(Opcional) Acompanhe os logs:**
    Para ver os logs da API e do Nginx em tempo real:
    ```bash
    docker compose logs -f
    ```

---

## 💻 Instalação e Uso (Local - Alternativo)

Para usuários que preferem rodar os serviços diretamente no host.

### Requisitos
-   Python 3.10+
-   `git`
-   `npm` (Node.js) para o build do CSS

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/dionebr/cyberai.git
    cd cyberai
    ```

2.  **Execute o script de instalação:**
    Este script irá criar um ambiente virtual, instalar as dependências Python e Node, e compilar o CSS.
    ```bash
    bash src/scripts/install.sh
    ```
    *Nota: O script de download do modelo pode ser executado separadamente, se necessário.*

3.  **Baixe os modelos LLM:**
    
    **TinyLlama (Essencial - 668MB):**
    ```bash
    cd models
    wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf
    ```
    
    **Mistral (Opcional - 4GB):**
    ```bash
    huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
    ```
    
    > 💡 **Dica:** Para máquinas limitadas, use apenas TinyLlama. Para máxima qualidade, baixe ambos os modelos.

4.  **Inicie os serviços:**
    Você precisará de dois terminais.

    -   **Terminal 1: Iniciar a API**
        ```bash
        # Ative o ambiente virtual
        source .venv/bin/activate
        
        # Inicie o servidor da API
        python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
        ```

    -   **Terminal 2: Iniciar o Servidor Web**
        ```bash
        # O script 'npm start' serve a pasta 'src/web' corretamente
        npm start
        ```

5.  **Acesse a plataforma:**
    Abra seu navegador e acesse:
    -   **URL:** `http://localhost:8080/templates/index.html`

---

## 🛠️ Solução de Problemas (Troubleshooting)

-   **Erro 503 `Modelo indisponível` na API:**
    -   **Causa:** O arquivo do modelo GGUF não foi encontrado.
    -   **Solução:**
        ```bash
        # Baixar TinyLlama (essencial)
        cd models
        wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf
        
        # Verificar se foi baixado
        ls -la models/*.gguf
        
        # Reiniciar containers
        docker-compose restart api
        ```

-   **Respostas muito lentas (>30s):**
    -   **Causa:** Tentando usar Mistral em máquina limitada.
    -   **Solução:** Use apenas TinyLlama removendo o arquivo Mistral:
        ```bash
        cd models && mv mistral*.gguf mistral.backup
        docker-compose restart api
        ```

-   **Sistema não seleciona modelo correto:**
    -   **Verificação:** 
        ```bash
        curl http://localhost/api/models
        # Deve mostrar TinyLlama para técnicas rápidas
        ```

-   **Erro 404 em `/api/techniques`:**
    -   **Causa:** Proxy nginx não configurado corretamente.
    -   **Solução:** Use Docker compose (recomendado) ou verifique configuração nginx.

---

### 💡 Exemplos de Uso

### Chat Interativo ⚡
Use o chat flutuante na página inicial para perguntas rápidas com **TinyLlama**.
> **Você:** "Gere um comando Nmap agressivo para o alvo 10.10.11.123"  
> **CyberAI:** Resposta instantânea em ~5 segundos!

### Módulo de Payloads 🚀  
Acesse o módulo "Payloads" e preencha os campos para gerar reverse shells customizadas.
> **IP:** `10.10.14.2`, **Porta:** `9001`, **Plataforma:** `Linux`  
> **Resultado:** Múltiplas variações de reverse shells em segundos

### Sistema Híbrido em Ação 🧠
```bash
# Consulta rápida (TinyLlama - 5s)
curl -X POST http://localhost/api/generate \
-H "Content-Type: application/json" \
-d '{"prompt": "comandos de enumeração SMB", "technique": "recon"}'

# Análise complexa (Mistral - 30s, alta qualidade)  
curl -X POST http://localhost/api/generate \
-H "Content-Type: application/json" \
-d '{"prompt": "desenvolver exploit ROP chain para bypass ASLR", "technique": "advanced_exploit"}'
```

### Verificar Modelos Ativos 📊
```bash
curl http://localhost/api/models
# Mostra quais modelos estão disponíveis e suas especialidades
```

---

## 🎯 Performance Comparison

| Cenário | Modelo | Tempo | Qualidade | Uso Recomendado |
|---------|--------|--------|-----------|-----------------|
| Comandos básicos | TinyLlama | ~5s | ⭐⭐⭐⭐ | Tarefas diárias |
| Enumeração/Recon | TinyLlama | ~5-10s | ⭐⭐⭐⭐ | HTB, THM, CTFs |
| Web exploits | TinyLlama | ~5-10s | ⭐⭐⭐⭐ | OWASP Top 10 |  
| Payloads/Scripts | TinyLlama | ~5-10s | ⭐⭐⭐⭐ | Red team, Pentest |
| Análise profunda | Mistral | ~20-30s | ⭐⭐⭐⭐⭐ | Research, 0days |
| Malware analysis | Mistral | ~20-30s | ⭐⭐⭐⭐⭐ | Forensics, IR |

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir novas funcionalidades. 

### 🚀 Roadmap
- [ ] Integração com mais modelos (CodeLlama, Llama3, etc.)
- [ ] Sistema de caching inteligente
- [ ] Interface mobile otimizada
- [ ] Plugin system para extensões
- [ ] Integração com ferramentas populares (Burp, Metasploit)

### 💡 Como Contribuir
1. Fork o repositório
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⭐ Características Técnicas

### 🧠 Sistema Híbrido de IA
- **TinyLlama 1.1B:** 668MB, ~5-10s por resposta
- **Mistral 7B:** 4GB, ~20-30s por resposta
- **Seleção Automática:** Baseada em complexidade da técnica
- **Fallback Inteligente:** Se um modelo falha, tenta o outro

### ⚡ Otimizações de Performance  
- **Quantização Q4_K_M:** Melhor balanço qualidade/performance
- **Context Length:** Otimizado por modelo (512 vs 1024 tokens)
- **Batch Processing:** Ajustado por arquitetura (64 vs 32)
- **Threading:** CPU cores otimizados por modelo

### 🔒 Segurança e Privacidade
- **100% Offline:** Nenhum dado sai da sua máquina
- **Sem Telemetria:** Zero coleta de dados
- **Modelos Locais:** Controle total sobre IA
- **Containerizado:** Isolamento completo via Docker

## 📊 Especificações Mínimas vs Recomendadas

| Componente | Mínimo (TinyLlama) | Recomendado (Híbrido) |
|------------|--------------------|-----------------------|
| **RAM** | 2GB | 8GB+ |
| **Storage** | 2GB | 10GB |  
| **CPU** | 2 cores | 4+ cores |
| **GPU** | Nenhuma | CUDA/OpenCL (opcional) |
| **OS** | Linux/macOS/Windows | Linux (preferencialmente) |

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

### 🎯 **Experimente agora:**
```bash
git clone https://github.com/dionebr/cyberai.git
cd cyberai  
docker compose up --build -d
# Acesse: http://localhost
```

**CyberAI** - *Onde velocidade encontra inteligência em cibersegurança* 🛡️⚡