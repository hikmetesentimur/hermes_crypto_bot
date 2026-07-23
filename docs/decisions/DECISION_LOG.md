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

### DEC-0020 — Spread/slippage koruması varsayılan aktif ve kapatılabilir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-022, Q-023, Q-047, Q-050; DEC-0009, DEC-0010
- Karar: Maksimum spread ve slippage/fiyat sapması risk limitleri varsayılan aktif olacak; kullanıcı bunları kapatabilecek.
- Uygulama sonuçları:
  - Spread ve slippage ayrı ölçülür: spread karar anındaki yürütülebilir best bid/ask farkı; slippage tahmini/gerçekleşen yürütme fiyatının tanımlı referanstan sapmasıdır.
  - Eşikler bps/yüzde ve gerektiğinde mutlak quote değeriyle strateji/emir türü bazında yapılandırılabilir; güvenli varsayılanlar likidite/ürün sınıfına göre belirlenir.
  - Varsayılan davranış eşik aşımında yeni emir göndermemektir; kullanıcıya ölçüm, eşik, veri timestamp'i ve reason code gösterilir.
  - Kural kapatma veya eşiği önemli ölçüde gevşetme risk özeti, MFA/step-up ve audit kaydı gerektirir.
  - Kapatma kullanıcı limitini kaldırır; borsanın price band/percent-price/min-max kuralları, stale/invalid order-book kontrolü ve platformun olağan dışı piyasa/veri hard cap'leri devam eder.
  - Market, marketable-limit, Fiyat Korumalı Tetikleyici, Geri Çekilme Limit ve Stop-Limit için ölçüm/referans semantiği ayrı tanımlanır; tek metrik tüm emir türlerine körlemesine uygulanmaz.
  - Paper engine gerçek/varsayılan spread, order-book depth ve latency ile beklenen/gerçekleşen slippage'ı ayrı raporlar.
  - Limit kapalıyken oluşan emir ve fill'ler, korumanın devre dışı olduğu bilgisiyle audit/rapora işaretlenir.
- Gerekçe: Varsayılan korumayı sağlarken kullanıcıya yüksek volatilite veya özel stratejilerde kontrollü esneklik vermek.
- Ödünleşimler: Kural kapalıyken beklenmedik kötü fiyat ve likidite kaybı riski artar; market emirlerde sonuç fiyatı garanti edilemez.
- Önceki karar: DEC-0009, DEC-0010, DEC-0016 ve DEC-0017 ile birlikte uygulanır

### DEC-0021 — Risk kuralı bazında seçilebilir PnL/equity ölçümü

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-043, Q-044, Q-045, Q-046, Q-048, Q-049; DEC-0011
- Karar: Her risk kuralında ölçüm kaynağı Realized Net PnL, Unrealized Net PnL veya Toplam Equity Değişimi olarak seçilebilecek.
- Uygulama sonuçları:
  - Realized Net PnL ölçümü kapanan/kısmen kapanan fill'lerden gerçekleşen brüt PnL, fee, funding, faiz ve rebate ledger kayıtlarını kullanacak.
  - Unrealized Net PnL açık miktarın seçilen mark/valuation fiyatıyla değerlenmesini, tahakkuk etmiş maliyetleri ve ürün kurallarını kullanacak; gerçekleşmiş tutar gibi raporlanmayacak.
  - Toplam Equity Değişimi realized + unrealized sonuç ve ilgili bakiye varlıklarını kapsayacak; yatırma/çekme/iç transferler getiri veya zarar sayılmayacak şekilde normalize edilecek.
  - Her kural ölçüm kaynağına ek olarak kapsam, pencere, referans başlangıç/high-water mark, para birimi ve DEC-0017 aksiyonunu saklayacak.
  - Çoklu para birimleri seçilen raporlama para birimine timestamp'li kur kaynağıyla çevrilecek; kur yok/stale ise kuralın fail-closed/uyarı davranışı açıkça tanımlanacak.
  - Kısmi fill, fee'nin farklı varlıkta tahsili ve funding olayları ledger sırasıyla deterministik işlenecek; aynı olay iki kez sayılmayacak.
  - Kullanıcı arayüzü ölçülen değer, eşik, pencere ve bileşen dökümünü gösterecek; “zarar limiti” etiketi altında farklı ölçümler gizlenmeyecek.
  - Platform hard drawdown/capital-preservation kuralı kullanıcı seçimine bağlı olmadan Toplam Equity veya tanımlı daha muhafazakâr ölçümü kullanabilir.
- Gerekçe: Farklı risk hedefleri için gerçekleşmiş kayıp, açık piyasa riski ve toplam sermaye düşüşünü ayrı yönetebilmek.
- Ödünleşimler: Equity valuation, çoklu para birimi ve ledger olaylarının doğru zamanlanması risk motorunu karmaşıklaştırır.
- Önceki karar: DEC-0011, DEC-0016, DEC-0017 ve DEC-0018 ile birlikte uygulanır

### DEC-0022 — Kullanıcı iletişimi tamamen Türkçe olacak

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili alanlar: Tüm gereksinim soruları, seçenekler, açıklamalar, uyarılar, raporlar ve kullanıcı arayüzü metinleri
- Karar: Kullanıcı İngilizce anlamadığı için proje iletişimi açık ve sade Türkçe yürütülecek.
- Uygulama sonuçları:
  - Bütün sorular ve cevap seçenekleri Türkçe hazırlanacak.
  - Teknik İngilizce terimlerin önce Türkçe karşılığı kullanılacak; özgün terim gerekliyse yalnız parantez içinde verilecek.
  - Açıklanmamış İngilizce kısaltma ve jargon kullanıcıya gösterilmeyecek.
  - Kod, API ve veri şemasının zorunlu İngilizce adları korunabilir; arayüzde Türkçe açıklamaları bulunacak.
  - Örnek karşılıklar: `slippage` → “emir fiyat kayması”, `drawdown` → “sermayenin zirveden düşüşü”, `fill` → “emir gerçekleşmesi”, `paper trading` → “sanal bakiyeyle deneme işlemleri”.
- Gerekçe: Kullanıcının bütün ürün kararlarını eksiksiz anlayıp bilinçli biçimde onaylayabilmesi.
- Ödünleşimler: Zorunlu teknik adların Türkçe açıklamalarının tutarlı bir terim sözlüğüyle yönetilmesi gerekir.
- Önceki karar: Yok

### DEC-0023 — Kullanıcı seçilebilir üç benzetim düzeyi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-051, Q-052, Q-066; DEC-0009, DEC-0010, DEC-0011, DEC-0020
- Karar: Deneme modunda kullanıcı Temel, Orta veya İleri emir gerçekleşme benzetimi düzeyini seçebilecek.
- Uygulama sonuçları:
  - Temel düzey; alış-satış fiyat farkı, işlem ücreti ve yapılandırılabilir sabit fiyat kaymasını hesaba katar.
  - Orta düzey; Temel düzeye ek olarak piyasa derinliği, emrin parça parça gerçekleşmesi, işlem gecikmesi ve vadeli işlemlerde fonlama maliyetini hesaba katar.
  - İleri düzey; Orta düzeye ek olarak emir defterindeki sıra olasılığı, fiyatın emrin içinden geçmesi, borsa retleri, zaman aşımı, yeniden deneme ve daha ayrıntılı piyasa verisi davranışlarını canlandırır.
  - Yeni stratejiler için varsayılan düzey Orta olacaktır; kullanıcı isterse değiştirebilir.
  - Her çalışma seçilen düzeyi, ücret/fiyat kayması/gecikme varsayımlarını, veri kaynağını ve benzetim sürümünü değişmez sonuç kaydında saklar.
  - Düzeyler aynı strateji ve veri üzerinde karşılaştırılabilir olacak; sonuç ekranı aradaki farkların nedenlerini gösterecek.
  - Benzetim hiçbir düzeyde canlı piyasada aynı sonucun gerçekleşeceği garantisini vermeyecek; bu uyarı görünür olacaktır.
  - İleri düzey için yeterli piyasa derinliği veya işlem verisi yoksa sistem sessizce daha basit düzeye düşmeyecek; kullanıcıya eksik veriyi ve kullanılabilen düzeyi bildirecek.
  - Kullanıcı arayüzündeki bütün düzey adları ve açıklamalar sade Türkçe olacaktır.
- Gerekçe: Hızlı deneme ile gerçeğe daha yakın sınama arasında kullanıcıya açık seçim sunmak.
- Ödünleşimler: İleri düzey daha fazla piyasa verisi, işlem gücü, saklama alanı ve doğrulama testi gerektirir.
- Önceki karar: DEC-0009, DEC-0010, DEC-0011 ve DEC-0020 ile birlikte uygulanır

