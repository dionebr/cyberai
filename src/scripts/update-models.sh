#!/bin/bash

echo "[+] Atualizando modelos Ollama..."
ollama pull codellama:7b-code-q4_0
ollama pull llama2-uncensored:7b-chat-q4_0
ollama pull cyberdolphin:7b-q4_0
echo "[+] Modelos atualizados!"
