import requests

class OllamaClient:
	def __init__(self, base_url="http://localhost:11434"):
		self.base_url = base_url

	def generate(self, model, prompt, options=None, stream=False, timeout=120):
		url = f"{self.base_url}/api/generate"
		payload = {
			"model": model,
			"prompt": prompt,
			"stream": stream,
			"options": options or {}
		}
		response = requests.post(url, json=payload, timeout=timeout)
		response.raise_for_status()
		return response.json()

	def list_models(self):
		url = f"{self.base_url}/api/tags"
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
