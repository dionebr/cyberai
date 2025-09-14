from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.api.core.ollama_client import OllamaClient
from src.api.core.prompt_engine import PromptEngine

router = APIRouter()

class ChatRequest(BaseModel):
	prompt: str
	context: str = ""
	technique: str = ""
	target: str = ""

@router.post("/chat")
async def chat(request: ChatRequest):
	ollama = OllamaClient()
	engine = PromptEngine()
	system_prompt = f"Você é um especialista em cybersecurity ofensiva. CONTEXTO: {request.context} TÉCNICA: {request.technique} ALVO: {request.target}"
	full_prompt = engine.build_prompt(system_prompt, request.prompt)
	try:
		result = ollama.generate("cyberhack", full_prompt)
		return {"response": result["response"]}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
