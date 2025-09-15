import os

def detect_gpu_support():
    """Detecta se GPU CUDA está disponível"""
    try:
        import llama_cpp
        # Verifica se llama-cpp-python foi compilado com suporte CUDA
        return hasattr(llama_cpp.Llama, 'n_gpu_layers')
    except ImportError:
        return False

# Configuração dos modelos disponíveis com suporte GPU opcional
MODELS_CONFIG = {
    "tiny": {
        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf')),
        "n_ctx": 768,
        "n_threads": 8, 
        "n_batch": 512 if detect_gpu_support() else 64,
        "n_gpu_layers": 35 if detect_gpu_support() else 0,
        "max_tokens": 256,
        "description": f"Modelo rápido para tarefas simples (600MB){' - GPU Acelerado' if detect_gpu_support() else ''}"
    },
    "standard": {
        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')),
        "n_ctx": 2048,
        "n_threads": 4,
        "n_batch": 512 if detect_gpu_support() else 32,
        "n_gpu_layers": 32 if detect_gpu_support() else 0,
        "max_tokens": 768,
        "description": f"Modelo completo para tarefas complexas (4GB){' - GPU Acelerado' if detect_gpu_support() else ''}"
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
            gpu_layers = self.model_config.get("n_gpu_layers", 0)
            print(f"🚀 Carregando modelo: {self.model_config['description']}")
            if gpu_layers > 0:
                print(f"🎮 GPU Layers: {gpu_layers} (Aceleração GPU ativada)")
            else:
                print("💻 CPU Only (Sem GPU)")
                
            # Parâmetros do modelo com ou sem GPU
            model_params = {
                "model_path": self.model_config["path"],
                "n_ctx": self.model_config["n_ctx"],
                "n_threads": self.model_config["n_threads"],
                "n_batch": self.model_config["n_batch"],
                "verbose": False
            }
            
            # Adicionar GPU layers apenas se disponível
            if gpu_layers > 0:
                model_params["n_gpu_layers"] = gpu_layers
                
            self.model = Llama(**model_params)
            self.current_model_config = self.model_config

    def generate(self, prompt, temperature=0.7, top_p=0.9, max_tokens=None):
        self._ensure_loaded()
        
        # Usa limite específico do modelo se não especificado
        if max_tokens is None:
            max_tokens = self.model_config["max_tokens"]
        
        # Template para TinyLlama (ChatML format)
        if "tinyllama" in self.model_config["path"]:
            formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        # Template para Mistral (Instruct format)
        elif "mistral" in self.model_config["path"]:
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        else:
            formatted_prompt = prompt
            
        output = self.model(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["<|im_end|>", "</s>", "\n\n"] if "tinyllama" in self.model_config["path"] else ["</s>", "[/INST]", "\n\n"]
        )
        return output["choices"][0]["text"].strip()
