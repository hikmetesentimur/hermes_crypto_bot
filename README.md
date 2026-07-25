# Hermes Crypto Bot

Modüler borsa ve indikatör desteğine sahip, strateji oluşturma, simülasyon ve kontrollü canlı işlem yetenekleri hedefleyen kripto trading platformu.

> **Durum:** Sağlayıcıdan bağımsız MVP uygulaması başlatıldı. Canlı işlem yolu varsayılan kapalıdır ve güvenlik kapıları tamamlanmadan etkinleştirilmeyecektir.

## Proje belgeleri

| Belge | Amaç |
|---|---|
| [`docs/README.md`](docs/README.md) | Dokümantasyon haritası ve kaynakların önceliği |
| [`docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU.docx`](docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU.docx) | Kullanıcı tarafından sağlanan özgün senaryo |
| [`docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU_RAW.md`](docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU_RAW.md) | Özgün senaryonun aranabilir ham metni |
| [`docs/requirements/REQUIREMENTS_AUDIT.md`](docs/requirements/REQUIREMENTS_AUDIT.md) | Birleşik işlevsel, trading ve güvenlik denetimi |
| [`docs/requirements/OPEN_QUESTIONS.md`](docs/requirements/OPEN_QUESTIONS.md) | Kullanıcıyla karara bağlanacak konular |
| [`docs/decisions/DECISION_LOG.md`](docs/decisions/DECISION_LOG.md) | Onaylanan ürün ve teknik kararlar |
| [`docs/architecture/ADR-0001-provider-independent-foundation.md`](docs/architecture/ADR-0001-provider-independent-foundation.md) | Sağlayıcıdan bağımsız teknoloji ve mimari temeli |
| [`docs/architecture/SYSTEM_CONTEXT.md`](docs/architecture/SYSTEM_CONTEXT.md) | Bileşen sınırları ve kalıcı veri ilkeleri |
| [`.hermes/plans/2026-07-23_001041-requirements-foundation.md`](.hermes/plans/2026-07-23_001041-requirements-foundation.md) | Gereksinimden ürüne geçiş planı |

## Yerel geliştirme

### Python kalite ve test ortamı

Gereksinimler: Python 3.13 ve [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Sağlık API'sini yerelde çalıştırmak için:

```bash
uv run uvicorn hermes_crypto_bot.api:app --host 127.0.0.1 --port 8000
```

`http://127.0.0.1:8000/health` yanıtında `live_trading_enabled` her zaman `false` olmalıdır.

### Docker Compose geliştirme ortamı

1. `.env.example` dosyasını `.env` adıyla kopyalayın.
2. `POSTGRES_PASSWORD` değerini yalnız yerel geliştirmede kullanılacak güçlü bir parolayla değiştirin.
3. Docker Desktop açıkken aşağıdaki komutu çalıştırın:

```bash
docker compose up --build
```

Yalnız API, `127.0.0.1:8000` üzerinde yayınlanır; PostgreSQL ve Redis yalnız Compose iç ağı üzerinden erişilebilir. Bu Compose dosyası üretim dağıtımı değildir; TLS, dış güvenlik duvarı, KMS/gizli bilgi yöneticisi ve şifreli uzak yedek sağlayıcı seçimiyle ayrıca yapılandırılacaktır.

## Güvenlik durumu

Canlı işlem özelliği; API anahtarı güvenliği, risk limitleri, emir tekrarını önleme, borsa mutabakatı, kill switch ve test kabul kriterleri tamamlanıp kullanıcı tarafından onaylanmadan etkinleştirilmeyecektir.
