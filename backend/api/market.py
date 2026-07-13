import logging

import yfinance as yf

logger = logging.getLogger(__name__)


def get_stock_history(ticker: str, start: str, end: str) -> list[dict]:
    """
    Belirtilen hisse için tarih aralığındaki günlük OHLCV verisini döner.
    ticker örnekleri: 'THYAO.IS', 'XU100.IS', 'AAPL'
    start/end formatı: 'YYYY-MM-DD'
    """
    logger.info("Borsa verisi çekiliyor: %s (%s -> %s)", ticker, start, end)
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        logger.warning("Veri bulunamadı: %s", ticker)
        return []

    data = data.reset_index()
    data.columns = [str(c[0]) if isinstance(c, tuple) else str(c) for c in data.columns]
    return data.to_dict(orient="records")


def get_current_price(ticker: str) -> dict:
    """Bir hissenin güncel fiyat bilgisini döner."""
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "currency": info.get("currency"),
        "previous_close": info.get("previousClose"),
    }
