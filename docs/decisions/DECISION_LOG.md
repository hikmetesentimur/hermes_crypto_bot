# Karar Günlüğü

Bu dosya yalnızca kullanıcı tarafından açıkça onaylanmış kalıcı kararları içerir. Öneriler ve varsayımlar burada kesin karar olarak kaydedilmez.

## Durum değerleri

- `ONAYLANDI`: Uygulama için bağlayıcı karar
- `DEĞİŞTİRİLDİ`: Daha yeni bir karar tarafından geçersiz kılındı
- `İPTAL`: Kapsamdan çıkarıldı

## Kararlar

### DEC-0001 — MVP tek kullanıcı, mimari çoklu kullanıcıya hazır

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001
- Karar: İlk ürün sürümü Hikmet Esentimur'un kullanımına yönelik tek kullanıcı olarak geliştirilecek. Sistem sınırları, veri modeli ve yetkilendirme tasarımı gelecekte birden fazla kullanıcının kendi borsa hesaplarını güvenli ve izole biçimde bağlayabileceği yapıya geçişi engellemeyecek.
- Uygulama sonuçları:
  - MVP arayüzünde self-service kayıt, ekip üyeliği, faturalandırma ve çoklu kullanıcı yönetimi bulunmayacak.
  - Sahiplik gerektiren temel kayıtlarda gelecekte tenant/user ayrımına geçişi engelleyecek global varsayımlar yapılmayacak.
  - Borsa hesapları, stratejiler, emir niyetleri, işlemler ve audit olayları sahiplik sınırıyla tasarlanacak.
  - Tek kullanıcı olması kimlik doğrulama, MFA, oturum güvenliği, secret izolasyonu veya audit gereksinimlerini kaldırmayacak.
  - Çoklu kullanıcı özelliği sonraki fazda ayrıca onay ve migration planıyla etkinleştirilecek.
- Gerekçe: İlk sürümün karmaşıklığını ve geliştirme süresini azaltırken, daha sonra pahalı veri modeli/mimari yeniden yazımını önlemek.
- Ödünleşimler: MVP'de bazı tenant-aware alanlar ve sınırlar gelecekteki ihtiyaç için korunacak; ancak kullanılmayan SaaS özellikleri geliştirilmeyecek.
- Önceki karar: Yok

### DEC-0002 — MVP Binance ve MEXC Spot + Futures desteği

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-003; Q-004 henüz açık
- Karar: İlk çalışan sürümde Binance ve MEXC borsalarının hem Spot hem Futures ürünleri desteklenecek.
- Uygulama sonuçları:
  - `ExchangeAdapter` ortak sözleşmesi en az market metadata, semboller, mum/ticker/order-book, bakiye, emir, fill, pozisyon, kaldıraç/marjin ve reconciliation yeteneklerini kapsayacak.
  - Binance ve MEXC ayrı adaptörler olacak; ortak çekirdekte borsaya özel koşul dalları biriktirilmeyecek.
  - Her adaptör desteklediği ürün, emir tipi, time-in-force, post-only, native TP/SL, hedge/one-way, periyot ve test ortamını capability olarak bildirecek.
  - UI yalnız seçilen borsa/ürünün gerçekten desteklediği seçenekleri gösterecek.
  - Ortak davranış sözleşme testleriyle, borsaya özel davranışlar fixture ve uygun sandbox/testnet veya kontrollü mock testleriyle doğrulanacak.
  - Borsalardan birinin özelliği eksikse diğer adaptörün yeteneği yapay olarak kısıtlanmayacak; güvenli fallback veya açık “desteklenmiyor” durumu kullanılacak.
- Gerekçe: Kullanıcı ilk sürümden itibaren iki borsa ve iki işlem türünü birlikte kullanmak istiyor.
- Ödünleşimler: MVP kapsamı, test matrisi, hata yönetimi ve bakım yükü tek borsa yaklaşımına göre belirgin biçimde büyür.
- Önceki karar: Yok

### DEC-0003 — Uzun vadeli non-custodial abonelik/SaaS modeli

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-005, Q-057, Q-058, Q-071, Q-072
- Karar: MVP tek kullanıcıyla başlayacak. Uzun vadede ürün, kullanıcıların kendi borsa hesaplarını bağladığı abonelik/SaaS hizmetine dönüşecek. Platform kullanıcı fonunu veya özel saklama anahtarını tutmayacak; para yatırma/çekme yetkisi almayacak.
- Uygulama sonuçları:
  - Kullanıcı borsa hesabının ve fonlarının sahibi olarak kalacak; emirler kullanıcının açıkça bağladığı trade-only API yetkisiyle iletilecek.
  - Withdrawal yetkili API anahtarları reddedilecek; mümkünse borsa sub-account ve IP allowlist kullanılacak.
  - Borsa kimlik bilgileri kullanıcı/tenant sahipliğiyle, şifreli ve izole saklanacak; destek personeli plaintext secret göremeyecek.
  - Veri modeli MVP'den itibaren kullanıcı/tenant sahiplik sınırlarını destekleyecek, fakat kayıt/faturalandırma/ekip yönetimi SaaS fazına kadar uygulanmayacak.
  - Paper, testnet ve live portföyleri kullanıcı bazında kesin ayrılacak.
  - Ürün kâr garantisi, yatırım tavsiyesi veya platformun kullanıcı fonunu yönettiği iddiasıyla pazarlanmayacak.
  - Ticari/SaaS yayından ve çoklu kullanıcı live özelliğinden önce hizmetin emir iletimi/yönetimi, KVKK ve ilgili finansal mevzuat kapsamı uzman hukuk görüşüyle değerlendirilecek.
