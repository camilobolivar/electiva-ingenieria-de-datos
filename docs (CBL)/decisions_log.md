# Decisions Log

## Decisión: Trazabilidad del dataset raw

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