#!/usr/bin/env python3
"""
Script para executar CyberAI com aceleração GPU
Instala automaticamente llama-cpp-python com suporte CUDA se necessário
"""
import subprocess
import sys
import os

def check_cuda():
    """Verifica se CUDA está disponível no sistema"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_llama_cpp_cuda():
    """Instala llama-cpp-python com suporte CUDA"""
    print("🚀 Instalando llama-cpp-python com suporte CUDA...")
    
    env = os.environ.copy()
    env['CMAKE_ARGS'] = '-DLLAMA_CUBLAS=on'
    env['FORCE_CMAKE'] = '1'
    
    cmd = [sys.executable, '-m', 'pip', 'install', 'llama-cpp-python', '--force-reinstall', '--no-deps', '--user']
    
    result = subprocess.run(cmd, env=env)
    return result.returncode == 0

def check_llama_cpp_cuda():
    """Verifica se llama-cpp-python tem suporte CUDA"""
    try:
        import llama_cpp
        # Teste simples para verificar se CUDA está disponível
        return hasattr(llama_cpp.Llama, 'n_gpu_layers')
    except ImportError:
        return False

def main():
    print("🎮 CyberAI GPU Accelerated")
    print("=" * 50)
    
    # Verificar CUDA
    if not check_cuda():
        print("❌ CUDA/NVIDIA não detectado no sistema!")
        print("Executando sem aceleração GPU...")
        return False
    
    print("✅ CUDA detectado!")
    print("🔧 Verificando llama-cpp-python...")
    
    # Verificar se llama-cpp-python tem suporte CUDA
    if not check_llama_cpp_cuda():
        print("⚠️  llama-cpp-python sem suporte CUDA detectado")
        print("🔄 Reinstalando com suporte CUDA...")
        
        if install_llama_cpp_cuda():
            print("✅ llama-cpp-python com CUDA instalado!")
        else:
            print("❌ Falha na instalação. Executando sem GPU...")
            return False
    else:
        print("✅ llama-cpp-python com CUDA já instalado!")
    
    # Iniciar API
    print("🚀 Iniciando CyberAI API com aceleração GPU...")
    
    # Definir variáveis de ambiente para CUDA
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = '0'
    
    # Executar API
    cmd = [sys.executable, '-m', 'uvicorn', 'src.api.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload']
    
    try:
        subprocess.run(cmd, env=env, cwd='/home/dione/cyberai')
    except KeyboardInterrupt:
        print("\n🛑 CyberAI API interrompida pelo usuário")
    
    return True

if __name__ == "__main__":
    main()