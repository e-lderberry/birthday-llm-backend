FROM python:3.11-slim

WORKDIR /app

# Build tools for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Force CPU build
ENV CMAKE_ARGS="-DLLAMA_BLAS=OFF"
ENV FORCE_CMAKE=1

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create models dir
RUN mkdir -p models

# ⬇️ DOWNLOAD MODEL HERE (CRITICAL FIX)
RUN curl -L \
  https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  -o models/qwen2.5-0.5b-instruct.gguf

# Copy app code (but not model)
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
