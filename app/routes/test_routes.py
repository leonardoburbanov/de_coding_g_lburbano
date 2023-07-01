from flask import Blueprint, jsonify


test_routes = Blueprint('test', __name__)

@test_routes.route('/test', methods=['GET'])
def get_test():
    result={
        'test':'OK'
    }
    return jsonify(result), 200