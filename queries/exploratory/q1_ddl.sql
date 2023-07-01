-- Create database and user
CREATE DATABASE globant;
CREATE USER globant WITH PASSWORD 'xspDFr8b09t0';
GRANT ALL PRIVILEGES ON DATABASE globant TO globant;

GRANT ALL PRIVILEGES ON DATABASE globant TO globant;
GRANT USAGE ON SCHEMA public TO globant;
GRANT CREATE ON SCHEMA public TO globant;
COMMIT;
GRANT SELECT, INSERT, UPDATE, DELETE ON jobs TO globant;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO globant;

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




select *
from departments;

delete from departments;


select *
from jobs;

delete from jobs;



delete
from hired_employees;


SELECT
    d.department,
    j.job,
    COUNT(he.id) AS employee_count,
    EXTRACT(QUARTER FROM CAST(he.datetime AS DATE)) AS quarter
FROM
    hired_employees he
JOIN
    departments d ON he.department_id = d.id
JOIN
    jobs j ON he.job_id = j.id
WHERE
    he.datetime LIKE '2021-%%'
GROUP BY
    d.department,
    j.job,
    quarter
ORDER BY
    d.department,
    j.job;

   
   select *,cast(datetime as date)
   from hired_employees
   limit 100;
   
  
