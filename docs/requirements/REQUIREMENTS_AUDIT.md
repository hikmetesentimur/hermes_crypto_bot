# Gereksinim Denetimi — Birleşik Sonuç

- Kaynak: `docs/source/KRIPTO_TRADING_BOT_SITE_SENARYOSU.docx`
- Kapsam: Kaynak belgenin 258 satırının tamamı
- Yöntem: Birbirinden bağımsız işlevsel, trading-domain ve mimari/güvenlik/operasyon denetimleri
- Durum: İlk denetim tamamlandı; karar soruları kullanıcıyla cevaplandıkça normalize gereksinimler üretilecek

## Tam denetim raporları

Bu sentez belge özet niteliğindedir. Hiçbir ayrıntının kaybolmaması için üç tam rapor sürüm kontrolündedir:

1. [`01-functional-requirements-audit.md`](audits/01-functional-requirements-audit.md)
2. [`02-trading-domain-audit.md`](audits/02-trading-domain-audit.md)
3. [`03-architecture-security-operations-audit.md`](audits/03-architecture-security-operations-audit.md)

Karar sorularının tamamı: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md)

---

## Yönetici özeti

Özgün belge güçlü ve ayrıntılı bir ürün fikri sunuyor; ancak mevcut haliyle gerçek para yöneten deterministik bir sistemin doğrudan geliştirme spesifikasyonu değildir. Özellikle aşağıdaki alanlar kodlamadan önce kesinleştirilmelidir:

1. Ürün/tenant ve hukuki hizmet modeli
2. Strateji yaşam döngüsü ve sürümleme
3. Koşul ağacı, sinyal zamanı ve yeniden tetikleme
4. Emir/fill/pozisyon durum makineleri
5. Marjin, kaldıraç, notional ve bakiye ayrımı
6. Fill-ledger tabanlı net PnL
7. Simülasyon gerçekçilik modeli
8. Risk motoru ve zorunlu güvenlik sınırları
9. API secret güvenliği ve canlı moda geçiş
10. Reconciliation, gözlemlenebilirlik, yedekleme ve felaket kurtarma

Kodlama, bu kararların tümünü beklemek zorunda değildir; ancak ilk uygulama yalnızca **test/paper mode** olarak başlatılmalı ve cevaplanmamış P0 konular canlı emir yolunu bloklamalıdır.

---

## Kritik düzeltmeler

### AUD-K01 — Strateji yaşam döngüsü eksik

Kaydetme, başlatma, durdurma, duraklatma, hata, yeniden başlatma ve açık risk davranışları ayrı durumlar olarak tanımlanmalıdır. Önerilen çekirdek durumlar:

`DRAFT → VALIDATING → READY → RUNNING ↔ PAUSED → STOPPED`, ayrıca `ERROR` ve `ARCHIVED`.

Her geçiş için şunlar tanımlanmalıdır:

- Yeni sinyal değerlendirmesi devam eder mi?
- Yeni giriş emri üretilebilir mi?
- Bekleyen giriş emirleri iptal edilir mi?
- Koruyucu çıkış emirleri korunur mu?
- Açık pozisyon yönetimi hangi strateji sürümüyle devam eder?
- Yeniden başlatmada otomatik devam mı, fail-closed mu?

### AUD-K02 — Tek tıkla canlı moda geçiş kaldırılmalı

UI toggle tek başına gerçek moda geçiş yapmamalıdır. Güvenli geçiş en az şunları gerektirir:

- yeniden kimlik doğrulama/MFA;
- API izin ve ortam doğrulaması;
- sembol, precision, bakiye, marjin ve kaldıraç doğrulaması;
- maksimum notional/kayıp özeti;
- açık emir/pozisyon mutabakatı;
- test durumunun canlıya taşınmaması;
- açık kullanıcı onayı ve audit kaydı;
- platform/hesap/strateji kill switch kontrolü.

### AUD-K03 — Borsa “API bilgileri” kod klasörüne yazılmamalı

`borsalar/binance` yalnız adaptör kodu, capability şeması ve halka açık endpoint yapılandırması içermelidir. Kullanıcı API key/secret değerleri:

- Git, kaynak dosyası, tarayıcı depolaması veya düz config içinde tutulmamalı;
- KMS/Vault/secret manager ile şifrelenmeli;
- withdrawal yetkisi olan anahtar reddedilmeli;
- mümkünse IP allowlist ve ayrı sub-account kullanılmalı;
- loglarda maskelenmeli;
- rotasyon/revoke runbook'u bulunmalıdır.

### AUD-K04 — Koşul motoru formal bir AST olmalı

`VE/VEYA`, unary/binary operatörler, tip uyumluluğu ve zaman senkronizasyonu UI sırasına bırakılmamalıdır. Koşullar sürümlü, tip güvenli bir JSON AST olarak saklanmalı; en az şunları tanımlamalıdır:

