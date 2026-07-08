FROM python:3.11-slim
WORKDIR /app

# Perbaikan: Mengganti libgl1-mesa-glx menjadi libgl1
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install small packages first (mediapipe, fastapi, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi==0.115.0 "uvicorn[standard]==0.30.6" mediapipe==0.10.11 numpy==1.26.4 pillow==10.4.0 python-multipart==0.0.12

# Install tensorflow WITHOUT GPU/CUDA dependencies (saves ~2GB)
RUN pip install --no-cache-dir --no-deps tensorflow==2.17.0 && \
    pip install --no-cache-dir \
        absl-py astunparse gast google-pasta grpcio h5py keras \
        libclang ml-dtypes opt-einsum packaging protobuf six \
        termcolor typing-extensions wrapt tensorflow-io-gcs-filesystem

COPY . .
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]