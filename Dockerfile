# ---------- STAGE 1: builder ----------
FROM python:3.10-slim-buster AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------- STAGE 2: runtime ----------
FROM python:3.10-slim-buster

WORKDIR /app

# copy only installed packages (no build junk)
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["python3", "app.py"]
