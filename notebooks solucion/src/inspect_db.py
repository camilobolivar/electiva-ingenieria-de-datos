import duckdb

con = duckdb.connect("data/exoplanets.duckdb")

print("=== TABLAS ===")
print(con.execute("""
SELECT table_name 
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
""").fetchall())

print("\n=== VISTAS ===")
print(con.execute("""
SELECT table_name 
FROM information_schema.views
""").fetchall())

print("\n=== GOLD BY DISCOVERY METHOD ===")
print(con.execute("SELECT * FROM gold_by_discoverymethod LIMIT 5").fetchdf())

print("\n=== GOLD BY HOST ===")
print(con.execute("SELECT * FROM gold_by_host LIMIT 5").fetchdf())