import argparse
import csv
import os
import sys
from decimal import Decimal, InvalidOperation
from typing import Dict, List

import requests


BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
FRANKFURTER_URL = "https://api.frankfurter.dev/v2/rate"

TIMEOUT = 10

#major currencies info
CURRENCY_INFO = {
    "USD": {"symbol": "$", "name": "USD"},
    "KES": {"symbol": "KSh", "name": "KES"},
    "EUR": {"symbol": "€", "name": "EUR"},
    "GBP": {"symbol": "£", "name": "GBP"},
    "JPY": {"symbol": "¥", "name": "JPY"},
    "CNY": {"symbol": "¥", "name": "CNY"},
    "INR": {"symbol": "₹", "name": "INR"},
    "AUD": {"symbol": "A$", "name": "AUD"},
    "CAD": {"symbol": "C$", "name": "CAD"},
    "CHF": {"symbol": "CHF", "name": "CHF"},
    "ZAR": {"symbol": "R", "name": "ZAR"},
    "NGN": {"symbol": "₦", "name": "NGN"},
    "GHS": {"symbol": "GH₵", "name": "GHS"},
    "UGX": {"symbol": "USh", "name": "UGX"},
    "TZS": {"symbol": "TSh", "name": "TZS"},
    "RWF": {"symbol": "RF", "name": "RWF"},
}


#binance stablecoins
USD_STABLECOINS = {"USDT","USDC","BUSD",}

def get_binance_price(symbol: str) -> Decimal:
    """current binance price for a trading pair. Example:BTCUSDT = 64582.31"""
    symbol = symbol.upper()

    try:
        response = requests.get(BINANCE_URL,params={"symbol": symbol},timeout=TIMEOUT,)
        response.raise_for_status()

    except requests.RequestException as exception:
        raise RuntimeError(f"Could not fetch {symbol} from Binance: {exception}") from exception

    try:
        data = response.json()
    except ValueError as exception:
        raise RuntimeError(f"Invalid JSON response from Binance for {symbol}") from exception

    if "price" not in data:
        message = data.get("msg", "binance error")
        raise RuntimeError(f"Binance error for {symbol}: {message}")
    try:
        return Decimal(data["price"])
    except (InvalidOperation, TypeError) as exception:
        raise RuntimeError(f"Invalid price returned by Binance for {symbol}") from exception

def get_currency_rate(currency: str) -> Decimal:
    """get usd - currency exchange rate. eg USD/KESUSD/EURUSD/GBP"""
    currency = currency.upper()

    if currency == "USD":
        return Decimal("1")

    try:
        response = requests.get(f"{FRANKFURTER_URL}/USD/{currency}",timeout=TIMEOUT,)
        response.raise_for_status()

    except requests.RequestException as exception:
        raise RuntimeError(f"Could not fetch USD/{currency} exchange rate: {exception}") from exception

    try:
        data = response.json()
    except ValueError as exception:
        raise RuntimeError(f"Invalid JSON response for USD/{currency}") from exception

    if "rate" not in data:
        raise RuntimeError(f"Could not find an exchange rate for USD/{currency}")

    try:
        return Decimal(str(data["rate"]))

    except (InvalidOperation, TypeError) as exception:
        raise RuntimeError(f"Invalid exchange rate returned for USD/{currency}") from exception

def get_asset_usd_price(asset: str) -> Decimal:
    """convert a binance crypto assetto approximate usd value. eg:BTC -> BTCUSDTETH -> ETHUSDT"""
    asset = asset.upper()

    #usd stablecoins are approximately $1.
    if asset in USD_STABLECOINS:
        return Decimal("1")

    symbol = f"{asset}USDT"

    try:
        return get_binance_price(symbol)

    except RuntimeError as exception:
        raise RuntimeError(f"Cannot convert Binance quote asset {asset} to USD. "f"Tried {symbol}.") from exception

def get_price_in_usd(symbol: str) -> Decimal:
    """get the approximate usd price of one unit of the base asset.
    eg
        BTCUSDT -> BTC price directly
        ETHUSDT -> ETH price directly
        ETHBTC  -> ETH/BTC * BTC/USD
        ETHEUR  -> ETH/EUR * EUR/USD
    """
    symbol = symbol.upper()

    price = get_binance_price(symbol)

    #check longer quote assets first.
    quote_assets = [
        "USDT",
        "USDC",
        "BUSD",
        "FDUSD",
        "TUSD",
        "BTC",
        "ETH",
        "BNB",
        "EUR",
        "GBP",
        "AUD",
        "TRY",
        "BRL",
        "RUB",
        "DAI",
    ]

    quote_asset = None

    for quote in quote_assets:
        if symbol.endswith(quote):
            quote_asset = quote
            break

    if quote_asset is None:
        raise RuntimeError(f"Could not determine quote currency for {symbol}. "
            "Please use a Binance pair with a supported quote asset.")

    base_asset = symbol[:-len(quote_asset)]

    if not base_asset:
        raise RuntimeError(f"Could not determine base asset for {symbol}")

    #USDT/USDC/BUSD treated approximately as USD.
    if quote_asset in USD_STABLECOINS:
        return price

    #crypto quote assets.
    # ETHBTC = BTC per ETH
    # BTCUSDT = USD per BTC
    # ETH USD = ETHBTC * BTCUSDT
    if quote_asset in {"BTC","ETH","BNB","DAI",}:
        quote_usd = get_asset_usd_price(quote_asset)
        return price * quote_usd

    #fiat quote currencies.
    #ETH/EUR * EUR/USD
    #Frankfurter gives USD/EUR, so invert it.
    if quote_asset in CURRENCY_INFO:
        usd_to_quote = get_currency_rate(quote_asset)

        if usd_to_quote == 0:
            raise RuntimeError(f"Invalid zero exchange rate for USD/{quote_asset}")
        return price / usd_to_quote

    raise RuntimeError(f"Unsupported quote asset {quote_asset} in {symbol}")


