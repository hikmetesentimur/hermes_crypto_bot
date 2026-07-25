"""Hermes Crypto Bot HTTP API'si."""

from typing import TypedDict

from fastapi import FastAPI


class HealthResponse(TypedDict):
    """Sağlık uç noktasının kararlı yanıt sözleşmesi."""

    status: str
    live_trading_enabled: bool


app = FastAPI(title="Hermes Crypto Bot", version="0.1.0")


@app.get("/health")
def health() -> HealthResponse:
    """Uygulama sağlık durumunu ve kapalı canlı işlem kapısını bildir."""
    return HealthResponse(status="ok", live_trading_enabled=False)
