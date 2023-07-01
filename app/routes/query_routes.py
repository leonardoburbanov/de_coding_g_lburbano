from flask import Blueprint, jsonify
from models.models import db
from sqlalchemy import text
import os

query_routes = Blueprint('query', __name__)

@query_routes.route('/employee-stats', methods=['GET'])
def get_employee_stats():
    query_file = os.path.join(os.path.dirname(__file__), '../queries/employee_stats.sql')
    with open(query_file, 'r') as file:
        query = file.read()

    result = db.session.execute(text(query)).fetchall()
    stats = []
    for row in result:
        stats.append({
            'department': row.department,
            'job': row.job,
            'employee_count': int(row.employee_count),
            'quarter': int(row.quarter)
        })

    return jsonify(stats), 200

@query_routes.route('/department-stats', methods=['GET'])
def get_department_stats():
    query_file = os.path.join(os.path.dirname(__file__), '../queries/department_stats.sql')
    with open(query_file, 'r') as file:
        query = file.read()

    result = db.session.execute(text(query)).fetchall()

    stats = []
    for row in result:
        stats.append({
            'department_id': row.department_id,
            'department': row.department,
            'employee_count': int(row.employee_count)
        })

    return jsonify(stats), 200