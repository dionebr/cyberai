import { formatCodeBlock } from './main.js';

export async function sendMessage(message, context, technique, target) {
	if (!message) return;
	try {
		const response = await fetch('http://localhost:8000/generate', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ prompt: message, context, technique, target })
		});
		const data = await response.json();
		return data.response;
	} catch (error) {
		return 'Erro de conexão. Verifique se a API está rodando.';
	}
}
