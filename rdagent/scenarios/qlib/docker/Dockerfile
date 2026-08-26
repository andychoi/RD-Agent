FROM python:3.12-slim-bookworm

# The factor workflow uses Qlib + LightGBM on CPU. A multi-architecture Python
# base runs natively on Apple Silicon and avoids emulating the stock CUDA/amd64
# image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    coreutils \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/microsoft/qlib.git /workspace/qlib

WORKDIR /workspace/qlib

RUN git fetch && git reset 2fb9380b342556ddb50a4b24e4fe8655d548b2b8 --hard

RUN python -m pip install --no-cache-dir --upgrade pip cython \
    && python -m pip install --no-cache-dir -e . \
    && python -m pip install --no-cache-dir tables