- Gerekçe: Kullanıcının uzun vadeli ticari ürün hedefini desteklerken custody ve para çekme riskini kapsam dışında tutmak.
- Ödünleşimler: Non-custodial olmak API secret, emir güvenliği, veri koruma ve olası düzenleyici yükümlülükleri ortadan kaldırmaz; çoklu kullanıcı izolasyonu ve operasyon yükü devam eder.
- Önceki karar: DEC-0001 ile uyumlu

### DEC-0004 — MVP erişim modeli hosting keşfine ertelendi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-002
- Karar: MVP'nin VPN/IP kısıtlı özel erişim, internete açık alan adı veya yerel ağ modeli hosting bilgileri sağlanana kadar kesinleştirilmeyecek.
- Uygulama sonuçları:
  - Şimdilik belirli bir cloud, reverse proxy, DNS veya ağ ürünü varsayılmayacak.
  - Geliştirme ve test ortamları varsayılan olarak live trading kapalı ve dış erişimi en aza indirilmiş halde çalışacak.
  - Hosting keşfinde OS/runtime, TLS, DNS, firewall, sabit egress IP, secret manager, veri konumu, yedekleme ve izleme birlikte değerlendirilecek.
  - Dağıtım tasarımı kimlik doğrulama, MFA ve least-privilege gereksinimlerini ertelemez; yalnız erişim topolojisi ertelenir.
  - Hosting özellikleri bilinmeden production-ready veya live-ready iddiasında bulunulmayacak.
- Gerekçe: Erişim ve secret/network tasarımı hedef hosting yeteneklerine doğrudan bağlıdır.
- Ödünleşimler: Dağıtım otomasyonu ve IP allowlist tasarımının bir kısmı hosting bilgileri gelene kadar kesinleşemez.
- Önceki karar: Yok

### DEC-0005 — Futures tutarı Marjin veya Notional olarak seçilebilir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-031; Q-032 henüz açık
- Karar: Futures pozisyon büyüklüğü girilirken kullanıcı tutar türünü “Marjin Tutarı” veya “Notional Pozisyon Tutarı” olarak seçebilecek.
- Uygulama sonuçları:
  - Marjin modunda girilen değer hedef ayrılan başlangıç marjinini ifade eder; hedef notional seçilen kaldıraç ve borsa kurallarıyla hesaplanır.
  - Notional modunda girilen değer hedef piyasa maruziyetini ifade eder; gerekli başlangıç marjini seçilen kaldıraç ve borsa kurallarıyla hesaplanır.
  - UI girilen türü, hesaplanan karşı değerini, efektif kaldıracı, başlangıç/bakım marjini, ücret tamponunu ve tahmini liquidation bilgilerini ayrı etiketlerle gösterecek.
  - Emir miktarı tick/step/min-notional kurallarına normalize edildiğinde ortaya çıkan gerçek notional ve marjin emir öncesi yeniden gösterilecek/doğrulanacak.
  - Bakiye yetersizliği, marjin bracket veya sembol kaldıraç limiti nedeniyle hedefe ulaşılamıyorsa tutar sessizce değiştirilmeden emir engellenecek ve neden gösterilecek.
  - Tüm hesaplar Decimal ile yapılacak; “cüzdandan düşen tutar” ile “pozisyon notional değeri” aynı alan olarak raporlanmayacak.
  - Spot işlemlerde bu seçim gösterilmeyecek; Spot sabit tutarı quote asset harcama bütçesini ifade edecek.
- Gerekçe: Kullanıcının hem risk/marjin bütçesine göre hem de hedef piyasa maruziyetine göre strateji tanımlayabilmesi.
- Ödünleşimler: UI ve validasyon karmaşıklığı artar; iki modun aynı risk sınırlarına tutarlı uygulanması gerekir.
- Önceki karar: Yok

### DEC-0006 — Yüzdelik boyutlandırmada seçilebilir bakiye tabanı

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-032; DEC-0005
- Karar: Kullanıcı yüzde bazlı pozisyon büyüklüğünde referans tabanını “Toplam Bakiye”, “Kullanılabilir Bakiye” veya “Strateji Bütçesi” olarak seçebilecek.
- Uygulama sonuçları:
  - Bakiye türleri borsa ve ürün bazında açık adlarla gösterilecek; Spot ve Futures değerleri birbirine karıştırılmayacak.
  - Toplam Bakiye seçimi kilitli/rezerve bakiyeyi harcanabilir hale getirmez. Hesaplanan hedef, kullanılabilir bakiye ve borsa/risk limitini aşarsa emir engellenir.
  - Kullanılabilir Bakiye; açık emir rezervleri, gerekli marjin, borsa tarafından kilitlenen tutarlar ve güvenlik/ücret tamponu dikkate alınarak adaptörden normalize edilir.
  - Strateji Bütçesi kullanıcı tarafından ayrılan hard üst sınırdır; aynı bütçeyi kullanan açık pozisyon ve emirler atomik biçimde düşülür.
  - Futures'ta yüzde sonucu, DEC-0005'te seçilen tutar türüne göre hedef marjin veya hedef notional olarak yorumlanacak; her iki karşı değer emir öncesi gösterilecek.
  - Yüzde hesabı snapshot timestamp'iyle kaydedilecek; stale bakiye verisinde emir gönderilmeyecek.
  - Global/hesap/strateji hard risk limitleri her seçimde üstün gelir; yüzde tabanı risk kapılarını aşamaz.
