WITH salary_rank AS(
SELECT department_id, salary,
DENSE_RANK() OVER (PARTITION BY department_id
ORDER BY salary DESC
) rank
FROM employee
)
SELECT salary_diff.department_id, e.first_name, last_name, e.salary, salary_diff.salary_gap
FROM (SELECT salary_rank.department_id, MAX(rank.salary) - MIN(rank.salary) AS salary_gap, MAX(rank.salary) AS max_var
      FROM salary_rank
      GROUP BY salary_rank.department_id
      WHERE salary_rank.rank<3;
      ) salary_diff
JOIN employee e
ON salary_diff.department_id = e.department_id
AND salary_diff.max_var = e.salary
;