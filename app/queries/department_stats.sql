SELECT
    d.id AS department_id,
    d.department,
    COUNT(he.id) AS employee_count
FROM
    hired_employees he
JOIN
    departments d ON he.department_id = d.id
WHERE
    he.datetime LIKE '2021-%'
GROUP BY
    d.id,
    d.department
HAVING
    COUNT(he.id) > (SELECT AVG(count_he) FROM (SELECT COUNT(he.id) AS count_he FROM hired_employees he WHERE he.datetime LIKE '2021-%' GROUP BY he.department_id) AS subquery)
ORDER BY
    employee_count DESC;