# Guia de Prompts - CyberAI

## 🧠 Sistema Híbrido: Prompts Otimizados

O CyberAI usa **dois modelos de IA** com especialidades diferentes. Use os prompts adequados para cada modelo:

---

## ⚡ Prompts para TinyLlama (Ultra-Rápido)
*Respostas em 5-10 segundos - Ideal para tarefas práticas e comandos*

### 🔍 Reconhecimento (`technique: "recon"`)
```json
{
  "prompt": "Comando nmap completo para 10.10.11.123 com detecção de versão",
  "technique": "recon",
  "target": "10.10.11.123"
}
```
**Saída esperada:** Comandos nmap específicos e práticos

### 💻 Payloads (`technique: "payloads"`)
```json
{
  "prompt": "Reverse shell bash e python para 10.10.14.5:4444",
  "technique": "payloads", 
  "target": "10.10.14.5:4444"
}
```
**Saída esperada:** Comandos de reverse shell prontos para usar

### 🌐 Web Exploits
```json
{
  "prompt": "Payloads XSS para contornar filtros básicos",
  "technique": "xss",
  "context": "Input field com filtro de script tags"
}
```

```json
{
  "prompt": "SQL injection para bypass de login admin",  
  "technique": "sql_injection",
  "context": "MySQL login form"
}
```

### 🔓 Exploração Rápida (`technique: "exploit"`)
```json
{
  "prompt": "PoC para CVE-2023-12345 em Apache 2.4.50",
  "technique": "exploit",
  "target": "Apache 2.4.50"
}
```

### 📈 Pós-Exploração (`technique: "post"`) 
```json
{
  "prompt": "Comandos de enumeração local Linux após initial access",
  "technique": "post",
  "context": "Shell como www-data"
}
```

---

## 🎯 Prompts para Mistral (Análise Profunda)
*Respostas em 20-30 segundos - Ideal para análises complexas*

### 🔬 Análise Detalhada
```json
{
  "prompt": "Análise forense completa deste código malicioso: [CÓDIGO_COMPLEXO]",
  "technique": "malware_analysis",
  "context": "Binário suspeito encontrado em /tmp/"
}
```

### ⚙️ Exploit Development Avançado
```json
{
  "prompt": "Desenvolver exploit ROP chain para bypass ASLR+DEP no Windows 10", 
  "technique": "advanced_exploit",
  "context": "Vulnerabilidade heap overflow em aplicação custom"
}
```

---

## 🎯 Prompts por Módulo

### 🟢 Reconhecimento
**Prompt Básico (TinyLlama):**
> "Enumerar subdomínios de target.com"

**Prompt Avançado (Mistral):**
> "Desenvolva uma metodologia completa de OSINT para organização target.com incluindo infraestrutura, funcionários e tecnologias, considerando técnicas de evasão de detecção"

### 🔵 Payloads  
**Prompt Básico (TinyLlama):**
> "Reverse shell PowerShell ofuscado para Windows"

**Prompt Avançado (Mistral):**
> "Desenvolva um framework de C2 custom em Go com técnicas de domain fronting, encrypt-then-MAC e heartbeat randomizado para evasão de EDR enterprise"

### 🟣 Análise de Binários
**Prompt Básico (TinyLlama):**
> "Comandos radare2 para análise inicial de malware.exe"

**Prompt Avançado (Mistral):**
> "Análise comportamental profunda de APT29 variant, incluindo técnicas anti-sandbox, processo injection methods, e comunicação C2 via DNS tunneling"

### 🔴 Exploração
**Prompt Básico (TinyLlama):**
> "PoC para explorar EternalBlue (MS17-010)"

**Prompt Avançado (Mistral):**
> "Desenvolva exploit 0-day para vulnerabilidade de race condition em kernel Linux 5.15, incluindo heap spraying, KASLR bypass e privilege escalation"

### 🟡 Pós-Exploração
**Prompt Básico (TinyLlama):**
> "Comandos para persistência básica Linux"

**Prompt Avançado (Mistral):**
> "Estratégia completa de movimento lateral em ambiente Active Directory com 5000+ hosts, incluindo Kerberoasting, Golden Ticket, e evasão de Microsoft Defender for Identity"

---

