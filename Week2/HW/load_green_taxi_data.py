import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# ehail_fee,trip_type
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Task 1: Add a data loader block and use Pandas to read data for the final quarter of 2020 (months 10, 11, 12)
    Task 2: Load the final three months using a for loop and pd.concat
    """
    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'RatecodeID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'trip_type': pd.Int64Dtype(),
        'congestion_surcharge': float
    }
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    all_df = []
    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{0}-{1:02}.csv.gz'
    target_year = ['2020']
    target_months = ['10', '11', '12']

    for year in target_year:
        for month in target_months:
            target_url = base_url.format(year, month)
            print('Extracing {0}-{1:02} green taxi data ...'.format(year, month))
            df = pd.read_csv(target_url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
            all_df.append(df)
    print('Concatenating All Dataframes ...')
    return pd.concat(all_df, axis=0)