"""Ingesting Data"""
import os
import sqlite3
import time
import logging
import pandas as pd
import numpy as np

logging.basicConfig(
    filename="answers/solution.log",
    filemode="a",
    format="%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger("Ingest Data")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def ingest_data(directory):
    """Ingesting Data into database
    Args:
        directory (_type_): path of the directory
    """
    # List to store Pandas dataframes for each file
    start = time.time()
    logger.info(f"Start time: {start}")
    dfs = []

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)

                # Create Pandas dataframe from text file
                df = pd.read_csv(
                    filepath,
                    sep="\t",
                    header=None,
                    names=[
                        "date",
                        "maximum_temperature",
                        "minimum_temperature",
                        "precipitation",
                    ],
                )

                station_id = os.path.splitext(filename)[0]
                # Add station_id column
                df["station_id"] = station_id
                dfs.append(df)

        # Concatenate Pandas dataframes into one
        df = pd.concat(dfs)
        logger.info(f"No of records found: {len(df)}")
        # Drop rows with -9999 indicating empty values
        sdf = df[
            (df["maximum_temperature"] != -9999)
            | (df["minimum_temperature"] != -9999)
            | (df["precipitation"] != -9999)
        ]

        sdf = sdf.replace(-9999, np.nan)
        # Compute the final dataframe
        stats = (
            sdf.groupby(["station_id", sdf["date"].astype(str).str[:4]])
            .agg(
                {
                    "maximum_temperature": "mean",
                    "minimum_temperature": "mean",
                    "precipitation": "sum",
                }
            )
            .reset_index()
        )

        # Rename columns
        stats.rename(
            columns={
                "date": "year",
                "maximum_temperature": "avg_max_temp",
                "minimum_temperature": "avg_min_temp",
                "precipitation": "total_acc_precipitation",
            },
            inplace=True,
        )

        # Create a SQLite database connection
        conn = sqlite3.connect("src/db.sqlite3")
        
        logger.info(f"Inserting Rows...")
        # Write data to the database
        weather_rows_inserted = df.to_sql(
            "app_weather", conn, if_exists="replace", index=True, index_label="id"
        )
        logger.info(f"Weather Rows inserted: {weather_rows_inserted}")
        weather_stat_rows_inserted = stats.to_sql(
            "app_weatherstats", conn, if_exists="replace", index=True, index_label="id"
        )
        logger.info(f"Weather Stats Rows inserted: {weather_stat_rows_inserted}")

    except Exception as ex:
        print("Failed to ingest data", ex)
    # Close the database connection
    conn.close()
    end = time.time()
    logger.info(f"Data Ingested in: {end - start:.2f} seconds")


ingest_data("./wx_data")
