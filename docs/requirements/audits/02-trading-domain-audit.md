## Denetim sonucu

Kaynak DOCX doğrudan incelendi. Repo ayrıca kontrol edildi; `main` dalında yalnızca tek satırlık `README.md` var. Emir motoru, simülasyon, borsa adaptörü, risk yönetimi veya test kodu bulunmadığından uygulama düzeyinde doğrulama yapılamıyor. Aşağıdaki bulgular gereksinim/domain denetimidir.

### P0 — Canlı işlemden önce mutlaka düzeltilmeli

- **Tek tıkla Test → Gerçek geçiş güvenli değil** (belge 40–47, 102–106, 141–145). Canlı geçiş için açık onay, yeniden kimlik doğrulama, API yetki kontrolü, sembol/bakiye doğrulaması, maksimum canlı notional limiti ve kill-switch gerekli. Simülasyondaki açık pozisyon ve emirler canlıya taşınmamalı.
- **Koruyucu emirlerin site üzerinde izlenmesi tehlikeli** (64–65). TP/SL mümkün olduğunca borsada native `stop`, `take-profit`, OCO/bracket ve `reduceOnly/closePosition` olarak tutulmalı. Uygulama, ağ veya WebSocket kesilirse yalnızca site tarafındaki stop çalışmaz.
- **Market order semantiği yanlış** (57–59). Market emrini sinyal fiyatıyla kıyaslayıp fiyat uygun olana kadar bekletmek, market order değil koşullu emirdir; sinyal süresiz bekleyebilir. Market emir derhal gönderilmeli; sapma sınırı isteniyorsa süre sonlu marketable-limit veya açıkça tanımlanmış slippage guard kullanılmalı.
- **“Tetiklemeli Limit Order” gerçekte tetiklemeli emir değil** (60–63). Sinyal anında mevcut fiyattan aşağıya/yukarıya pasif limit yerleştiriliyor. Stop-limit, take-profit-limit ve retracement-entry birbirinden ayrı emir türleri olarak tanımlanmalı.
- **PnL modeli net PnL üretmiyor** (195–254). Formüller yalnızca basit fiyat getirisi/teorik ROE’dir. Komisyon, funding, slippage, fee para birimi, maker rebate, kısmi fill ve liquidation maliyetleri yok. Bu değerlerle risk limitleri veya gerçek kârlılık ölçülemez.
- **Kaldıracı getiri oranına doğrudan uygulamak yanıltıcıdır** (212–233). `fiyat getirisi × kaldıraç` yaklaşık brüt ROE olabilir; gerçekleşen PnL değildir. Linear futures için PnL adet/notional üzerinden, inverse kontratlarda ise farklı formülle hesaplanmalı. Kullanılan marjin, maintenance margin ve maliyetler ayrıca tutulmalı.
- **Borsa filtreleri hiç tanımlanmamış.** Emirden hemen önce tick size, quantity step, min/max quantity, minimum notional, market lot, fiyat bantları, sembol durumu, izin verilen emir türleri, maksimum açık/algo emir ve leverage bracket kontrolleri uygulanmalı. Decimal kullanılmalı; binary float kullanılmamalı.
- **Order-state ve mutabakat modeli eksik.** `NEW`, kısmi fill, filled, cancel-pending, canceled, rejected, expired durumları; benzersiz client-order-id, idempotent retry, WebSocket kopması sonrası REST reconciliation ve startup recovery tanımlanmadan canlı işlem güvenli değildir.

### P1 — Domain doğruluğu açısından ciddi eksikler

#### Spot / futures / marjin

- “Spot = yalnızca Long” arayüz kısıtı makul olsa da spot satışın yalnızca mevcut envanteri kapatabileceği açıkça modellenmeli; serbest, kilitli ve borç alınmış bakiye ayrılmalı.
- Futures için linear/inverse, perpetual/delivery, USDT/coin margined, one-way/hedge mode, `positionSide`, contract size ve settlement asset ayrımları yok.
- 1–100 kaldıraç sabiti yanlış genelleme (50). Geçerli kaldıraç sembole, pozisyon notional’ına ve borsanın risk bracket’ına bağlıdır.
- Cross/isolated yalnızca UI seçeneği olarak ele alınmış (49). Cross marjinde diğer pozisyonların PnL’si ve tüm uygun bakiye liquidation riskini değiştirir.
- Pozisyon büyüklüğünde “toplam bakiye” yerine **available balance**, mevcut açık emir rezervleri, bakım marjı ve fee tamponu kullanılmalı.
- “10 USDT × 5 = 50 USDT futures cüzdanından açılır” ifadesi (52–53) düzeltilmeli: yaklaşık 50 USDT **notional** açılır; cüzdandan 50 USDT çekilmez, başlangıç marjı ve maliyetler rezerve edilir.

#### Emirler ve çıkışlar

- “Anlık gerçek tahta fiyatı” belirsiz (55–65): last, best bid, best ask, midpoint, mark ve index fiyatlarından hangisinin kullanılacağı emir yönüne göre tanımlanmalı.
- Sinyal anındaki fiyatın limit fiyatı yapılması fill garantilemez. Buy/sell yönü, spread ve time-in-force (`GTC/IOC/FOK/GTX`) belirtilmeli.
- Post-only emir fiyatı karşı tarafı keserse reddedilebilir veya borsaya göre iptal olabilir. Otomatik yeniden fiyatlama yapılacaksa maksimum deneme/sapma sınırı konmalı.
- TP/SL emirleri `reduceOnly` olmalı; kısmi fill ve kademeli kapanışlarda kalan miktara atomik biçimde yeniden boyutlandırılmalı. Aksi halde aşırı kapanışla ters pozisyon açılabilir.
- Trailing stop tanımı hatalı (81–83): girişten itibaren “%3 zarar” değildir; aktivasyon sonrası en iyi fiyattan callback oranı kadar geri dönüşte tetiklenir. Activation price, callback, mark/last kaynağı tanımlanmalı.
- DCA “Kademeli Alım” yalnızca long diliyle yazılmış (84–90). Short pozisyonda ek satış/increase-short semantiği, her kademede yeniden hesaplanan ortalama giriş ve koruyucu emirler tanımlanmalı.
- Kademe çarpanı geometrik maruziyet yaratabilir. Maksimum toplam notional, ayrılmış marjin ve liquidation mesafesi kontrol edilmeden etkinleştirilmemeli.
- Aynı sembolde tekrarlanan sinyallerin yeni pozisyon mu, mevcut pozisyona ekleme mi olduğu belirtilmemiş.

