import os
import json
import subprocess
import redis
from flask import Flask, jsonify


app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
CACHE_TTL = int(os.getenv("CACHE_TTL", "5"))


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def get_metrics():
    """
    Intenta obtener métricas del cache Redis.
    Si no hay cache, ejecuta el script bash y cachea el resultado.
    """
    r = get_redis()
    cached = r.get("metrics")

    if cached:
        data = json.loads(cached)
        data["cached"] = True
        return data

    result = subprocess.run(
        ["/scripts/collect_metrics.sh"],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode != 0:
        raise RuntimeError(f"Script error: {result.stderr}")

    data = json.loads(result.stdout)
    data["cached"] = False

    r.setex("metrics", CACHE_TTL, json.dumps(data))

    return data


@app.route("/")
def index():
    return jsonify({
        "service": "DevOps Health Dashboard API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "endpoints": ["/metrics", "/health"]
    })


@app.route("/metrics")
def metrics():
    try:
        data = get_metrics()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    status = {"api": "ok", "redis": "error"}
    http_code = 200

    try:
        r = get_redis()
        r.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis_error"] = str(e)
        http_code = 503

    return jsonify(status), http_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