- iç içe ALL/ANY grupları;
- operatörün operand sayısı ve veri tipi;
- kapanmış/açık mum seçimi;
- farklı periyotların hizalanması;
- cross/trend operatörlerinin matematiksel tanımı;
- edge-trigger/level-trigger ve cooldown;
- sinyal idempotency anahtarı.

### AUD-K05 — “Anlık gerçek tahta fiyatı” kullanılabilir bir tanım değil

Her kullanım için ayrı fiyat kaynağı tanımlanmalıdır:

- indikatör/koşul: ilgili barın kapanış fiyatı veya açıkça seçilmiş seri;
- market buy koruması: best ask/order-book yürütme fiyatı;
- market sell koruması: best bid/order-book yürütme fiyatı;
- futures risk/likidasyon: uygun yerde mark/index;
- raporlama: fill fiyatları.

Her fiyat timestamp ve maksimum veri yaşı taşımalıdır. Stale veri durumunda yeni girişler fail-closed durmalıdır.

### AUD-K06 — Market ve tetiklemeli emir semantiği düzeltilmeli

Belgedeki Market Order davranışı fiyat uygun olana kadar bekleyen koşullu emirdir; market emir değildir. Seçenekler ayrılaştırılmalıdır:

- **Market:** Derhal gönderilir; slippage/spread guard uygulanır.
- **Marketable Limit:** Yürütülebilir fakat maksimum fiyat sapmasıyla sınırlı limit.
- **Passive Limit:** Belirli fiyat, time-in-force ve expiry ile bekler.
- **Post-Only Limit:** Taker olacaksa reddedilir/yeniden fiyatlanır; politika açıkça seçilir.
- **Stop-Limit / Take-Profit-Limit:** Borsanın desteklediği tetikleyici semantiği.
- **Retracement Entry:** Sinyal fiyatına göre yüzdesel geri çekilmede pasif giriş; belgede “Tetiklemeli Limit” diye tarif edilen davranışa en yakın kavram.

### AUD-K07 — Emir/fill durum makinesi ve idempotency zorunlu

En az aşağıdaki katmanlar ayrı tutulmalıdır:

- `order_intent`: Stratejinin üretmek istediği emir
- `exchange_order`: Borsaya gönderilen emir
- `fill`: Gerçekleşen her dolum
- `position`: Fill ledger'dan türetilen açık risk

Önerilen durumlar:

`CREATED → RISK_APPROVED → SUBMITTING → ACKNOWLEDGED → PARTIALLY_FILLED → FILLED/CANCELLED/REJECTED/EXPIRED/UNKNOWN`

Timeout sonrası kör retry yapılmamalı; kalıcı `clientOrderId` ile önce borsa sorgulanmalı ve reconcile edilmelidir.

### AUD-K08 — Futures tutar örnekleri düzeltilmeli

`10 USDT × 5 kaldıraç = 50 USDT` sonucu **yaklaşık notional pozisyon büyüklüğüdür**. Cüzdandan 50 USDT düşülmesi anlamına gelmez. Ayrı alanlar:

- kullanılabilir bakiye;
- ayrılan başlangıç marjini;
- bakım marjini;
- kaldıraç;
- notional;
- fee/funding rezervi;
- liquidation fiyatı/mesafesi.

Kaldıraç 1–100 sabit olmamalı; borsa, sembol ve notional bracket'a göre dinamik sınır uygulanmalıdır.

### AUD-K09 — PnL fill-ledger üzerinden yeniden tanımlanmalı

Belgedeki `fiyat değişimi yüzdesi × kaldıraç` yaklaşık brüt ROE olabilir; net gerçekleşmiş PnL değildir. Kaldıraç, “işlem tutarı” notional ise ikinci kez sayılabilir.

Ayrı metrikler gösterilmelidir:

- fiyat getirisi;
- realized PnL;
- unrealized PnL;
- net PnL (fee + funding + rebate + diğer maliyetler dahil);
- kullanılan marjine göre ROE;
- strateji sermayesine göre getiri.

Çoklu giriş ve çıkışlarda her fill ayrı muhasebeleştirilmeli; ağırlıklı ortalama yalnız sunum/pozisyon maliyeti için kullanılmalıdır.

### AUD-K10 — Risk limitleri zorunlu ve katmanlı olmalı

Boş alanın “sınırsız” anlamına gelmesi canlı mod için güvenli değildir. En az şu katmanlar gereklidir:

- platform hard cap;
- kullanıcı/hesap cap;
- borsa/ürün cap;
- strateji cap;
- sembol/konsantrasyon cap.

Limit aşımının varsayılan davranışı:

1. yeni girişleri engelle;
2. bekleyen giriş emirlerini iptal et;
3. koruyucu çıkış yönetimini sürdür;
4. alarm ve audit üret;
5. otomatik piyasa kapatmayı ayrı acil politika olarak tut.

