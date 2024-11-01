import pandas as pd
import yfinance as yf
import sys
import csv
import os
from typing import List


def extract_symbols(filepath: str, exch: str) -> str:
    symbols = []
    with open(filepath, mode="r", encoding="latin-1") as file:
        if exch == "b3":
            csv_reader = csv.reader(file, delimiter=";")
            next(csv_reader)
            next(csv_reader)
            for row in csv_reader:
                symbol = row[0] + ".SA"
                symbols.append(symbol)
            symbols = symbols[:-2]
        elif exch in {"nyse", "nasdaq", "sp100"}:
            csv_reader = csv.reader(file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                symbol = row[0]
                symbol = symbol.replace("/", "-").replace(".", "-")
                symbols.append(symbol)
        else:
            raise ValueError(
                f"Invalid exchange '{exch}'. Must be 'b3', 'nyse', 'nasdaq' or 'sp100'"
            )

    directory = os.path.dirname(filepath)
    filename, extension = os.path.splitext(os.path.basename(filepath))
    new_filename = f"parsed_{filename}{extension}"
    output_filepath = os.path.join(directory, new_filename)
    with open(output_filepath, "w") as output_file:
        output_file.write(",".join(symbols))

    return output_filepath


def check_integrity(filepath: str, start_date: str, end_date: str) -> None:
    """
    Check the integrity of stock data by downloading adjusted close prices from Yahoo Finance.

    Args:
        filepath (str): The path to the CSV file containing stock symbols.
        start_date (str): The start date for downloading stock data (YYYY-MM-DD).
        end_date (str): The end date for downloading stock data (YYYY-MM-DD).
    """
    tickers = []
    with open(filepath, "r") as file:
        for line in file:
            tickers.extend(line.strip().split(","))

    dados = pd.DataFrame()
    failed_tickers = []
    i = 0

    for stock in tickers:
        i += 1
        print(f"Downloading data from {stock}... ({i}/{len(tickers)})")
        stock_data = yf.download(stock, start=start_date, end=end_date)[["Adj Close"]]
        if stock_data.empty:
            print(f"No data found for {stock}, skipping...")
            failed_tickers.append(stock)
            continue
        else:
            dados = pd.concat([dados, stock_data], axis=1)

    # Identify columns with NaN values
    columns_with_nan = dados.columns[dados.isna().any()].tolist()
    dados_dropped = dados[columns_with_nan].columns.get_level_values(1).tolist()

    # Remove stocks with NaN values from original DataFrame
    dados_clean = dados.drop(columns=columns_with_nan)
    cleaned_symbols = dados_clean.columns.get_level_values(1).tolist()

    # Save stocks symbols that failed the dowload
    directory1 = "removed_data"
    if not os.path.exists(directory1):
        print(f"Warning: The directory {directory1} does not exist. Creating it.")
        os.makedirs(directory1, exist_ok=True)

    directory_d = "failed_download"
    directory_d = os.path.join(directory1, directory_d)
    if not os.path.exists(directory_d):
        print(f"Warning: The directory {directory_d} does not exist. Creating it.")
        os.makedirs(directory_d, exist_ok=True)

    filename, extension = os.path.splitext(os.path.basename(filepath))

    new_filename_d = f"download_failed_{filename}{extension}"
    output_filepath1 = os.path.join(directory_d, new_filename_d)
    with open(output_filepath1, "w") as output_file:
        output_file.write(",".join(failed_tickers))
    print(f"Failed downloads saved to {output_filepath1}")

    directory_n = "NaN_values"
    directory_n = os.path.join(directory1, directory_n)
    if not os.path.exists(directory_n):
        print(f"Warning: The directory {directory_n} does not exist. Creating it.")
        os.makedirs(directory_n, exist_ok=True)

    new_filename_n = f"NaN_values_{filename}{extension}"
    output_filepath2 = os.path.join(directory_n, new_filename_n)
    with open(output_filepath2, "w") as output_file:
        output_file.write(",".join(dados_dropped))
    print(f"NaN values saved to {output_filepath2}")

    # Save stocks that contained NaN values
    directory2 = "pre_processed_data"
    if not os.path.exists(directory2):
        print(f"Warning: The directory {directory2} does not exist. Creating it.")
        os.makedirs(directory2, exist_ok=True)

    new_filename3 = f"pre_processed_{filename}{extension}"
    output_filepath3 = os.path.join(directory2, new_filename3)
    with open(output_filepath3, "w") as output_file:
        output_file.write(",".join(cleaned_symbols))
    print(f"Cleaned data saved to {output_filepath3}")
