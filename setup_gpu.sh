#!/bin/bash

# Script de instalação GPU para CyberAI
# Instala llama-cpp-python com suporte CUDA

echo "🎮 CyberAI GPU Setup"
echo "=" * 50

# Verificar se CUDA está disponível
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ CUDA/NVIDIA não encontrado no sistema!"
    echo "Instale os drivers NVIDIA primeiro."
    exit 1
fi

echo "✅ CUDA detectado!"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits

# Verificar se nvidia-container-toolkit está instalado
if ! command -v nvidia-ctk &> /dev/null; then
    echo "⚠️  nvidia-container-toolkit não encontrado"
    echo "Instalando nvidia-container-toolkit..."
    sudo pacman -S nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
fi

echo "✅ nvidia-container-toolkit configurado!"

# Criar Dockerfile GPU
echo "🔧 Criando Dockerfile.gpu..."

cat > Dockerfile.gpu << 'EOF'
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential cmake curl git && \
    rm -rf /var/lib/apt/lists/*

# Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
ENV FORCE_CMAKE=1
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=on"

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel

# Install llama-cpp-python with CUDA support
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-deps

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Criar docker-compose.gpu.yml
echo "🔧 Criando docker-compose.gpu.yml..."

cat > docker-compose.gpu.yml << 'EOF'
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.gpu
    network_mode: host
    volumes:
      - .:/app
    restart: always
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
  web:
    image: nginx:alpine
    network_mode: host
    volumes:
      - ./src/web/templates:/usr/share/nginx/html
      - ./src/web/static:/usr/share/nginx/html/static
      - ./config/nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api
EOF

echo "✅ Arquivos GPU criados!"
echo ""
echo "🚀 Para usar com GPU, execute:"
echo "   docker-compose -f docker-compose.gpu.yml up --build"
echo ""
echo "🔄 Para voltar ao modo CPU:"
echo "   docker-compose up"
echo ""
echo "⚡ Performance esperada:"
echo "   - TinyLlama: 2-3x mais rápido"  
echo "   - Mistral 7B: 4-5x mais rápido"