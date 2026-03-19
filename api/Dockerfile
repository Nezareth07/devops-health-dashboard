FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       procps \
    && rm -rf /var/lib/apt/lists/*
# Un solo RUN con && encadena comandos y reduce capas
# --no-install-recommends evita instalar paquetes innecesarios
# rm -rf /var/lib/apt/lists/* limpia el cache de apt — reduce tamaño de imagen

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir evita guardar el cache de pip en la imagen

COPY app.py .

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
# || exit 1 — si curl falla, el healthcheck falla explícitamente

CMD ["python", "app.py"]
