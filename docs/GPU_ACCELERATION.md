# Aceleração GPU para CyberAI

## 🎮 Visão Geral

O CyberAI agora suporta aceleração GPU NVIDIA para aumentar significativamente a velocidade de geração de respostas.

## 📋 Pré-requisitos

✅ **Já configurado no seu sistema:**
- GPU NVIDIA GTX 1650 (4GB VRAM) 
- Driver NVIDIA 580.82.09
- CUDA 13.0 suportado
- nvidia-container-toolkit instalado

## ⚡ Benefícios de Performance

| Modelo | CPU (atual) | GPU (novo) | Melhoria |
|--------|-------------|------------|----------|
| TinyLlama 1.1B | ~8-10s | ~3-4s | 2-3x mais rápido |
| Mistral 7B | ~15-20s | ~4-6s | 4-5x mais rápido |

## 🚀 Como Usar

### Modo GPU (Recomendado)
```bash
# Iniciar com aceleração GPU
docker-compose -f docker-compose.gpu.yml up --build

# Para parar
docker-compose -f docker-compose.gpu.yml down
```

### Modo CPU (Padrão)
```bash
# Iniciar sem GPU
docker-compose up

# Para parar  
docker-compose down
```

## 🔧 Configuração Automática

O sistema detecta automaticamente se há suporte GPU:
- ✅ **Com GPU**: Usa CUDA automaticamente
- ⚙️ **Sem GPU**: Funciona normalmente na CPU

## 📊 Monitoramento GPU

Verifique o uso da GPU durante inferência:
```bash
# Ver status da GPU
nvidia-smi

# Monitoramento em tempo real
watch -n 1 nvidia-smi
```

## 🛠️ Solução de Problemas

### GPU não detectada
```bash
# Verificar drivers
nvidia-smi

# Reinstalar container toolkit se necessário
sudo pacman -S nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Erro de memória VRAM
A GTX 1650 (4GB) pode carregar:
- ✅ TinyLlama 1.1B (600MB) + sistema
- ✅ Mistral 7B Q4 (4GB) - uso total de VRAM
- ❌ Modelos maiores (>4GB) - usar CPU

### Build lento na primeira vez
O primeiro build baixa ~3GB de imagem CUDA base:
- ⏱️ Tempo estimado: 10-15 min (depende da internet)
- 💾 Espaço necessário: ~6GB adicional
- 🔄 Próximos builds são mais rápidos (cache)

## 🎯 Configurações Otimizadas

O sistema usa configurações otimizadas automaticamente:

**TinyLlama GPU:**
- 35 camadas na GPU (todas)
- Batch size: 512
- Context: 768 tokens

**Mistral 7B GPU:**  
- 32 camadas na GPU (máximo)
- Batch size: 512
- Context: 2048 tokens

## 📈 Próximos Passos

1. **Modelos maiores**: Quando houver GPU com mais VRAM
2. **Quantização**: Modelos INT4/INT8 para melhor velocidade
3. **Multi-GPU**: Suporte para múltiplas GPUs
4. **AMD GPU**: Suporte ROCm para GPUs AMD