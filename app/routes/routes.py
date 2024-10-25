from flask import Blueprint
from app.controllers.health_controller import HealthController
from app.controllers.client_controller import ClientController

def init_app(app, name=''):
    service_name = "Client"

    health_controller = HealthController(service_name)
    client_controller = ClientController()

    bp = Blueprint('main', __name__)
    
    @bp.route('/client/health')
    def health():
        return health_controller.health()

    @bp.route('/client/api/v1/sign-up', methods=['POST'])
    def add():
        return client_controller.add_client()

    @bp.route('/client/api/v1/sign-in', methods=['POST'])
    def login():
        return client_controller.login()

    app.register_blueprint(bp)