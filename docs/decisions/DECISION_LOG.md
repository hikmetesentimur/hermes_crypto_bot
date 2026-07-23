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
