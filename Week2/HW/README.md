# Extract Data From Various Sources
- Extract the last quarter of 2020's NYC Green Taxi Data from [DataTalksClub](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)
- Code Workflow:
    1. Define Data Types and Date Columns: It first defines a dictionary `taxi_dtypes` that maps column names to their respective data types for the taxi data. This is used to ensure that the data is loaded into the DataFrame with the correct data types. It also defines a list `parse_dates` that contains the names of the date columns in the data. These columns will be parsed as dates when the data is loaded.

    2. Initialize Storage for DataFrames: It then initializes an empty list `all_df` that will store the DataFrame objects for each month's data.

    3. Define Data URL and Target Months: It sets a `base_url` string that contains placeholders for the year and month of the taxi data to be extracted. It also specifies the `target_year` (2020) and `target_months` (October, November, and December) from which the data will be extracted.

    4. Load Data: It then enters a nested loop that iterates over the specified year and months. For each month of the year, it:
        - Forms the `target_url` by formatting the `base_url` with the current year and month.
        - Prints a message indicating that it is extracting the data for the current year and month.
        - Reads the data from the `target_url` using `pd.read_csv()`, which reads a CSV file into a pandas DataFrame. The data is read directly from the compressed gzip file (`compression="gzip"`). The dtype argument is used to specify the data types of the DataFrame columns as per the `taxi_dtypes` dictionary. The `parse_dates` argument is used to parse the columns as date-time.
        - Appends the DataFrame (df) to the `all_df` list.
    5. Concatenate DataFrames: After the loop, it prints a message indicating that it is concatenating all the DataFrames. It then concatenates all the DataFrames in `all_df` along the row axis (`axis=0`) using `pd.concat()`, and returns the resulting DataFrame.
- Code: [load_green_taxi_data.py](./load_green_taxi_data.py)
# Transform Data For Consistency
- Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
- Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
- Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id
- Assertion:
  1. vendor_id is one of the existing values in the column (currently)
  2. passenger_count is greater than 0
  3. trip_distance is greater than 0
- Code Workflow:
    1. It creates two boolean filters: `filter_1` and `filter_2`. `filter_1` is `True` for rows where the 'passenger_count' is not equal to 0. `filter_2` is `True` for rows where 'trip_distance' is not equal to 0.
    2. It then applies these filters to the DataFrame `data`, keeping only the rows where both `filter_1` and `filter_2` are `True` (i.e., rows where both 'passenger_count' and 'trip_distance' are not zero). The result is assigned back to `data`.
    3. It adds a new column to `data` named `lpep_pickup_date`. This column is created by converting the `lpep_pickup_datetime` column to a date format using the `.dt.date` attribute. This strips the time component from the datetime, leaving just the date.
    4. It renames the columns in `data` from `CamelCase` to `snake_case`. It does this by applying the `camel_to_snake` function (defined elsewhere in the script) to each column name in `data.columns`. The `camel_to_snake` function converts `CamelCase` strings to `snake_case`. The transformed column names are then assigned back to `data.columns`.
    5. After all transformations have been made, the function returns the transformed DataFrame `data`.
- Code: [transform_green_taxi_data.py](./transform_green_taxi_data.py)
# Load Data Into the Warehouse
- Export Cleaned Data to PostgreSQL in our Docker Container
    - Code Workflow:
        - Setting Up Parameters:
            1. schema_name and table_name are defined as `mage` and `green_taxi` respectively. These define the schema and the table in the PostgreSQL database where the data will be exported.
            2. `config_path` is defined as the path to the `io_config.yaml` file. This file contains the configuration settings for connecting to the PostgreSQL database. The `get_repo_path()` function (defined elsewhere) is used to get the root directory of the repository, and `path.join` is used to construct the full path to the `io_config.yaml` file.
            3. `config_profile` is defined as `dev`. This indicates the profile to be used from the `io_config.yaml` file.
        - Exporting Data:
            1. A context manager is created using Postgres.`with_config(ConfigFileLoader(config_path, config_profile))`. This sets up a connection to the PostgreSQL database using the configuration settings specified in `io_config.yaml` under the `dev` profile. The `ConfigFileLoader` class is used to load these settings.
            2. Within the context manager, the `loader.export` method is called to export the DataFrame df to the PostgreSQL database.
               - `df` is the DataFrame to be exported.
               - `schema_name` and `table_name` specify where in the database the data should be exported.
               - `index=False` specifies that the index of df should not be included in the exported table.
               - `if_exists='replace'` specifies that if a table with the same name already exists in the database, it should be replaced with the new data.
    - Code: [green_taxi_data_to_postgres.py](./green_taxi_data_to_postgres.py)
- Export Cleaned Data to Google BigQuery
    - Code Workflow:
        - Setting Up Parameters
            1. `table_id` is defined as `amazing-modem-411901.mage.green_taxi`. This ID will be used to specify the destination table in BigQuery where the data will be exported.
            2. `config_path` is defined as the path to the `io_config.yaml` file. This file contains the configuration settings for connecting to the BigQuery. The `get_repo_path()` function (defined elsewhere) is used to get the root directory of the repository, and path.join is used to construct the full path to the `io_config.yaml` file.
            3. `config_profile` is defined as `default`. This indicates the profile to be used from the `io_config.yaml` file.
        - Exporting Data
            1. `BigQuery.with_config(ConfigFileLoader(config_path, config_profile))` sets up a connection to the BigQuery using the configuration settings specified in `io_config.yaml` under the `default `profile. The ConfigFileLoader class is used to load these settings.
            2. The export method is then called on this connection to export the DataFrame df to BigQuery.
                - `df` is the DataFrame to be exported.
                - `table_id` specifies where in the BigQuery the data should be exported.
                - `if_exists='replace'` specifies that if a table with the same name already exists in the database, it should be replaced with the new data.
    - Code: [green_taxi_data_to_bigquery.py](./green_taxi_data_to_bigquery.py)
- Export Cleaned Data to Google Cloud Storage by partitioning the data by month
    - Code Workflow:
        - Table Creation
            - The `pa.Table.from_pandas(data)` call is used to convert the input pandas DataFrame (data) into a PyArrow Table (table). PyArrow is a cross-language development platform for in-memory data that is used for data exchange and data processing patterns.
        - File System Setup
            - `pa.fs.GcsFileSystem()` creates a Google Cloud Storage (GCS) file system object (gcs). This object is used to interact with data stored in GCS.
        - Data Export
            - `pq.write_to_dataset()` is used to write the PyArrow Table to a Parquet dataset.
            - `table` is the **PyArrow** **Table** to be written.
            - `root_path` specifies the path in the GCS where the dataset should be written. Please note that `root_path` is not defined in the function, so it should be defined elsewhere in the code or passed as an argument.
            - `partition_cols=['lpep_pickup_date']` specifies that the dataset should be partitioned by the `lpep_pickup_date` column. This means that separate Parquet files will be created for each unique value in the `lpep_pickup_date` column.
            - `filesystem=gcs` specifies that the GCS file system object created earlier should be used to write the data.
    - Code: [green_taxi_to_gcs_partitioned_parquet.py](./green_taxi_to_gcs_partitioned_parquet.py)