import os

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')
)

class LlamaClient:
    def __init__(self, model_path=MODEL_PATH, n_ctx=1024, n_threads=4, n_batch=32):
        self.model = None
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_batch = n_batch

    def _ensure_loaded(self):
        if self.model is not None:
            return
        try:
            from llama_cpp import Llama
        except Exception as e:
            raise RuntimeError("llama-cpp-python não está instalado no ambiente da API.") from e
        if not os.path.exists(self.model_path):
            raise RuntimeError(
                f"Modelo GGUF não encontrado em {self.model_path}. Baixe o modelo antes de usar."
            )
        self.model = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_batch=self.n_batch,
        )

    def generate(self, prompt, temperature=0.7, top_p=0.9, max_tokens=256):
        self._ensure_loaded()
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["<|end|>"]
        )
        return output["choices"][0]["text"].strip()
