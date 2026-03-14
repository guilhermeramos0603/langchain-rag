# Common SQL Errors

## SQL Injection
**Pattern:** Concatenating user input directly into SQL queries.
**Example:** `f"SELECT * FROM users WHERE name = '{user_input}'"`.
**Fix:** Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))`.

## NULL Comparison
**Pattern:** Using `= NULL` instead of `IS NULL`.
**Example:** `SELECT * FROM users WHERE email = NULL` returns no rows.
**Fix:** Use `IS NULL`: `SELECT * FROM users WHERE email IS NULL`.

## GROUP BY Missing Column
**Pattern:** Selecting columns not in GROUP BY or aggregate functions.
**Example:** `SELECT name, department, COUNT(*) FROM employees GROUP BY department`.
**Fix:** Include all non-aggregated columns in GROUP BY or use aggregate functions.

## N+1 Query Problem
**Pattern:** Executing one query per item instead of a batch query.
**Example:** Looping through users and querying orders for each one separately.
**Fix:** Use JOINs or IN clauses to fetch related data in a single query.

## Cartesian Product (Missing JOIN Condition)
**Pattern:** Joining tables without a proper ON clause.
**Example:** `SELECT * FROM users, orders` without `WHERE users.id = orders.user_id`.
**Fix:** Always specify JOIN conditions explicitly.
