# Decisions Log

## w01

- Fecha: 2026-02-20

- Decisión:
Guardar el hash SHA-256 del archivo CSV raw en la carpeta `artifacts/` en cada ejecución del pipeline.

- Razón:
Permitir detectar cambios invisibles en el dataset original y garantizar trazabilidad del dato procesado.  
Esto mejora la **reliability** y **operability** del pipeline según los principios del Capítulo 1 de *Designing Data-Intensive Applications*.

- Alternativas consideradas:

1. Confiar solo en el nombre del archivo → rechazada.
2. Registrar solo la fecha de descarga → rechazada.
3. Usar checksum SHA-256 del archivo → aceptada.

- Evidencia:

raw_file = data/raw/pscomppars.csv  
raw_sha256 = 9f992b43366d010e4a57b9eeb9fbe52fad0a7f76017ed168b95a1506228db98b  
n_rows = 6107  
n_cols = 16




##  W02

- Fecha: 2026-02-20

**Decisión:** Filtrar `pl_rade > 30` para identificar outliers de radio planetario
antes de incluirlos en análisis estadísticos.

**Evidencia:**
Query ejecutado:
SELECT pl_name, pl_rade
FROM raw_ps
WHERE pl_rade > 30
ORDER BY pl_rade DESC

Resultado:
| pl_name        | pl_rade |
|----------------|---------|
| V2376 Ori b    | 87.21   |
| HD 100546 b    | 77.34   |
| GQ Lup b       | 33.60   |
| Kepler-297 d   | 32.60   |
| PDS 70 b       | 30.49   |
| DH Tau b       | 30.26   |

**Conclusión:** Existen 6 planetas con radio mayor a 30 radios terrestres que
son candidatos a ser outliers o proto-planetas. Incluirlos en promedios
distorsionaría el análisis, por lo que se recomienda filtrarlos o tratarlos
por separado según el contexto del estudio.