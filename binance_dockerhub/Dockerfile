FROM python:3.12-slim

LABEL org.opencontainers.image.title="Crypto Xtrakt" \
      org.opencontainers.image.description="Get latest crypto data" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Kevin Odhiambo"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY crypto.py ./

CMD ["python", "crypto.py"]