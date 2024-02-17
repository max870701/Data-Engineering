# Workshop 1: Data Ingestion with dlt
## Create a generator to extract data from a data source
## Create a pipeline to ingest data into an in-memory database (e.g. DuckDB) or a data warehouse (e.g. BigQuery)
```python
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='generators')
```

## Replace or merge data in the in-memory database or data warehouse
```python
info = generators_pipeline.run(people_1(), table_name='people', write_disposition='replace', primary_key='ID')
info_2 = generators_pipeline.run(people_2(), table_name='people', write_disposition='merge', primary_key='ID')
```

## Query the data in the in-memory database or data warehouse
```python
conn = duckdb.connect(f'{generators_pipeline.pipeline_name}.duckdb')

conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
print(conn.sql("show tables"))

print("\n\n\n people table below:")

people = conn.sql("SELECT * FROM people").df()
print(people)

query = """
SELECT SUM(age) AS total_age
FROM people
"""

res = conn.sql(query)
print(res)
```