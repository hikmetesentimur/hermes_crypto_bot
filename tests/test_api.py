import asyncio

import httpx

from hermes_crypto_bot.api import app


def test_health_reports_live_trading_is_disabled() -> None:
    async def request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/health")

    response = asyncio.run(request())

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "live_trading_enabled": False,
    }