### DEC-0024 — İlk sürümde ayrıntılı geçmiş veri sınaması

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-020, Q-043, Q-051, Q-052, Q-066, Q-077; DEC-0007, DEC-0011, DEC-0023
- Karar: İlk sürümde stratejileri geçmiş piyasa verileri üzerinde ayrıntılı biçimde sınama özelliği bulunacak.
- Uygulama sonuçları:
  - Kullanıcı borsa, işlem türü, işlem çifti veya işlem çifti evreni, başlangıç-bitiş tarihi, başlangıç sermayesi ve benzetim düzeyini seçecek.
  - Sistem gelecekteki veriyi geçmiş karar anında kullanmayacak; mum kapanışı, farklı zaman aralıklarının hizalanması ve indikatörlerin başlangıç veri ihtiyacı açık kurallarla uygulanacak.
  - İşlem ücretleri, fonlama maliyeti, fiyat kayması, alış-satış fiyat farkı, emrin parça parça gerçekleşmesi ve borsa kuralları seçilen benzetim düzeyine göre hesaba katılacak.
  - Veri eksikleri, sonradan listelenen veya işlemden kaldırılan varlıklar ve seçime göre değişen varlık evreni sonuçları yapay biçimde iyileştirmeyecek; tüm eksikler raporlanacak.
  - Aynı stratejiyi geliştirme, doğrulama ve ileri dönem parçalarında sınama desteği olacak; kullanıcı yalnız iyi görünen dönemi seçmenin yanıltıcı olabileceği konusunda uyarılacak.
  - Rapor en az net kâr/zarar, sermayenin zirveden düşüşü, başarı oranı, kazanç-kayıp oranı, işlem sayısı, ücret/fonlama toplamı, açık kalma süresi ve ölçüm yöntemlerini gösterecek.
  - Her sınama strateji sürümü, veri kümesi kimliği/sürümü, benzetim düzeyi, bütün varsayımlar ve yazılım sürümüyle yeniden üretilebilir kayıt oluşturacak.
  - Geçmiş sınama sonucu canlı piyasada aynı sonucun gerçekleşeceği garantisi olarak sunulmayacak.
  - Büyük veri işleri arka planda çalışacak; ilerleme, iptal, başarısızlık nedeni ve tamamlanmış rapor kullanıcıya Türkçe gösterilecek.
- Gerekçe: Kullanıcı ilk sürümden itibaren stratejileri farklı geçmiş piyasa koşullarında ayrıntılı biçimde değerlendirmek istiyor.
- Ödünleşimler: Piyasa verisi temini, saklama, hesaplama gücü, veri sürümleme ve yanlılık önleme ilk sürüm kapsamını büyütür.
- Önceki karar: DEC-0007, DEC-0011 ve DEC-0023 ile birlikte uygulanır

### DEC-0025 — Taslak Olarak Kaydet veya Kaydet ve Başlat seçenekleri

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-053, Q-054, Q-073, Q-075, Q-087; DEC-0014, DEC-0015
- Karar: Strateji kaydedilirken kullanıcı “Taslak Olarak Kaydet” veya “Kaydet ve Başlat” seçeneklerinden birini seçebilecek.
- Uygulama sonuçları:
  - “Taslak Olarak Kaydet” strateji sürümünü saklar fakat piyasa verisi izleme, sinyal üretimi veya emir oluşturma başlatmaz.
  - “Kaydet ve Başlat” önce değişmez strateji sürümünü oluşturur, ardından doğrulama ve başlatma işlemini ayrı ve izlenebilir bir adım olarak yürütür.
  - Eksik/zıt ayar, borsa desteği, işlem çifti kuralı, bakiye, risk sınırı veya güvenlik kontrolü hatasında kayıt korunabilir fakat strateji çalışmaya başlamaz; Türkçe hata nedenleri gösterilir.
  - Deneme modu ve gerçek mod aynı başlatma düğmesini paylaşsa bile gerçek modda `DEC-0015` kapsamındaki risk uyarısı, çok aşamalı kimlik doğrulama ve atlanamayan teknik kontroller uygulanır.
  - Kullanıcı düğmeye birden fazla kez bassa veya ağ yanıtı kesilse bile aynı strateji sürümü için yinelenen çalışma örneği/emir oluşmayacak.
  - Başlatma durumu en az Taslak, Doğrulanıyor, Hazır, Başlatılıyor, Çalışıyor ve Hatalı aşamalarını ayırt edecek.
  - Kaydetme başarılı fakat başlatma başarısızsa kullanıcıya iki sonuç ayrı gösterilecek; “strateji kayboldu” veya “çalışıyor” izlenimi verilmeyecek.
  - Duraklatma, durdurma, arşivleme, açık emir/pozisyon davranışı ve sunucu yeniden başlatma kuralları Q-087 ile ayrıca kesinleştirilecek.
- Gerekçe: Hızlı başlatma kolaylığı sunarken taslak hazırlama ve güvenli doğrulama ihtiyacını korumak.
- Ödünleşimler: Tek düğme arkasında kayıt ve başlatma iki ayrı güvenilir işlem olarak yönetilmelidir.
- Önceki karar: DEC-0014 ve DEC-0015 ile birlikte uygulanır

### DEC-0026 — Duraklatma korumayı sürdürür, durdurma açık işlem seçimi sunar

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-037, Q-053, Q-056, Q-073, Q-087, Q-088; DEC-0014, DEC-0017, DEC-0025
- Karar: Strateji duraklatıldığında yeni girişler duracak ve bekleyen giriş emirleri iptal edilecek; açık işlemlerin kâr alma, zarar durdurma ve diğer koruyucu çıkış yönetimi devam edecek. Strateji durdurulurken kullanıcı açık işlemleri korumayı veya güvenli biçimde kapatmayı seçecek.
- Uygulama sonuçları:
  - Duraklatma başlar başlamaz yeni sinyalden giriş emri üretimi engellenir ve henüz gerçekleşmemiş giriş ile kademeli ek alım emirleri güvenli biçimde iptal edilir.
  - Açık işlemlerin borsadaki kâr alma, zarar durdurma, hareketli zarar durdurma ve azaltıcı çıkış emirleri iptal edilmez; yönetim hizmeti bunları izlemeyi sürdürür.
  - Duraklatma sırasında yeni kademeli alım yapılmaz; yalnız pozisyon riskini azaltan çıkış davranışlarına izin verilir.
  - Durdurma ekranı “Açık İşlemleri Koru” ve “Açık İşlemleri Kapat” seçeneklerini, etkilenecek emir/işlem sayısını ve tahmini riskleri gösterir.
  - “Açık İşlemleri Koru” seçilirse yeni girişler kalıcı olarak kapanır fakat koruyucu yönetim, işlemler tamamen kapanana kadar ayrı bir yönetim durumu olarak devam eder.
  - “Açık İşlemleri Kapat” seçilirse bekleyen girişler iptal edilir; pozisyonlar borsanın yalnız azaltma/pozisyon kapatma özelliğiyle kapatılır ve parçalı gerçekleşme bitene kadar izlenir.
  - Koruyucu emirler, pozisyonun kapandığı doğrulanmadan kaldırılmaz. Kapatma başarısız veya kısmi kalırsa sistem kullanıcıyı uyarır ve kalan riski görünür tutar.
  - Duraklatma, devam ettirme ve durdurma işlemleri tekrar gönderildiğinde yinelenen emir üretmeyecek ve tamamı kayıt altına alınacaktır.
  - Sunucu yeniden başlatma sonrası devam davranışı bu karara dahil değildir; Q-088 ile ayrıca belirlenecektir.
- Gerekçe: Yeni riski hemen keserken açık işlemleri korumasız bırakmamak ve durdurma anında kullanıcıya açık işlem tercihi vermek.
- Ödünleşimler: Durdurulmuş stratejiye bağlı açık işlemler kapanana kadar koruyucu yönetim hizmetinin çalışması gerekir.
- Önceki karar: DEC-0014, DEC-0017 ve DEC-0025 ile birlikte uygulanır

### DEC-0027 — Yeniden başlatmada deneme otomatik, gerçek mod onaylı devam eder

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-037, Q-055, Q-065, Q-073, Q-087, Q-088; DEC-0015, DEC-0026
- Karar: Sunucu yeniden açıldığında deneme modundaki çalışan stratejiler kayıtlı durumları doğrulandıktan sonra otomatik devam edecek. Gerçek moddaki stratejiler borsa hesabı karşılaştırması tamamlandıktan sonra kullanıcı onayı bekleyecek.
- Uygulama sonuçları:
  - Deneme modunda sanal bakiye, açık sanal işlemler, bekleyen sanal emirler, strateji sürümü ve son işlenen piyasa verisi geri yüklenir; yinelenen sinyal/emir oluşmadan devam edilir.
  - Gerçek moddaki stratejiler başlangıçta “Karşılaştırma Bekliyor” durumuna geçer ve yeni giriş üretemez.
  - Sistem borsadaki bakiye, açık emir, gerçekleşen emir ve açık işlemleri yerel kayıtlarla karşılaştırır; bilinmeyen veya eksik kayıtları kullanıcıya Türkçe bildirir.
  - Açık işlemlerin borsadaki koruyucu emirleri önce doğrulanır. Koruma eksikse yeni girişlerden önce güvenli yeniden kurma veya acil uyarı işlemi uygulanır.
  - Karşılaştırma temiz olsa bile gerçek strateji kullanıcı açıkça “Devam Et” onayı vermeden yeni giriş üretmez.
  - Fark varsa kullanıcıya otomatik düzeltme yapılmadan önce ayrıntılı etki özeti ve güvenli seçenekler sunulur; belirsiz durumda sistem kapalı kalır.
  - Devam onayı çok aşamalı kimlik doğrulama gerektirebilir ve strateji sürümü, hesap, karşılaştırma sonucu ve kullanıcı kimliğiyle kayıt altına alınır.
  - Sistem açılışında bağlantı veya borsa verisi alınamıyorsa gerçek mod güvenli biçimde bekler; deneme modu veri akışı sağlanmadan ilerlemez.
- Gerekçe: Deneme çalışmalarını kolayca sürdürürken gerçek para işlemlerinde kesinti sonrası kayıt farkı ve çift emir riskini önlemek.
- Ödünleşimler: Gerçek mod, kullanıcı onayı gelene kadar yeni fırsatları kaçırabilir; buna karşılık bilinmeyen hesap durumunda otomatik risk alınmaz.
- Önceki karar: DEC-0015, DEC-0025 ve DEC-0026 ile birlikte uygulanır