Drawdown, spread/slippage, stale data, API hata serisi, liquidation mesafesi ve saat sapması için circuit breaker eklenmelidir.

### AUD-K11 — Koruyucu çıkışlar yalnız site belleğine bağlı olmamalı

TP/SL mümkün olduğunda borsada native `stop`, `take-profit`, OCO/bracket ve futures için `reduceOnly/closePosition` olarak kurulmalıdır. Uygulama seviyesinde izlenen koruma varsa yüksek erişilebilirlik, stale-data kontrolü ve kesinti senaryosu zorunludur.

Giriş gerçekleştikten sonra koruyucu emirlerin kurulduğu doğrulanamazsa sistem alarm vermeli, yeni risk alımını durdurmalı ve tanımlı acil politikayı uygulamalıdır.

### AUD-K12 — Aktif strateji düzenleme/kopyalama/silme finansal davranışı eksik

- Çalışan strateji immutable `strategy_version` ile bağlı olmalıdır.
- Düzenleme yeni taslak/sürüm üretmelidir.
- Kopya yeni kimlik ve sıfır istatistikle test modunda başlamalıdır.
- Silme finansal/audit kayıtlarını fiziksel olarak kaldırmamalı; arşiv/soft-delete olmalıdır.
- Açık risk varken durdurma/arşivleme etkisi kullanıcıya açıkça gösterilmelidir.

---

## Yüksek öncelikli ürün eksikleri

| Kimlik | Eksik/Belirsiz özellik | Gereken ekleme |
|---|---|---|
| AUD-Y01 | Strateji adı alanı yok | Zorunluluk, uzunluk, benzersizlik, karakter ve kopya adı kuralları |
| AUD-Y02 | Plugin klasörü sözleşme sağlamıyor | Sürümlü `ExchangeAdapter`, indicator manifest/schema ve capability modeli |
| AUD-Y03 | İki hacim metriği ayırt edilemiyor | Base/quote/rolling-24h/candle volume açık adları |
| AUD-Y04 | Bağımlı alan değişimi | Borsa/ürün değişince geçersiz alanları atomik sıfırlama ve uyarı |
| AUD-Y05 | Mum/grafik seçenekleri | Standart/Japon tekrarını kaldırma; Renko kutu, çizgi fiyat kaynağı |
| AUD-Y06 | Isınma ve periyot | Minimum history, unsupported interval aggregation, timezone |
| AUD-Y07 | Koşul tip uyumluluğu | Numeric/boolean/series/category type checking |
| AUD-Y08 | Aynı sembolde tekrar | Edge trigger, cooldown, one-position ve hedge/one-way kararı |
| AUD-Y09 | TP yürütmesi | Emir tipi, native yerleşim, reduce-only, toplam %100, rounding |
| AUD-Y10 | Stop/DCA ilişkisi | Birlikte kullanım, short DCA, exposure ve final hard stop |
| AUD-Y11 | Trailing stop tanımı | Activation + peak/trough + callback + fiyat kaynağı |
| AUD-Y12 | Borsa sınırları | Tick/step/min notional, rate limit, clock drift, delist, retries |
| AUD-Y13 | Kaydetme atomikliği | Validasyon, idempotency, optimistic locking, hata/başarı durumu |
| AUD-Y14 | Silme/audit | Soft delete, confirm/impact özeti, finansal kayıt saklama |
| AUD-Y15 | İstatistikler | Test/live ayrımı, fee sonrası sonuç, break-even, partial close |
| AUD-Y16 | İşlem detayı | Açık/kısmi durum, fill'ler, yön, mod, borsa, fee/funding, unrealized |
| AUD-Y17 | Kademeli kapanış tespiti | Fill sayısı ve kalan miktar; toplam kapanış miktarı testi değil |
| AUD-Y18 | Sıfır/işaret standardı | Break-even, negatif oran ve pozitif mutlak zarar tutarı gösterimi |

---

## Eksik ortak özellikler

Özgün senaryoya eklenmesi önerilen ürün yetenekleri:

- Strateji `Başlat / Duraklat / Durdur / Arşivle` yaşam döngüsü
- Sunucu taraflı otomatik taslak ve optimistic locking
- Backtest, deterministik replay ve walk-forward testleri
- Strateji sürümleme ve deployment geçmişi
- Exchange reconciliation ve startup recovery
- Global/hesap/strateji kill switch
- Manuel “tüm açık emirleri iptal et” ve ayrı “acil pozisyon kapat” eylemleri
- Kullanıcıya “neden işlem açılmadı?” açıklama kaydı
- Telegram/uygulama içi kritik olay bildirimleri
- Append-only audit log
- CSV işlem/PnL dışa aktarımı
- Veri kalite/stale-data paneli
- Yedekleme, restore testi ve felaket kurtarma runbook'u
- CI güvenlik/secret/dependency/container taramaları
- Responsive ve WCAG uyumlu arayüz; kâr/zararı yalnız renkle göstermeme
- Hukuki kapsam, KVKK ve risk açıklaması incelemesi

