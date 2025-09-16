FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && \
		DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
			build-essential cmake curl && \
		rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install llama-cpp-python with potential CUDA support
# This will use CUDA if available, fall back to CPU if not
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install --no-cache-dir llama-cpp-python==0.2.78 --force-reinstall || \
    pip install --no-cache-dir llama-cpp-python==0.2.78

COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