### DEC-0028 — Kullanıcı içinde benzersiz strateji adları

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-053, Q-057, Q-074; DEC-0001, DEC-0003
- Karar: Her kullanıcının strateji adları benzersiz olacak; aynı kullanıcı aynı adla ikinci bir strateji kaydedemeyecek.
- Uygulama sonuçları:
  - Ad karşılaştırılırken baştaki/sondaki boşluklar kaldırılır, birden fazla gereksiz boşluk düzenlenir ve büyük-küçük harf farkı aynı ad kabul edilir.
  - Türkçe ve diğer dil karakterleri desteklenir; teknik güvenlik için denetim karakterleri ve görünmez yanıltıcı karakterler engellenir veya düzeltilir.
  - Benzersizlik yalnız arayüzde değil, veri tabanında kullanıcı kimliği + düzeltilmiş ad üzerinde güvenli kısıtlamayla uygulanır.
  - Eşzamanlı iki kaydetme isteği aynı adı oluşturmaya çalışırsa yalnız biri başarılı olur; diğerine Türkçe ve anlaşılır hata gösterilir.
  - Strateji kopyalandığında sistem “Ad Kopyası”, “Ad Kopyası 2” gibi ilk uygun benzersiz adı önerir; kullanıcı kaydetmeden önce değiştirebilir.
  - Strateji adı değiştirilebilir fakat her değişiklik benzersizlik kontrolünden geçer ve geçmiş kayıtlar değişmez strateji kimliğiyle bağlı kalır.
  - Arşivlenmiş stratejiler de aynı kullanıcı ad alanını korur; kullanıcı eski adı yeniden kullanmak isterse önce arşivdeki stratejiyi yeniden adlandırmalı veya kalıcı silme kurallarını uygulamalıdır.
  - Kesin en az/en çok karakter sınırı arayüz ve veri tabanı gereksinimleriyle ayrıca belirlenecek; boş ad kabul edilmeyecek.
- Gerekçe: Uyarı, rapor, seçim listesi ve işlem kayıtlarında stratejilerin adla karışmasını önlemek.
- Ödünleşimler: Arşivlenmiş adların da ayrılmış kalması bazı adların yeniden kullanımını sınırlar; kalıcı kimlik yine ad değil sistem numarasıdır.
- Önceki karar: DEC-0001 ve DEC-0003 ile birlikte uygulanır

### DEC-0029 — Bağlı ayarlar etki özeti ve onay sonrası temizlenir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-003, Q-004, Q-005, Q-053, Q-075, Q-076; DEC-0002, DEC-0014
- Karar: Kullanıcı borsa, Spot/Vadeli işlem türü veya işlem yönünü değiştirmeden önce etkilenecek bağlı ayarlar gösterilecek; kullanıcı onayladığında yalnız uyumsuz ayarlar temizlenecek.
- Uygulama sonuçları:
  - Etki özeti temizlenecek, değişmeden kalacak ve yeniden seçilmesi gerekecek alanları ayrı listeler.
  - Bağlı alanlara en az işlem çiftleri, emir türleri, yalnız azaltma ve yalnız pasif emir özellikleri, marjin türü, kaldıraç, Long/Short yönü, pozisyon büyüklüğü, kâr alma/zarar durdurma ve borsaya özel ayarlar dahildir.
  - Kullanıcı onaylamazsa ana değişiklik ve bağlı alan temizliği uygulanmaz; mevcut taslak aynen korunur.
  - Onay sonrası yalnız yeni seçimin desteklemediği veya anlamını kaybeden alanlar temizlenir; uyumlu ortak ayarlar korunur.
  - Temizlenen her alan kullanıcıya Türkçe neden ve yeniden seçim gereksinimiyle gösterilir; gizli eski değer çalıştırma sırasında kullanılmaz.
  - Çalışan bir stratejide değişiklik doğrudan mevcut sürümü değiştirmez; `DEC-0014` gereğince yeni ve değişmez strateji sürümü oluşturur.
  - Açık işlemlere uygulanmak istenirse ayrıca `DEC-0014` kapsamındaki etki önizlemesi ve güvenli taşıma kuralları uygulanır; borsada değiştirilemeyen alanlar reddedilir.
  - Borsa yetenek bilgisi alınamıyor veya güncel değilse sistem uyumluluk varsaymaz; kaydetme/başlatma güvenli biçimde engellenir.
  - Sunucu tarafı doğrulama, arayüz önizlemesinden bağımsız olarak tüm uyumsuz alanları tekrar kontrol eder.
- Gerekçe: Eski ve görünmeyen ayarların yeni borsa/işlem türünde yanlış emir üretmesini önlemek.
- Ödünleşimler: Her ana seçim değişikliğinde kullanıcıya ek onay adımı ve ayrıntılı bağlılık haritası gerekir.
- Önceki karar: DEC-0002 ve DEC-0014 ile birlikte uygulanır

### DEC-0030 — Riskli finansal alanlar boş ve zorunlu gelir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-031, Q-032, Q-033, Q-034, Q-046, Q-049, Q-054, Q-076; DEC-0005, DEC-0006, DEC-0015–DEC-0019
- Karar: Yeni stratejide pozisyon tutarı, kaldıraç, zarar durdurma ve risk sınırları hazır değerle doldurulmayacak; kullanıcı bu alanları zorunlu olarak kendisi girecek.
- Uygulama sonuçları:
  - Arayüz riskli alanlarda örnek açıklama gösterebilir fakat örnek sayı gerçek değer olarak kaydedilmez veya sessizce emre dönüşmez.
  - Spot işlemlerde kaldıraç alanı gösterilmez; Vadeli işlemlerde kullanıcı açıkça kaldıraç seçmeden strateji başlatılamaz.
  - Pozisyon tutarı, `DEC-0005` ve `DEC-0006` kapsamındaki tutar türü ve bakiye tabanıyla birlikte açıkça seçilir.
  - Zarar durdurma zorunlu alan olur; kullanıcı fiyat/yüzde türünü ve değeri seçer. Borsada desteklenen koruyucu emir kurulmadan gerçek giriş güvenli kabul edilmez.
  - En az bir risk kuralı tanımlanmadan strateji başlatılamaz; kapsam, ölçüm, eşik, zaman penceresi ve aksiyon alanları eksiksiz olmalıdır.
  - Kullanıcı değerleri borsanın en az/en çok miktar, fiyat adımı, kaldıraç dilimi, kullanılabilir bakiye ve platform hard sınırlarına göre sunucu tarafında denetlenir.
  - Deneme ve geçmiş veri sınamasında da aynı zorunlu alanlar kullanılır; böylece eksik risk ayarıyla iyimser sonuç üretilmez.
  - Strateji kopyalanırken değerler kopyalanabilir fakat kullanıcı yeni borsa/hesapta başlatmadan önce etki özetini ve risk değerlerini yeniden onaylar.
  - Hazır değer bulunmaması, platformun atlanamayan hard güvenlik sınırları olmadığı anlamına gelmez.
- Gerekçe: Sistem kullanıcının haberi olmadan finansal risk seçmesin; kullanıcı kritik değerleri bilinçli ve açık biçimde belirlesin.
- Ödünleşimler: Strateji oluşturma daha uzun sürer ve hızlı başlangıç azalır; yanlışlıkla varsayılan risk alınması önlenir.
- Önceki karar: DEC-0005, DEC-0006, DEC-0015, DEC-0016 ve DEC-0019 ile birlikte uygulanır

### DEC-0031 — Ayrıntılı strateji başarı ve risk ölçümleri

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-043, Q-044, Q-045, Q-051, Q-052, Q-077, Q-080; DEC-0011, DEC-0023, DEC-0024
- Karar: Strateji sonuçlarında temel ölçümlere ek olarak ayrıntılı başarı, maliyet ve risk ölçümleri gösterilecek.
- Uygulama sonuçları:
  - Zorunlu ölçümler: net kâr/zarar, brüt kâr/zarar, başarı oranı, toplam işlem sayısı, sermayenin en yüksek noktadan düşüşü, kazanç-kayıp oranı, ortalama işlem sonucu, toplam işlem ücretleri, toplam fonlama maliyeti, ortalama/aşırı açık kalma süresi ve en uzun art arda kayıp dizisi.
  - `DEC-0011` gereğince fiyat getirisi, brüt/net kâr-zarar, kullanılan marjine göre getiri ve strateji sermayesi getirisi ayrı gösterilir.
  - Tam kapanmış, kısmen kapanmış, başabaş ve açık işlemler ayrı sayılır; başarı oranının pay/paydasında hangi sınıfların kullanıldığı raporda açıklanır.
  - Deneme modu, geçmiş veri sınaması ve gerçek işlemler ayrı raporlanır; kullanıcı açıkça karşılaştırma istemedikçe sonuçlar birleştirilmez.
  - Her ölçüm dönem başlangıcı/bitişi, raporlama para birimi, borsa/hesap, strateji sürümü, işlem türü ve kullanılan benzetim düzeyiyle birlikte gösterilir.
  - Para yatırma, çekme ve hesaplar arası aktarım strateji getirisi sayılmaz; sermaye değişimleri düzeltilmiş hesaplamayla ele alınır.
  - Ücret ve fonlama maliyetleri hem toplam hem işlem bazında görülebilir; eksik borsa maliyet verisi varsa net sonuç “eksik veri” uyarısıyla işaretlenir.
  - Ölçümlerin kesin matematiksel tanımları, yuvarlama kuralları ve örnekleri gereksinim/hesaplama belgesinde yazılacak ve otomatik testlerle doğrulanacaktır.
  - Sonuç ekranındaki bütün ölçüm adları ve açıklamaları sade Türkçe olacaktır.