- Gerekçe: Farklı sermaye yönetimi yaklaşımlarını desteklerken hesaplanan hedefin hangi bakiye kavramına dayandığını açık tutmak.
- Ödünleşimler: Üç seçeneğin tutarlı açıklanması ve eşzamanlı stratejilerde atomik bütçe rezervasyonu gerekir.
- Önceki karar: DEC-0005 ile birlikte uygulanır

### DEC-0007 — Strateji bazında Kapanmış Mum veya Canlı Mum sinyali

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-016, Q-017, Q-018, Q-020
- Karar: Her stratejide sinyal değerlendirme kaynağı “Kapanmış Mum” veya “Canlı Mum” olarak seçilebilecek. Yeni stratejilerin varsayılanı “Kapanmış Mum” olacak.
- Uygulama sonuçları:
  - Kapanmış Mum modunda yalnız borsa/adaptör tarafından kapanışı doğrulanmış barlar sinyal üretir; bar başına veri revizyonu ve duplicate olaylar idempotent ele alınır.
  - Canlı Mum modunda indikatör ve koşullar bar kapanmadan değişebilir/repaint edebilir; UI kaydetme ve canlıya alma sırasında görünür risk uyarısı gösterir.
  - Strateji sürümü seçilen modu saklar; sinyal, emir niyeti, backtest/paper/live işlem ve audit kayıtları kullanılan bar kimliği, kapanış durumu ve veri timestamp'ini taşır.
  - Canlı mum değerlendirme frekansı ve aynı mumda tekrar tetikleme Q-018 kapsamında ayrıca kesinleştirilecek; bu karar sınırsız emir üretimine izin vermez.
  - Backtest/replay, karar anında erişilemeyecek gelecekteki mum verisini kullanmayacak; look-ahead bias testleri zorunlu olacak.
  - Farklı zaman dilimleri son ortak kullanılabilir veri noktasında hizalanacak; ayrıntılı hizalama Q-020 kararıyla tamamlanacak.
  - Kullanıcı açıkça değiştirmedikçe kopyalanan/yeni stratejiler güvenli varsayılan olan Kapanmış Mum modunda çalışacak.
- Gerekçe: Güvenli ve tekrarlanabilir varsayılanı korurken, daha hızlı intrabar stratejilere kontrollü esneklik sağlamak.
- Ödünleşimler: Canlı Mum modu simülasyon ve üretim davranışını karmaşıklaştırır; repaint, duplicate ve gecikme yönetimi gerekir.
- Önceki karar: Yok

### DEC-0008 — İç içe TÜMÜ/EN AZ BİRİ koşul ağacı

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-015, Q-016, Q-017, Q-018, Q-020
- Karar: Strateji kıyaslama koşulları iç içe grup/parantez yapısını destekleyecek. Her grup çocuklarını “TÜMÜ (AND)” veya “EN AZ BİRİ (OR)” mantığıyla değerlendirecek.
- Uygulama sonuçları:
  - Koşullar sıralı metin olarak değil, sürümlü ve tip güvenli bir JSON AST olarak saklanacak.
  - Grup düğümü `ALL` veya `ANY`; yaprak düğümü tipli sol operand, uyumlu operatör ve operatörün gerektirdiği sağ operandı içerecek.
  - Unary operatörler sağ operand istemeyecek; binary operatörler uyumlu sağ operand olmadan kaydedilemeyecek.
  - UI drag/drop veya açık grup kontrolleriyle parantez yapısını görünür kılacak ve insan tarafından okunabilir özet üretecek.
  - Boş grup, döngüsel referans, kayıp indikatör, uyumsuz zaman serisi veya tip hatası olan ağaç aktive edilemeyecek.
  - Değerlendirme kısa devre yapabilse bile her sonuç kullanılan veri sürümleri ve reason kodlarıyla denetlenebilir olacak.
  - Kaydetme/çalıştırma sırasında maksimum derinlik ve düğüm sayısı için güvenli sistem sınırı uygulanacak; kesin limit performans testleriyle belirlenecek.
  - “Tüm koşullardan ortak sinyal” ifadesi artık kök grubun seçilen `ALL/ANY` semantiğine göre yorumlanacak; gizli operatör önceliği olmayacak.
- Gerekçe: Karmaşık stratejileri belirsiz operatör önceliği olmadan ifade etmek ve test edilebilir hale getirmek.
- Ödünleşimler: UI, validasyon, açıklama ve test matrisi düz listeye göre daha karmaşıktır.
- Önceki karar: Yok