#### PnL, komisyon, funding ve slippage

- Gerçekleşmiş ve gerçekleşmemiş PnL ayrımı yok.
- Kısmi çıkışlarda yalnızca ağırlıklı kapanış fiyatı göstermek yetersiz; her fill için realized PnL ve kalan pozisyon maliyeti tutulmalı.
- “İşlem tutarı × kaldıraçlı oran” (249–254), işlem tutarı notional ise kaldıracı ikinci kez sayabilir; işlem tutarı marjin ise yine fee/funding nedeniyle net sonuç vermez.
- Futures funding yalnızca perpetual ürünlere, gerçekleşen funding zamanında ve o andaki pozisyon büyüklüğüne göre işlenmeli.
- Maker/taker komisyonu emir tipinden değil gerçekleşen her fill’in likidite rolünden hesaplanmalı.
- Slippage sabit yüzde varsayımıyla değil en azından bid/ask ve order-book depth üzerinden; simülasyonda latency ve kısmi fill ile modellenmeli.
- Fee’nin quote/base/başka token ile tahsil edilmesi ve indirim/rebate senaryoları muhasebeleştirilmeli.

#### Simülasyon

- “Anlık piyasa fiyatından gerçekmiş gibi işlem” (41–44) yeterli değildir ve sonuçları sistematik olarak iyimser yapar.
- Limit/post-only simülasyonu için spread, order-book kuyruğu, trade-through, kısmi fill ve cancel latency gerekir.
- Market simülasyonu order-book derinliğine göre VWAP/slippage hesaplamalı.
- Funding, komisyon, liquidation, margin call, WebSocket gecikmesi/kayıp veri ve borsa reddi simüle edilmeli.
- Mum kapanmadan üretilen sinyal ile kapanmış mum sinyali ayrılmalı; look-ahead bias engellenmeli.
- Deterministik event replay, sanal saat, seed ve exchange testnet aşaması eklenmeli. Paper trading başarısı canlı performans garantisi olarak kabul edilmemeli.

#### Risk kontrolleri

- Maksimum zarar limitlerinde başlangıç referansı belirsiz: başlangıç sermayesi, gün başı equity veya high-water mark açıkça seçilmeli.
- Realized/unrealized PnL, komisyon ve funding’in limite dahil olup olmadığı belirtilmemiş.
- Limit aşımında “durdurabilir” (93) yerine kesin davranış tanımlanmalı: yeni girişi engelle, bekleyen girişleri iptal et, çıkış emirlerini koru; pozisyonları otomatik kapatmak ayrı ve açık politika olmalı.
- Günlük/haftalık/aylık reset timezone ve dönem sınırları tanımlanmalı.
- Maksimum eşzamanlı pozisyon kontrolü atomik olmalı; çoklu worker aynı anda limiti aşmamalı.
- Sembol başına, strateji başına ve toplam gross/net exposure; konsantrasyon, korelasyon, maksimum emir notional’ı ve rate-limit kontrolleri eksik.
- Boş alanın “sınırsız” anlamına gelmesi canlı mod için güvenli değil. Canlı modda muhafazakâr zorunlu üst sınırlar bulunmalı.
- Stale market data, saat senkronizasyonu, art arda API hatası, veri feed ayrışması ve günlük drawdown için circuit breaker gerekli.
- Liquidation mesafesi ve maintenance margin limiti risk kapısı olarak kullanılmalı.

### Belgedeki hacim filtresi belirsizliği

- “Para birimi olarak hacim” ile “24 saatlik para birimi olarak hacim” (8–9) arasındaki fark tanımlanmamış.
- Base volume, quote volume, rolling 24h volume ve mum hacmi ayrılmalı.
- Futures hacminin kontrat, base asset veya quote notional olarak raporlanması borsaya göre normalize edilmeli.

### Güvenli canlı geçiş için minimum kapılar

1. Salt trade yetkili, withdrawal kapalı API anahtarı; şifreli secret saklama ve IP allowlist.
2. Sembol özellikleri, hesap modu, margin modu, leverage, bakiye ve saat senkronizasyonu doğrulaması.
3. Açık emir/pozisyon reconciliation; simülasyon durumunun canlı hesaba aktarılmaması.
4. Kullanıcıya maksimum olası notional/marjin/kayıp özeti ve güçlü onay.
5. Önce testnet, sonra düşük notional canary; varsayılan global canlı limit.
6. Native koruyucu emirlerin başarıyla kurulduğu doğrulanmadan giriş emrinin aktif bırakılmaması.
7. Global ve strateji bazlı kill-switch; restart sonrası fail-closed davranışı.
8. Tam audit log, fill bazlı muhasebe ve uyarı sistemi.

### Repo ve dosya durumu

- Repo: yalnızca `README.md`; implementasyon ve test yok.
- Test çalıştırılamadı çünkü çalıştırılabilir proje bulunmuyor.
- **Oluşturulan/değiştirilen dosya yok.**