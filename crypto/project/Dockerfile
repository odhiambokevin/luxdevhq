#builder
FROM python:3.12-slim AS builder


LABEL org.opencontainers.image.title="Crypto Api" \
      org.opencontainers.image.description="Extracts data of select crypto from coinpaprika.com" \
      org.opencontainers.image.version="0.0.1" \
      org.opencontainers.image.authors="Kevin Odhiambo"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/install -r requirements.txt

#runner
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

COPY extract.py transform.py load.py main.py ./

CMD ["python", "main.py"]