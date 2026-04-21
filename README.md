# Simplified Trading Bot for Binance Futures Testnet

Python 3 command-line trading bot to place **MARKET**, **LIMIT**, and **STOP-LIMIT** orders on Binance USDT-M Futures Testnet with structured validation, logging, and exception handling.

## Features

- Places MARKET orders
- Places LIMIT orders
- Places STOP-LIMIT orders (bonus)
- Supports BUY and SELL
- Uses `argparse`-based CLI
- Validates all user inputs before API calls
- Handles validation, network, authentication, and API errors
- Logs API requests, responses, and exceptions to `trading_bot.log`
- Prints clean request, response, and final status output

## Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── cli.py
├── README.md
└── requirements.txt
```

## Setup

### 1) Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Set environment variables

Set your Binance Futures Testnet API credentials:

Windows PowerShell:

```powershell
$env:BINANCE_API_KEY="your_testnet_api_key"
$env:BINANCE_API_SECRET="your_testnet_api_secret"
```

macOS/Linux:

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

Optional `.env` file (same directory as `cli.py`):

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

## How to Run

### MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

### STOP-LIMIT order (bonus)

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP-LIMIT --quantity 0.01 --price 59500 --stop_price 59600
```

## CLI Arguments

- `--symbol` (required): trading pair symbol, e.g., `BTCUSDT`
- `--side` (required): `BUY` or `SELL`
- `--type` (required): `MARKET`, `LIMIT`, or `STOP-LIMIT`
- `--quantity` (required): positive float quantity
- `--price` (required for `LIMIT` and `STOP-LIMIT`): positive float limit price
- `--stop_price` (required for `STOP-LIMIT`): positive float stop trigger price

## Sample Console Output

```text
Order Request Summary:
- Symbol: BTCUSDT
- Side: BUY
- Order Type: MARKET
- Quantity: 0.01

Order Response Details:
- orderId: 123456789
- status: NEW
- executedQty: 0.01
- avgPrice: 0

Final Status: SUCCESS - Order placed successfully.
```

## Example Log Output

### MARKET order

```text
2026-04-21 10:22:11,003 - INFO - Testing Binance Futures Testnet connectivity.
2026-04-21 10:22:11,210 - INFO - Connected to Binance Futures Testnet successfully.
2026-04-21 10:22:11,212 - INFO - Sending MARKET order BTCUSDT BUY qty=0.01 price=None stopPrice=None
2026-04-21 10:22:11,212 - INFO - API request payload: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
2026-04-21 10:22:11,514 - INFO - API response: {'orderId': 12345, 'status': 'NEW', 'executedQty': '0.01', 'avgPrice': '0'}
2026-04-21 10:22:11,514 - INFO - Order placed successfully orderId=12345 status=NEW
```

### LIMIT order

```text
2026-04-21 10:25:42,113 - INFO - Sending LIMIT order BTCUSDT SELL qty=0.01 price=60000.0 stopPrice=None
2026-04-21 10:25:42,114 - INFO - API request payload: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.01, 'price': 60000.0, 'timeInForce': 'GTC'}
2026-04-21 10:25:42,404 - INFO - API response: {'orderId': 12346, 'status': 'NEW', 'executedQty': '0', 'avgPrice': '0'}
2026-04-21 10:25:42,404 - INFO - Order placed successfully orderId=12346 status=NEW
```

## Error Handling Covered

- Invalid symbol format
- Invalid side or order type
- Missing `--price` for LIMIT/STOP-LIMIT
- Missing `--stop_price` for STOP-LIMIT
- Negative or zero quantity/price values
- Network request failures
- Binance API failures
- Missing/invalid authentication credentials

## Assumptions

- Binance Futures Testnet API key/secret are active and authorized for futures trading.
- Symbol is provided in uppercase Binance format (e.g., `BTCUSDT`).
- User runs commands from the `trading_bot` project root.

