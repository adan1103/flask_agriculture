from flask import Blueprint

test_controller = Blueprint('test_controller', __name__)

@test_controller.route('/test_controller')
def test_controller_route():
    return 'test_controller'