---

## Tekrarlar ve belge düzeni

Aşağıdaki kaynak bölümleri normalize belgede tek gereksinime indirgenmelidir:

- Mod geçişi: kaynak satır 102–106 ve 141–145
- Düzenle: 107–110 ve 146–149
- Kopyala: 111–122 ve 150–161
- Sil: 123–125 ve 162–164
- Borsaya göre gruplama: 127–136 içinde tekrar
- İkinci indikatör ayar akışı: 26–34, ilk indikatör akışının tekrarı

Ortak bileşenler olarak `IndicatorSelector`, `IndicatorSettingsEditor`, `ConditionEditor` ve `StrategyCardActions` tanımlanmalıdır.

---

## Yazım ve terminoloji düzeltmeleri

### Terminoloji standardı önerisi

| Kaynak ifade | Normalize ifade |
|---|---|
| Para Birimi | Karşıt Varlık / Quote Asset |
| koin | Baz varlık / varlık |
| tahta fiyatı | Kullanıma göre best bid, best ask, last, mark veya index |
| Cross | Çapraz Marjin |
| Futures İşlem | Tek tercih: “Vadeli İşlem (Futures)” |
| indicators / indikatörler | Kodda `indicators`, UI'da “İndikatörler” |
| Tetikleme Sapması / Tetiklemeli Limit | Karar sonrası kesin emir adı |
| Normal Mum / Japon Mum | Fark yoksa “Standart (Japon) Mum” |

### Belirgin yazım düzeltmeleri

- `sonradanda` → `sonradan da`
- `içerisinede` → `içerisine de`
- `açılr` → `açılır`
- `tıklanıncada` → `tıklandığında da`
- `parametleri` → `parametreleri`
- `yada` → `ya da`
- `olarakta` → `olarak da`
- `kaydırmadanda` → `kaydırmadan da`
- `noktasıda` → `noktası da`
- `değerlerde dahil` → `değerler de dâhil`
- `seçeneğide` → `seçeneği de`
- `Merket Order` → `Market Order`
- `lisletelenen` → `listelenen`
- `hemde` → `hem de`
- `tamemen` → `tamamen`
- Finansal bağlamda `kar` → `kâr`
- `API` yazımı her yerde büyük harf

Özgün DOCX değiştirilmeden saklanır; bu düzeltmeler normalize ürün gereksinimine uygulanır.

---

## Her gereksinime eklenecek kabul kriteri şablonu

1. Amaç ve kapsam
2. Ön koşullar
3. Zorunlu/opsiyonel alanlar
4. Varsayılan değerler
5. Veri tipi, aralık, hassasiyet ve Decimal yuvarlama
6. Başarılı akış
7. Hatalı/boş/veri gelmeyen akış
8. Loading/retry/timeout davranışı
9. Yetkilendirme ve güvenlik
10. Kalıcılık, atomiklik, idempotency ve eşzamanlılık
11. Emir/pozisyon/strateji durum geçişleri
12. Audit olayları
13. Performans/veri yaşı sınırları
14. Given/When/Then senaryoları
15. Borsa hata kodlarının kullanıcıya ve çalışma durumuna etkisi
16. İzlenebilirlik: kaynak satır → gereksinim → karar → test

---

## Mimari başlangıç önerisi — henüz karar değildir

İlk sürüm için önerilen yaklaşım:

- Modüler monolit ve ayrı worker süreçleri
- PostgreSQL ana kayıt sistemi
- Redis yalnız kuyruk, kısa cache ve dağıtık lock
- Web/API, market-data, strategy evaluator, execution/risk, paper engine ve reconciliation worker sınırları
- Paper/live için ortak strateji ve risk çekirdeği; ayrı execution adapter
- Tüm finansal değerlerde Decimal/NUMERIC
- Immutable strategy version ve koşullar için tipli JSON AST
- `order_intent`, `exchange_order`, `fill`, `position`, `balance_snapshot`, `audit_event` ayrımı

Teknoloji seçimi, kullanıcı cevapları ve hedef hosting özellikleri netleşince ADR olarak onaylanacaktır.

---

## Hukuki not

Üçüncü kişilere sunulan, kullanıcı adına emir ileten/yöneten veya fon/saklama işlevine yaklaşan bir hizmet farklı düzenleyici yükümlülükler doğurabilir. Türkiye hedefleniyorsa gerçek mod veya ticari yayın öncesi sermaye piyasası/fintek ve KVKK uzmanından yazılı kapsam değerlendirmesi alınmalıdır. Bu belge hukuki tavsiye değildir.