- Gerekçe: Yalnız kâr ve başarı oranına bakarak risk, maliyet ve sürdürülebilirlik hakkında yanıltıcı sonuç çıkarılmasını önlemek.
- Ödünleşimler: Ayrıntılı rapor daha fazla veri, hesaplama, açıklama ve kullanıcı arayüzü alanı gerektirir.
- Önceki karar: DEC-0011, DEC-0023 ve DEC-0024 ile birlikte uygulanır

### DEC-0032 — Ayrıntılı emir aşamaları, sade ana ekran ve tam ayrıntı geçmişi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-021–Q-027, Q-055, Q-065, Q-078, Q-085; DEC-0009, DEC-0010, DEC-0027
- Karar: Sistem emirlerin bütün ayrıntılı işlem aşamalarını ve geçişlerini kaydedecek; ana ekranda sade durum, emir ayrıntısında zaman sıralı tüm aşamalar gösterilecek.
- Uygulama sonuçları:
  - İç durumlar en az Hazırlanıyor, Gönderiliyor, Borsa Kabul Etti, Kısmen Gerçekleşti, Tamamlandı, İptal Bekliyor, İptal Edildi, Süresi Doldu, Reddedildi, Durumu Belirsiz ve Durumu Araştırılıyor aşamalarını ayırt eder.
  - Ana ekranda bu durumlar Bekliyor, Kısmen Gerçekleşti, Tamamlandı, İptal Edildi, Başarısız ve İnceleniyor gibi anlaşılır Türkçe özetlere dönüştürülür.
  - Ayrıntı sayfası her geçişin zamanı, gerçekleşen/kalan miktar, ortalama fiyat, ücret, borsa emir numarası, neden açıklaması ve ilgili sistem olayını gösterir.
  - Her durum değişikliği sona eklenen değişmez olay kaydına yazılır; geçmiş durumlar yerinde değiştirilmez veya silinmez.
  - “Durumu Belirsiz” emir otomatik olarak yeniden gönderilmez; önce borsada emir numarası veya benzersiz istem numarasıyla araştırılır. Böylece çift emir önlenir.
  - Parçalı gerçekleşmeler ayrı ayrı kaydedilir ve toplam emir durumu bunlardan hesaplanır; kalan miktar hiçbir zaman varsayımla sıfırlanmaz.
  - İptal isteği gönderilmesi emrin iptal edildiği anlamına gelmez; borsa onayı veya karşılaştırma sonucu gelene kadar “İptal Bekliyor” gösterilir.
  - Borsadan gelen ret/hata kodu korunur fakat kullanıcıya sade Türkçe açıklama ve yapılabilecek işlem gösterilir.
  - Deneme, geçmiş sınama ve gerçek işlem aynı temel durum modelini kullanır; kaynak modu açıkça etiketlenir.
- Gerekçe: Kullanıcıya sade görünüm sunarken finansal işlem geçmişini eksiksiz, araştırılabilir ve çift emir riskine dayanıklı tutmak.
- Ödünleşimler: Durum geçişleri, olay kaydı ve borsa karşılaştırması basit bir “başarılı/başarısız” alanından daha karmaşıktır.
- Önceki karar: DEC-0009, DEC-0010 ve DEC-0027 ile birlikte uygulanır

### DEC-0033 — Önce borsada koruma, destek yoksa açık uyarılı sistem takibi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-028–Q-030, Q-034, Q-037, Q-055, Q-065, Q-079; DEC-0015, DEC-0026, DEC-0027
- Karar: Kâr alma, zarar durdurma ve diğer koruyucu çıkış emirleri öncelikle doğrudan borsaya yerleştirilecek. Borsa ilgili korumayı desteklemiyorsa kullanıcıya açık kesinti riski gösterilerek sistem tarafından takip seçeneği sunulacak.
- Uygulama sonuçları:
  - Borsa desteği; borsa, Spot/Vadeli ürün, emir türü ve hesap modu için güncel yetenek kaydından doğrulanır; destek varsayılmaz.
  - Borsaya yerleştirilen koruyucu emrin kabul edildiği, doğru miktar/yön/fiyatla açık olduğu doğrulanmadan işlem “korunuyor” olarak gösterilmez.
  - Vadeli işlemlerde koruyucu çıkışlar yalnız pozisyon azaltma veya pozisyon kapatma özelliğini kullanır; yanlışlıkla ters yeni pozisyon açamaz.
  - Borsa desteği yoksa arayüz sistem takibinin sunucu, ağ, veri akışı veya borsa bağlantısı kesilirse çalışmayabileceğini açık Türkçe uyarıyla anlatır.
  - Sistem takibi kullanıcı tarafından ayrıca seçilip onaylanır; sessizce veya otomatik olarak borsa korumasının yerine geçmez.
  - Gerçek modda sistem takibi için güncel piyasa verisi, zaman uyumu, sürekli izleme, alarm, yedek çalışma süreci ve kesinti davranışı zorunlu teknik kontroldür.
  - Veri eski, bağlantı kopuk veya sistem sağlığı yetersizse yeni korumasız giriş güvenli biçimde engellenir; mevcut açık risk için acil uyarı üretilir.
  - Koruma türü, borsadaki emir numarası veya sistem takip kuralı, son doğrulama zamanı ve koruma durumu işlem ayrıntısında gösterilir.
  - Koruyucu emir değiştirilirken yeni koruma doğrulanmadan eski koruma kaldırılmaz; eşzamanlı iki çıkışın pozisyonu tersine çevirmemesi için miktar ve yalnız azaltma denetimi yapılır.
- Gerekçe: Borsa tarafındaki koruma ile kesintiye dayanıklılığı artırırken borsanın desteklemediği durumlarda kullanıcıya bilinçli bir seçenek sunmak.
- Ödünleşimler: Sistem takibi borsa üzerindeki koruma kadar güvenli değildir ve yüksek erişilebilirlik, izleme, uyarı ve kullanıcı onayı gerektirir.
- Önceki karar: DEC-0015, DEC-0026 ve DEC-0027 ile birlikte uygulanır

### DEC-0034 — Üç işlem sonucu ayrı tutulur, yan yana karşılaştırılabilir

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-043, Q-051, Q-052, Q-054, Q-077, Q-080, Q-085; DEC-0011, DEC-0023, DEC-0024, DEC-0031
- Karar: Geçmiş veri sınaması, sanal bakiyeyle deneme ve gerçek para işlem sonuçları ayrı kayıt ve raporlarda tutulacak; kullanıcı isterse bunları yan yana karşılaştırabilecek.
- Uygulama sonuçları:
  - Her emir, gerçekleşme, işlem, bakiye hareketi ve ölçüm kaydı kaynak türünü değişmez biçimde taşır: Geçmiş Sınama, Deneme veya Gerçek.
  - Bir kaynak türündeki sanal bakiye, emir veya açık işlem başka kaynak türüne aktarılmaz; gerçek mod finansal sonuçları sıfırdan ve gerçek borsa kayıtlarından oluşur.
  - Ana raporlar kaynak türüne göre ayrı sekme/filtre sunar; toplam net kâr gibi finansal değerler üç tür arasında toplanmaz.
  - Karşılaştırma ekranında aynı strateji ailesi/sürümü, aynı veya açıkça farklı dönem, borsa, işlem çifti ve para birimi yan yana gösterilir.
  - Dönem, strateji sürümü, veri kaynağı veya ayarlar farklıysa karşılaştırma ekranı farkları görünür biçimde işaretler; eşdeğer sonuç izlenimi vermez.
  - Karşılaştırmada net kâr/zarar, başarı oranı, sermayenin en yüksek noktadan düşüşü, işlem sayısı, ücret/fonlama ve emir gerçekleşme farkları ayrı sütunlarda gösterilir.
  - Geçmiş sınama ve deneme sonuçlarında kullanılan benzetim düzeyi ve varsayımlar; gerçek sonuçlarda gerçekleşen ücret/fiyat kayması açıkça gösterilir.
  - Dışa aktarılan dosyalar kaynak türünü her satırda veya değişmez rapor üst bilgisinde taşır.
  - Erişim ve saklama kuralları ayrı uygulanabilse de denetim izi üç kaynak türünde de korunur.
- Gerekçe: Sanal veya geçmiş sonuçların gerçek kazanç gibi görünmesini önlerken strateji davranışındaki farkları inceleme olanağı vermek.
- Ödünleşimler: Ayrı kayıt kümeleri ve karşılaştırma eşleştirmesi daha fazla veri modeli ve arayüz işi gerektirir.
- Önceki karar: DEC-0011, DEC-0023, DEC-0024 ve DEC-0031 ile birlikte uygulanır

