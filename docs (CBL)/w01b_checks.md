# W01B — Sanity Checks

Dataset: NASA Exoplanet Archive (pscomppars)

---

## Check 1 — Número de filas y columnas

Query:

```sql
SELECT COUNT(*) FROM raw_ps

Resultado:

n_rows = 6107

Query:

SELECT COUNT(*) FROM pragma_table_info('raw_ps')

Resultado:

n_cols = 16

Objetivo: verificar que el dataset fue cargado correctamente.

Check 2 — Valores nulos en pl_name

Query:

SELECT COUNT(*) 
FROM raw_ps
WHERE pl_name IS NULL

Resultado:

0

Objetivo: verificar que la columna clave pl_name no contiene valores nulos.

Check 3 — Sample de registros

Query:

SELECT pl_name, hostname, discoverymethod, disc_year
FROM raw_ps
WHERE pl_name IS NOT NULL
LIMIT 10

Resultado:

Se observaron registros válidos con nombres de planetas, hostnames y métodos de descubrimiento.

Objetivo: validar que los datos tienen formato correcto.

Check 4 (extra) — Años fuera de rango en disc_year

Query:

SELECT COUNT(*) AS n_bad_years
FROM raw_ps
WHERE disc_year IS NOT NULL
  AND (disc_year < 1980 OR disc_year > EXTRACT(YEAR FROM CURRENT_DATE));

  Resultado:

n_bad_years = 0

Query adicional (rango observado):

SELECT MIN(disc_year) AS min_year, MAX(disc_year) AS max_year
FROM raw_ps
WHERE disc_year IS NOT NULL;

Resultado:

min_year = 1992
max_year = 2026

Objetivo: verificar que los años de descubrimiento estén dentro de un rango lógico
No se detectaron valores fuera de rango.