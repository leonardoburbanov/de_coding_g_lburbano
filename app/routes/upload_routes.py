from flask import Blueprint, request, jsonify
from models.models import db, HiredEmployees, Departments, Jobs

upload_csv_routes = Blueprint('upload_csv', __name__)

@upload_csv_routes.route('/upload_csv', methods=['POST'])
def upload_csv():

    file = request.files['file']
    if not file:
        return jsonify({'message': 'No file provided'}), 400

    table_name = request.args.get('table', 'employees')
    batch_size = request.args.get('batch_size', 1000, type=int)


    if batch_size > 1000:
        batch_size = 1000
    elif batch_size < 1:
        batch_size = 1
    else:
        batch_size = batch_size

    data = file.read().decode('utf-8').splitlines()

    # Perform batch insertions
    rows = [row.split(',') for row in data]
    batches = [rows[i:i+batch_size] for i in range(0, len(rows), batch_size)]

    total_rows = len(rows)  # Count all rows in the CSV
    inserted_rows = 0
    error_rows = []  # Collect the rows with errors
    batch_errors = []  # Collect errors during batch insertions

    if table_name == 'departments':
        for batch in batches:
            departments = []
            for row in batch:
                if len(row) != 2:
                    error_rows.append(row)
                    continue
                try:
                    department_id = int(row[0])
                    department = row[1]
                    if not isinstance(department_id, int):
                        raise ValueError("Invalid department ID")
                    department_obj = Departments(id=department_id, department=department)
                    departments.append(department_obj)
                except ValueError:
                    error_rows.append(row)
            try:
                # Perform batch insertion for departments
                db.session.bulk_save_objects(departments)
                db.session.commit()
                inserted_rows += len(departments)  # Count the successfully inserted rows
            except Exception as e:
                # Rollback the session in case of error
                db.session.rollback()
                batch_errors.extend(batch)  # Append the entire batch to batch_errors

    elif table_name == 'jobs':
        for batch in batches:
            jobs = []
            for row in batch:
                if len(row) != 2:
                    error_rows.append(row)
                    continue
                try:
                    job_id = int(row[0])
                    job = row[1]
                    if not isinstance(job_id, int):
                        raise ValueError("Invalid job ID")
                    job_obj = Jobs(id=job_id, job=job)
                    jobs.append(job_obj)
                except ValueError:
                    error_rows.append(row)
            try:
                # Perform batch insertion for jobs
                db.session.bulk_save_objects(jobs)
                db.session.commit()
                inserted_rows += len(jobs)  # Count the successfully inserted rows
            except Exception as e:
                # Rollback the session in case of error
                db.session.rollback()
                batch_errors.extend(batch)  # Append the entire batch to batch_errors

    elif table_name == 'employees':
        for batch in batches:
            employees = []
            for row in batch:
                if len(row) != 5:
                    error_rows.append(row)
                    continue
                try:
                    employee_id = int(row[0])
                    name = row[1]
                    datetime = row[2]
                    department_id = int(row[3])
                    job_id = int(row[4])
                    if not isinstance(employee_id, int) or not isinstance(department_id, int) or not isinstance(job_id, int):
                        raise ValueError("Invalid ID or department ID or job ID")
                    employee_obj = HiredEmployees(
                        id=employee_id,
                        name=name,
                        datetime=datetime,
                        department_id=department_id,
                        job_id=job_id
                    )
                    employees.append(employee_obj)
                except (ValueError, IndexError):
                    error_rows.append(row)
            try:
                # Perform batch insertion for employees
                db.session.bulk_save_objects(employees)
                db.session.commit()
                inserted_rows += len(employees)  # Count the successfully inserted rows
            except Exception as e:
                # Rollback the session in case of error
                db.session.rollback()
                batch_errors.extend(batch)  # Append the entire batch to batch_errors

    else:
        return jsonify({'message': 'Invalid table name provided'}), 400

    error_row_count = total_rows - inserted_rows

    if error_row_count > 0:
        return jsonify({'error_rows': error_rows,
                        'batch_errors': batch_errors,
                        '_total_rows': total_rows,
                        '_inserted_rows': inserted_rows,
                        '_error_row_count': error_row_count,
                        '_message': f'CSV uploaded with errors to {table_name} table'}), 200
    else:
        return jsonify({'_total_rows': total_rows,
                        '_inserted_rows': inserted_rows,
                        'error_row_count': error_row_count,
                        '_message': f'CSV uploaded successfully to {table_name} table'}), 200
