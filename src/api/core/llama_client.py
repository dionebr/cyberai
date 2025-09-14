import os
from llama_cpp import Llama

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf'))

class LlamaClient:
    def __init__(self, model_path=MODEL_PATH, n_ctx=1024, n_threads=4, n_batch=32):
        self.model = Llama(model_path=model_path, n_ctx=n_ctx, n_threads=n_threads, n_batch=n_batch)

    def generate(self, prompt, temperature=0.7, top_p=0.9, max_tokens=256):
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["<|end|>"]
        )
        return output["choices"][0]["text"].strip()
