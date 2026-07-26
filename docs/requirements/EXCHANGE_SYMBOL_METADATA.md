# Borsa Sembol Metadata ve Güvenli Değer Normalizasyonu Gereksinimleri

## Amaç

Borsa adaptörlerinden gelen işlem çifti ve filtre bilgilerini, borsa/ürün/ortam/emir türü bağını kaybetmeden ortak çekirdeğe taşımak; fiyat, miktar ve işlem değeri doğrulamasını kesin ondalık aritmetik ve güvenli ret ilkesiyle gerçekleştirmek.

## Kapsam

Bu dikey paket şunları kapsar:

- sağlayıcıdan ve somut borsadan bağımsız salt-okunur metadata portu;
- borsa, ürün ve ortam kimliği ile capability şema sürümü, snapshot kimliği ve UTC gözlem zamanına bağlı değişmez sembol metadata kaydı;
- emir türüne bağlı fiyat, miktar ve işlem değeri kuralları;
- Spot/Vadeli sözleşme büyüklüğü ayrımı;
- açık yön seçilen fiyat adımlama ve aşağı yönlü miktar adımlama;
- sembol durumuna göre giriş/çıkış uygunluğu;
- metadata–yetenek manifesti sözleşme doğrulaması;
- kararlı ve sır içermeyen adaptör hata sınıflandırması.

Bu paket gerçek Binance/MEXC HTTP veya WebSocket bağlantısı, API anahtarı, bakiye/pozisyon erişimi, emir gönderimi, veritabanı kalıcılığı veya canlı işlem içermez. Gerçek borsa filtre değerleri resmî kaynak ve sözleşme testleri olmadan kodlanmaz.

## Normalize gereksinimler

### REQ-META-001 — Bağlı ve değişmez sembol kimliği

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0036, DEC-0076, DEC-0105, DEC-0106
- **Gereksinim:** Her sembol metadata kaydı borsa kodu, capability şema sürümü, snapshot kimliği, UTC gözlem zamanı, çalışma ortamı, ürün türü, borsadaki sembol kodu, baz varlık, karşıt varlık, işlem durumu ve emir türü bazlı kural kayıtlarını birlikte taşımalıdır.
- **Kabul kriterleri:**
  1. Borsa/sembol/varlık tanımlayıcıları yalnız açıkça izin verilen güvenli ASCII biçiminde kabul edilir; boş, boşluklu, kontrol karakterli veya yol benzeri değerler reddedilir.
  2. Baz ve karşıt varlık aynı olamaz.
  3. Çalışma ortamı, ürün, sembol durumu ve emir türleri ham metin olarak geçirilemez; tanımlı enum değerleri zorunludur.
  4. Metadata değişmezdir; emir kuralları yalnız sonlu `list/tuple` kabul eder, tanımlı emir türü sayısını aşamaz ve değiştirilebilir liste savunmacı kopyalanır.
  5. Capability şema sürümü pozitif tam sayıdır; snapshot kimliği güvenli ASCII’dir; gözlem zamanı saat dilimi bilgili UTC’dir.
  6. Aynı emir türü bir sembol metadata kaydında iki kez bildirilemez.
  7. Aynı sembol kodu bir metadata görüntüsünde iki kez bildirilemez.

### REQ-META-002 — Emir türüne bağlı filtreler

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0069, DEC-0081; REQ-EXC-002
- **Gereksinim:** Fiyat, miktar ve işlem değeri filtreleri tek bir sembol-geneli Kartezyen küme olarak değil, seçilen ortam içindeki seçilen emir türünün `OrderSymbolRules` kaydı olarak doğrulanmalıdır.
- **Kabul kriterleri:**
  1. Her emir kuralında pozitif ve sonlu miktar adımı ile pozitif ve sonlu asgari miktar bulunur.
  2. Azami miktar varsa asgari miktardan küçük olamaz.
  3. Fiyat taşıyan emir türlerinde pozitif ve sonlu fiyat adımı zorunludur; Market emir kuralı fiyat adımı taşımaz.
  4. Asgari/azami fiyat ve işlem değeri alanları varsa sonlu ve pozitiftir; her azami değer ilgili asgari değerden küçük olamaz. `None` yalnız adaptörün otoritatif biçimde filtrenin bu emir türüne uygulanmadığını veya bulunmadığını bildirdiği anlamına gelir; bilinmeyen/ayrıştırılamayan filtre `None` yapılamaz.
  5. Spot sembol sözleşme büyüklüğü taşıyamaz ve yalnız `SPOT` notional formülünü kullanır; Vadeli sembolde pozitif ve sonlu sözleşme büyüklüğü ile açık `LINEAR_CONTRACT` veya `FIXED_QUOTE_CONTRACT` formülü zorunludur.
  6. Lineer Vadeli filtre, sabit karşıt-değerli sözleşme filtresi yerine kullanılamaz; bu formüllere eşlenemeyen sözleşme bilinmeyen kabul edilip reddedilir.
  7. Bir ortam veya emir türündeki filtre başka ortam, ürün ya da emir türünde destek varsayımı oluşturamaz.

