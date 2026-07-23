# Hermes Crypto Bot

Modüler borsa ve indikatör desteğine sahip, strateji oluşturma, simülasyon ve kontrollü canlı işlem yetenekleri hedefleyen kripto trading platformu.

> **Durum:** Gereksinim analizi ve karar netleştirme aşaması. Canlı işlem kodu henüz oluşturulmamıştır.

## Proje belgeleri

| Belge | Amaç |
|---|---|
| [`docs/README.md`](docs/README.md) | Dokümantasyon haritası ve kaynakların önceliği |
| [`docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU.docx`](docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU.docx) | Kullanıcı tarafından sağlanan özgün senaryo |
| [`docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU_RAW.md`](docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU_RAW.md) | Özgün senaryonun aranabilir ham metni |
| [`docs/requirements/REQUIREMENTS_AUDIT.md`](docs/requirements/REQUIREMENTS_AUDIT.md) | Birleşik işlevsel, trading ve güvenlik denetimi |
| [`docs/requirements/OPEN_QUESTIONS.md`](docs/requirements/OPEN_QUESTIONS.md) | Kullanıcıyla karara bağlanacak konular |
| [`docs/decisions/DECISION_LOG.md`](docs/decisions/DECISION_LOG.md) | Onaylanan ürün ve teknik kararlar |
| [`.hermes/plans/2026-07-23_001041-requirements-foundation.md`](.hermes/plans/2026-07-23_001041-requirements-foundation.md) | Gereksinimden ürüne geçiş planı |

## Güvenlik durumu

Canlı işlem özelliği; API anahtarı güvenliği, risk limitleri, emir tekrarını önleme, borsa mutabakatı, kill switch ve test kabul kriterleri tamamlanıp kullanıcı tarafından onaylanmadan etkinleştirilmeyecektir.
