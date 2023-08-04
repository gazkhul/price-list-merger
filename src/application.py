import csv
import sys

import numpy as np
import pandas as pd
from pandas import DataFrame

from core.constants import (
    COLUMNS_ORDER,
    DOUBLEQUOTE,
    EMPTY_PHOTO,
    ENCODINGS_LIST,
    OUTPUT_FILE,
    PRICE,
    PRODUCT_NAME,
    PRODUCT_PHOTO,
    PRODUCT_TYPE,
    RRP,
    TECHNOSTOR_COLUMNS_TO_RENAME,
    TECHNOSTOR_DROP_LIST,
    VSTROYKA_SOLO_COLUMNS_TO_RENAME,
    VSTROYKA_SOLO_DROP_LIST,
)


# from tqdm import tqdm
# tqdm.pandas(desc="qqqqqqqq")
# .progress_apply(lambda x: pd.Timestamp).reset_index()


def read_csv_file(file_path: str) -> None | DataFrame:
    """
    Reads a CSV file using pandas. Automatically detects encoding,
    separator, and set quote character.
    """
    try:
        for encoding in ENCODINGS_LIST:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    dialect = csv.Sniffer().sniff(file.read(2048))
                    delimiter = dialect.delimiter
                    quotechar = DOUBLEQUOTE
                df = pd.read_csv(
                    file_path,
                    sep=delimiter,
                    quotechar=quotechar,
                    encoding=encoding,
                )
                return df
            except UnicodeDecodeError:
                continue
        return None
    except FileNotFoundError as e:
        raise SystemExit(f"Error reading the CSV file: {e}")


def drop_unwanted_columns(
    df1: DataFrame, df2: DataFrame
) -> tuple[DataFrame, DataFrame]:
    """
    Removes unwanted columns from the input DataFrames
    based on predefined drop lists.
    """
    for col in df1.columns:
        if col in TECHNOSTOR_DROP_LIST:
            df1.drop(col, axis=1, inplace=True)

    for col in df2.columns:
        if col in VSTROYKA_SOLO_DROP_LIST:
            df2.drop(col, axis=1, inplace=True)

    return df1, df2


def rename_columns(
    df1: DataFrame, df2: DataFrame
) -> tuple[DataFrame, DataFrame]:
    """
    Renames the columns of two DataFrames,
    according to predefined column mappings.
    """
    df1 = df1.rename(columns=TECHNOSTOR_COLUMNS_TO_RENAME)
    df2 = df2.rename(columns=VSTROYKA_SOLO_COLUMNS_TO_RENAME)

    return df1, df2


def product_photo_operations(df_list):
    for df in df_list:
        df.loc[df[PRODUCT_PHOTO] == EMPTY_PHOTO, PRODUCT_PHOTO] = np.nan

    technostor_arr = (
        df_list[0].set_index(PRODUCT_NAME)[PRODUCT_PHOTO].to_dict()
    )
    vstroyka_arr = df_list[1].set_index(PRODUCT_NAME)[PRODUCT_PHOTO].to_dict()

    for i in technostor_arr:
        if i is np.nan and i in vstroyka_arr:
            technostor_arr[i] = vstroyka_arr.get(i)

    for i in vstroyka_arr:
        if i is np.nan or i in technostor_arr:
            vstroyka_arr[i] = technostor_arr.get(i)

    df_list[0][PRODUCT_PHOTO] = df_list[0][PRODUCT_NAME].map(technostor_arr)

    df_list[1][PRODUCT_PHOTO] = df_list[1][PRODUCT_NAME].map(vstroyka_arr)

    return df_list


def concatenate_dataframes(*dataframes: DataFrame):
    """
    Concatenates multiple DataFrames while aligning columns
    according to a specified order. Updates the Price column
    based on the values in the RRP column.
    """
    df_list = []
    for df in dataframes:
        for col in COLUMNS_ORDER:
            if col not in df.columns:
                df[col] = 0
        df_list.append(df[COLUMNS_ORDER])

    df_list = product_photo_operations(df_list)

    for df in df_list:
        df[PRICE] = df.apply(
            lambda row: row[RRP]
            if pd.notnull(row[RRP]) and row[RRP] > 0
            else row[PRICE],
            axis=1,
        )

    df = pd.concat(df_list)

    return df


def main(*args: tuple[str, str]):
    df1 = read_csv_file(args[0])
    df2 = read_csv_file(args[1])

    df1, df2 = drop_unwanted_columns(df1, df2)

    df1, df2 = rename_columns(df1, df2)

    df = concatenate_dataframes(df1, df2)

    df = df.sort_values([PRODUCT_NAME, PRICE], ascending=True).drop_duplicates(
        subset=[PRODUCT_NAME], keep="first"
    )

    df = df.sort_values([PRODUCT_TYPE, PRODUCT_NAME])

    df = df.iloc[:, :8]

    df.to_csv(OUTPUT_FILE, encoding="utf-8", index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