### REQ-META-003 — Kesin ondalık normalizasyon ve güvenli ret

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0050, DEC-0069
- **Gereksinim:** Fiyat, miktar ve işlem değeri hesaplarında yalnız `Decimal` kullanılmalı; desteklenmeyen veya minimumu karşılamayan değerler sessizce büyütülmeden açık neden koduyla reddedilmelidir.
- **Kabul kriterleri:**
  1. `float`, `int`, `bool`, NaN, sonsuz, sıfır ve negatif finansal girdiler reddedilir; Decimal değerler proje standardıyla uyumlu olarak en fazla 128 anlamlı basamak ve `[-127,+127]` ayarlanmış exponent sınırında kalır.
  2. Miktar, belirtilen adıma her zaman aşağı yuvarlanır; sıfıra veya asgari miktarın altına düşerse otomatik büyütülmez.
  3. Fiyat adımlamasında yön için hazır değer yoktur; çağıran `UP` veya `DOWN` yönünü açıkça vermeden fiyat normalize edilemez.
  4. Adımlama ve çarpım Python’ın hazır Decimal bağlam hassasiyetine bağlı kalmaz; tam tamsayı katsayı/exponent aritmetiğiyle kayıpsız yapılır.
  5. Normalize fiyat ve miktar, ilgili asgari/azami sınırlar içinde doğrulanır.
  6. İşlem değeri `SPOT` için `fiyat × miktar`, `LINEAR_CONTRACT` için `fiyat × miktar × sözleşme_büyüklüğü`, `FIXED_QUOTE_CONTRACT` için `miktar × sözleşme_büyüklüğü` olarak kesin ondalıkla hesaplanır.
  7. Market emrinde fiyat uydurulmaz; fiyat gerektiren notional filtresi varsa açıkça verilen pozitif ve sonlu değerleme fiyatı kullanılır. Sabit karşıt-değerli formülde değerleme fiyatı kabul edilmez.
  8. Ham girdiler kadar türetilmiş miktar, fiyat ve notional da 128 basamak/`[-127,+127]` sınırında kalır; adımlama veya çarpım sınırı aşarsa türüne özgü kararlı ret kodu döner.
  9. Sonuç; normalize fiyat, miktar ve aritmetik olarak doğrulanmış işlem değerini değişmez kayıt olarak döndürür. Bu sonuç emir yetkilendirmesi değildir.

### REQ-META-004 — Sembol durumu ve emir amacı

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0074, DEC-0076
- **Gereksinim:** Sembol durumu yeni giriş ve risk azaltan çıkış için ayrı yorumlanmalıdır.
- **Kabul kriterleri:**
  1. `TRADING` yeni giriş ve çıkışa izin verir.
  2. `EXIT_ONLY` yeni girişi reddeder; `EXIT` amacı yalnız aritmetik hazırlamaya izin verir ve gerçek risk azaltımını kanıtlamaz.
  3. `SUSPENDED` ve `DELISTED` yeni giriş ve çıkış hazırlığını reddeder; açık riskin gerçek borsa mutabakatı bu paketin dışında kalır.
  4. Emir amacı `ENTRY` veya `EXIT` olarak açıkça verilmeden değer hazırlama yapılamaz.
  5. Durum kaynaklı retler kararlı neden kodu taşır.
  6. Gerçek `EXIT_ONLY` emri daha sonraki yürütme kapısında güncel pozisyon sahipliği, miktar sınırı ve destekleniyorsa reduce-only semantiği doğrulanmadan gönderilemez.

