def format_code_block(text: str) -> str:
	"""Formata blocos de código para exibição."""
	if text.startswith('```'):
		return f'<pre><code>{text[3:-3]}</code></pre>'
	return text
