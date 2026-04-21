from typing import Any, Dict, Optional
from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.logging_config import get_logger

logger = get_logger("orders")

def _normalise_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "orderId":     raw.get("orderId"),
        "symbol":      raw.get("symbol"),
        "side":        raw.get("side"),
        "type":        raw.get("type"),
        "status":      raw.get("status"),
        "origQty":     raw.get("origQty"),
        "executedQty": raw.get("executedQty"),
        "avgPrice":    raw.get("avgPrice") or raw.get("price"),
    }

def place_market_order(client, symbol, side, quantity):
    logger.info("Sending MARKET order | symbol=%s side=%s qty=%s", symbol, side, quantity)
    try:
        response = client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity)
        result = _normalise_response(response)
        logger.info("MARKET order placed | orderId=%s status=%s", result["orderId"], result["status"])
        return result
    except (BinanceAPIException, BinanceOrderException) as exc:
        logger.error("API error placing MARKET order: %s", exc)
        raise

def place_limit_order(client, symbol, side, quantity, price):
    logger.info("Sending LIMIT order | symbol=%s side=%s qty=%s price=%s", symbol, side, quantity, price)
    try:
        response = client.futures_create_order(symbol=symbol, side=side, type="LIMIT", quantity=quantity, price=price, timeInForce="GTC")
        result = _normalise_response(response)
        logger.info("LIMIT order placed | orderId=%s status=%s", result["orderId"], result["status"])
        return result
    except (BinanceAPIException, BinanceOrderException) as exc:
        logger.error("API error placing LIMIT order: %s", exc)
        raise

def place_stop_limit_order(client, symbol, side, quantity, price, stop_price):
    logger.info("Sending STOP_LIMIT order | symbol=%s side=%s qty=%s price=%s stop=%s", symbol, side, quantity, price, stop_price)
    try:
        response = client.futures_create_order(symbol=symbol, side=side, type="STOP", quantity=quantity, price=price, stopPrice=stop_price, timeInForce="GTC")
        result = _normalise_response(response)
        logger.info("STOP_LIMIT order placed | orderId=%s status=%s", result["orderId"], result["status"])
        return result
    except (BinanceAPIException, BinanceOrderException) as exc:
        logger.error("API error placing STOP_LIMIT order: %s", exc)
        raise

def dispatch_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    if order_type == "MARKET":
        return place_market_order(client, symbol, side, quantity)
    if order_type == "LIMIT":
        return place_limit_order(client, symbol, side, quantity, price)
    if order_type == "STOP_LIMIT":
        return place_stop_limit_order(client, symbol, side, quantity, price, stop_price)
    raise ValueError(f"Unsupported order type: {order_type}")
