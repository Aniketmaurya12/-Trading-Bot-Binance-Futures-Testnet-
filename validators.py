import re
from typing import Optional
from bot.logging_config import get_logger

logger = get_logger("validators")

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z]{2,20}$")

def validate_symbol(symbol: str) -> str:
    normalised = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(normalised):
        raise ValueError(f"Invalid symbol '{symbol}'. Expected 2-20 uppercase letters (e.g. BTCUSDT).")
    return normalised

def validate_side(side: str) -> str:
    normalised = side.strip().upper()
    if normalised not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return normalised

def validate_order_type(order_type: str) -> str:
    normalised = order_type.strip().upper()
    if normalised not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET, LIMIT, or STOP_LIMIT.")
    return normalised

def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    return quantity

def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    if order_type in ("LIMIT", "STOP_LIMIT"):
        if price is None:
            raise ValueError(f"Price is required for {order_type} orders.")
        if price <= 0:
            raise ValueError(f"Invalid price '{price}'. Must be a positive number.")
    return price

def validate_stop_price(stop_price: Optional[float], order_type: str) -> Optional[float]:
    if order_type == "STOP_LIMIT":
        if stop_price is None:
            raise ValueError("stop_price is required for STOP_LIMIT orders (--stop_price).")
        if stop_price <= 0:
            raise ValueError(f"Invalid stop_price '{stop_price}'. Must be a positive number.")
    return stop_price
