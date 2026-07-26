# Alan Veri Modeli

## Amaç ve sınır

Bu belge, sağlayıcıdan bağımsız çekirdek alan kayıtlarının güncel yapısını açıklar. PostgreSQL tablo şeması değildir; kalıcılık modeli ayrı bir dikey pakette tasarlanacaktır. Buradaki modeller borsa, web çerçevesi ve barındırma sağlayıcısı SDK’larından bağımsızdır.

## Borsa yetenek modeli

```text
CapabilityManifest
└── ProductCapabilities (Spot veya Vadeli)
    └── EnvironmentCapabilities (Sandbox, Testnet veya Live)
        └── OrderCapabilities (Market, Limit, Stop, ...)
```

Bu hiyerarşi, bir ürünün veya ortamın yeteneğinin başka bir kombinasyona sızmasını önler.

- Mum aralıkları ortam profiline bağlıdır.
- Süre türü, post-only, reduce-only, borsa-yerel koruma ve pozisyon modu emir profiline bağlıdır.
- Bildirilmeyen ürün/ortam/emir kombinasyonu destekleniyor kabul edilmez.

Kaynak: `src/hermes_crypto_bot/domain/exchange_capabilities.py` ve REQ-EXC-001–REQ-EXC-003.

## Sembol metadata modeli

```text
SymbolMetadata
├── exchange_code / capability_schema_version
├── snapshot_id / observed_at (UTC)
├── environment
├── product
├── exchange_symbol
├── base_asset / quote_asset
├── status
├── notional_formula / contract_size
└── OrderSymbolRules[]
    ├── order_type
    ├── quantity_step / min_quantity / max_quantity
    ├── price_tick / min_price / max_price
    └── min_notional / max_notional
```

### Kimlik ve kapsam

Bir `SymbolMetadata` kaydı tek bir borsa, ürün ve ortam içindir. İçindeki her `OrderSymbolRules` yalnız kendi emir türü için geçerlidir. Başka ürün, ortam veya emir profilindeki filtreler birleştirilemez.

- Borsa ve sembol kimlikleri sınırlandırılmış güvenli ASCII’dir.
- Baz ve karşıt varlık büyük ASCII tanımlayıcılarıdır ve birbirinden farklıdır.
- Capability şema sürümü manifest ile eşleşir; her görüntü tek snapshot kimliği ve tek UTC gözlem zamanı taşır.
- Aynı emir türü bir sembolde yalnız bir kez bildirilebilir.
- Yalnız sınırlı list/tuple kabul edilir; generator/iterator tüketilmez ve değiştirilebilir liste tuple’a kopyalanır.

### Spot ve Vadeli ayrımı

- Spot metadata sözleşme büyüklüğü taşımaz ve `SPOT` formülüyle `fiyat × miktar` hesaplar.
- Vadeli metadata pozitif, sonlu ve `Decimal` sözleşme büyüklüğü taşımak zorundadır.
- `LINEAR_CONTRACT`, `fiyat × miktar × sözleşme_büyüklüğü` hesaplar.
- `FIXED_QUOTE_CONTRACT`, `miktar × sözleşme_büyüklüğü` hesaplar ve değerleme fiyatı kullanmaz.
- Bu açık formüllere eşlenemeyen ters/özel sözleşme metadata oluşturamaz; destekleniyor varsayılmaz.

### Sembol durumu

| Durum | Yeni giriş | Risk azaltan çıkış hazırlığı |
|---|---:|---:|
| `TRADING` | Evet | Evet |
| `EXIT_ONLY` | Hayır | Evet |
| `SUSPENDED` | Hayır | Hayır |
| `DELISTED` | Hayır | Hayır |

Bu tablo yalnız yerel değer hazırlığını tanımlar. Açık riskin borsa tarafında kapatılması ve mutabakat daha sonraki yürütme paketlerinin sorumluluğudur.

## Emir değeri normalizasyonu

`normalize_order_values`, doğrulanmış metadata ve seçilen emir türü üzerinde çalışır.

1. Ham finansal girdilerin gerçek `Decimal`, pozitif ve sonlu olduğu; en fazla 128 anlamlı basamak ve `[-127,+127]` ayarlanmış exponent sınırını koruduğu doğrulanır.
2. Sembol durumu, açık `ENTRY` veya `EXIT` amacına göre kontrol edilir.
3. Yalnız seçilen emir türünün kuralı bulunur; başka profil tahmin edilmez.
4. Miktar adımına aşağı yuvarlanır.
5. Fiyat taşıyan emirde çağıran `UP` veya `DOWN` yönünü açıkça verir; hazır yön yoktur.
6. Market emrinde emir fiyatı kabul edilmez. Fiyat gerektiren notional filtresi varsa açık değerleme fiyatı zorunludur; sabit karşıt-değerli sözleşme fiyat kullanmaz.
7. Miktar ve fiyat sınırları geçmeden bunlardan türetilmiş işlem değeri hesaplanmaz.
8. Adımlama ve notional, varsayılan Decimal hassasiyetinde yuvarlanmadan tam tamsayı katsayı/exponent aritmetiğiyle hesaplanır.
9. Türetilmiş miktar, fiyat veya notional 128 basamak/`[-127,+127]` sınırını aşarsa türüne özgü kodla reddedilir.
10. Minimumu karşılamayan değer otomatik büyütülmez; kararlı ihlal koduyla reddedilir.

Başarılı `NormalizedOrderValues(quantity, price, notional)` kaydı yalnız aritmetik hazırlık sonucudur; emir gönderme yetkisi, güncel piyasa verisi kanıtı veya risk azaltma kanıtı değildir.

## Metadata portu

`ExchangeMetadataPort`, dış borsa entegrasyonunun salt-okunur sınırıdır:

- yetenek manifestini sunar;
- ürün/ortam sembollerini eşzamansız listeler;
- tek sembol metadata kaydını eşzamansız getirir.

Portta bakiye, özel hesap veya emir gönderme metodu yoktur. `validate_metadata_snapshot`, port çıktısını aynı manifestteki seçili ürün/ortam/emir profiline bağlar; borsa/scope uyuşmazlığı, duplicate sembol veya desteklenmeyen emir kuralında görüntüyü reddeder.

`ExchangeAdapterError`, yalnız normalize kod, operasyon ve borsa kimliği taşır. Ham borsa yanıtı veya gizli bilgi alanı bulunmaz. Yeniden denenebilirlik yalnız önceden sınıflandırılmış geçici hata kodlarından hesaplanır.

Kaynak: `src/hermes_crypto_bot/domain/exchange_symbols.py`, `src/hermes_crypto_bot/ports/exchange_metadata.py` ve REQ-META-001–REQ-META-006.

## Henüz kalıcı olmayan kayıtlar

Yetenek manifesti, sembol metadata ve normalize emir değerleri bu aşamada süreç içi değişmez alan kayıtlarıdır. Metadata snapshot kimliği, capability sürüm bağı ve gözlem zamanı taşır; ancak kalıcılık, değişim denetimi ve ölçülmüş freshness eşiği PostgreSQL veri şeması ile halka açık piyasa verisi adaptörü paketlerinde ayrıca ele alınacaktır. Bu paket gerçek borsa yeteneği veya canlı emir desteği iddia etmez.