### DEC-0009 — Market Emir ve Fiyat Korumalı Tetikleyici ayrı seçenekler

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-021, Q-022, Q-023, Q-024, Q-050
- Karar: Sinyal sonrası derhal gönderilen Market Emir ile sinyal fiyatına göre uygun fiyat koşulunu bekleyen Fiyat Korumalı Tetikleyici iki ayrı giriş davranışı olarak desteklenecek.
- Uygulama sonuçları:
  - Market Emir, risk ve veri güncelliği kontrolleri geçince beklemeden execution katmanına gönderilecek; sinyal fiyatına geri dönüşü süresiz beklemeyecek.
  - Market Emir için kullanıcı/strateji bazlı maksimum spread ve slippage/fiyat sapması hard guard uygulanacak; guard aşıldığında emir gönderilmeyecek veya güvenli marketable-limit politikası uygulanacak. Kesin seçenek Q-050 ile tamamlanacak.
  - Fiyat Korumalı Tetikleyici, Long için tanımlanmış üst fiyat koşulunu; Short için tanımlanmış alt fiyat koşulunu sonlu süre izleyecek. Referans fiyat, tolerans ve yön semantiği ayrı alanlar olacak.
  - Fiyat Korumalı Tetikleyici zorunlu TTL/son kullanma, iptal nedeni ve tekil sinyal kimliği taşıyacak; süre dolunca sessizce Market Emre dönüşmeyecek.
  - Bekleme sırasında koşul ağacının hâlâ geçerli olması gerekip gerekmediği, yeniden değerlendirme ve fiyat kaynağı emir spesifikasyonunda açıkça tanımlanacak.
  - Paper ve live motorları aynı emir niyeti ve expiry semantiğini kullanacak; simülasyon sonucu bu iki davranışı ayrı raporlayacak.
  - UI emir adını, bekleme durumunu, kalan süreyi ve gönderilmeme/iptal nedenini gösterecek.
- Gerekçe: Kullanıcının hem hızlı market yürütmeyi hem de daha iyi fiyatı bekleyen davranışı kullanabilmesi; teknik olarak farklı semantikleri aynı “Market” adı altında karıştırmamak.
- Ödünleşimler: Emir türü ve durum makinesi genişler; fiyat korumalı tetikleyici için kalıcı scheduler, stale-data ve restart yönetimi gerekir.
- Önceki karar: Yok

### DEC-0010 — Geri Çekilme Limit ve Stop-Limit ayrı emir türleri

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-021, Q-022, Q-024, Q-025; DEC-0009
- Karar: Belgedeki belirsiz “Tetikleme Sapması/Tetiklemeli Limit Order” tek bir emir olarak uygulanmayacak. “Geri Çekilme Limit Emri” ve gerçek “Stop-Limit Emir” iki ayrı seçenek olacak.
- Uygulama sonuçları:
  - Geri Çekilme Limit Emri, koşul sinyalinden sonra referans fiyatın Long için belirlenen yüzde altında, Short için belirlenen yüzde üstünde pasif limit giriş oluşturur.
  - Geri Çekilme Limit Emrinin limit fiyatı sinyal/reference snapshot'ından Decimal ile hesaplanır, tick size'a riski artırmayacak yönde normalize edilir ve seçilen time-in-force/expiry ile yönetilir.
  - Stop-Limit Emir iki ayrı fiyat taşır: tetik fiyatı ve tetik sonrası gönderilecek limit fiyatı/offset'i. Tetiklenmek dolum garantisi değildir.
  - Native stop-limit desteği borsa/ürün capability'sinden alınır. Native destek yoksa site-side emülasyon varsayılan olarak eşdeğer sayılmaz; live kullanım için gecikme, kesinti ve fail-closed politikası ayrıca onaylanır.
  - Geri Çekilme Limit, Stop-Limit, Market, Fiyat Korumalı Tetikleyici ve standart Limit seçenekleri UI'da ayrı ad, açıklama, risk ve durumlarla gösterilecek.
  - Post-only yalnız borsanın ve ilgili emir türünün desteklediği yerde gösterilecek; cross edecek fiyat için Q-025 politikası uygulanacak.
  - Paper engine her iki türü ayrı semantikle, spread/order-book/partial fill/latency varsayımlarıyla simüle edecek.
- Gerekçe: Kullanıcının hem pasif geri çekilme girişi hem de gerçek koşullu stop-limit davranışını kullanabilmesi; yanlış emir adı kaynaklı finansal riski kaldırmak.
- Ödünleşimler: Emir capability matrisi ve test kapsamı büyür; MEXC/Binance ürünleri arasında feature parity varsayılamaz.
- Önceki karar: DEC-0009 ile birlikte uygulanır

