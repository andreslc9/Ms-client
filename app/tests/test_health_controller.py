import pytest
from app.controllers.health_controller import HealthController
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    return app.test_client()

# Test con un nombre de servicio válido
def test_health_valid_service_name(client):
    controller = HealthController("TestService")
    with client.application.test_request_context():
        response = controller.health()
        assert response.status_code == 200
        assert b"Everything ok with the service TestService" in response.data

# Test con un nombre de servicio vacío
def test_health_empty_service_name():
    with pytest.raises(ValueError, match="Invalid service name"):
        HealthController("")

# Test con un nombre de servicio que solo contiene espacios
def test_health_service_name_spaces():
    with pytest.raises(ValueError, match="Invalid service name"):
        HealthController("   ")

# Test con un nombre de servicio no string
def test_health_service_name_non_string():
    with pytest.raises(ValueError, match="Invalid service name"):
        HealthController(123)  # Proporcionamos un número en lugar de una cadena
