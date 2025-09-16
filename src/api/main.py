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
	max_tokens: int = 768  # Aumentado para respostas mais completas
	temperature: float = 0.7
	top_p: float = 0.9
	preferred_model: str = "auto"  # "auto", "tinyllama", "mistral"

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
	"payloads": "Geração de payloads ofensivos completos e funcionais: reverse shells multi-plataforma (Bash, Python, PowerShell, Node, PHP, C#, Java), bind shells, meterpreter payloads, web shells, variações com ofuscação, encoding, bypass de firewall e evasão de antivírus. Forneça código funcional, instruções de uso e variações para diferentes cenários.",
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
	
	# Sistema de prompts otimizado para contexto limitado
	system_prompt = f"""CyberAI - Especialista em Cybersecurity Ofensiva

FOCO: {technique_prompt if technique_prompt else "Cybersecurity geral"}
CONTEXTO: {request.context if request.context else "N/A"}
ALVO: {request.target if request.target else "Sistemas diversos"}

FORMATO DE RESPOSTA:
🎯 Objetivo e uso prático
🔧 Código/comandos funcionais comentados  
⚡ Variações e otimizações
🛡️ Evasão/bypass quando aplicável
📚 Referências técnicas

Regras: Seja técnico, detalhado, funcional. Use markdown para código. Evite disclaimers.

PERGUNTA:"""
	
	full_prompt = f"{system_prompt}\n{request.prompt}"
	
	# Determinar modelo baseado no modelo preferido
	model_type = "auto"
	if request.preferred_model == "tinyllama":
		model_type = "tiny"
	elif request.preferred_model == "mistral":
		model_type = "standard"
	
	# Cria cliente específico para a técnica/modelo
	client = LlamaClient(technique=request.technique, model_type=model_type)
	
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

@api_router.get("/gpu-status")
async def get_gpu_status():
	"""
	Endpoint para verificar o status atual da GPU
	"""
	try:
		import subprocess
		from src.api.core.llama_client import detect_gpu_support
		
		# Verificar se NVIDIA está disponível no sistema
		try:
			result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
			nvidia_available = result.returncode == 0
			if nvidia_available:
				# Extrair info básica da GPU
				lines = result.stdout.split('\n')
				gpu_info = "GPU detectada"
				for line in lines:
					if "GTX" in line or "RTX" in line or "GeForce" in line:
						gpu_info = line.split()[2:5]  # Nome da GPU
						gpu_info = " ".join(gpu_info)
						break
			else:
				gpu_info = None
		except:
			nvidia_available = False
			gpu_info = None
		
		# Verificar se llama-cpp-python tem suporte CUDA
		cuda_support = detect_gpu_support()
		
		# Determinar status
		if nvidia_available and cuda_support:
			status = "GPU Disponível e Ativada"
			gpu_enabled = True
		elif nvidia_available and not cuda_support:
			status = "GPU Detectada (CUDA não compilado)"
			gpu_enabled = False
		else:
			status = "CPU Only"
			gpu_enabled = False
		
		return JSONResponse(content={
			"gpu_enabled": gpu_enabled,
			"nvidia_available": nvidia_available,
			"cuda_support": cuda_support,
			"status": status,
			"gpu_info": gpu_info or "Nenhuma GPU detectada"
		})
		
	except Exception as e:
		logger.error(f"Erro ao verificar status GPU: {str(e)}")
		return JSONResponse(content={
			"gpu_enabled": False,
			"nvidia_available": False,
			"cuda_support": False,
			"status": "Erro ao verificar GPU",
			"gpu_info": str(e)
		})

class GPUToggleRequest(BaseModel):
	enable_gpu: bool

@api_router.post("/toggle-gpu")
async def toggle_gpu_mode(request: GPUToggleRequest):
	"""
	Endpoint para alternar entre modo CPU e GPU
	Usa o gpu_manager.py para fazer a troca real dos containers
	"""
	try:
		import subprocess
		import os
		import asyncio
		
		# Caminho do projeto
		project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		gpu_manager_path = os.path.join(project_path, "gpu_manager.py")
		
		target_mode = "gpu" if request.enable_gpu else "cpu"
		
		logger.info(f"🔄 Tentando alternar para modo {target_mode.upper()}...")
		
		try:
			# Executar gpu_manager em background
			process = subprocess.Popen(
				["python", gpu_manager_path, target_mode],
				cwd=project_path,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)
			
			# Aguardar conclusão (máximo 30 segundos)
			stdout, stderr = process.communicate(timeout=30)
			
			if process.returncode == 0:
				logger.info(f"✅ Modo {target_mode.upper()} ativado com sucesso")
				
				# Aguardar containers estarem prontos
				await asyncio.sleep(3)
				
				return JSONResponse(content={
					"success": True,
					"gpu_enabled": request.enable_gpu,
					"status": f"{target_mode.upper()} Ativado",
					"message": f"Sistema alterado para modo {target_mode.upper()} com sucesso!",
					"details": stdout.strip() if stdout else ""
				})
			else:
				error_msg = stderr.strip() if stderr else "Erro desconhecido"
				logger.error(f"❌ Erro ao alternar para {target_mode}: {error_msg}")
				
				return JSONResponse(content={
					"success": False,
					"gpu_enabled": not request.enable_gpu,  # Manter estado anterior
					"status": "Erro na Alternação",
					"message": f"Erro ao alternar para {target_mode}: {error_msg}"
				}, status_code=400)
				
		except subprocess.TimeoutExpired:
			process.kill()
			logger.error("⏰ Timeout ao alternar modo GPU/CPU")
			return JSONResponse(content={
				"success": False,
				"gpu_enabled": not request.enable_gpu,
				"status": "Timeout",
				"message": "Timeout ao alternar modo. Tente novamente."
			}, status_code=408)
			
	except Exception as e:
		logger.error(f"Erro crítico ao alternar GPU: {str(e)}")
		return JSONResponse(content={
			"success": False,
			"gpu_enabled": False,
			"status": "Erro Crítico",
			"message": f"Erro interno: {str(e)}"
		}, status_code=500)

app.include_router(api_router)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
