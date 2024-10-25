# tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Crea una instancia de la aplicación Flask para usar en las pruebas"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
@pytest.fixture
def client(app):
    """Cliente de prueba para enviar solicitudes a la aplicación"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner para ejecutar comandos CLI de Flask"""
    return app.test_cli_runner()