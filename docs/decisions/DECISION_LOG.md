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
