# W03 — SQL Esencial II: JOINs + CTEs y Cardinalidad Práctica

---

## Análisis de cardinalidad: dim_host_bad

| Conteo | Valor |
|--------|-------|
| n_fact | 6107 |
| n_join_good (con dim_host_ra) | 6107 |
| n_join_bad (con dim_host_bad) | 10779 |
| n_join_fixed (CTE + DISTINCT) | 6107 |

**¿Qué pasó?**
`dim_host_bad` se construyó sin deduplicar, por lo que hosts como KOI-351
aparecen 8 veces y TRAPPIST-1 aparece 7 veces. Al hacer el JOIN, cada planeta
se multiplicó por el número de veces que su hostname aparecía en la dimensión
mala, inflando el resultado de 6107 a 10779 filas falsas. La corrección con
`WITH dim_host_fixed AS (SELECT DISTINCT hostname ...)` garantizó una sola fila
por hostname antes del JOIN, devolviendo el conteo correcto de 6107.

---

## TODO 1 — LEFT JOIN y no-match

```sql
SELECT COUNT(*) AS sin_match
FROM fact_planet_raw f
LEFT JOIN dim_host_ra h
  ON f.hostname = h.hostname
WHERE h.hostname IS NULL
```

**Resultado:** `sin_match = 0`  
Todos los planetas de `fact_planet_raw` tienen match en `dim_host_ra`.
El dataset está completo en esta dimensión.

---

## TODO 2 — CTE + ranking: método #1 por año

```sql
WITH counts AS (
  SELECT
    disc_year,
    discoverymethod,
    COUNT(*) AS n
  FROM fact_planet_raw
  WHERE disc_year IS NOT NULL
  GROUP BY disc_year, discoverymethod
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY disc_year ORDER BY n DESC) AS rn
  FROM counts
)
SELECT disc_year, discoverymethod, n
FROM ranked
WHERE rn = 1
ORDER BY disc_year
LIMIT 10
```

**Resultado (primeros 10):**
| disc_year | discoverymethod | n |
|-----------|----------------|---|
| 1992 | Pulsar Timing | 2 |
| 1994 | Pulsar Timing | 1 |
| 1995 | Radial Velocity | 1 |
| 1996 | Radial Velocity | 6 |
| 1997 | Radial Velocity | 1 |
| 1998 | Radial Velocity | 6 |
| 1999 | Radial Velocity | 13 |
| 2000 | Radial Velocity | 16 |
| 2001 | Radial Velocity | 12 |
| 2002 | Radial Velocity | 28 |

---

## TODO 3 — Validación de cardinalidad en dim_discovery

```sql
SELECT
  discoverymethod,
  disc_year,
  COUNT(*) AS cnt
FROM dim_discovery
GROUP BY discoverymethod, disc_year
HAVING COUNT(*) > 1
ORDER BY cnt DESC
```

**Resultado:** `[]`  
No hay duplicados. La combinación `(discoverymethod, disc_year)` es única
en `dim_discovery`, por lo que es segura como llave compuesta para JOINs.

---

## TODO 4 — JOIN + agregación: planetas y RA promedio por método

```sql
SELECT
  f.discoverymethod,
  COUNT(*) AS n_planets,
  ROUND(AVG(h.ra), 2) AS avg_ra
FROM fact_planet_raw f
JOIN dim_host_ra h
  ON f.hostname = h.hostname
WHERE f.discoverymethod IS NOT NULL
  AND h.ra IS NOT NULL
GROUP BY f.discoverymethod
ORDER BY n_planets DESC
```

**Resultado:**
| discoverymethod | n_planets | avg_ra |
|----------------|-----------|--------|
| Transit | 4501 | 246.80 |
| Radial Velocity | 1166 | 175.89 |
| Microlensing | 266 | 267.30 |
| Imaging | 92 | 182.86 |
| Transit Timing Variations | 39 | 250.08 |
| Eclipse Timing Variations | 17 | 223.46 |
| Orbital Brightness Modulation | 9 | 292.91 |
| Pulsar Timing | 8 | 218.74 |
| Astrometry | 6 | 235.42 |
| Pulsation Timing Variations | 2 | 315.24 |
| Disk Kinematics | 1 | 167.01 |

---

## Consultas extra

### Extra 1 — TOP 10 planetas más masivos con RA de su host (JOIN)

```sql
SELECT
  f.pl_name,
  f.pl_bmasse,
  h.ra
FROM fact_planet_raw f
JOIN dim_host_ra h
  ON f.hostname = h.hostname
WHERE f.pl_bmasse IS NOT NULL
ORDER BY f.pl_bmasse DESC
LIMIT 10
```

**Resultado:**
| pl_name | pl_bmasse | ra |
|---------|-----------|-----|
| 2MASS J22501512+2325342 b | 9534.85 | 342.56 |
| CD-35 2722 b | 9375.94 | 92.33 |
| Luhman 16 b | 9344.16 | 162.33 |
| HD 188641 b | 9333.03 | 299.40 |
| KMT-2018-BLG-0885L b | 9217.02 | 268.97 |
| DENIS-P J082303.1-491201 b | 9057.77 | 125.76 |
| HD 26161 b | 9045.40 | 62.41 |
| HD 6860 b | 8981.83 | 17.43 |
| HD 206893 b | 8899.20 | 326.34 |
| TOI-5422 b | 8899.20 | 86.84 |

### Extra 2 — Años donde Transit superó a Radial Velocity (CTE)

```sql
WITH metodos AS (
  SELECT
    disc_year,
    discoverymethod,
    COUNT(*) AS n
  FROM fact_planet_raw
  WHERE disc_year IS NOT NULL
    AND discoverymethod IN ('Transit', 'Radial Velocity')
  GROUP BY disc_year, discoverymethod
),
comparacion AS (
  SELECT
    disc_year,
    MAX(CASE WHEN discoverymethod = 'Transit' THEN n END) AS transit,
    MAX(CASE WHEN discoverymethod = 'Radial Velocity' THEN n END) AS radial_velocity
  FROM metodos
  GROUP BY disc_year
)
SELECT *
FROM comparacion
WHERE transit > radial_velocity
ORDER BY disc_year
```

**Resultado:**
| disc_year | transit | radial_velocity |
|-----------|---------|----------------|
| 2010 | 47 | 41 |
| 2011 | 79 | 43 |
| 2012 | 93 | 35 |
| 2013 | 80 | 33 |
| 2014 | 798 | 48 |
| 2015 | 99 | 46 |
| 2016 | 1432 | 50 |
| 2017 | 87 | 49 |
| 2018 | 242 | 46 |
| 2019 | 107 | 65 |
| 2020 | 165 | 46 |
| 2021 | 457 | 76 |
| 2022 | 191 | 118 |
| 2023 | 224 | 57 |
| 2024 | 187 | 28 |
| 2025 | 141 | 61 |
| 2026 | 10 | 8 |

**Interpretación:** Transit domina desde 2010 en adelante. El salto masivo en
2014 y 2016 coincide con las misiones Kepler y K2 que confirmaron cientos de
planetas en esos años usando tránsitos.