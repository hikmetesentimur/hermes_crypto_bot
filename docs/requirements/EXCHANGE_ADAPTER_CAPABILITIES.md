# Borsa Adaptörü Yetenek Sözleşmesi Gereksinimleri

## Amaç

Borsa adaptörleri, Binance ve MEXC arasında özellik eşitliği varsaymadan, seçilen ürün ve çalışma ortamında gerçekten sunabildikleri yetenekleri ortak çekirdeğe bildirir. Strateji doğrulama ve ilerideki emir hazırlama akışları yalnız bu bildirime göre karar verir; bildirilmeyen özellik desteklenmiyor kabul edilir.

## Kapsam

Bu dikey paket şunları kapsar:

- sürümlü ve değişmez yetenek manifesti;
- Spot/Vadeli ürün ayrımı;
- sandbox, testnet ve canlı borsa ortamı bildirimi;
- emir türü ve emir geçerlilik süresi türü;
- desteklenen mum zaman aralıkları;
- post-only, borsa-yerel koruma, yalnız-azaltan emir ve pozisyon modu;
- kararlı neden kodlarıyla güvenli ret.

Bu paket gerçek Binance/MEXC bağlantısı, API kimlik bilgisi, sembol metadata'sı, fiyat/miktar filtreleri veya emir gönderimi içermez. Somut borsa manifestleri ancak resmî belgeler, kontrollü fixture'lar ve adaptör sözleşme testleriyle eklenir. Canlı işlem kapalı kalır.

## Normalize gereksinimler

### REQ-EXC-001 — Sürümlü ve değişmez manifest

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0105, ADR-0001
- **Gereksinim:** Her adaptör yalnız desteklenen şema sürümünde, güvenli borsa koduyla ve en az bir benzersiz ürün kaydı içeren değişmez bir yetenek manifesti sağlamalıdır. Manifest ortamları ürünlerden bağımsız bildiremez; yalnız şema sürümü, borsa kodu ve ürün kayıtlarını taşır.
- **Kabul kriterleri:**
  1. Şema sürümü tam sayı `1` dışında bir değer ise manifest reddedilir; `True` değeri `1` sayılmaz.
  2. Borsa kodu 2–32 karakterlik güvenli küçük ASCII tanımlayıcısı değilse reddedilir.
  3. Ürün listesi boşsa manifest reddedilir; her ürünün bağlı ortam profili listesi boşsa ilgili ürün reddedilir.
  4. Aynı ürün iki kez bildirilirse manifest reddedilir.
  5. Adaptörün verdiği değiştirilebilir koleksiyonlar savunmacı olarak kopyalanır; kaynak koleksiyonun sonradan değişmesi manifesti değiştirmez.

### REQ-EXC-002 — Ürün → ortam → emir bağlı yetenek matrisi

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0010, DEC-0033, DEC-0073, DEC-0074, DEC-0081
- **Gereksinim:** Manifest tam bağlı `ürün → ortam → emir` matrisi taşır. `ProductCapabilities` yalnız ürünü ve ona bağlı `EnvironmentCapabilities` profillerini; her ortam profili yalnız ortam enum'unu, o ortama bağlı emir profillerini ve mum aralıklarını taşır. Her `OrderCapabilities` tek bir emir türünü ve yalnız o profile ait süre türlerini, post-only/yalnız-azaltan desteğini, borsa-yerel korumaları ve pozisyon modlarını birlikte taşır. Bu alanlar üst seviyeye yükseltilerek Kartezyen destek varsayımı üretilemez.
- **Kabul kriterleri:**
  1. Her ürün en az bir ortam profili; her ortam en az bir emir profili ve bir mum zaman aralığı bildirir.
  2. Ham metinler enum alanlarına yetenekmiş gibi geçirilemez.
  3. Mum zaman aralığı yalnız 1–16 karakterlik güvenli ASCII tanımlayıcısıdır; borsaya özgü büyük/küçük harf korunur. Mum aralığı koleksiyonu yerine verilen tekil `str` veya `bytes` açıkça reddedilir ve karakterlere bölünemez.
  4. Spot ürün vadeli pozisyon modu veya yalnız-azaltan vadeli emir semantiği bildiremez.
  5. Aynı ortam enum'u bir ürün içinde, aynı emir türü bir ortam içinde iki kez bildirilemez.
  6. Manifest içindeki iç içe bütün koleksiyonlar savunmacı olarak kopyalanır ve değişmez olur.
  7. Aynı ürünün TESTNET ve LIVE profilleri birbirinden bağımsızdır; bir ortamın mum, emir veya emir-altı yeteneği diğer ortama geçemez.

