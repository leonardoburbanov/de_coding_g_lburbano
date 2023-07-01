from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HiredEmployees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    datetime = db.Column(db.String)
    department_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String)