### DEC-0035 — İlk sürüm normal hız, yüksek hız sonraki çalışma

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-051, Q-052, Q-065, Q-081, Q-089; DEC-0007, DEC-0023, DEC-0024
- Karar: İlk sürüm normal işlem hızına göre tasarlanacak; yüksek hızlı işlemler daha sonraki ayrı bir çalışma ve sürüm kapsamında ele alınacak.
- Uygulama sonuçları:
  - İlk sürüm 1 dakika ve üzeri mum/strateji aralıklarına ve normal borsa uygulama bağlantılarına odaklanır.
  - Saniyenin çok küçük bölümlerinde emir yarışına, borsaya çok yakın özel sunuculara veya özel ağ bağlantısına dayalı yüksek hızlı işlem ilk sürüm kapsamında değildir.
  - Öncelik sırası: doğru piyasa verisi, güvenilir sinyal hesabı, güvenli risk denetimi, yinelenmeyen emir gönderimi, borsa hesabı karşılaştırması ve ölçülebilir gecikmedir.
  - Piyasa verisi alma, sinyal değerlendirme, risk denetimi, emir gönderme ve borsa yanıtı süreleri ayrı ayrı ölçülür ve izlenir.
  - Veri yaşı güvenlik sınırı olarak kalır; veri belirlenen sınırdan eskiyse hızlı davranmak yerine yeni emir güvenli biçimde engellenir.
  - Ağ/borsa gecikmesi sistem işlem süresinden ayrı raporlanır; borsanın yavaş yanıtı uygulamanın kendi süresi gibi gizlenmez.
  - Mimari ileride yüksek hız çalışmasını engellemeyecek açık arayüzler ve ölçüm noktaları kullanır; fakat ilk sürüm gereksiz düşük gecikme karmaşıklığı ve maliyeti taşımaz.
  - Yüksek hız çalışması başlatıldığında veri kaynağı, sunucu konumu, özel bağlantı, işletim sistemi ayarı, emir yolu, risk denetimi ve yeni sayısal hedefler ayrı mimari/karar kaydı gerektirir.
  - İlk sürümün kesin sayısal gecikme, veri yaşı ve hizmet sürekliliği kabul sınırları gerçek hosting ve borsa denemeleriyle ölçülüp Q-089 kapsamında onaylanacaktır.
- Gerekçe: İlk sürümü güvenli ve gerçekçi kapsamda tamamlamak; yüksek hızlı işlem için gereken farklı altyapı ve maliyeti sonraki aşamaya bırakmak.
- Ödünleşimler: İlk sürüm saniyelik veya daha hızlı fiyat fırsatlarını hedeflemez; buna karşılık geliştirme ve işletim karmaşıklığı azalır.
- Önceki karar: DEC-0007, DEC-0023 ve DEC-0024 ile birlikte uygulanır

### DEC-0036 — Sinyal verisi ve emir aynı borsada

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-003–Q-006, Q-010, Q-019, Q-022, Q-082; DEC-0002, DEC-0007
- Karar: Her stratejide sinyal verisinin alındığı borsa ile emrin gönderildiği borsa aynı olacak.
- Uygulama sonuçları:
  - Binance stratejisi Binance piyasa verisi ve mumlarıyla sinyal üretip Binance hesabına emir gönderir; MEXC için aynı ilke uygulanır.
  - Gösterge hesapları, sinyal fiyatı, emir koruma fiyatları, kâr alma ve zarar durdurma aynı borsa, Spot/Vadeli ürün ve işlem çifti kaynağına bağlanır.
  - Kullanıcı arayüzünde ayrı “Sinyal Borsası” ve “Emir Borsası” alanları bulunmaz; tek borsa seçimi tüm bağlı alanları belirler.
  - Strateji sürümü borsa, ürün türü ve işlem çifti kimliğini değişmez biçimde saklar; çalışma anında başka borsa verisine sessizce geçilmez.
  - Seçilen borsanın piyasa verisi kesilir veya eski kalırsa başka borsa fiyatı yedek olarak kullanılıp emir üretilmez; strateji güvenli biçimde yeni girişleri durdurur ve uyarı verir.
  - Borsalar arasındaki fiyat, mum oluşumu, işlem hacmi, fonlama ve işlem çifti kuralları tek bir ortak fiyatmış gibi karıştırılmaz.
  - Geçmiş veri sınaması ve sanal bakiyeyle deneme de seçilen yürütme borsasının verisini kullanır; kullanılan veri kaynağı raporda gösterilir.
  - İleride borsalar arası sinyal istenirse fiyat farkı, zaman uyumu, likidite, ücret, veri yaşı ve risk modeli için yeni kullanıcı kararı ve ayrı özellik gerekir.
- Gerekçe: Borsalar arası fiyat ve mum farklarının yanlış sinyal, koruma ve performans hesabı üretmesini önlemek.
- Ödünleşimler: Kullanıcı bir borsadaki göstergeden yararlanıp başka borsada emir veremez; buna karşılık ilk sürüm daha tutarlı ve güvenli olur.
- Önceki karar: DEC-0002 ve DEC-0007 ile birlikte uygulanır

### DEC-0037 — Geniş kişisel kullanım için 50 strateji ve strateji başına 200 çift

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-006, Q-009, Q-019, Q-065, Q-081, Q-083; DEC-0001, DEC-0035
- Karar: İlk sürüm geniş kişisel kullanım için 1 kullanıcı, en fazla 50 eşzamanlı çalışan strateji ve strateji başına en fazla 200 işlem çiftini destekleyecek.
- Uygulama sonuçları:
  - En yüksek kuramsal çalışma yükü 10.000 strateji–işlem çifti birleşimidir; bu sayı yük ve dayanıklılık sınamasının üst senaryosu olarak kullanılır.
  - Aynı borsa, Spot/Vadeli ürün, işlem çifti ve zaman aralığı birden fazla stratejide kullanılıyorsa piyasa verisi bağlantısı ve temel mum verisi paylaşılır; her strateji ayrı bağlantı açmaz.
  - Stratejilerin koşul hesapları ve durumları birbirinden ayrılır; bir stratejinin hatası diğer stratejilerin emir veya risk durumunu bozamaz.
  - Borsa bağlantı ve istek sınırları merkezi olarak izlenir; 50×200 sınırı borsanın izin verdiği bağlantı/istek sayısını aşma hakkı vermez.
  - Yüksek yükte yeni abonelik ve istekler kontrollü sıraya alınır; güncel olmayan veriyle sinyal üretmek yerine güvenli biçimde gecikme/engelleme uygulanır.
  - Yük sınamaları en az piyasa verisi işleme, gösterge hesabı, sinyal değerlendirme, veri tabanı yazımı, emir kuyruğu, yeniden bağlanma ve toplu borsa kesintisi senaryolarını kapsar.
  - Kabul raporu işlemci, bellek, ağ, veri tabanı, veri yaşı, sinyal gecikmesi ve hata oranını ayrı gösterir; ölçüm yapılan donanım/hosting açıkça kaydedilir.
  - Kullanıcı 50 çalışan strateji veya strateji başına 200 çift sınırına ulaştığında yeni çalışma başlatılamaz; anlaşılır Türkçe sınır mesajı gösterilir.
  - Taslak, durdurulmuş ve arşivlenmiş stratejiler 50 çalışan strateji sınırına dahil edilmez; koruyucu yönetimi süren açık işlemler kaynak kullanımında ayrıca sayılır.
  - Çok kullanıcılı hizmet mimarisi `DEC-0001` gereğince geleceğe hazırlanır fakat ilk sürüm kabul yükü tek kullanıcı içindir.
- Gerekçe: Tek kullanıcı için geniş tarama/strateji kapasitesi sağlarken ilk sürümü ölçülebilir bir üst sınırla tasarlamak.
- Ödünleşimler: 10.000 değerlendirme birleşimi önemli veri ve işlem gücü gerektirebilir; barındırma boyutu gerçek yük sınamasıyla belirlenecektir.
- Önceki karar: DEC-0001 ve DEC-0035 ile birlikte uygulanır

### DEC-0038 — Yalnız sinyal sonrası engellenen işlemler için açıklama kaydı

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-015, Q-038, Q-046–Q-050, Q-065, Q-084; DEC-0007, DEC-0016–DEC-0020
- Karar: “Neden işlem açılmadı?” kaydı yalnız geçerli giriş sinyali oluştuğu hâlde risk, bakiye, borsa, veri veya emir kuralı nedeniyle işlem açılamadığında oluşturulacak.
- Uygulama sonuçları:
  - Koşul ağacı giriş sinyali üretmediyse her olağan değerlendirme için kalıcı ayrıntılı kayıt oluşturulmaz.
  - Giriş sinyali oluştuktan sonra risk sınırı, kullanılabilir bakiye, açık işlem sınırı, eski veri, fiyat farkı, desteklenmeyen borsa özelliği, yinelenen sinyal/emir veya borsa reddi işlemi engellerse açıklama kaydı oluşur.
  - Kayıt en az zaman, strateji ve sürüm, borsa/ürün/işlem çifti, yön, sinyal kimliği, engel aşaması, Türkçe neden kodu, kullanıcıya açıklama ve ilgili kural kimliğini içerir.
  - Karar anındaki yalnız gerekli değerler saklanır: örneğin istenen/kullanılabilir tutar, eşik/ölçülen risk, veri yaşı, izin verilen/ölçülen fiyat farkı. API anahtarı ve hassas bilgiler kayda girmez.
  - Bir sinyal birden fazla nedenle engellendiyse birincil neden ve güvenle hesaplanabilen diğer nedenler ayrı gösterilir; kontrol sırası sonucu gizlenmez.
  - Aynı sinyal için yeniden deneme/karşılaştırma olayları tek karar zincirine bağlanır; kullanıcıya yinelenen bağımsız işlem gibi gösterilmez.
  - Borsanın ret kodu değişmeden saklanabilir fakat kullanıcı ekranında sade Türkçe açıklaması ve önerilen düzeltme gösterilir.
  - Sinyal öncesi koşul incelemesine gerek duyulursa geçici teknik günlük veya tanılama oturumu kullanılabilir; bu, varsayılan kalıcı kullanıcı kaydı değildir.
  - Saklama süresi ve dışa aktarma kuralları veri saklama kararında ayrıca belirlenir.
