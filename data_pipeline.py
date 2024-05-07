import pandas as pd
from sqlalchemy import create_engine

def extract_data(filename: str) -> pd.DataFrame:
    """
    Function yang digunakan untuk Extract Data dari Source Data

    Parameters
    ----------
    filename (str): filename dari data source yang dimiliki

    Returns
    -------
    data (pd.DataFrame): data source yang dalam bentuk DataFrame
    """
    data = pd.read_csv(filename)

    return data

def transform_data(data: list) -> pd.DataFrame:
    """
    Function yang digunakan untuk melakukan proses Transform Data,
    mulai dari menggabungkan menjadi satu dan filter data

    Parameters
    ----------
    data (list): variable yang menampung DataFrame yang akan digabung menjadi satu

    Returns
    -------
    full_data (pd.DataFrame): data yang sudah digabung menjadi satu 
    """
    # concat data 
    full_data = pd.concat(data)

    # filter "selling_price" value more than 14000
    full_data = full_data[full_data["selling_price"] > 14000]

    return full_data

def load_data(data: pd.DataFrame) -> None:
    """
    Function yang digunakan untuk memasukkan data terbaru ke dalam Postgres
    dengan menggunakan Pandas

    Parameters
    ----------
    data (pd.DataFrame): data yang ingin kita insert ke dalam Postgres
    """
    # config database
    DB_USERNAME = "postgres"
    DB_PASSWORD = "mypassword"
    DB_HOST = "localhost"
    DB_PORT = "5434"
    DB_NAME = "db_sales"

    # create database engine
    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # insert database using pandas
    data.to_sql(name = "car_sales",
                con = engine,
                if_exists = "append",
                index = False)


if __name__ == "__main__":
    print("====== Start Data Pipeline Process ======")

    # 1. read data from five sources
    FILE_PATH = "data/"

    print("Start Extracting Data from Source...")
    # read data from each states
    california_data = extract_data(filename = FILE_PATH + "california-sales-data.csv")
    florida_data = extract_data(filename = FILE_PATH + "florida-sales-data.csv")
    georgia_data = extract_data(filename = FILE_PATH + "georgia-sales-data.csv")
    pennsylvania_data = extract_data(filename = FILE_PATH + "pennsylvania-sales-data.csv")
    texas_data = extract_data(filename = FILE_PATH + "texas-sales-data.csv")

    print("End of Process Extracting Data...")

    # 2. transform data
    print("Start Transforming Data...")
    transformed_data = transform_data([california_data, florida_data, georgia_data,
                                       pennsylvania_data, texas_data])

    print("End of Process Transforming Data...")

    # 3. load data
    print("Start Load Data to Database...")
    load_data(data = transformed_data)

    print("End of Process Load Data...")

    print("====== End Data Pipeline Process ======")