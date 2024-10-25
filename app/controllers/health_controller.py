from flask import jsonify

class HealthController:
    def __init__(self, service_name):
        if not isinstance(service_name, str) or not service_name.strip():
            raise ValueError("Invalid service name")
        self.service_name = service_name

    def health(self):
        print("hola mundo")
        return jsonify(message=f"Everything ok with the service {self.service_name}")
