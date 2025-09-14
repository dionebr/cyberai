from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Dict
from src.api.core.llama_client import LlamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CyberAI Offensive API", version="1.0")

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
	max_tokens: int = 512  # Novo campo para limitar tokens
	temperature: float = 0.7
	top_p: float = 0.9

class ExploitRequest(BaseModel):
	cve: str = ""
	vulnerability_type: str = ""
	target_os: str = ""
	target_app: str = ""
	constraints: Dict = {}

llama_client = LlamaClient()

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
	"memory_analysis": "Técnicas de análise de memória e dumping de credenciais."
}

@app.post("/generate")
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
	try:
		response_text = llama_client.generate(
			prompt=full_prompt,
			temperature=request.temperature,
			top_p=request.top_p,
			max_tokens=request.max_tokens
		)
		return {
			"response": response_text,
			"technique": request.technique,
			"context": request.context
		}
	except Exception as e:
		logger.error(f"Error generating response: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_exploit")
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
	try:
		response_text = llama_client.generate(
			prompt=exploit_prompt,
			temperature=0.7,
			top_p=0.9,
			max_tokens=1024  # Reduzido para otimizar tempo
		)
		return {
			"exploit_code": response_text,
			"metadata": {
				"cve": request.cve,
				"target_os": request.target_os,
				"target_app": request.target_app
			}
		}
	except Exception as e:
		logger.error(f"Error generating exploit: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))

@app.get("/techniques")
async def get_techniques():
	return {"techniques": list(TECHNIQUE_PROMPTS.keys())}

@app.get("/models")
async def get_models():
	return {"models": ["llama-2-7b.Q4_K_M.gguf"]}

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
