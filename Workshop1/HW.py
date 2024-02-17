# Create a generator
def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Question 1: What is the sum of the outputs of the generator for limit = 5? 
res = 0
limit = 13
generator = square_root_generator(limit)

for sqrt_value in generator:
    res = sqrt_value

print(f'{res:.4f}')

# Question 2: What is the 13th number yielded
res = 0
limit = 5
generator = square_root_generator(limit)

for sqrt_value in generator:
    res += sqrt_value

print(f'{res:.4f}')

# Question 3: Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.
def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}

total_age = sum(p['Age'] for p in people_1()) + sum(p['Age'] for p in people_2())

print(total_age)

# Question 4: Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above.
import dlt
import duckdb

generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='generators')
info = generators_pipeline.run(people_1(), table_name='people', write_disposition='replace', primary_key='ID')

print(info)

info_2 = generators_pipeline.run(people_2(), table_name='people', write_disposition='merge', primary_key='ID')
print(info_2)

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
