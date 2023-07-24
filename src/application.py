import csv

import pandas as pd


def read_csv_file(file_path):
    """
    Reads a CSV file using pandas. Automatically detects encoding,
    separator, and set quote character.
    """
    encodings = ["utf-8", "cp1251"]
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                dialect = csv.Sniffer().sniff(file.read(2048))
                delimiter = dialect.delimiter
                quotechar = dialect.quotechar if dialect.doublequote else '"'
            df = pd.read_csv(file_path, sep=delimiter, quotechar=quotechar)
            return df
        except FileNotFoundError as e:
            raise SystemExit(f"Error reading the CSV file: {e}")


if __name__ == "__main__":
    # print(read_csv_file("price_0.csv"))
    read_csv_file("price_1.csv")
