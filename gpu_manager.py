#!/usr/bin/env python3
"""
Serviço de automação para alternar entre CPU e GPU
Executa em background e gerencia containers Docker automaticamente
"""

import subprocess
import time
import os
import signal
import sys
from pathlib import Path

class GPUManager:
    def __init__(self):
        self.project_path = Path("/home/dione/cyberai")
        self.current_mode = "cpu"  # cpu ou gpu
        self.is_running = False
        
    def check_gpu_available(self):
        """Verifica se GPU NVIDIA está disponível"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def get_current_mode(self):
        """Detecta qual modo está ativo atualmente"""
        try:
            # Verificar qual docker-compose está rodando
            result = subprocess.run(['docker-compose', 'ps'], 
                                  capture_output=True, text=True, cwd=self.project_path)
            
            if "cyberai-api" in result.stdout:
                return "cpu"
            
            result = subprocess.run(['docker-compose', '-f', 'docker-compose.gpu.yml', 'ps'], 
                                  capture_output=True, text=True, cwd=self.project_path)
            
            if "cyberai-api" in result.stdout:
                return "gpu"
                
            return "none"
        except:
            return "none"
    
    def switch_to_cpu(self):
        """Alterna para modo CPU"""
        print("🔄 Alternando para modo CPU...")
        
        # Parar containers GPU se estiverem rodando
        subprocess.run(['docker-compose', '-f', 'docker-compose.gpu.yml', 'down'], 
                      cwd=self.project_path, capture_output=True)
        
        # Iniciar containers CPU
        result = subprocess.run(['docker-compose', 'up', '-d'], 
                               cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.current_mode = "cpu"
            print("✅ Modo CPU ativado")
            return True
        else:
            print(f"❌ Erro ao ativar CPU: {result.stderr}")
            return False
    
    def switch_to_gpu(self):
        """Alterna para modo GPU"""
        if not self.check_gpu_available():
            print("❌ GPU NVIDIA não disponível")
            return False
            
        print("🔄 Alternando para modo GPU...")
        
        # Parar containers CPU se estiverem rodando
        subprocess.run(['docker-compose', 'down'], 
                      cwd=self.project_path, capture_output=True)
        
        # Iniciar containers GPU
        result = subprocess.run(['docker-compose', '-f', 'docker-compose.gpu.yml', 'up', '-d'], 
                               cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.current_mode = "gpu"
            print("✅ Modo GPU ativado")
            return True
        else:
            print(f"❌ Erro ao ativar GPU: {result.stderr}")
            return False
    
    def toggle_mode(self, target_mode):
        """Alterna entre modos"""
        current = self.get_current_mode()
        
        if target_mode == "gpu" and current != "gpu":
            return self.switch_to_gpu()
        elif target_mode == "cpu" and current != "cpu":
            return self.switch_to_cpu()
        else:
            print(f"ℹ️  Já está no modo {current}")
            return True
    
    def status(self):
        """Retorna status atual"""
        mode = self.get_current_mode()
        gpu_available = self.check_gpu_available()
        
        return {
            "current_mode": mode,
            "gpu_available": gpu_available,
            "containers_running": mode != "none"
        }

def signal_handler(sig, frame):
    print("\n🛑 Parando serviço GPU Manager...")
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print("Uso: python gpu_manager.py [cpu|gpu|status]")
        sys.exit(1)
    
    manager = GPUManager()
    command = sys.argv[1].lower()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    if command == "status":
        status = manager.status()
        print(f"Modo atual: {status['current_mode']}")
        print(f"GPU disponível: {status['gpu_available']}")
        print(f"Containers rodando: {status['containers_running']}")
    
    elif command == "cpu":
        success = manager.toggle_mode("cpu")
        sys.exit(0 if success else 1)
    
    elif command == "gpu":
        success = manager.toggle_mode("gpu")
        sys.exit(0 if success else 1)
    
    else:
        print("Comando inválido. Use: cpu, gpu, ou status")
        sys.exit(1)

if __name__ == "__main__":
    main()