- Gerekçe: Kullanıcının gerçek bir fırsatın neden işleme dönüşmediğini anlayabilmesini sağlarken 10.000'e kadar değerlendirme birleşiminde gereksiz veri büyümesini önlemek.
- Ödünleşimler: Sinyal hiç oluşmadığında kullanıcı geçmişte her koşulun neden yanlış olduğunu kalıcı kayıttan göremez; bunun için geçici tanılama gerekir.
- Önceki karar: DEC-0007 ve DEC-0016–DEC-0020 ile birlikte uygulanır

### DEC-0039 — İşlem özet satırı ve açılır gerçekleşme alt satırları

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-036–Q-045, Q-077, Q-078, Q-080, Q-085; DEC-0011, DEC-0031, DEC-0032, DEC-0034
- Karar: Her işlem ana listede tek bir özet satırında gösterilecek; kullanıcı satırı açtığında giriş ve çıkış emir gerçekleşmeleri zaman sırasıyla alt satırlarda görülecek.
- Uygulama sonuçları:
  - Özet satırı en az strateji adı/sürümü, kaynak türü, borsa, Spot/Vadeli, işlem çifti, yön, durum, ilk giriş zamanı, toplam giriş/çıkış miktarı, kalan miktar ve ortalama fiyatları gösterir.
  - Gerçekleşmiş ve gerçekleşmemiş net kâr-zarar ayrı alanlardır; açık veya kısmi işlemde toplam sonuç kesinleşmiş gibi gösterilmez.
  - Ücret, fonlama maliyeti ve diğer maliyetler özet toplamlarında ayrı görünür; ayrıntıda ilgili gerçekleşme veya zaman olayına bağlanır.
  - Açılır alt satırlar her giriş/çıkış gerçekleşmesinin zamanı, miktarı, fiyatı, ücreti, emir numarası ve gerçekleşme numarasını gösterir.
  - Kısmi gerçekleşme, kısmi kapanış, kâr alma, zarar durdurma, kullanıcı kapatması ve acil risk kapatması anlaşılır Türkçe neden etiketi taşır.
  - Henüz oluşmamış çıkış zamanı/fiyatı gibi alanlar sıfır veya uydurma değerle doldurulmaz; “Henüz gerçekleşmedi” olarak gösterilir.
  - Bir işlemde birden fazla emir ve gerçekleşme varsa özet değerler değişmez gerçekleşme kayıtlarından hesaplanır; elle tutulan ayrı toplamlar nedeniyle sapma oluşmaz.
  - İşlem ayrıntısından `DEC-0032` kapsamındaki tam emir aşaması geçmişine geçiş yapılabilir.
  - Liste kaynak türüne göre Geçmiş Sınama, Deneme ve Gerçek olarak ayrı tutulur; `DEC-0034` karşılaştırması dışında finansal toplamlar birleşmez.
  - Büyük listelerde sayfalama, tarih/strateji/borsa/çift/durum filtreleri ve dışa aktarma bulunur; parasal hassasiyet yuvarlama nedeniyle kaybedilmez.
- Gerekçe: Kullanıcıya hızlı okunabilir tek işlem özeti verirken parçalı emir gerçekleşmelerinin denetlenebilir ayrıntısını korumak.
- Ödünleşimler: Özetlerin çok sayıda gerçekleşmeden doğru hesaplanması ve büyük listelerin hızlı açılması için dikkatli veri modeli/sorgu tasarımı gerekir.
- Önceki karar: DEC-0011, DEC-0031, DEC-0032 ve DEC-0034 ile birlikte uygulanır

### DEC-0040 — Yerel benzetim, resmî borsa denemesi, ardından gerçek hesap

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-003, Q-004, Q-051, Q-052, Q-054, Q-058, Q-079; DEC-0002, DEC-0015, DEC-0023, DEC-0024, DEC-0033
- Karar: Borsa bağlantısı ve emir davranışı önce yerel benzetimde, sonra ilgili borsanın resmî deneme ortamında, en son gerçek hesapta sınanacak.
- Uygulama sonuçları:
  - Yerel benzetim; başarı, ret, zaman aşımı, bağlantı kopması, parçalı gerçekleşme, yinelenen yanıt, eski veri ve borsa kural hatalarını tekrarlanabilir senaryolarla kapsar.
  - Binance ve MEXC için Spot/Vadeli her ürünün resmî deneme ortamı ve desteklediği özellikler ayrı doğrulanır; bir ürünün deneme desteği diğerine varsayılmaz.
  - Resmî deneme ortamı sınamaları gerçek bağlantı imzalama, saat uyumu, miktar/fiyat adımı, en az işlem tutarı, emir aşamaları, iptal ve hesap karşılaştırmasını kapsar.
  - Deneme ortamındaki sonuçlar gerçek para sonucu olarak raporlanmaz ve gerçek hesap kayıtlarıyla birleştirilmez.
  - Bir borsanın/ürünün resmî deneme ortamı yoksa veya gerekli emir davranışını desteklemiyorsa aşama sessizce geçilmiş sayılmaz; eksik kabul sınaması ve risk açıkça kaydedilir.
  - Böyle bir eksiklikte gerçek hesapta sınama, ayrı kullanıcı onayı, tutar/risk tavanı, geri dönüş planı, sürekli izleme ve acil durdurma hazırlığı olmadan başlatılmaz.
  - Resmî deneme ortamından gerçek hesaba anahtar, hesap numarası, bakiye veya açık emir taşınmaz; ortamlar ayrı gizli bilgiler ve veri kayıtları kullanır.
  - Gerçek hesap aşaması `DEC-0015` kapsamındaki risk uyarısı, çok aşamalı kimlik doğrulama ve atlanamayan teknik kontrollerden sonra açılır.
  - Her aşamanın kabul ölçütleri ve gerçek çıktıları repoda sürümlü sınama raporuna yazılır.
- Gerekçe: Gerçek para riski almadan önce emir yolunu kademeli ve borsaya özgü biçimde doğrulamak.
- Ödünleşimler: Resmî deneme ortamlarının gerçek piyasa davranışını tam yansıtmaması veya bazı ürünlerde bulunmaması ek plan ve süre gerektirebilir.
- Önceki karar: DEC-0002, DEC-0015, DEC-0023, DEC-0024 ve DEC-0033 ile birlikte uygulanır

### DEC-0041 — Seçilebilir iki güçlü giriş yöntemi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-002, Q-005, Q-054, Q-058, Q-090, Q-091; DEC-0001, DEC-0003, DEC-0015
- Karar: Kullanıcı uygulamaya parola + doğrulama uygulaması koduyla veya cihaz parmak izi/yüz tanıma ya da fiziksel güvenlik anahtarıyla giriş yöntemlerinden birini seçebilecek.
- Uygulama sonuçları:
  - Parola ile girişte telefondaki doğrulama uygulamasının süreli tek kullanımlık kodu zorunludur; yalnız parola ile girişe izin verilmez.
  - Parolalar geri döndürülemeyen, güçlü ve güncel bir parola türetme yöntemiyle tuzlanarak saklanır; düz metin veya çözülebilir biçimde tutulmaz.
  - Cihazla giriş, tarayıcı/işletim sisteminin alan adına bağlı güçlü kimlik doğrulama standardını kullanır; biyometrik veri sunucuya veya projeye gelmez.
  - Kullanıcı birden fazla güvenilir cihaz veya fiziksel güvenlik anahtarı kaydedebilir; her kaydın adı, oluşturulma ve son kullanım zamanı görünür olur.
  - Kurtarma kodları yalnız oluşturulurken bir kez gösterilir, tek kullanımlıdır ve sunucuda geri okunabilir biçimde saklanmaz.
  - Yeni cihaz/anahtar ekleme, mevcut yöntemi kaldırma, borsa anahtarı değiştirme ve gerçek modu açma gibi hassas işlemler yeniden güçlü doğrulama gerektirir.
  - Son çalışan giriş yöntemi, doğrulanmış ikinci yöntem veya güvenli kurtarma süreci olmadan kaldırılamaz; kullanıcı yanlışlıkla hesabını erişilemez yapamaz.
  - Başarısız girişlerde hız sınırlama, artan bekleme, güvenlik kaydı ve kullanıcı uyarısı uygulanır; hata mesajı hangi alanın doğru olduğunu saldırgana açıklamaz.
  - Kimlik doğrulama çerezi güvenli, yalnız şifreli bağlantıda, betik erişimine kapalı ve istek sahteciliğine dayanıklı ayarlarla tutulur.
  - İlk kullanıcı oluşturma ve hesap kurtarma akışı dağıtım/hosting güvenliğiyle birlikte ayrıca belgelenecektir; arka kapı niteliğinde varsayılan parola olmayacaktır.
  - Oturum süresi/yeniden doğrulama Q-090, gelecekteki çok kullanıcılı roller Q-091 ile ayrıca kesinleştirilecektir.
- Gerekçe: Kullanıcıya seçim sunarken parola çalınmasına ve sahte giriş sayfalarına karşı güçlü koruma sağlamak.
- Ödünleşimler: İki giriş yöntemi, cihaz yönetimi ve kurtarma akışı geliştirme/sınama kapsamını büyütür.
- Önceki karar: DEC-0001, DEC-0003 ve DEC-0015 ile birlikte uygulanır