### DEC-0011 — Ayrı fiyat getirisi, brüt/net PnL, ROE ve strateji getirisi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-043, Q-044, Q-045, Q-047, Q-077
- Karar: Fiyat getirisi, brüt PnL, net PnL, kullanılan marjine göre ROE ve strateji sermayesine göre getiri ayrı metrikler olarak hesaplanacak ve gösterilecek.
- Uygulama sonuçları:
  - PnL'nin kayıt kaynağı order/fill ledger olacak; yalnız ortalama açılış-kapanış fiyatından türetilen rapor finansal gerçek kabul edilmeyecek.
  - Fiyat getirisi Long/Short yönüne göre fiyat hareketini gösterir ve kaldıraç içermez.
  - Brüt PnL, gerçekleşen fill miktarları ve ürünün linear/inverse/contract-size formülüne göre ücretlerden önce hesaplanır.
  - Net PnL, brüt PnL'den gerçekleşmiş maker/taker komisyonu, funding, borç faizi ve diğer borsa maliyetlerini düşer; rebate/indirimler ayrı ledger kaydıyla eklenir.
  - Realized ve unrealized PnL ayrı tutulur; kısmi kapanışlarda her fill'in realized PnL'si ve kalan pozisyon maliyeti korunur.
  - ROE'nin paydası kullanılan/atanan marjindir; hesapta payda, dönem ve sıfır/negatif marjin edge-case'i açıkça kaydedilir.
  - Strateji getirisi, seçilen strateji bütçesi/dönem başı sermayesi ve nakit transferlerinden arındırılmış zaman aralığıyla raporlanır.
  - “Fiyat değişimi × kaldıraç” yalnız açıkça etiketlenmiş yaklaşık teorik brüt ROE önizlemesi olabilir; net PnL veya muhasebe gerçeği olarak kullanılmaz.
  - Paper/backtest/live metrikleri ayrı tutulur ve kullanılan ücret/slippage/funding modeli raporda görünür.
- Gerekçe: Kaldıracı iki kez saymayı, maliyetleri gizlemeyi ve risk limitlerini yanlış PnL ile tetiklemeyi önlemek.
- Ödünleşimler: Fill ve maliyet ledger'ı ile ürün bazlı hesaplama daha kapsamlı veri modeli ve test gerektirir.
- Önceki karar: DEC-0005 ve DEC-0006 ile birlikte uygulanır

### DEC-0012 — MVP Türkiye'ye özel vergi raporu üretir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-044, Q-061, Q-062, Q-069, Q-072; takip sorusu gerekli
- Karar: MVP, fill-ledger ve net PnL kayıtlarından Türkiye'ye özel vergi raporu üretecek.
- Uygulama sonuçları:
  - Vergi raporu yalnız özet PnL ekranından değil; immutable işlem, fill, fee, funding, transfer ve varlık hareketi kayıtlarından üretilecek.
  - Her rapor dönem, para birimi/kur dönüşüm kaynağı, kullanılan maliyet yöntemi, kural seti sürümü, mevzuat/kaynak tarihi ve oluşturulma timestamp'ini taşıyacak.
  - Vergi kuralları kod içine dağınık sabitler olarak gömülmeyecek; sürümlü, test edilmiş ve geçmiş raporu yeniden üretebilir kural seti olacak.
  - Kullanıcıya ham kayıt, hesaplama adımı ve özet sonuç CSV/uygun formatlarda dışa aktarılacak; yuvarlama ve eksik veri açıkça işaretlenecek.
  - Borsa dışı transferler, başka cüzdan/borsa maliyet tabanı ve kayıp geçmiş veri kullanıcı doğrulaması olmadan varsayılmayacak.
  - Kural seti Türkiye'deki güncel mevzuat ve yetkin mali müşavir/vergi hukukçusu görüşüyle doğrulanmadan rapor “resmî beyanname” veya “vergi tavsiyesi” olarak etiketlenmeyecek.
  - Mevzuat değişikliğinde eski raporlar kendi kural sürümüyle yeniden üretilebilir kalacak; yeni kural geçmiş raporu sessizce değiştirmeyecek.
  - Kişisel/finansal rapor verileri erişim kontrolü, şifreleme, audit ve saklama-imha politikasına tabi olacak.
- Gerekçe: Kullanıcı MVP'den itibaren Türkiye'ye özel vergi görünürlüğü istiyor.
- Ödünleşimler: Mevzuat takibi, uzman doğrulaması, kur/maliyet tabanı verisi ve sürümlü hesaplama motoru MVP kapsamını önemli ölçüde büyütür.
- Önceki karar: DEC-0011 temel finansal kayıt modelini sağlar

### DEC-0013 — Vergi raporu bilgilendirme ve mali müşavir çalışma dosyasıdır

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-044, Q-069, Q-072, Q-086; DEC-0012
- Karar: MVP'deki Türkiye'ye özel vergi raporu bilgilendirme ve mali müşavir çalışma dosyası niteliğinde olacak; resmî beyanname veya kişiye özel vergi tavsiyesi olarak sunulmayacak.
- Uygulama sonuçları:
  - Rapor ve indirmelerde görünür kapsam/sorumluluk açıklaması bulunacak.
  - Rapor ham fill, fee, funding, transfer ve kur dönüşüm kayıtlarıyla birlikte denetlenebilir çalışma dosyası sağlayacak.
  - Eksik maliyet tabanı, borsa dışı transfer, eksik kur veya sınıflandırılamayan olaylar sessizce tahmin edilmeyecek; kullanıcı/mali müşavir incelemesi için işaretlenecek.
  - Kural seti sürümü ve kaynak tarihi gösterilecek; güncel mevzuat uygunluğu garantisi verilmeyecek.
  - Kullanıcı raporu mali müşavirine iletebilecek; CSV ve insan tarafından okunabilir özet asgari çıktılar olacak.
  - Resmî beyannameye esas doğrulanmış mod ileride istenirse ayrı kapsam, uzman onayı, test ve hukuki değerlendirme ile etkinleştirilecek.
