import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import get_logger

logger = get_logger("client")

def create_client() -> Client:
    api_key = os.environ.get("BINANCE_API_KEY", "").strip()
    api_secret = os.environ.get("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        raise EnvironmentError(
            "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET."
        )

    logger.debug("Creating Binance Futures Testnet client...")
    try:
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True,
        )
        client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        logger.info("Binance Futures Testnet client created successfully.")
        return client
    except BinanceAPIException as exc:
        logger.error("Binance API authentication error: %s", exc)
        raise
    except Exception as exc:
        logger.error("Unexpected error while creating client: %s", exc)
        raise