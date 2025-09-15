import os

# Configuração dos modelos disponíveis
MODELS_CONFIG = {
    "tiny": {
        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf')),
        "n_ctx": 512,
        "n_threads": 8, 
        "n_batch": 64,
        "max_tokens": 128,
        "description": "Modelo rápido para tarefas simples (600MB)"
    },
    "standard": {
        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')),
        "n_ctx": 1024,
        "n_threads": 4,
        "n_batch": 32, 
        "max_tokens": 256,
        "description": "Modelo completo para tarefas complexas (4GB)"
    }
}

# Técnicas que usam modelo rápido (tarefas simples)
FAST_TECHNIQUES = {
    "recon", "payloads", "post", "binarios", "exploit", 
    "relatorios", "gestao", "ferramentas", "intelligence",
    "buffer_overflow", "xss", "sql_injection", "rce", 
    "lfi_rfi", "privesc", "lab", "treinamento"
}

class LlamaClient:
    def __init__(self, technique="", model_type="auto"):
        self.model = None
        self.technique = technique
        self.current_model_config = None
        
        # Seleciona o modelo baseado na técnica
        if model_type == "auto":
            model_key = "tiny" if technique in FAST_TECHNIQUES else "standard"
        else:
            model_key = model_type
            
        self.model_config = MODELS_CONFIG.get(model_key, MODELS_CONFIG["tiny"])
        
    def _ensure_loaded(self):
        if self.model is not None and self.current_model_config == self.model_config:
            return
        try:
            from llama_cpp import Llama
        except Exception as e:
            raise RuntimeError("llama-cpp-python não está instalado no ambiente da API.") from e
        if not os.path.exists(self.model_config["path"]):
            raise RuntimeError(
                f"Modelo GGUF não encontrado em {self.model_config['path']}. Baixe o modelo antes de usar."
            )
        
        # Carrega o modelo apenas se mudou
        if self.current_model_config != self.model_config:
            print(f"🚀 Carregando modelo: {self.model_config['description']}")
            self.model = Llama(
                model_path=self.model_config["path"],
                n_ctx=self.model_config["n_ctx"],
                n_threads=self.model_config["n_threads"], 
                n_batch=self.model_config["n_batch"],
                verbose=False
            )
            self.current_model_config = self.model_config

    def generate(self, prompt, temperature=0.7, top_p=0.9, max_tokens=None):
        self._ensure_loaded()
        
        # Usa limite específico do modelo se não especificado
        if max_tokens is None:
            max_tokens = self.model_config["max_tokens"]
        
        # Template para TinyLlama (ChatML format)
        if "tinyllama" in self.model_config["path"]:
            formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        else:
            formatted_prompt = prompt
            
        output = self.model(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["<|im_end|>", "</s>", "\n\n"] if "tinyllama" in self.model_config["path"] else ["<|end|>", "\n\n"]
        )
        return output["choices"][0]["text"].strip()
