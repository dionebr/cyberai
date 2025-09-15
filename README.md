# CyberAI: Assistente Ofensivo de Cibersegurança

**CyberAI** é uma suíte de ferramentas acelerada por LLM (Large Language Model), projetada para apoiar profissionais e entusiastas de cibersegurança em tarefas ofensivas. A plataforma opera de forma **100% offline**, garantindo privacidade e segurança, e serve como um poderoso assistente para treinamento, pentesting e pesquisa em ambientes como HackTheBox, TryHackMe e VulnHub.

![CyberAI Screenshot](https://raw.githubusercontent.com/dionebr/cyberai/main/docs/images/cyberai-showcase.png)

---

## ✨ Funcionalidades Principais

-   **LLM Offline:** Utilize modelos de linguagem de ponta (GGUF) sem depender de APIs externas.
-   **Interface Web Intuitiva:** Acesse todas as ferramentas através de uma interface moderna e responsiva.
-   **Suíte de Módulos Especializados:** Cobertura completa do ciclo de pentesting, desde o reconhecimento até a pós-exploração.
-   **Geração de Código e Payloads:** Crie reverse shells, exploits e scripts de automação sob demanda.
-   **Ambiente Dockerizado:** Instalação e execução simplificadas com Docker e Nginx.
-   **Privacidade Total:** Seus dados e interações nunca saem da sua máquina local.

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

3.  **Baixe o modelo LLM:**
    O modelo padrão é o `Mistral-7B-Instruct-v0.2`.
    ```bash
    huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
    ```

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
    -   **Causa:** O arquivo do modelo GGUF não foi encontrado ou `llama-cpp-python` não foi compilado corretamente.
    -   **Solução:**
        1.  Verifique se o arquivo `.gguf` está na pasta `models/`.
        2.  Execute o comando de download do modelo novamente.
        3.  Se o erro persistir, reinstale `llama-cpp-python` com as flags de compilação corretas para sua arquitetura (ex: `CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python`).

-   **Erro 404 em `dist.css` ou `utils.js` (modo local):**
    -   **Causa:** O servidor web foi iniciado na pasta errada.
    -   **Solução:** Certifique-se de iniciar o servidor a partir da raiz do projeto (`/home/dione/cyberai`) e que o comando sirva o diretório `src/web`. Use `npm start`.

-   **Interface não carrega ou módulos não respondem:**
    -   **Causa:** A API pode não estar rodando ou estar bloqueada por um firewall.
    -   **Solução:** Verifique se o processo da API está ativo na porta 8000 e se não há regras de firewall impedindo a conexão.

---

## 💡 Exemplos de Uso

### Chat Interativo
Use o chat flutuante na página inicial para perguntas rápidas.
> "Gere um comando Nmap agressivo para o alvo 10.10.11.123, com detecção de versão e scripts."

### Módulo de Payloads
Acesse o módulo "Payloads" e preencha os campos para gerar reverse shells customizadas.
> **IP:** `10.10.14.2`, **Porta:** `9001`, **Plataforma:** `Linux`

### Exemplo com `curl`
Você pode interagir diretamente com a API:
```bash
curl -X POST http://localhost:8000/generate \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Estou explorando uma máquina Linux e tenho acesso como www-data. Quais os primeiros passos para escalação de privilégios?",
  "technique": "privesc",
  "context": "Kernel: 5.4.0, Distro: Debian 10"
}'
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir novas funcionalidades. Se desejar contribuir com código, por favor, abra um *Pull Request*.

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.