- Gerekçe: Kullanışlı vergi görünürlüğü sağlarken doğrulanmamış mevzuat yorumunun resmî beyan gibi sunulmasını önlemek.
- Ödünleşimler: Kullanıcı/mali müşavir nihai sınıflandırma ve beyan sorumluluğunu korur; ürün otomatik beyanname üretmez.
- Önceki karar: DEC-0012'yi sınırlar ve açıklar

### DEC-0014 — Strateji sürümü ve seçilebilir açık pozisyon migrasyonu

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-035, Q-037, Q-053, Q-056, Q-073
- Karar: Her strateji düzenlemesi yeni ve değişmez bir sürüm oluşturacak. Kullanıcı kaydederken “Yalnız Yeni İşlemler” veya “Eski Pozisyonlara Uygula” seçebilecek.
- Uygulama sonuçları:
  - Yeni sürüm eski strateji sürümünü veya geçmiş sinyal/emir/fill kayıtlarını yerinde değiştirmeyecek.
  - “Yalnız Yeni İşlemler” seçildiğinde mevcut açık pozisyonlar ve onların koruyucu yönetimi bağlı oldukları önceki sürüm/policy ile devam eder; yeni girişler aktive edilen sürümü kullanır.
  - “Eski Pozisyonlara Uygula” seçildiğinde sistem etkilenen pozisyonları, değişecek TP/SL/trailing/DCA/risk emirlerini ve olası iptal-yeniden kurma etkisini önizler ve açık onay ister.
  - Geçmiş giriş fiyatı, fill, realized PnL veya audit verisi yeniden yazılamaz. Borsada değiştirilemeyen kaldıraç/marjin/ürün/yön gibi alanlar migrate edilemez ve UI'da nedenleri gösterilir.
  - Koruyucu emir değişimi position bazında kalıcı migration state machine ile yürütülür; yeni koruma doğrulanmadan eski koruma körlemesine kaldırılmaz. Kısmi başarısızlık alarm ve manuel müdahale gerektirir.
  - Her pozisyon `entry_strategy_version` ve zaman içinde uygulanan `management_policy_version` geçmişini taşır.
  - Migrasyon risk limitlerini veya borsa capability'sini ihlal ederse o pozisyon için uygulanmaz; diğer pozisyonların sonucu ayrı raporlanır.
  - Paper ve live pozisyonları ayrı migrate edilir; paper durumu live pozisyona aktarılmaz.
- Gerekçe: Kullanıcıya açık pozisyon yönetimini güncelleme esnekliği verirken geçmişi ve finansal denetlenebilirliği korumak.
- Ödünleşimler: Açık pozisyona güvenli policy migrasyonu, yalnız yeni işlemlere uygulamaya göre çok daha karmaşık ve yüksek risklidir.
- Önceki karar: DEC-0007, DEC-0008 ve DEC-0010 ile birlikte uygulanır

### DEC-0015 — Paper performans şartı olmadan uyarı + MFA ile canlı geçiş

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-005, Q-046, Q-049, Q-054, Q-058, Q-059, Q-065, Q-076
- Karar: Kullanıcının canlı moda geçmesi için minimum paper süresi, minimum işlem sayısı veya performans eşiği zorunlu olmayacak. Kullanıcı risk uyarısını onaylayıp MFA/re-auth tamamladıktan sonra canlı geçiş talep edebilecek.
- Uygulama sonuçları:
  - UI toggle doğrudan mod değiştirmez; sunucuda doğrulanan bir canlıya alma talebi başlatır.
  - Kullanıcıya borsa/hesap, strateji sürümü, ürün, sembol evreni, maksimum kaldıraç, boyutlandırma, TP/SL, DCA ve hard risk limitlerini içeren etki özeti gösterilir.
  - MFA veya yakın zamanda yapılmış step-up authentication ve açık risk onayı olmadan talep kabul edilmez.
  - Aşağıdaki teknik kontroller atlanamaz: trade-only/withdrawal kapalı API yetkisi, doğru live credential, borsa/simge capability, precision/min-notional, kullanılabilir bakiye/marjin, stale-data ve clock kontrolü, açık emir/pozisyon reconciliation, idempotency altyapısı, kill switch, zorunlu platform risk sınırları ve audit/monitoring sağlığı.
  - Herhangi bir hard kontrol başarısızsa strateji live olmaz; paper/test durumunda kalır ve neden kullanıcıya gösterilir.
  - Paper/backtest emirleri, pozisyonları ve bakiyeleri canlı hesaba taşınmaz; live deployment yeni ayrı çalışma örneği oluşturur.
  - Canlıya geçiş ve geri dönüş kullanıcı, zaman, MFA olayı, strateji sürümü ve kontrol sonuçlarıyla append-only audit log'a yazılır.
  - Kullanıcı paper performans şartını atlayabilse de ürün simülasyonun canlı sonuç garantisi olmadığını açıkça belirtir.
