#!/usr/bin/env python
# coding: utf-8
from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import requests
from urllib.parse import urlparse
from os.path import basename

def parquet_to_csv(parquet_file_path, csv_file_path):
    try:
        df = pd.read_parquet(parquet_file_path)
        df.to_csv(csv_file_path, index=False)
        print(f"Successfully convert the parquet file to csv format and save it into {csv_file_path}")
        return csv_file_path
    except Exception as e:
        print(f"Convert Failed: {e}")
        return

def download_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = basename(urlparse(url).path)
            if not file_name:
                print(f"Unable to extract file name from URL: {url}")
                return

            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Successfully downloaded the file and saved it as {file_name}")
            return file_name
        else:
            print(f"Download failed, Status Code: {response.status_code}")
            return

    except Exception as e:
        print(f"Download failed: {e}")
        return

def process_dataframe(df):
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
    return df

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    source = params.source
    
    csv_name = ""
    if urlparse(source).scheme in ['http', 'https']:
        parquet_file = download_file(url=source)
        if parquet_file is not None:
            csv_name = parquet_to_csv(parquet_file, parquet_file.replace('.parquet', '.csv'))
    else:
        csv_name = source

    if csv_name == "":
        return

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    try:
        df_iter = pd.read_csv(f'{csv_name}', iterator=True, chunksize=100000)

        for i, df in enumerate(df_iter):
            t_start = time()

            if i == 0:
                df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            
            df = process_dataframe(df)
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False, method='multi')

            t_end = time()
            print(f'Inserted chunk {i}, took {t_end - t_start:.3f} seconds')

    except StopIteration:
        print("All chunks processed")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to PostgreSQL")
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='post for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results')
    parser.add_argument('--source', help='source of the csv file')

    args = parser.parse_args()

    main(args)
