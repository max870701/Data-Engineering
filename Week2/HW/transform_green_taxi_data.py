import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    if "_" in name or name.islower():
        return name
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@transformer
def transform(data, *args, **kwargs):
    """
    Task 1: Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    Task 2: Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    Task 3: Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id
    """
    # print("Rows with zero passengers: ", data['passenger_count'].isin([0]).sum())
    print("Task 1: Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero ...")
    filter_1 = data['passenger_count'] != 0
    filter_2 = data['trip_distance'] != 0
    data = data[filter_1 & filter_2]

    print("Task 2: Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date ... ")
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    print("Task 3: Rename columns in Camel Case to Snake Case ...")
    data.columns = [camel_to_snake(col) for col in data.columns]
    # print(data.columns)

    return data


@test
def test_output(output, *args) -> None:
    """
    Add three assertions:
    1.vendor_id is one of the existing values in the column (currently)
    2.passenger_count is greater than 0
    3.trip_distance is greater than 0
    """
    assert output['vendor_id'].isin([1, 2]).all(), 'There is vendor id not existing in the current dataframe.'
    assert not output['passenger_count'].isin([0]).any(), 'There is ride with zero passenger.'
    assert not output['trip_distance'].isin([0]).any(), 'There is trip with zero distance.'