- Gerekçe: Kullanıcı stratejiyi ne zaman canlıya alacağına kendisi karar vermek istiyor.
- Ödünleşimler: Zorunlu paper kanıtı ve düşük limitli canary olmadan kullanıcı finansal riski artar; teknik hard güvenlik kapıları bu kararla kaldırılamaz.
- Önceki karar: DEC-0003 ve proje canlı işlem güvenlik kapısıyla birlikte uygulanır

### DEC-0016 — Risk limitlerinde kullanıcı seçilebilir kapsam katmanları

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-046, Q-047, Q-048, Q-049, Q-050, Q-065, Q-076
- Karar: Kullanıcı her risk limiti için kapsam seviyesini seçebilecek. Desteklenen kapsamlar Global, borsa hesabı, strateji ve sembol olacak; aynı işlem veya risk üzerinde birden fazla limit varsa en sıkı sonuç uygulanacak.
- Uygulama sonuçları:
  - Risk kuralı tür, kapsam, scope kimliği, eşik, ölçüm birimi, zaman penceresi, aksiyon, etkinlik ve sürüm alanlarını taşıyacak.
  - Global kapsam tek kullanıcı MVP'de tüm bağlı hesapları; SaaS fazında tenant/kullanıcı sınırını ifade edecek. Platform operatörü hard cap'i kullanıcı Global limitinden ayrı tutulacak.
  - Borsa hesabı kapsamı belirli credential/sub-account ve Spot/Futures ürün ayrımını açıkça kaydedecek.
  - Strateji kapsamı immutable strateji deployment/sürüm ilişkisiyle; sembol kapsamı borsa+ürün+sembol anahtarıyla uygulanacak.
  - Aynı emir niyetini etkileyen limitler atomik risk değerlendirmesinde birlikte hesaplanacak; limit yarışıyla eşzamanlı worker'ların sınırı aşması engellenecek.
  - En sıkı limit/aksiyon kazanacak; kullanıcıya hangi kapsam ve kuralın işlemi engellediği reason code ile gösterilecek.
  - Limit kapsamı değiştirilirken mevcut açık risk üzerinde etki önizlemesi, validasyon ve audit kaydı oluşturulacak.
  - Kullanıcı seçimi platformun atlanamayan maksimum kaldıraç, notional, drawdown, stale-data, emir frekansı ve diğer hard safety cap'lerini gevşetemez.
- Gerekçe: Kullanıcının farklı strateji ve hesaplar için esnek sermaye/risk yönetimi yapabilmesi.
- Ödünleşimler: Çok katmanlı limit birleştirme, atomik rezervasyon ve açıklanabilirlik tek kapsamlı modele göre daha karmaşıktır.
- Önceki karar: DEC-0006 ve DEC-0015 ile birlikte uygulanır

### DEC-0017 — Risk kuralı bazında seçilebilir aksiyonlar

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-047, Q-049, Q-050, Q-065, Q-076; DEC-0016
- Karar: Her risk kuralı “Uyar”, “Yeni Girişleri Durdur”, “Bekleyen Giriş Emirlerini İptal Et” veya “Pozisyonları Acil Kapat” aksiyonlarından birini taşıyabilecek.
- Uygulama sonuçları:
  - `WARN`: alarm, UI olayı ve audit üretir; tek başına yeni emirleri engellemez. Platform hard safety ihlallerinde izin verilen minimum aksiyon daha güçlü olabilir.
  - `BLOCK_ENTRIES`: ilgili kapsamda yeni giriş order intent'lerini atomik olarak reddeder; mevcut koruyucu pozisyon yönetimini sürdürür.
  - `CANCEL_PENDING_ENTRIES`: yeni girişleri bloklamaya ek olarak bekleyen giriş ve add-to-position/DCA emirlerini idempotent iptal eder; koruyucu çıkış emirlerini körlemesine iptal etmez.
  - `EMERGENCY_CLOSE`: bekleyen girişleri iptal eder, açık pozisyonları borsanın desteklediği reduce-only/close-position semantiğiyle kapatmayı dener ve kısmi fill/kalan risk tamamlanana kadar izler.
  - Acil kapatma market veya güvenli marketable-limit politikasını, maksimum sapma ve timeout davranışını açıkça tanımlar; tam dolum garantisi verilmez.
  - Birden fazla kural aynı anda tetiklenirse en güçlü aksiyon uygulanır; kapsam birleştirme DEC-0016'ya göre yapılır.
  - Koruyucu emirler, pozisyon kapandığı doğrulanmadan veya atomik güvenli replacement olmadan kaldırılmaz.
  - Tetiklenen kural, ölçülen değer, eşik, seçilen/gerçekte uygulanan aksiyon, borsa sonuçları ve yeniden başlatma şartı audit log'da saklanır.
  - Risk durdurmasından çıkış otomatik süre dolumu veya yetkili manuel reset olarak kural bazında ayrıca tanımlanır; hard incident reset'i MFA ve reconciliation gerektirir.
