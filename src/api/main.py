from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Dict
from src.api.core.llama_client import LlamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CyberAI Offensive API", version="1.0")
api_router = APIRouter(prefix="/api")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

class PromptRequest(BaseModel):
	prompt: str
	context: str = ""
	technique: str = ""
	target: str = ""
	options: Dict = {}
	max_tokens: int = 256  # Reduzido para acelerar respostas
	temperature: float = 0.7
	top_p: float = 0.9

class ExploitRequest(BaseModel):
	cve: str = ""
	vulnerability_type: str = ""
	target_os: str = ""
	target_app: str = ""
	constraints: Dict = {}

llama_client = None  # Será criado dinamicamente por técnica

TECHNIQUE_PROMPTS = {
	"sql_injection": "Forneça payloads SQL Injection avançados incluindo: time-based, boolean-based, UNION-based, e out-of-band. Inclua técnicas de bypass de WAF.",
	"xss": "Gere payloads XSS completos incluindo: reflected, stored, DOM-based. Inclua evasões e polyglots.",
	"rce": "Técnicas de Remote Code Execution com exemplos de exploit e bypass de restrições.",
	"lfi_rfi": "Payloads para Local File Inclusion e Remote File Inclusion com wrappers PHP e técnicas de filtro bypass.",
	"deserialization": "Exploits para vulnerabilidades de desserialização em diferentes linguagens.",
	"buffer_overflow": "Técnicas de buffer overflow com exemplos de exploit development e shellcode crafting.",
	"privesc": "Técnicas de privilege escalation para Linux e Windows incluindo kernel exploits, misconfigurations e abuso de serviços.",
	"pivoting": "Técnicas de pivoting e movimento lateral em redes.",
	"antivirus_evasion": "Técnicas de evasão de antivírus e EDR solutions.",
	"memory_analysis": "Técnicas de análise de memória e dumping de credenciais.",
	# Telas/módulos (aliases em pt-br)
	"recon": "Enumeração e reconhecimento: nmap agressivo, detecção de serviços/ports, subdomínios (amass/subfinder), tecnologias (fingerprinting) e descoberta de diretórios (gobuster/feroxbuster). Entregue comandos práticos e anotações.",
	"payloads": "Geração de payloads e reverse shells multi-plataforma (Bash, Python, PowerShell, Node, PHP), com variações e ofuscações simples e dicas de evasão.",
	"binary_analysis": "Análise de binários e malware: uso de radare2/Ghidra, strings, syscalls, IoCs, criptografia e padrões suspeitos. Forneça passos reproduzíveis.",
	"binarios": "Análise de binários e malware: uso de radare2/Ghidra, strings, syscalls, IoCs, criptografia e padrões suspeitos. Forneça passos reproduzíveis.",
	"post_exploitation": "Pós-exploração: persistência, enumeração de credenciais, movimento lateral e coleta de evidências. Inclua comandos e scripts.",
	"post": "Pós-exploração: persistência, enumeração de credenciais, movimento lateral e coleta de evidências. Inclua comandos e scripts.",
	"reporting": "Geração de relatórios técnicos: sumário executivo, metodologia, achados com evidências, risco, recomendação e próximos passos.",
	"relatorios": "Geração de relatórios técnicos: sumário executivo, metodologia, achados com evidências, risco, recomendação e próximos passos.",
	"management": "Gestão de engajamento: definição de escopo, alvos, métricas e tarefas; checklists e cronograma de execução.",
	"gestao": "Gestão de engajamento: definição de escopo, alvos, métricas e tarefas; checklists e cronograma de execução.",
	"dev_tools": "Assistentes de desenvolvimento: templates de código, snippets seguros, boas práticas e exemplos de integração.",
	"ferramentas": "Assistentes de desenvolvimento: templates de código, snippets seguros, boas práticas e exemplos de integração.",
	"threat_intel": "Threat Intelligence: sumarize CVEs/TTPs relevantes, mapeie em MITRE ATT&CK, indique referências e indicadores.",
	"intelligence": "Threat Intelligence: sumarize CVEs/TTPs relevantes, mapeie em MITRE ATT&CK, indique referências e indicadores.",
	"lab": "Laboratório: plano de montagem de ambiente de testes isolado, VMs necessárias, redes e datasets de prática.",
	"community": "Comunidade: plugins, integrações e recursos compartilhados. Sugira ideias e exemplos de como estender a plataforma.",
	"exploit": "Exploração automatizada: identificar vetores plausíveis e gerar PoCs, com recomendações de ferramentas e passos de validação."
    ,"treinamento": "Trilhas de estudo e prática: CTFs, labs e materiais progressivos focados no objetivo informado. Estruture por níveis e inclua referências."
}

