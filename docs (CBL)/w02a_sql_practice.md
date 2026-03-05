# W02A — SQL Practice

## Consultas 1–6

### TODO 1 — Planetas por año (top 15)
```sql
[(2016, 1496),
 (2014, 869),
 (2021, 564),
 (2022, 369),
 (2023, 324),
 (2018, 315),
 (2024, 259),
 (2025, 240),
 (2020, 234),
 (2019, 196),
 (2015, 155),
 (2017, 152),
 (2012, 139),
 (2011, 135),
 (2013, 128)]
```

### TODO 2 — Top 10 sistemas con más planetas
```sql
[('KOI-351', 8),
 ('TRAPPIST-1', 7),
 ('TOI-178', 6),
 ('Kepler-80', 6),
 ('Kepler-20', 6),
 ('HD 10180', 6),
 ('HD 34445', 6),
 ('HD 110067', 6),
 ('Kepler-11', 6),
 ('HIP 41378', 6)]
```

### TODO 3 — Fracción de nulos en pl_bmasse
```sql
[(6107, 6076, 31, 0.005076142131979695)]
```

### TODO 4 — 10 planetas con mayor radio
```sql
[('V2376 Ori b', 87.20586985),
 ('HD 100546 b', 77.3421),
 ('GQ Lup b', 33.6),
 ('Kepler-297 d', 32.6),
 ('PDS 70 b', 30.48848),
 ('DH Tau b', 30.2643),
 ('Kepler-1979 b', 29.33),
 ('TOI-1408 b', 25.0),
 ('CT Cha b', 24.66),
 ('HAT-P-67 b', 23.9872187)]
```

### TODO 5 — COUNT(*) vs COUNT(disc_year) por método
```sql
[('Transit', 4501, 4500),
 ('Radial Velocity', 1166, 1166),
 ('Microlensing', 266, 266),
 ('Imaging', 92, 92),
 ('Transit Timing Variations', 39, 39),
 ('Eclipse Timing Variations', 17, 17),
 ('Orbital Brightness Modulation', 9, 9),
 ('Pulsar Timing', 8, 8),
 ('Astrometry', 6, 6),
 ('Pulsation Timing Variations', 2, 2),
 ('Disk Kinematics', 1, 1)]
```

### TODO 6 — Resumen por método: n_planets y mediana del periodo orbital
```sql
[('Transit', 4501, 8.15872),
 ('Radial Velocity', 1166, 298.895),
 ('Transit Timing Variations', 39, 30.0),
 ('Imaging', 25, 33000.0),
 ('Eclipse Timing Variations', 17, 3160.0),
 ('Microlensing', 12, 3142.5),
 ('Orbital Brightness Modulation', 9, 0.81161),
 ('Pulsar Timing', 7, 25.262),
 ('Astrometry', 6, 334.76),
 ('Pulsation Timing Variations', 2, 1005.0)]
```

---

## 4 Consultas adicionales

### Calidad 1 — Duplicados por nombre de planeta
```sql
SELECT pl_name, COUNT(*) AS veces
FROM raw_ps
GROUP BY pl_name
HAVING COUNT(*) > 1
ORDER BY veces DESC
```
**Resultado:** `[]` — No se encontraron duplicados exactos por nombre. El dataset
está limpio en esta dimensión.

### Calidad 2 — Outliers de radio (pl_rade > 30)
```sql
SELECT pl_name, pl_rade
FROM raw_ps
WHERE pl_rade > 30
ORDER BY pl_rade DESC
```
**Resultado:**
| pl_name       | pl_rade |
|---------------|---------|
| V2376 Ori b   | 87.21   |
| HD 100546 b   | 77.34   |
| GQ Lup b      | 33.60   |
| Kepler-297 d  | 32.60   |
| PDS 70 b      | 30.49   |
| DH Tau b      | 30.26   |

### Científica 1 — Temperatura promedio por método de descubrimiento
```sql
SELECT
  discoverymethod,
  ROUND(AVG(pl_eqt), 2) AS temp_promedio_k
FROM raw_ps
WHERE pl_eqt IS NOT NULL
GROUP BY discoverymethod
ORDER BY temp_promedio_k DESC
```
**Resultado:**
| discoverymethod                | temp_promedio_k |
|-------------------------------|-----------------|
| Orbital Brightness Modulation | 2140.00         |
| Imaging                       | 1577.27         |
| Transit                       | 922.90          |
| Transit Timing Variations     | 684.43          |
| Radial Velocity               | 558.46          |
| Microlensing                  | 56.00           |

**Interpretación:** Los planetas detectados por brillo orbital y por imagen directa
tienden a ser mucho más calientes. Esto tiene sentido porque son métodos que
favorecen planetas muy cercanos a su estrella o muy masivos y jóvenes, ambos
escenarios asociados a altas temperaturas.

### Científica 2 — Sistemas con más de 3 planetas y distancia promedio
```sql
SELECT
  hostname,
  COUNT(*) AS n_planetas,
  ROUND(AVG(sy_dist), 2) AS dist_promedio_pc
FROM raw_ps
GROUP BY hostname
HAVING COUNT(*) > 3
ORDER BY n_planetas DESC
```
**Resultado (primeros registros):**
| hostname   | n_planetas | dist_promedio_pc |
|------------|------------|------------------|
| KOI-351    | 8          | 848.25           |
| TRAPPIST-1 | 7          | 12.43            |
| HD 34445   | 6          | 46.09            |
| Kepler-80  | 6          | 369.45           |
| HD 110067  | 6          | 32.16            |
| TOI-178    | 6          | 62.70            |
| ...        | ...        | ...              |

**Interpretación:** TRAPPIST-1 destaca por ser el sistema más cercano con muchos
planetas (solo 12.43 parsecs), lo que lo convierte en uno de los más estudiados.
KOI-351 tiene el mayor número de planetas pero está casi 70 veces más lejos.

---

## Reflexión

**¿Qué consulta te pareció más difícil y por qué?**
La más difícil fue el TODO 6 porque combina varias operaciones al mismo tiempo:
primero el motor debe organizar los datos en grupos por `discoverymethod`, luego
sobre cada grupo aplica `MEDIAN(pl_orbper)`, una función estadística que internamente
requiere ordenar todos los valores del grupo para encontrar el punto medio. A esto
se suma que el filtro de nulos también tiene peso porque se deben descartar muchas
filas antes de que el cálculo tenga sentido. Es la consulta que más trabajo
le exige al motor en conjunto.

**Si el dataset creciera 100×, ¿qué consultas crees que empeoran más?**
Las que más sufrirían son las que combinan `GROUP BY` con funciones estadísticas
como `MEDIAN()`, porque ordenar internamente cada grupo escala mal con el volumen.
También empeoraría la consulta de outliers si el umbral no usa un índice, ya que
tendría que escanear toda la tabla. Las consultas de conteo simple como TODO 1
y TODO 2 escalarían mejor porque solo acumulan, no ordenan internamente.