- Gerekçe: Farklı risk olayları için uyarıdan acil kapatmaya kadar esnek ve açıklanabilir müdahale sağlamak.
- Ödünleşimler: Acil kapatma slippage ve likidite riski taşır; seçilebilir aksiyonlar kapsam/öncelik ve recovery state machine gerektirir.
- Önceki karar: DEC-0015 ve DEC-0016 ile birlikte uygulanır

### DEC-0018 — Risk kuralı bazında takvim/kayan pencere ve saat dilimi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-006, Q-045, Q-048; DEC-0011, DEC-0016, DEC-0017
- Karar: Her dönemsel risk kuralında Takvim Penceresi veya Kayan Pencere seçilebilecek ve pencerenin IANA saat dilimi yapılandırılabilecek.
- Uygulama sonuçları:
  - Kalıcı olay ve ledger timestamp'leri UTC saklanacak; seçilen IANA timezone yalnız takvim pencere sınırlarını üretmek için kullanılacak.
  - Takvim penceresi günlük, haftalık veya aylık olabilir. Haftalık kurallarda hafta başlangıç günü açıkça saklanacak; aylık pencereler gerçek takvim ayı kullanacak.
  - Kayan pencerede süre ISO-8601/normalize edilmiş duration olarak saklanacak; örneğin 24 saat, 7 gün veya 30 gün takvim döneminden farklıdır.
  - Gün ışığından yararlanma değişimleri timezone kütüphanesiyle ele alınacak; sabit UTC offset metni timezone yerine kullanılmayacak.
  - Her değerlendirme ölçüm aralığının başlangıç/bitiş timestamp'ini, timezone/pencere sürümünü ve kullanılan ledger olaylarını denetlenebilir biçimde kaydedecek.
  - Dönem başı equity gereken kurallarda immutable snapshot oluşturulacak; yatırma/çekme ve hesaplar arası transferler PnL'dan ayrılacak.
  - Risk kuralının timezone veya pencere tipi değişirse geçmiş olaylar yeniden yazılmayacak; yeni kural sürümü belirlenmiş etkinleşme anından itibaren uygulanacak.
  - Birden fazla pencere aynı riski etkilerse DEC-0016 ve DEC-0017'ye göre en sıkı sonuç/aksiyon kazanacak.
- Gerekçe: Kullanıcının yerel takvim bazlı ve sürekli kayan risk denetimlerini birlikte tanımlayabilmesi.
- Ödünleşimler: Timezone/DST, snapshot ve yüksek hacimli kayan pencere hesapları ek veri ve test karmaşıklığı getirir.
- Önceki karar: DEC-0016 ve DEC-0017 ile birlikte uygulanır

### DEC-0019 — Kullanıcı drawdown/liquidation kuralları varsayılan aktif ve kapatılabilir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-046, Q-047, Q-049, Q-076; DEC-0015–DEC-0018
- Karar: Kullanıcı düzeyindeki Maksimum Drawdown ve Futures Liquidation Mesafesi risk kuralları varsayılan aktif olacak fakat kullanıcı tarafından kapatılabilecek.
- Uygulama sonuçları:
  - Yeni live strateji/hesap konfigürasyonunda iki kural da güvenli varsayılan eşiklerle etkin başlar; kesin eşikler ayrı risk kararı/ortam ayarıyla belirlenir.
  - Kapatma işlemi MFA/step-up, etki özeti, açık risk önizlemesi ve audit kaydı gerektirir; sessiz veya toplu varsayılan değişiklik yapılamaz.
  - Kullanıcı kuralı kapatmak yalnız kendi yapılandırılabilir kuralını devre dışı bırakır; platformun atlanamayan maksimum kaldıraç/notional, stale-data, borsa liquidation bütünlüğü ve operasyonel hard safety cap'lerini kaldırmaz.
  - Drawdown ölçümü seçilen kapsam, pencere, equity kaynağı ve PnL bileşenleriyle sürümlü tanımlanır; high-water mark ve transfer düzeltmeleri kaydedilir.
  - Liquidation Mesafesi kuralı yalnız Futures'ta uygulanır; borsa mark price, maintenance margin/bracket ve gerçek liquidation verisiyle hesaplanır.
  - Cross marjinde hesap düzeyi etkiler; izole marjinde pozisyon düzeyi etkiler. Değer hesaplanamıyorsa live yeni giriş fail-closed olur.
  - Kural yeniden açıldığında mevcut risk hemen değerlendirilir; ihlal varsa seçilen DEC-0017 aksiyonu uygulanır.
- Gerekçe: Kullanıcıya strateji esnekliği verirken güvenli varsayılan ve platform bütünlüğünü korumak.
- Ödünleşimler: Kullanıcı kuralı kapatmak finansal kayıp/likidasyon riskini artırır; UI bu riski açıkça göstermelidir.
- Önceki karar: DEC-0015, DEC-0016, DEC-0017 ve DEC-0018 ile birlikte uygulanır

<!--
### DEC-XXXX — Karar başlığı

- Tarih: YYYY-MM-DD
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili gereksinimler: FR-..., NFR-...
- Karar: ...
- Gerekçe: ...
- Sonuçları / ödünleşimler: ...
- Önceki karar: Yok
-->