### REQ-META-005 — Salt-okunur metadata portu

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0040, DEC-0105, ADR-0001
- **Gereksinim:** Somut adaptörler, çekirdeğin uygulama ayrıntısına bağımlı olmadığı sürümlü bir `ExchangeMetadataPort` sözleşmesini uygulamalıdır.
- **Kabul kriterleri:**
  1. Port yetenek manifestini sunar; ürün/ortam için sembolleri listeler ve tek sembol metadata kaydı getirir.
  2. Ağ yapabilecek port metotları eşzamansızdır; çekirdek somut HTTP istemcisi veya sağlayıcı SDK’sı içe aktarmaz.
  3. Port yalnız metadata okur; bakiye, özel hesap ve emir gönderme metodu içermez.
  4. Yapısal protokol sahte adaptörle sınanabilir ve gerçek ağ gerektirmez.
  5. Adaptör hata kodu, operasyon ve yeniden denenebilirlik bilgisi taşır; kullanıcıya/günlüğe ham borsa yanıtı veya sır aktarmaz.

### REQ-META-006 — Metadata–yetenek sözleşmesi doğrulaması

- **Öncelik:** P0
- **Karar dayanağı:** DEC-0002, DEC-0036, DEC-0040; REQ-EXC-003
- **Gereksinim:** Adaptör metadata görüntüsü, aynı adaptörün yetenek manifesti ve istenen borsa/ürün/ortam kapsamıyla fail-closed olarak karşılaştırılmalıdır.
- **Kabul kriterleri:**
  1. Metadata borsa kodu manifest borsa koduyla eşleşmezse reddedilir.
  2. İstenen ürün veya ortam manifestte yoksa alt filtreler tahmin edilmez.
  3. Metadata içindeki her emir türü seçilen ürün/ortam yetenek profilinde bildirilmiş olmalıdır.
  4. Başka ürün ya da ortamın yeteneği seçilen metadata kaydını geçerli kılamaz.
  5. Görüntüde istenen ürün/ortamdan farklı kayıt veya kapsamdan bağımsız yinelenen sembol varsa görüntü reddedilir.
  6. Yalnız sonlu `list/tuple` kabul edilir; görüntü 100.000 kayıtlık koruyucu teknik tavanı aşamaz ve değiştirilebilir liste tuple’a kopyalanır. Generator/iterator tüketilmez.
  7. Her kayıt manifestin capability şema sürümüne bağlıdır; bir görüntü tek snapshot kimliği ve tek UTC gözlem zamanı taşır.
  8. Birleşik ihlaller kayıt sırasından bağımsız olarak `MetadataViolationCode` enum sırasıyla döner.

## Güvenlik sınırları

- Canlı emir yolu yoktur.
- API anahtarı veya özel hesap çağrısı yoktur.
- Bilinmeyen metadata veya filtre destekleniyor kabul edilmez.
- Otomatik minimuma büyütme yoktur.
- Fiyat yuvarlama yönü sessizce seçilmez.
- Market `valuation_price`, bu pakette yalnız güvenilir çağıranın verdiği aritmetik referanstır; kaynak, taraf ve freshness kanıtı değildir. Paket 4 doğrulanmış piyasa verisi nesnesi olmadan bu sonuç pre-trade yetkisi sayılamaz.
- `EXIT` amacı risk azaltımını kanıtlamaz; pozisyon/reduce-only doğrulaması yürütme katmanının zorunlu kapısıdır.
- Binance/MEXC’ye ait gerçek filtre değeri veya uç nokta bu pakette kodlanmaz.

## İzlenebilirlik

| Gereksinim | Uygulama | Otomatik test |
|---|---|---|
| REQ-META-001 | `domain/exchange_symbols.py::SymbolMetadata` | `tests/domain/test_exchange_symbols.py`: kimlik, enum, değişmezlik, duplicate |
| REQ-META-002 | `domain/exchange_symbols.py::OrderSymbolRules` | Decimal filtre ve Spot/Vadeli semantik testleri |
| REQ-META-003 | `normalize_order_values` | yön, adım, min/max/notional ve hatalı girdi testleri |
| REQ-META-004 | `SymbolTradingStatus`, `OrderPurpose` | giriş/çıkış durum matrisi testleri |
| REQ-META-005 | `ports/exchange_metadata.py` | `tests/ports/test_exchange_metadata.py`: sahte port ve hata sınıflandırması |
| REQ-META-006 | `validate_metadata_snapshot` | ürün/ortam/emir/borsa sızıntısı negatif sözleşme testleri |
