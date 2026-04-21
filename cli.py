#!/usr/bin/env python3
"""
cli.py — Command-line entry point for the Binance Futures Testnet trading bot.

Usage examples
--------------
# Market buy
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Limit sell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000

# Stop-limit buy (bonus order type)
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT \\
    --quantity 0.01 --price 62000 --stop_price 61500
"""

import argparse
import sys
from typing import Optional

from dotenv import load_dotenv

from bot.client import create_client
from bot.logging_config import setup_logging
from bot.orders import dispatch_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

# ──────────────────────────────────────────────────────────────────────────────
# Bootstrap
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()
logger = setup_logging()


# ──────────────────────────────────────────────────────────────────────────────
# CLI argument parser
# ──────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place MARKET, LIMIT, or STOP_LIMIT orders on Binance Futures Testnet.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair symbol, e.g. BTCUSDT.",
    )
    parser.add_argument(
        "--side", required=True,
        help="Order side: BUY or SELL.",
    )
    parser.add_argument(
        "--type", dest="order_type", required=True,
        help="Order type: MARKET, LIMIT, or STOP_LIMIT.",
    )
    parser.add_argument(
        "--quantity", required=True, type=float,
        help="Order quantity (must be positive).",
    )
    parser.add_argument(
        "--price", type=float, default=None,
        help="Limit price. Required for LIMIT and STOP_LIMIT orders.",
    )
    parser.add_argument(
        "--stop_price", type=float, default=None,
        help="Trigger (stop) price. Required for STOP_LIMIT orders.",
    )
    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Output helpers
# ──────────────────────────────────────────────────────────────────────────────

_SEP = "=" * 52


def print_request_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
    stop_price: Optional[float],
) -> None:
    """Print a formatted order-request summary to the console."""
    print(f"\n{_SEP}")
    print("          ORDER REQUEST SUMMARY")
    print(_SEP)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Order Type : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price}")
    print(_SEP)


def print_order_response(result: dict) -> None:
    """Print a formatted order-response block to the console."""
    print(f"\n{_SEP}")
    print("          ORDER RESPONSE DETAILS")
    print(_SEP)
    print(f"  Order ID     : {result.get('orderId')}")
    print(f"  Status       : {result.get('status')}")
    print(f"  Executed Qty : {result.get('executedQty')}")
    avg_price = result.get("avgPrice")
    if avg_price and str(avg_price) not in ("0", "0.00000000", ""):
        print(f"  Avg Price    : {avg_price}")
    print(_SEP)


def print_final_status(success: bool, message: str = "") -> None:
    """Print the final SUCCESS or FAILURE banner."""
    print()
    if success:
        print("  ✅  SUCCESS — Order placed on Binance Futures Testnet.")
    else:
        print(f"  ❌  FAILURE — {message}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Main flow
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    """
    Parse CLI args, validate inputs, place the order, and display results.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    parser = build_parser()
    args = parser.parse_args()

    # ── Validation ─────────────────────────────────────────────────────────
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)
        price      = validate_price(args.price, order_type)
        stop_price = validate_stop_price(args.stop_price, order_type)
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print_final_status(False, str(exc))
        return 1

    # ── Display request summary ─────────────────────────────────────────────
    print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    # ── Create Binance client ───────────────────────────────────────────────
    try:
        client = create_client()
    except EnvironmentError as exc:
        logger.error("Environment error: %s", exc)
        print_final_status(False, str(exc))
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to create Binance client: %s", exc)
        print_final_status(False, f"Client creation failed: {exc}")
        return 1

    # ── Place order ─────────────────────────────────────────────────────────
    try:
        result = dispatch_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Order placement failed: %s", exc)
        print_final_status(False, str(exc))
        return 1

    # ── Display response & final status ─────────────────────────────────────
    print_order_response(result)
    print_final_status(True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