### REQ-EXC-003 — Bildirilmeyen yetenekte güvenli ret

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0015, DEC-0025
- **Gereksinim:** Strateji/emir gereksinimi manifestle karşılaştırıldığında desteklenmeyen veya bildirilmeyen her özellik açık makine koduyla reddedilmelidir.
- **Kabul kriterleri:**
  1. Desteklenmeyen ortam, ürün, emir türü, süre türü, mum zaman aralığı, post-only, borsa-yerel koruma, yalnız-azaltan emir ve pozisyon modu ayrı neden kodu üretir.
  2. Ürün hiç bildirilmemişse alt özellikler tahmin edilmez; `product_unsupported` döner.
  3. Ürün bildirilmiş ancak seçilen ortam profili yoksa yalnız `environment_unsupported` döner; alt özellikler ve başka ortamların desteği tahmin edilmez.
  4. Seçilen ortamda emir türü bildirilmemişse `order_type_unsupported` döner. Mum aralığı seçilen ortam düzeyinde ayrıca doğrulanabilir; süre türü, post-only, yalnız-azaltan, yerel koruma ve pozisyon modu tahmin edilmez.
  5. Emir türü bildirilmişse süre türü, post-only, yalnız-azaltan, borsa-yerel koruma ve pozisyon modu yalnız seçilen ortamın seçilen emir profilinden doğrulanır.
  6. Mum aralığı yalnız seçilen ortam profilinden doğrulanır; aynı ürünün başka ortamındaki mum desteği talebi geçerli kılmaz.
  7. Birden fazla bağımsız eksik yetenek kararlı sırada birlikte raporlanır.
  8. Zorunlu kontrol işlevi eksik yetenekte Türkçe alan hatası üretir.
  9. Borsa koduna göre çekirdekte özel koşul dalı kullanılmaz.

### REQ-EXC-004 — Gerçek borsa iddiasını erteleme

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0040, DEC-0105
- **Gereksinim:** Resmî kaynak ve adaptör sözleşme testleri olmadan Binance veya MEXC için somut destek iddiası kodlanmamalıdır.
- **Kabul kriterleri:**
  1. Birim testleri yalnız açıkça fixture olarak adlandırılmış yapay manifest kullanır.
  2. Üretim kodunda gerçek API uç noktası, anahtar veya emir gönderimi bulunmaz.
  3. Somut adaptörler eklendiğinde ortak sözleşme testlerinden ve uygun sandbox/testnet doğrulamasından geçer.
  4. Canlı ortam bildirimi tek başına canlı işlem güvenlik kapısını açmaz.

## Kararlı neden kodları

| Kod | Anlamı |
|---|---|
| `environment_unsupported` | Seçilen borsa ortamı bildirilmemiş |
| `product_unsupported` | Spot/Vadeli ürün bildirilmemiş |
| `order_type_unsupported` | Emir türü desteklenmiyor |
| `time_in_force_unsupported` | Emir geçerlilik süresi desteklenmiyor |
| `candle_interval_unsupported` | Mum zaman aralığı desteklenmiyor |
| `post_only_unsupported` | Post-only desteklenmiyor |
| `native_protection_unsupported` | İstenen koruma borsada yerel değil |
| `reduce_only_unsupported` | Yalnız-azaltan emir desteği bildirilmemiş |
| `position_mode_unsupported` | Pozisyon modu desteklenmiyor |

## İzlenebilirlik

| Gereksinim | Uygulama | Test |
|---|---|---|
| REQ-EXC-001 | `domain/exchange_capabilities.py::CapabilityManifest` | `test_manifest_*`, `test_unknown_or_invalid_schema_versions_*`, `test_nested_mutable_*` |
| REQ-EXC-002 | `ProductCapabilities` → `EnvironmentCapabilities` → `OrderCapabilities` | `test_product_*`, `test_environment_*`, `test_order_*`, `test_spot_*`, `test_nested_mutable_*`, `test_*_do_not_leak_*` |
| REQ-EXC-003 | `check_capabilities`, `require_capabilities` | `test_testnet_only_candle_*`, `test_*_do_not_leak_*`, `test_undeclared_*`, `test_unknown_order_*`, `test_*_regression_*`, `test_unsupported_*` |
| REQ-EXC-004 | Bu kapsam belgesi ve fixture manifesti | `test_supported_requirement_passes_without_exchange_specific_branching` |
