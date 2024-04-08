import json
import time 
import pandas as pd
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'
topic = 'green-trips'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()

df = pd.read_csv("green_tripdata_2019-10.csv.gz", compression="gzip")
selected_cols = ['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID',
                 'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount']
df_green = df[selected_cols]

t0 = time.time()
for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    print(row_dict)

    # Send the data to the Kafka server
    producer.send(topic, row_dict)

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')

# Flush the producer to ensure the data is sent
producer.flush()

t2 = time.time()
print(f'took {(t2 - t1):.2f} seconds')