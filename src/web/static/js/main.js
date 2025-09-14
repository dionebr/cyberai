// Funções utilitárias para CyberAI Web
export function formatCodeBlock(text) {
	const codeBlocks = text.match(/```[\s\S]*?```/g);
	let formattedText = text;
	if (codeBlocks) {
		codeBlocks.forEach(block => {
			const codeContent = block.replace(/```(\w+)?\n/, '').replace('```', '');
			const codeHtml = `<pre class="bg-black p-3 rounded overflow-x-auto"><code>${codeContent}</code></pre>`;
			formattedText = formattedText.replace(block, codeHtml);
		});
	}
	return formattedText;
}
