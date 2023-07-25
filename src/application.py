import csv
import sys

import pandas as pd
from pandas import DataFrame

from core.constants import (
    DOUBLEQUOTE,
    ENCODINGS_LIST,
    TECHNOSTOR_DROP_LIST,
    VSTROYKA_SOLO_DROP_LIST,
)


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


def main(*args):
    df1 = read_csv_file(args[0])
    df2 = read_csv_file(args[1])

    df1, df2 = drop_unwanted_columns(df1, df2)

    print(df1)

    # df1 = df1.rename(
    #     columns={
    #         "Артикул": "Код артикула",
    #         "Категория": "Тип товаров",
    #         "Производитель": "Производитель",
    #         "Товар": "Наименование",
    #         "Цена": "Цена",
    #         "РРЦ": "РРЦ",
    #         "Москва": "В наличии",
    #         "Модель": "Модель",
    #         "Изображение": "Изображения товаров",
    #     }
    # )
    # df2 = df2.rename(
    #     columns={
    #         "Артикул": "Код артикула",
    #         "Категория": "Тип товаров",
    #         "Бренд": "Производитель",
    #         "Наименование": "Наименование",
    #         "Цена": "Цена",
    #         "Раздел": "В наличии",
    #         "Модель": "Модель",
    #         "Фото": "Изображения товаров",
    #         "РРЦ": "РРЦ",
    #     }
    # )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
