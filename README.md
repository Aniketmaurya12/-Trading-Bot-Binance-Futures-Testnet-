# Binance Futures Testnet Trading Bot

A production-quality Python CLI application that places **MARKET**, **LIMIT**, and **STOP_LIMIT** orders on the [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com). Built with clean, modular architecture and full logging.

---

## Features

- Place **MARKET**, **LIMIT**, and **STOP_LIMIT** (bonus) orders via the command line
- Supports both **BUY** and **SELL** sides
- Full **input validation** with descriptive error messages
- Structured **file logging** (`trading_bot.log`) with timestamps, levels, and messages
- Clear **console output** — request summary, response details, and final status
- Credentials loaded securely from **environment variables** (never hardcoded)
- Clean, modular project layout — ready for GitHub

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package exports
│   ├── client.py            # Binance Futures Testnet client factory
│   ├── orders.py            # MARKET / LIMIT / STOP_LIMIT order functions
│   ├── validators.py        # Input validation utilities
│   └── logging_config.py   # Logging setup (file + console handlers)
│
├── cli.py                   # CLI entry point (argparse)
├── README.md
└── requirements.txt
```

---

## Requirements

- Python 3.9+
- A free [Binance Futures Testnet](https://testnet.binancefuture.com) account with API keys

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root (loaded automatically via `python-dotenv`):

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> **Never** commit your `.env` file. Add it to `.gitignore`.

Alternatively, export them in your shell:

```bash
export BINANCE_API_KEY="your_testnet_api_key_here"
export BINANCE_API_SECRET="your_testnet_api_secret_here"
```

---

## Usage

```
python cli.py --symbol SYMBOL --side SIDE --type TYPE --quantity QTY [--price PRICE] [--stop_price STOP_PRICE]
```

| Argument | Required | Description |
|---|---|---|
| `--symbol` | ✅ | Trading pair, e.g. `BTCUSDT` |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET`, `LIMIT`, or `STOP_LIMIT` |
| `--quantity` | ✅ | Positive float, e.g. `0.01` |
| `--price` | ⚠️ LIMIT / STOP_LIMIT | Limit fill price |
| `--stop_price` | ⚠️ STOP_LIMIT only | Trigger price |

---

## Example Commands

**Market buy**
```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.01
```

**Limit sell**
```bash
python cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.01 \
  --price 60000
```

**Stop-limit buy (bonus)**
```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP_LIMIT \
  --quantity 0.01 \
  --price 62000 \
  --stop_price 61500
```

---

## Sample Output

### MARKET order

```
====================================================
          ORDER REQUEST SUMMARY
====================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.01
====================================================

====================================================
          ORDER RESPONSE DETAILS
====================================================
  Order ID     : 3951823410
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 63412.50000000
====================================================

  ✅  SUCCESS — Order placed on Binance Futures Testnet.
```

### LIMIT order

```
====================================================
          ORDER REQUEST SUMMARY
====================================================
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : LIMIT
  Quantity   : 0.01
  Price      : 60000.0
====================================================

====================================================
          ORDER RESPONSE DETAILS
====================================================
  Order ID     : 3951823511
  Status       : NEW
  Executed Qty : 0.00
====================================================

  ✅  SUCCESS — Order placed on Binance Futures Testnet.
```

### Validation failure

```
====================================================
          ORDER REQUEST SUMMARY
====================================================
  ...

  ❌  FAILURE — Price is required for LIMIT orders.
```

---

## Log File

All API activity is written to `trading_bot.log` in the project root:

```
2024-07-15 14:23:01 [INFO]  trading_bot.orders - Sending MARKET order | symbol=BTCUSDT side=BUY qty=0.01
2024-07-15 14:23:02 [INFO]  trading_bot.orders - MARKET order placed successfully | orderId=3951823410 status=FILLED executedQty=0.01
2024-07-15 14:25:10 [INFO]  trading_bot.orders - Sending LIMIT order | symbol=BTCUSDT side=SELL qty=0.01 price=60000
2024-07-15 14:25:11 [INFO]  trading_bot.orders - LIMIT order placed successfully | orderId=3951823511 status=NEW executedQty=0.00
2024-07-15 14:27:00 [ERROR] trading_bot.validators - Invalid quantity '-1.0'. Quantity must be a positive number.
2024-07-15 14:28:45 [ERROR] trading_bot.orders - API error placing MARKET order: APIError(code=-1121): Invalid symbol.
```

---

## Error Handling

The bot handles the following error conditions gracefully:

| Error | Handled by |
|---|---|
| Missing / invalid `BINANCE_API_KEY` or `BINANCE_API_SECRET` | `client.py` |
| Invalid symbol format | `validators.py` |
| Invalid side (not BUY/SELL) | `validators.py` |
| Invalid order type | `validators.py` |
| Negative or zero quantity | `validators.py` |
| Missing price for LIMIT / STOP_LIMIT | `validators.py` |
| Missing stop_price for STOP_LIMIT | `validators.py` |
| Binance API / order errors | `orders.py` |
| Network / connection errors | `client.py` + `orders.py` |

---

## Assumptions

1. The Binance Futures Testnet environment is used; no real funds are involved.
2. API keys must be obtained from [https://testnet.binancefuture.com](https://testnet.binancefuture.com).
3. Quantity precision must comply with the specific symbol's lot-size filter on the testnet; submitting a quantity with too many decimal places will result in a Binance API error (`-1111`).
4. `STOP_LIMIT` maps to Binance Futures order type `STOP` (trigger + limit price).
5. All LIMIT orders use `timeInForce=GTC` (Good Till Cancelled).
6. The `.env` file approach is provided for developer convenience; production deployments should inject secrets via a secrets manager (Vault, AWS Secrets Manager, etc.).