def format_money(value: Decimal, currency: str) -> str:
    """format a number using the appropriate currency symbol"""
    currency = currency.upper()

    info = CURRENCY_INFO.get(
        currency,
        {
            "symbol": currency,
            "name": currency,
        },
    )

    symbol = info["symbol"]
    return f"{symbol} {value:,.2f}"


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch cryptocurrency prices from Binance, "
            "convert them to one or more currencies, "
            "and output the results to the terminal, CSV, "
            "or PostgreSQL."
        )
    )

    parser.add_argument(
        "--symbol",
        nargs="+",
        required=True,
        help=(
            "One or more Binance trading symbols. "
            "Example: BTCUSDT ETHUSDT SOLUSDT"
        ),
    )

    parser.add_argument(
        "--currency",
        nargs="+",
        default=["KES"],
        help=(
            "One or more target currencies. "
            "Default: KES. "
            "Example: KES USD EUR GBP"
        ),
    )

    parser.add_argument(
        "--output",
        choices=["terminal", "csv", "postgres"],
        default="terminal",
        help=(
            "Output destination. "
            "Default: terminal. "
            "Options: terminal, csv, postgres"
        ),
    )

    parser.add_argument(
        "--csv-file",
        default="crypto_prices.csv",
        help=(
            "CSV output filename when --output csv is used. "
            "Default: crypto_prices.csv"
        ),
    )

    return parser.parse_args()

def print_single_result(symbol: str,usd_price: Decimal,currencies: List[str],rates: Dict[str, Decimal],) -> None:
    print()
    print("-" * 50)
    print("BINANCE CRYPTO PRICE")
    print("_" * 50)

    print(f"{'Symbol:':<20}{symbol}")

    print(
        f"{'USD Price:':<20}"
        f"{format_money(usd_price, 'USD')}"
    )

    for currency in currencies:
        converted = usd_price * rates[currency]

        print(
            f"{'Price ' + currency + ':':<20}"
            f"{format_money(converted, currency)}"
        )

        if currency == "KES":
            print(
                f"{'USD/KES Rate:':<20}"
                f"{rates[currency]:,.2f}"
            )

    print("-" * 50)
    print("Source: Binance")
    print("_" * 50)


def print_multiple_results(results: Dict[str, Decimal],currencies: List[str],rates: Dict[str, Decimal],) -> None:
    print()
    print("_" * 80)

    header = f"{'SYMBOL':<15}"
    header += f"{'USD PRICE':<20}"

    for currency in currencies:
        header += f"{currency + ' PRICE':<25}"

    print(header)
    print("_" * 80)

    for symbol, usd_price in results.items():
        row = f"{symbol:<15}"
        row += f"{format_money(usd_price, 'USD'):<20}"

        for currency in currencies:
            converted = usd_price * rates[currency]

            row += f"{format_money(converted, currency):<25}"

        print(row)

    print("_" * 80)


def build_output_rows(results: Dict[str, Decimal],currencies: List[str],rates: Dict[str, Decimal],) -> List[Dict[str, object]]:
    """convert transformed results into flat records.
    each row represents one cryptocurrency/currency combination.
    eg
        BTCUSDT | USD | 65000 | 65000
        BTCUSDT | KES | 65000 | 8500000
    """
    rows = []

    for symbol, usd_price in results.items():
        for currency in currencies:
            converted = usd_price * rates[currency]
            rows.append(
                {
                    "symbol": symbol,
                    "currency": currency,
                    "usd_price": usd_price,
                    "exchange_rate": rates[currency],
                    "converted_price": converted,
                }
            )

    return rows


def write_csv(rows: List[Dict[str, object]],filename: str,) -> None:
    """write transformed results to csv"""
    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=[
                    "symbol",
                    "currency",
                    "usd_price",
                    "exchange_rate",
                    "converted_price",
                ],
            )

            writer.writeheader()

            for row in rows:
                writer.writerow(
                    {
                        "symbol": row["symbol"],
                        "currency": row["currency"],
                        "usd_price": str(row["usd_price"]),
                        "exchange_rate": str(
                            row["exchange_rate"]
                        ),
                        "converted_price": str(
                            row["converted_price"]
                        ),
                    }
                )

    except OSError as exception:
        raise RuntimeError(
            f"Could not write CSV file {filename}: {exception}"
        ) from exception


