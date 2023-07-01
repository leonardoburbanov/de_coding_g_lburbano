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