### DEC-0042 — Tarayıcı kapanana kadar oturum, hassas işlemlerde yeniden doğrulama

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-002, Q-005, Q-054, Q-058, Q-090; DEC-0004, DEC-0015, DEC-0041
- Karar: Kullanıcı oturumu tarayıcı kapanana kadar açık kalacak; hassas işlemler gerçekleştirilmeden önce yeniden güçlü doğrulama istenecek.
- Uygulama sonuçları:
  - Oturum kimliği kalıcı “beni hatırla” kaydı olarak saklanmaz; tarayıcı oturumu çerezi kullanılır ve normal tarayıcı kapanışında istemci tarafında sona erer.
  - Sunucu oturum kaydını güvenli biçimde doğrular, döndürür ve kullanıcı çıkış yaptığında veya tüm oturumları kapattığında derhal geçersiz kılar.
  - Yalnız sayfa görüntüleme için hareketsizlik nedeniyle otomatik çıkış uygulanmaz; kullanıcı ortak/başkasına ait cihaz kullanmaması konusunda açıkça uyarılır.
  - Hassas işlemler en az gerçek modu açma/devam ettirme, gerçek emir verme/iptal etme/pozisyon kapatma, borsa anahtarı ekleme/değiştirme/silme, risk veya pozisyon tutarı değiştirme, giriş yöntemi/cihaz/kurtarma kodu değiştirme ve veri dışa aktarma işlemlerini kapsar.
  - Hassas işlem anında kullanıcı mevcut güçlü yöntemlerinden biriyle yeniden doğrulanır; yalnız açık oturumun varlığı yeterli sayılmaz.
  - Bir doğrulamanın birden fazla hassas işlem için ne kadar kısa süre geçerli olacağı güvenlik yapılandırmasında üst sınırla tutulur; gerçek para etkili kritik onaylar gerekirse her seferinde istenir.
  - Tarayıcıların “önceki sekmeleri/oturumu geri yükleme” davranışı sınanır; oturum çerezi geri yüklenebiliyorsa bu risk kullanıcıya açıklanır ve sunucu tarafı ek koruma uygulanır.
  - Kullanıcı aktif cihaz/oturum listesini, son kullanım zamanını ve yaklaşık bağlantı bilgisini görebilir; tek oturumu veya tüm diğer oturumları kapatabilir.
  - Parola/giriş yöntemi değişikliği, hesap kurtarma veya şüpheli girişte mevcut oturumların tamamını geçersiz kılma seçeneği sunulur.
  - Oturum çalınması şüphesinde para etkili işlemler yeniden doğrulama olmadan yapılamaz; güvenlik olayları değişmez kayda ve kullanıcı uyarısına dönüşür.
- Gerekçe: Kullanıcının tarayıcı açıkken tekrar tekrar giriş yapmasını önlerken gerçek para ve hesap güvenliği etkili işlemleri ek doğrulamayla korumak.
- Ödünleşimler: Tarayıcı uzun süre açık bırakılırsa görüntüleme erişimi de açık kalır; ortak cihaz kullanımı için daha yüksek risk taşır.
- Önceki karar: DEC-0015 ve DEC-0041 ile birlikte uygulanır

### DEC-0043 — Sabit Sahip ve özel oluşturulabilir yetki rolleri

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-005, Q-057–Q-059, Q-071, Q-091; DEC-0001, DEC-0003, DEC-0041
- Karar: Çok kullanıcılı sürümde Sahip rolü sabit olacak; diğer roller sayfa ve işlem yetkileri seçilerek özel oluşturulabilecek.
- Uygulama sonuçları:
  - İlk tek kullanıcılı sürümde kullanıcı Sahip olarak çalışır; özel rol yönetim ekranının tamamlanması ilk sürüm için zorunlu değildir.
  - Veri modeli kullanıcı, hesap/kuruluş, rol, izin, rol-izin ve kullanıcı-rol bağlarını gelecekte çok kullanıcıya açılabilecek biçimde ayırır.
  - Sahip; sahiplik devri, borsa anahtarı yönetimi, güvenlik yöntemleri, rol/izin yönetimi, gerçek mod yetkisi, faturalandırma ve kuruluş silme gibi en yüksek yetkilere sahiptir.
  - Özel roller görüntüleme, strateji oluşturma/düzenleme, deneme çalıştırma, gerçek modu başlatma, manuel emir/pozisyon işlemleri, risk ayarı, rapor dışa aktarma ve kullanıcı yönetimi gibi küçük izinlerden oluşturulur.
  - İzinler varsayılan kapalıdır; rol yalnız açıkça seçilen işlemleri yapabilir ve yalnız ihtiyaç duyduğu hesap/strateji kapsamına sınırlandırılabilir.
  - Hiçbir özel rol Sahip rolünü değiştiremez, sahipliği devredemez veya kendisinin/atayan kullanıcının sahip olmadığı yetkiyi veremez.
  - Borsa gizli anahtarının açık değerini hiçbir rol arayüzde göremez; yetkili rol yalnız bağlantı ekleme, değiştirme, sınama veya iptal işlevlerini kullanabilir.
  - Gerçek para etkili izinler ayrı ve açık olur; “strateji düzenleyebilir” izni kendiliğinden “gerçek modu açabilir” veya “pozisyon kapatabilir” anlamına gelmez.
  - Rol ve izin değişiklikleri güçlü yeniden doğrulama, etki özeti, değişmez denetim kaydı ve etkilenen kullanıcıya bildirim gerektirir.
  - Son Sahip kaldırılamaz; sahiplik devri yeni sahibin güçlü doğrulaması ve açık kabulünden sonra tamamlanır.
  - Sunucu tarafı her istekte yetkiyi denetler; arayüzde düğmenin gizlenmesi güvenlik kontrolü sayılmaz.
- Gerekçe: Gelecekte farklı ekip görevlerine uygun esneklik sağlarken sahiplik ve gerçek para yetkilerini açıkça ayırmak.
- Ödünleşimler: Özel rol sistemi sabit üç/beş rolden daha karmaşıktır ve izin birleşimleri için kapsamlı güvenlik sınaması gerektirir.
- Önceki karar: DEC-0001, DEC-0003 ve DEC-0041 ile birlikte uygulanır

### DEC-0044 — Göstergeleri yalnız Sahip yayımlar, kullanıcılar talep oluşturur

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001, Q-012, Q-013, Q-019, Q-057, Q-059, Q-091; DEC-0001, DEC-0043
- Karar: İlk sürümde göstergeleri yalnız Sahip ekleyip yayımlayacak. Çok kullanıcılı sürümde kullanıcılar gösterge adı ve isteğe bağlı kaynak bağlantısı, TradingView kodu, görsel veya ekran görüntüsüyle gösterge ekleme talebi oluşturabilecek; göstergeyi yine yalnız Sahip inceleyip sisteme ekleyecek.
- Uygulama sonuçları:
  - İlk sürümde gösterge yönetimi yalnız Sahip yetkisindedir; diğer özel roller gösterge kodu yükleme, değiştirme, etkinleştirme veya silme yetkisi alamaz.
  - Kullanıcının talep formunda gösterge adı zorunlu; açıklama, kaynak bağlantısı, TradingView kodu, beklenen giriş/çıkışlar, örnek değerler, görseller ve ekran görüntüleri isteğe bağlıdır.
  - Kullanıcı talebi yalnız inceleme girdisidir; gönderilen kod, dosya, bağlantı veya görsel sunucuda gösterge olarak doğrudan çalıştırılmaz ve otomatik yayımlanmaz.
  - TradingView kodu referans olarak saklanır; sistem üzerinde doğrudan çalıştırılmaz. Sahip, davranışı projenin güvenli gösterge sözleşmesine uygun biçimde yeniden uygular veya denetlenmiş uyarlama yaptırır.
  - Dış bağlantılar sunucu tarafından otomatik ziyaret edilmez/indirilmez; güvenli görüntüleme ve inceleme kurallarıyla ele alınır. Böylece iç ağ veya gizli hizmetlere istek gönderme riski önlenir.
  - Yüklenen dosyalarda izin verilen tür, boyut ve adet sınırı; içerik türü doğrulama; zararlı dosya taraması; rastgele güvenli dosya adı ve kullanıcıdan ayrı saklama uygulanır.
  - Gösterge paketi çalıştırılabilir ayar dosyalarını arayüzde doğrudan keşfetmek yerine sürümlü ve tipli bir tanım kullanır: kimlik, ad, sürüm, giriş alanları, çıktı alanları, veri ihtiyacı, izinler ve uyumluluk bilgisi.
  - Yayımlanan gösterge varsayılan olarak ağ, dosya sistemi, işletim sistemi komutu, ortam değişkeni veya borsa gizli anahtarına erişemez; yalnız verilen piyasa verisi ve sınırlandırılmış hesaplama araçlarını kullanır.
  - Sahip yayımından önce kod incelemesi, tekrarlanabilir örnek sonuçlar, sınır/değer testleri, gelecekteki veriyi kullanmama testi, işlem süresi/bellek sınırı ve güvenlik taraması zorunludur.
  - Her gösterge sürümü değişmez kimlik ve kaynak kod sürümüyle kaydedilir; mevcut stratejiler eski sürüme bağlı kalır, yükseltme etki özeti ve yeni strateji sürümü gerektirir.
  - Talep durumları en az Alındı, İnceleniyor, Ek Bilgi Bekliyor, Kabul Edildi, Geliştiriliyor, Yayımlandı ve Reddedildi olarak izlenebilir; Sahip Türkçe açıklama ekleyebilir.
  - Talep sahibi, gönderdiği kod/görsel/bağlantıyı paylaşma hakkına sahip olduğunu onaylar; telif/lisans belirsizse gösterge yayımlanmaz.
  - Gösterge kaldırılır veya güvenlik nedeniyle devre dışı bırakılırsa yeni stratejilerde seçilemez; çalışan stratejiler güvenli biçimde durdurulur ya da onaylı sürüme taşınır ve kullanıcı uyarılır.