def get_postgres_connection():
    try:
        import psycopg2
    except ImportError as exception:
        raise RuntimeError(
            "PostgreSQL support requires psycopg2-binary. "
            "Install it with: pip install psycopg2-binary"
        ) from exception

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    missing = []

    if not host:
        missing.append("POSTGRES_HOST")

    if not database:
        missing.append("POSTGRES_DB")

    if not user:
        missing.append("POSTGRES_USER")

    if not password:
        missing.append("POSTGRES_PASSWORD")

    if missing:
        raise RuntimeError(
            "Missing PostgreSQL environment variables: "
            + ", ".join(missing)
        )

    try:
        return psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=10,
        )

    except psycopg2.Error as exception:
        raise RuntimeError(
            f"Could not connect to PostgreSQL: {exception}"
        ) from exception


def write_postgres(rows: List[Dict[str, object]],) -> None:
    """insert transformed results into postgres. table is created automatically if it does not exist."""
    connection = get_postgres_connection()

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id BIGSERIAL PRIMARY KEY,
            symbol VARCHAR(50) NOT NULL,
            currency VARCHAR(10) NOT NULL,
            usd_price NUMERIC(30, 12) NOT NULL,
            exchange_rate NUMERIC(30, 12) NOT NULL,
            converted_price NUMERIC(30, 12) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """

    insert_sql = """
        INSERT INTO crypto_prices (
            symbol,
            currency,
            usd_price,
            exchange_rate,
            converted_price
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        );
    """

    try:
        with connection:
            with connection.cursor() as cursor:

                cursor.execute(create_table_sql)

                for row in rows:
                    cursor.execute(
                        insert_sql,
                        (
                            row["symbol"],
                            row["currency"],
                            row["usd_price"],
                            row["exchange_rate"],
                            row["converted_price"],
                        ),
                    )

    except Exception as exception:
        raise RuntimeError(
            f"Could not write data to PostgreSQL: {exception}"
        ) from exception

    finally:
        connection.close()


def output_results(output: str,results: Dict[str, Decimal],currencies: List[str],rates: Dict[str, Decimal],csv_file: str,) -> None:
    """send transformed data to the selected output"""
    rows = build_output_rows(results,currencies,rates,)

    if output == "terminal":

        if len(results) == 1:
            symbol = next(iter(results))

            print_single_result(
                symbol,
                results[symbol],
                currencies,
                rates,
            )

        else:
            print_multiple_results(
                results,
                currencies,
                rates,
            )

        return

    if output == "csv":

        write_csv(
            rows,
            csv_file,
        )

        print(
            f"[LOAD] Successfully wrote "
            f"{len(rows)} records to {csv_file}"
        )

        return

    if output == "postgres":

        write_postgres(rows)

        print(
            f"[LOAD] Successfully inserted "
            f"{len(rows)} records into PostgreSQL "
            f"table crypto_prices"
        )

        return

    raise RuntimeError(
        f"Unsupported output destination: {output}"
    )


def main() -> None:
    args = get_arguments()

    symbols = [
        symbol.upper()
        for symbol in args.symbol
    ]

    currencies = [
        currency.upper()
        for currency in args.currency
    ]

    #remove duplicate currencies while preserving order.
    currencies = list(
        dict.fromkeys(currencies)
    )

    print(
        f"[START] Processing {len(symbols)} "
        f"symbol(s) and {len(currencies)} currency/currencies..."
    )

    #extract exchange rates

    rates = {}

    for currency in currencies:

        try:
            print(
                f"[EXTRACT] Fetching USD/{currency} "
                "exchange rate..."
            )

            rates[currency] = get_currency_rate(
                currency
            )

        except RuntimeError as exception:
            print(
                f"[ERROR] {exception}",
                file=sys.stderr,
            )
            sys.exit(1)

    #extract cryptocurrency prices

    results = {}

    for symbol in symbols:

        print(
            f"[EXTRACT] Fetching {symbol} "
            "from Binance..."
        )

        try:
            results[symbol] = get_price_in_usd(
                symbol
            )

        except RuntimeError as exception:
            print(
                f"[ERROR] {exception}",
                file=sys.stderr,
            )

    if not results:
        print(
            "[ERROR] No cryptocurrency prices "
            "could be retrieved.",
            file=sys.stderr,
        )

        sys.exit(1)

    #transform
    print(
        "[TRANSFORM] Calculating approximate "
        "currency values..."
    )

    #load/output

    try:
        output_results(
            output=args.output,
            results=results,
            currencies=currencies,
            rates=rates,
            csv_file=args.csv_file,
        )

    except RuntimeError as exception:
        print(
            f"[ERROR] {exception}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
