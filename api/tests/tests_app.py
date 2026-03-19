import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import app

@pytest.fixture
def client():
    """
    Fixture de pytest — crea un cliente de prueba de Flask.
    Se ejecuta antes de cada test que lo solicite.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_returns_200(client):
    """El endpoint raíz debe responder con 200."""
    response = client.get('/')
    assert response.status_code == 200

def test_index_contains_service_name(client):
    """El endpoint raíz debe incluir el nombre del servicio."""
    response = client.get('/')
    data = json.loads(response.data)
    assert "service" in data
    assert "DevOps Health Dashboard" in data["service"]

def test_health_endpoint_exists(client):
    """El endpoint /health debe existir."""
    with patch('app.get_redis') as mock_redis:
        mock_redis.return_value.ping.return_value = True
        response = client.get('/health')
        assert response.status_code in [200, 503]

def test_health_returns_api_ok(client):
    """El campo 'api' en /health debe ser siempre 'ok'."""
    with patch('app.get_redis') as mock_redis:
        mock_redis.return_value.ping.return_value = True
        response = client.get('/health')
        data = json.loads(response.data)
        assert data["api"] == "ok"

def test_metrics_endpoint_exists(client):
    """El endpoint /metrics debe existir."""
    mock_metrics = {
        "timestamp": "2026-03-19T10:00:00Z",
        "hostname": "test-host",
        "cpu": {"usage_pct": 10},
        "ram": {"used_mb": 512, "total_mb": 8192, "usage_pct": 6},
        "disk": {"used": "2G", "total": "100G", "usage_pct": 2},
        "load_average": {"1m": 0.1, "5m": 0.1, "15m": 0.1},
        "uptime": "1 hour"
    }
    with patch('app.get_metrics') as mock:
        mock.return_value = mock_metrics
        response = client.get('/metrics')
        assert response.status_code == 200

def test_metrics_structure(client):
    """Las métricas deben tener la estructura correcta."""
    mock_metrics = {
        "timestamp": "2026-03-19T10:00:00Z",
        "hostname": "test-host",
        "cpu": {"usage_pct": 10},
        "ram": {"used_mb": 512, "total_mb": 8192, "usage_pct": 6},
        "disk": {"used": "2G", "total": "100G", "usage_pct": 2},
        "load_average": {"1m": 0.1, "5m": 0.1, "15m": 0.1},
        "uptime": "1 hour"
    }
    with patch('app.get_metrics') as mock:
        mock.return_value = mock_metrics
        response = client.get('/metrics')
        data = json.loads(response.data)
        assert "cpu" in data
        assert "ram" in data
        assert "disk" in data
        assert "timestamp" in data
