from flask import jsonify, request
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.client import Client
from app import db

class ClientController:
    def add_client(self):
        data = request.get_json()

        # Verificar si el username ya existe
        existing_client = Client.query.filter_by(email=data['email']).first()
        if existing_client:
            return jsonify({"error": "El usuario ya existe"}), 400

        # Encriptar la contraseña
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Crear un nuevo cliente
        new_client = Client(
            nit=data['nit'],
            name=data['name'],
            email=data['email'],
            password=hashed_password
        )

        try:
            # Agregar el cliente a la base de datos
            db.session.add(new_client)
            db.session.commit()
            return jsonify({"message": "¡Cliente añadido de manera exitosa!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def login(self):
        data = request.get_json()
        client = Client.query.filter_by(email=data['email']).first()

        if client is None:
            return jsonify({"error":"Usuario no encontrado"}), 404

        if not check_password_hash(client.password, data['password']):
            return jsonify({"error":"Contraseña incorrecta"}), 401
        
        lambda_url = "http://10.0.1.7/api/token/create/"
        body = {"email": client.email} 

        try:
            lambda_response = requests.post(lambda_url, json=body)
            lambda_response.raise_for_status()  # Lanza un error si la respuesta no es 200
            token_data = lambda_response.json()

            # Devolver el token y un mensaje de éxito
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "token": token_data.get("token")  # Suponiendo que la respuesta tiene un campo 'token'
            }), 200
        
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Error al obtener el token", "details": str(e)}), 500