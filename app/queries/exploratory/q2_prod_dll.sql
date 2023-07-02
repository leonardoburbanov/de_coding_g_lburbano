CREATE DATABASE globant;
CREATE USER globant WITH PASSWORD 'passwd';
GRANT ALL PRIVILEGES ON DATABASE globant TO postgres;

GRANT ALL PRIVILEGES ON DATABASE globant TO globant;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO globant;
GRANT USAGE ON SCHEMA public TO globant;
GRANT CREATE ON SCHEMA public TO globant;
COMMIT;

-- Create departments table
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    department VARCHAR(255)
);

-- Create jobs table
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    job VARCHAR(255)
);

-- Create hired_employees table
CREATE TABLE hired_employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    datetime VARCHAR(255),
    department_id INTEGER,
    job_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments (id),
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

delete from hired_employees;
delete from departments;
delete from jobs;

