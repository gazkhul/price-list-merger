import csv
import sys

import pandas as pd
from pandas import DataFrame

from core.constants import (
    COLUMNS_ORDER,
    DOUBLEQUOTE,
    ENCODINGS_LIST,
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
    df1 = df1.rename(columns=TECHNOSTOR_COLUMNS_TO_RENAME)
    df2 = df2.rename(columns=VSTROYKA_SOLO_COLUMNS_TO_RENAME)

    return df1, df2


def concatenate_dataframes(*dataframes: DataFrame):
    df_list = []
    for df in dataframes:
        for col in COLUMNS_ORDER:
            if col not in df.columns:
                df[col] = 0
        df[COLUMNS_ORDER]
        df_list.append(df)

    combined_df = pd.concat(df_list).drop_duplicates(subset=["Наименование"])

    return combined_df


def main(*args: tuple[str, str]):
    df1 = read_csv_file(args[0])
    df2 = read_csv_file(args[1])

    df1, df2 = drop_unwanted_columns(df1, df2)

    df1, df2 = rename_columns(df1, df2)

    df = concatenate_dataframes(df1, df2)

    df.to_csv("merged.csv", index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
