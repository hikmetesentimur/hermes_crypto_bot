# Sistem Bağlamı ve Bileşen Sınırları

## Amaç

Hermes Crypto Bot; tek kullanıcıyla başlayan, Binance ve MEXC Spot/Vadeli ürünlerinde strateji oluşturma, geçmiş sınama, sanal bakiyeyle deneme ve ileride kontrollü canlı yürütme hedefleyen bir web uygulamasıdır.

## Dış aktörler ve sistemler

- **Sahip:** Strateji oluşturur, risk sınırlarını yönetir, deneme sonuçlarını inceler ve canlı geçiş talebi oluşturabilir.
- **Binance / MEXC:** Piyasa verisi, hesap durumu, borsa kuralları ve emir yürütme kaynağıdır.
- **Telegram:** Kritik olay bildirim kanalıdır; finansal gerçeğin kaynağı değildir.
- **Gizli bilgi sağlayıcısı:** Dağıtım sırasında seçilecek KMS/Vault/secret manager adaptörüdür.
- **Yedek hedefi:** Üretim sağlayıcısından ayrı arıza alanında, şifreli yedek saklar.

## Uygulama bileşenleri

| Bileşen | Sorumluluk | Güvenlik sınırı |
|---|---|---|
| Web/API | Kimlik doğrulama, Türkçe yönetim API'si, komut kabulü | İstemci kararına güvenmez; yetki ve doğrulama sunucudadır |
| Strateji çekirdeği | Değişmez strateji sürümleri, koşul AST'si, yaşam döngüsü | Borsa veya web çerçevesine bağımlı değildir |
| Piyasa verisi | Bağlantı, sıra boşluğu, mum/ticker/order-book normalizasyonu | Eski/eksik veri yeni girişi durdurur |
| Gösterge motoru | Sürümlü, deterministik gösterge hesapları | Kullanıcı kodunu doğrudan çalıştırmaz |
| Risk motoru | Katmanlı limitler, rezervasyon, kill switch | Canlı hard limitler atlanamaz |
| Emir niyeti ve yürütme | İdempotent niyet, borsa adaptörü, zaman aşımı ve mutabakat | Bilinmeyen sonuçta kör tekrar yoktur |
| Simülasyon/geçmiş sınama | Ayrı sanal hesap, deterministic replay, maliyet modelleri | Sonuçlar canlı hesapla birleşmez |
| Muhasebe | Gerçekleşme defteri, pozisyon, ücret, fonlama, PnL | Decimal/NUMERIC ve değişmez olaylar kullanır |
| Mutabakat worker'ı | Borsa ile yerel niyet/sahipliği uzlaştırır | Uyuşmazlıkta yeni risk kapalıdır |
| Bildirim | Telegram ve uygulama içi olay teslimi | Sır ve tam kimlik bilgisi içermez |
| Denetim | Eklemeli, bütünlük korumalı kritik olay geçmişi | Hassas değerleri maskeler |

## Kalıcı veri ilkeleri

1. PostgreSQL; strateji sürümü, emir niyeti, borsa emri, gerçekleşme, pozisyon, bakiye görüntüsü ve denetim olayının kayıt kaynağıdır.
2. Redis kaybı finansal geçmişi veya borsa durumunu kaybettirmemelidir.
3. Her kayıt UTC zamanı, sahiplik sınırı ve ilişki/yinelenmeme kimliği taşır.
4. Gerçekleşmeler ve maliyet olayları yeniden yazılmaz; düzeltmeler yeni olayla yapılır.
5. Sanal, geçmiş sınama ve gerçek işlem portföyleri kesin biçimde ayrıdır.

## Dağıtım bağımsızlığı

Uygulama imajları, PostgreSQL ve Redis standart Docker ağında çalışır. TLS sonlandırma, güvenlik duvarı, sabit çıkış IP'si, gizli bilgi yöneticisi, yedekleme ve izleme sağlayıcı seçildiğinde dağıtım adaptörleriyle bağlanır. Çekirdek modüller sağlayıcı SDK'sı içe aktaramaz.

## Bu ilk paketin kapsamı

- Python proje ve kalite iskeleti;
- güvenli ondalık kullanıcı girdisi ayrıştırması;
- strateji yaşam döngüsü durum makinesi;
- otomatik testler ve CI;
- geliştirme amaçlı Docker Compose.

Borsa bağlantısı, kullanıcı kimlik doğrulaması, kalıcı veri şeması ve canlı emir yolu sonraki dikey paketlerde ele alınacaktır. Canlı emir yolu varsayılan kapalı kalır.