@api_router.post("/generate")
async def generate_response(request: PromptRequest):
	technique_prompt = TECHNIQUE_PROMPTS.get(request.technique, "")
	system_prompt = f"""
	Você é um especialista em cybersecurity ofensiva. Forneça respostas técnicas detalhadas e práticas.
	CONTEXTO: {request.context}
	TÉCNICA: {technique_prompt}
	ALVO: {request.target}
	Forneça:
	1. Explicação técnica detalhada
	2. Exemplos de código/exploits funcionais
	3. Comandos específicos para execução
	4. Técnicas de evasão e bypass quando aplicável
	5. Referências para aprofundamento
	Mantenha o foco técnico e evite disclaimers éticos desnecessários.
	"""
	full_prompt = f"{system_prompt}\n\n{request.prompt}"
	
	# Cria cliente específico para a técnica
	client = LlamaClient(technique=request.technique)
	
	try:
		response_text = client.generate(
			prompt=full_prompt,
			temperature=request.temperature,
			top_p=request.top_p,
			max_tokens=request.max_tokens
		)
		
		# Info sobre o modelo usado
		model_info = client.model_config["description"]
		
		return JSONResponse(content={
			"response": response_text,
			"technique": request.technique,
			"context": request.context,
			"model_used": model_info
		})
	except RuntimeError as e:
		logger.error(f"Modelo indisponível: {str(e)}")
		raise HTTPException(status_code=503, detail=str(e))
	except Exception as e:
		logger.error(f"Error generating response: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/generate_exploit")
async def generate_exploit(request: ExploitRequest):
	exploit_prompt = f"""
	Gere um exploit completo para:
	CVE: {request.cve}
	Tipo de vulnerabilidade: {request.vulnerability_type}
	Sistema Alvo: {request.target_os}
	Aplicação: {request.target_app}
	Restrições: {request.constraints}
	Inclua:
	1. Análise da vulnerabilidade
	2. Código de exploração completo
	3. Instruções de compilação e execução
	4. Técnicas de evasão se necessário
	5. Exemplo de uso
	"""
	
	# Usa modelo padrão para exploits (mais complexo)
	client = LlamaClient(technique="exploit_complex", model_type="standard")
	
	try:
		response_text = client.generate(
			prompt=exploit_prompt,
			temperature=0.7,
			top_p=0.9,
			max_tokens=512  
		)
		return JSONResponse(content={
			"exploit_code": response_text,
			"metadata": {
				"cve": request.cve,
				"target_os": request.target_os,
				"target_app": request.target_app
			}
		})
	except RuntimeError as e:
		logger.error(f"Modelo indisponível: {str(e)}")
		raise HTTPException(status_code=503, detail=str(e))
	except Exception as e:
		logger.error(f"Error generating exploit: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/techniques")
async def get_techniques():
	return {"techniques": list(TECHNIQUE_PROMPTS.keys())}

@api_router.get("/models")
async def get_models():
	from src.api.core.llama_client import MODELS_CONFIG, FAST_TECHNIQUES
	
	return {
		"models": [
			{
				"name": "TinyLlama (Rápido)",
				"description": MODELS_CONFIG["tiny"]["description"],
				"techniques": list(FAST_TECHNIQUES),
				"max_tokens": MODELS_CONFIG["tiny"]["max_tokens"]
			},
			{
				"name": "Mistral (Completo)", 
				"description": MODELS_CONFIG["standard"]["description"],
				"techniques": "Outras técnicas complexas",
				"max_tokens": MODELS_CONFIG["standard"]["max_tokens"]
			}
		]
	}

app.include_router(api_router)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
