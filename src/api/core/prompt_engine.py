class PromptEngine:
	def __init__(self):
		pass

	def build_prompt(self, system_prompt, user_prompt):
		return f"{system_prompt}\n\n{user_prompt}"
