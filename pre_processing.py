import pandas as pd
import yfinance as yf
import sys
import csv
import os
from typing import List


def extract_symbols(filepath: str) -> str:
    with open(filepath, mode="r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        symbols = []

        for row in csv_reader:
            symbol = row[0]
            symbols.append(symbol)

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

    filename, extension = os.path.splitext(os.path.basename(filepath))

    new_filename1 = f"download_failed_{filename}{extension}"
    output_filepath1 = os.path.join(directory1, new_filename1)
    with open(output_filepath1, "w") as output_file:
        output_file.write(",".join(failed_tickers))
    print(f"Failed downloads saved to {output_filepath1}")

    new_filename2 = f"NaN_values_{filename}{extension}"
    output_filepath2 = os.path.join(directory1, new_filename2)
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


def main(filepath: str, start_date: str, end_date: str) -> None:
    filepath1 = extract_symbols(filepath)
    check_integrity(filepath1, start_date, end_date)


if __name__ == "__main__":
    # Check if CLI arguments are correct
    if len(sys.argv) != 4:
        print("Uso: python3 pre_processing.py <filepath.csv> <start_date> <end_date>")
        sys.exit(1)

    filepath = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")

    main(filepath, start_date, end_date)
