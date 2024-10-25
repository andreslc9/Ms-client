import pytest
from app.models.client import Client
from werkzeug.security import generate_password_hash
from app import db
import responses

def test_add_client_existing(client, app):
    # Crear un cliente existente
    existing_client = Client(
        nit=123456,
        name="Jane Doe",
        email="jane.doe@example.com",
        password=generate_password_hash("password123")
    )
    with app.app_context():
        db.session.add(existing_client)
        db.session.commit()

    # Intentar agregar un cliente con el mismo correo electrónico
    new_client_data = {
        "nit": 123457,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "password123"
    }

    response = client.post('/client/api/v1/sign-up', json=new_client_data)

    # Verificar que se reciba el error correspondiente
    assert response.status_code == 400
    assert response.get_json()["error"] == "El usuario ya existe"

def test_add_client_db_error(client, app, monkeypatch):
    # Simular un error de base de datos al agregar un cliente
    def mock_add_to_db(client):
        raise Exception("Database error")

    # Reemplazar la función original con la simulación
    monkeypatch.setattr(db.session, "add", mock_add_to_db)

    new_client_data = {
        "nit": 123456,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }

    response = client.post('/client/api/v1/sign-up', json=new_client_data)

    # Verificar que se maneje el error correctamente
    assert response.status_code == 500
    assert "Database error" in response.get_json()["error"]

@responses.activate
def test_login_success(client, app):
    # Crear un cliente válido
    valid_client = Client(
        nit=123456,
        name="John Doe",
        email="john.doe@example.com",
        password=generate_password_hash("password123")
    )
    with app.app_context():
        db.session.add(valid_client)
        db.session.commit()

    # Simula la respuesta de la Lambda para generar el token
    responses.add(
        responses.POST, "http://10.0.1.7/api/token/create/",
        json={"token": "fake-token"}, status=200
    )

    # Intentar iniciar sesión con credenciales correctas
    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post('/client/api/v1/sign-in', json=login_data)

    # Verificar que la respuesta sea exitosa y que se obtenga el token
    assert response.status_code == 200
    assert "token" in response.get_json()
    assert response.get_json()["token"] == "fake-token"

@responses.activate
def test_login_lambda_error(client, app):
    # Crear un cliente válido
    valid_client = Client(
        nit=123456,
        name="John Doe",
        email="john.doe@example.com",
        password=generate_password_hash("password123")
    )
    with app.app_context():
        db.session.add(valid_client)
        db.session.commit()

    # Simular un error de la Lambda
    responses.add(
        responses.POST, "http://10.0.1.7/api/token/create/",
        body="Lambda error", status=500
    )

    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post('/client/api/v1/sign-in', json=login_data)

    # Verificar que se maneje el error correctamente
    assert response.status_code == 500
    assert response.get_json()["error"] == "Error al obtener el token"

def test_login_invalid_password(client, app):
    # Crear un cliente válido
    valid_client = Client(
        nit=123456,
        name="John Doe",
        email="john.doe@example.com",
        password=generate_password_hash("password123")
    )
    with app.app_context():
        db.session.add(valid_client)
        db.session.commit()

    # Intentar iniciar sesión con una contraseña incorrecta
    login_data = {
        "email": "john.doe@example.com",
        "password": "wrongpassword"
    }
    response = client.post('/client/api/v1/sign-in', json=login_data)

    # Verificar que se reciba un error de contraseña incorrecta
    assert response.status_code == 401
    assert response.get_json()["error"] == "Contraseña incorrecta"

def test_login_client_not_found(client):
    # Intentar iniciar sesión con un cliente inexistente
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post('/client/api/v1/sign-in', json=login_data)

    # Verificar que se reciba un error de cliente no encontrado
    assert response.status_code == 404
    assert response.get_json()["error"] == "Usuario no encontrado"