- Gerekçe: Kullanıcıların ihtiyaçlarını toplayıp yalnız güvenli ve denetlenmiş göstergeleri yayımlarken keyfî kod çalıştırma ve gizli bilgi erişimi riskini önlemek.
- Ödünleşimler: Her talep Sahip incelemesi ve geliştirme gerektirdiği için yeni göstergenin yayımlanması anlık olmaz.
- Önceki karar: DEC-0001 ve DEC-0043 ile birlikte uygulanır

### DEC-0045 — Veri boşluğunda girişleri durdur, doğrulama sonrası otomatik devam et

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-014, Q-019, Q-050, Q-055, Q-065, Q-081, Q-089; DEC-0007, DEC-0020, DEC-0027, DEC-0035, DEC-0036
- Karar: Piyasa verisi geciktiğinde, sıra boşluğu/eksik mum oluştuğunda veya bağlantı koptuğunda yeni girişler hemen durdurulacak; eksik veri aynı borsadan tamamlanıp doğrulanınca strateji otomatik devam edecek ve kullanıcıya bildirim gönderilecek.
- Uygulama sonuçları:
  - Her borsa/ürün/işlem çifti/zaman aralığı veri akışı son mesaj zamanı, borsa zamanı, sıra numarası veya mum bütünlüğüyle izlenir.
  - Veri yaşı ya da sıra boşluğu güvenlik eşiğini aşınca etkilenen stratejiler yeni giriş sinyali ve giriş emri üretemez; eski fiyat “son geçerli fiyat” denilerek kullanılmaz.
  - Etki yalnız sorunlu veri kapsamına uygulanır; ortak veri kaynağı bozuksa onu kullanan tüm stratejiler birlikte güvenli duruma geçer.
  - Sistem eksik mum/işlemleri aynı yürütme borsasının resmî veri isteği üzerinden alır; `DEC-0036` gereğince başka borsa verisiyle boşluğu doldurmaz.
  - Tamamlama sırasında zaman sırası, yinelenen kayıt, fiyat/miktar biçimi, mum kapanışı ve son canlı mesajla kesişim doğrulanır.
  - İndikatörler gerekli geçmiş pencere eksiksiz ve veri güncel olmadan tekrar hesaplanıp yeni sinyal üretmez.
  - Doğrulama başarılı olduğunda strateji son işlenmiş kesin noktadan yinelenen sinyal/emir üretmeden otomatik devam eder.
  - Kesinti başlangıcı, etkilenen stratejiler/çiftler, neden, veri yaşı, tamamlama sonucu ve devam zamanı kullanıcıya Türkçe bildirim ve olay kaydı olarak sunulur.
  - Otomatik tamamlama başarısızsa sistem yeni girişlere kapalı kalır, artan aralıklarla sınırlı yeniden deneme yapar ve acil uyarı üretir; sonsuz hızlı istekle borsa sınırını aşmaz.
  - Açık işlemlerin borsadaki koruyucu emirleri çalışmaya devam eder. Sistem tarafından takip edilen koruma veri güvenilir değilse kullanıcıya yüksek öncelikli uyarı verilir ve önceden tanımlı acil risk davranışı uygulanır.
  - Veri akışı geri geldiğinde kesinti sırasında geçmişte oluşmuş olabilecek giriş sinyalleri topluca geriye dönük emre çevrilmez; yeniden başlama kuralı strateji/sinyal sözleşmesinde açıkça tanımlanır.
- Gerekçe: Eski veya eksik piyasa verisiyle yanlış işlem açmayı önlerken geçici kesintilerden doğrulanmış biçimde otomatik iyileşmek.
- Ödünleşimler: Veri sorunu sırasında bazı giriş fırsatları kaçırılır; güvenilirlik hızdan öncelikli tutulur.
- Önceki karar: DEC-0007, DEC-0020, DEC-0027, DEC-0035 ve DEC-0036 ile birlikte uygulanır

### DEC-0046 — Kesişme koşulunda seçilebilir eşitlik davranışı

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-015–Q-020; DEC-0007, DEC-0008
- Karar: Her “Yukarı Keser” ve “Aşağı Keser” koşulunda eşitliğin kesişmeye dahil veya hariç olduğu kullanıcı tarafından seçilecek.
- Uygulama sonuçları:
  - “Eşitlik Dahil” seçeneğinde Yukarı Keser: önceki sol değer sağ değerden küçük veya eşit ve güncel sol değer sağ değerden büyük olduğunda oluşur.
  - “Eşitlik Dahil” seçeneğinde Aşağı Keser: önceki sol değer sağ değerden büyük veya eşit ve güncel sol değer sağ değerden küçük olduğunda oluşur.
  - “Eşitlik Hariç” seçeneğinde Yukarı Keser: önceki sol değer sağ değerden kesin küçük ve güncel sol değer sağ değerden kesin büyük olduğunda oluşur.
  - “Eşitlik Hariç” seçeneğinde Aşağı Keser: önceki sol değer sağ değerden kesin büyük ve güncel sol değer sağ değerden kesin küçük olduğunda oluşur.
  - Eşitlik davranışı her kesişme koşulunun zorunlu alanıdır; kullanıcı seçmeden koşul/strateji kaydedilemez ve sessiz hazır değer uygulanmaz.
  - Kesişme iki ardışık kesin veri noktasıyla hesaplanır. `DEC-0007` uyarınca Kapanmış Mum modunda iki kapanmış veri noktası, Canlı Mum modunda değişebilen güncel değer kullanılır ve geri çekilme riski gösterilir.
  - Aynı koşul aynı veri adımı için en fazla bir kesişme olayı üretir; yeniden hesaplama, sayfa yenileme veya bağlantı tekrarı yeni olay sayılmaz.
  - Hesaplamada parasal/gösterge değerleri ikili kayan sayı yerine kesin ondalık veya göstergenin tanımlı sayısal hassasiyetiyle karşılaştırılır; yalnız görüntü yuvarlaması kesişme oluşturmaz.
  - Eksik, geçersiz veya henüz yeterli geçmişi olmayan değer kesişme üretmez; neden tanılama kaydında gösterilebilir.
  - Geçmiş sınama, deneme ve gerçek mod aynı kesişme tanımını ve gösterge sürümünü kullanır.
- Gerekçe: Farklı stratejilerin eşitlik noktasını farklı yorumlayabilmesini sağlarken kesişmeyi kesin ve yeniden üretilebilir tanımlamak.
- Ödünleşimler: Kullanıcı her kesişme koşulunda ek bir seçim yapmak zorundadır; strateji ayar ekranı ve sınama kapsamı büyür.
- Önceki karar: DEC-0007 ve DEC-0008 ile birlikte uygulanır

### DEC-0047 — Üç seçilebilir gösterge yönü yöntemi

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-010, Q-012, Q-013, Q-015–Q-020; DEC-0007, DEC-0008, DEC-0044, DEC-0046
- Karar: “Yukarı Yönlü / Aşağı Yönlü” koşulu için Son İki Değer, Art Arda Yön ve Dönemsel Değişim Eşiği yöntemleri ayrı seçenekler olarak desteklenecek.
- Uygulama sonuçları:
  - Son İki Değer yönteminde güncel değer önceki değerden büyükse Yukarı Yönlü, küçükse Aşağı Yönlü olur; eşitse iki yön de oluşmaz.
  - Art Arda Yön yönteminde kullanıcı gerekli ardışık değişim sayısını seçer; her komşu değer kesin artıyorsa Yukarı, kesin azalıyorsa Aşağı oluşur. Aradaki eşitlik diziyi keser.
  - Dönemsel Değişim Eşiği yönteminde kullanıcı bakılacak adım sayısını ve en az mutlak değişim yüzdesini seçer; ilk ve son değer arasındaki yüzdelik değişim eşiğe ulaşırsa yön oluşur.
  - Dönemsel yüzde hesabında başlangıç değeri sıfırsa sonuç geçersiz kabul edilir; sonsuz/uydurma yüzde üretilmez ve neden gösterilir.
  - Her yön koşulunda yöntem zorunlu alandır; seçilen yönteme ait adım sayısı/eşik gibi alanlar doldurulmadan strateji kaydedilemez.
  - Adım sayısı en az 1 ve göstergenin kullanılabilir geçmişiyle uyumlu olur; sistem aşırı değerleri yük/risk sınırına göre reddeder.
  - Değerlerin sayısal hassasiyeti gösterge sözleşmesinden gelir; yalnız ekranda yapılan yuvarlama yön üretmez.
  - `DEC-0007` uyarınca Kapanmış Mum ve Canlı Mum seçimleri aynen uygulanır; Canlı Mum yönü veri değiştikçe geri çekilebilir ve bu risk görünürdür.
  - Geçmiş sınama, deneme ve gerçek mod aynı yöntem, parametre, gösterge sürümü ve veri noktalarını kullanır.
  - Koşul özeti yöntemi ve parametreleri sade Türkçe gösterir; örneğin “RSI son 3 değişimde art arda yükseliyor”.
- Gerekçe: Basit tek adımlı yön, kalıcı ardışık hareket ve anlamlı dönemsel değişim ihtiyaçlarını ayrı ve açık yöntemlerle karşılamak.
- Ödünleşimler: Üç yöntem daha fazla arayüz alanı, doğrulama ve sınama birleşimi gerektirir.
- Önceki karar: DEC-0007, DEC-0008, DEC-0044 ve DEC-0046 ile birlikte uygulanır

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