## 🎨 Templates de Prompt Otimizados

### 📋 Template para Máquinas HTB/THM
```json
{
  "prompt": "Estou explorando a máquina [NOME] do [PLATAFORMA]. Portas abertas: [PORTAS]. Serviços: [SERVIÇOS]. Próximos passos de enumeração?",
  "technique": "recon",
  "context": "HTB machine enumeration",
  "target": "10.10.10.123"
}
```

### 🔧 Template para CTF
```json
{
  "prompt": "Challenge CTF de [CATEGORIA]: [DESCRIÇÃO]. Pistas: [HINTS]. Approach recomendado?",
  "technique": "ctf_challenge", 
  "context": "Reverse Engineering CTF"
}
```

### 📊 Template para Red Team
```json
{
  "prompt": "Red team assessment de [ORGANIZAÇÃO]. Objetivos: [GOALS]. Restrições: [CONSTRAINTS]. Metodologia de approach?",
  "technique": "red_team",
  "context": "Corporate environment assessment"
}
```

---

## 💡 Dicas de Prompt Engineering

### ✅ Prompts Eficazes (TinyLlama)
- **Específicos:** "nmap scan para WordPress" ✅
- **Diretos:** "comando sqlmap básico" ✅  
- **Práticos:** "reverse shell linux" ✅

### ❌ Prompts Inadequados (TinyLlama)
- **Muito abstratos:** "explique filosofia da segurança" ❌
- **Muito longos:** "análise completa de 500 linhas de código" ❌
- **Muito complexos:** "desenvolva framework enterprise" ❌

### ✅ Prompts Eficazes (Mistral)
- **Análises profundas:** "analise este APT campaign detalhadamente"
- **Desenvolvimento:** "crie exploit chain completo"  
- **Estratégicos:** "metodologia de red team para ambiente enterprise"

### 🎯 Maximizar Qualidade das Respostas

1. **Contexto específico:**
   ```json
   "context": "Ubuntu 20.04, Apache 2.4.41, PHP 7.4"
   ```

2. **Target bem definido:**
   ```json  
   "target": "10.10.11.123:8080/admin"
   ```

3. **Técnica apropriada:**
   ```json
   "technique": "web_exploit" // Para Mistral
   "technique": "xss"         // Para TinyLlama
   ```

---

## 📈 Exemplos Práticos por Plataforma

### 🏴 HackTheBox
```bash
# TinyLlama (rápido)
curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{
  "prompt": "Enumerar SMB shares em 10.10.10.123",
  "technique": "recon",
  "target": "10.10.10.123"
}'

# Mistral (análise profunda) 
curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{
  "prompt": "Análise completa de Active Directory vulnerabilities encontradas via Bloodhound em ambiente corporativo",
  "technique": "ad_analysis", 
  "context": "Domain with 500 users, multiple DCs"
}'
```

### 🟧 TryHackMe
```bash  
# Rooms básicas (TinyLlama)
curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{
  "prompt": "Comandos básicos para room OWASP Top 10",
  "technique": "web_exploit"
}'

# Rooms avançadas (Mistral)
curl -X POST http://localhost/api/generate -H "Content-Type: application/json" -d '{
  "prompt": "Solução completa para Advanced Persistent Threat room incluindo análise de IOCs, timeline reconstruction e attribution",
  "technique": "threat_hunting"
}'
```

---

## 🎯 Prompt Templates por Velocidade

### ⚡ Ultra-Rápido (5s) - Comandos Práticos
```
"[COMANDO] para [OBJETIVO] em [TARGET]"
Exemplo: "nmap para descobrir SSH em 192.168.1.0/24"
```

### 🚀 Rápido (10s) - Explicações Técnicas  
```
"Como [TÉCNICA] funciona em [CONTEXTO]? Inclua exemplo."
Exemplo: "Como SQL injection funciona em MySQL? Inclua exemplo."
```

### 🎯 Detalhado (30s) - Análises Complexas
```
"Análise detalhada de [FENÔMENO] considerando [FATORES] e impacto em [AMBIENTE]"
Exemplo: "Análise detalhada de APT29 TTPs considerando MITRE ATT&CK e impacto em ambiente Windows Enterprise"
```
