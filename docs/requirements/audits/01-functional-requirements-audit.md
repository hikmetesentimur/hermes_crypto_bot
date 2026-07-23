## Denetim sonucu

Belge doğrudan okunarak 258 satırın tamamı; işlevsel kapsam, tekrar, çelişki, belirsizlik, terminoloji/yazım ve test edilebilir kabul kriterleri bakımından incelendi. Belge güçlü bir ürün fikri sunuyor; ancak mevcut hâliyle özellikle gerçek para ile işlem, koşul motoru, emir yürütme, risk yönetimi ve kâr/zarar hesabı deterministik biçimde geliştirilemez.

### Önem dereceleri

- **Kritik:** Yanlış emir, sermaye kaybı, güvenlik ihlali veya temel mimarinin yanlış kurulması riski.
- **Yüksek:** Geliştiricilerin farklı yorumlayacağı ve ana işlevi etkileyen eksik/çelişkili gereksinim.
- **Orta:** Kullanılabilirlik, veri bütünlüğü veya uç durum eksikliği.
- **Düşük:** Yazım, terim ve belge düzeni sorunu.

---

# 1. Kritik bulgular

### K-01 — Stratejinin çalıştırılma/durdurulma yaşam döngüsü tanımlı değil
**Referans:** Satır 40-47, 95-106, 141-145

Test/Gerçek mod seçiliyor ve strateji kaydediliyor; fakat şunlar belirtilmiyor:

- Kaydetmek stratejiyi otomatik başlatır mı?
- Ayrı `Başlat / Durdur / Duraklat` durumu var mı?
- Gerçek moda geçiş anında emir üretimi başlar mı?
- Durdurulduğunda açık emirler ve pozisyonlar ne olur?
- Uygulama yeniden başlarsa çalışan stratejiler otomatik devam eder mi?

**Gerekli kabul kriteri:** Strateji durum makinesi en az `Taslak, Doğrulanıyor, Çalışıyor, Duraklatıldı, Durduruldu, Hatalı` durumlarıyla; her geçişin emir ve pozisyonlara etkisiyle tanımlanmalı.

---

### K-02 — Tek tıkla Gerçek Moda geçiş güvenlik kontrolüyle çelişiyor
**Referans:** Satır 45-47 ile 102-106 ve 141-145

Satır 46 güvenli geçiş kontrolü öngörürken satır 105/144 “tek tıklama ile” gerçek moda geçişe izin veriyor. Onayın niteliği belirsizdir.

**Risk:** Yanlışlıkla gerçek emir gönderilmesi.

**Gerekli kabul kriteri:**

- Gerçek moda geçişte açık bir onay penceresi olmalı.
- Borsa bağlantısı, API izinleri, bakiye, sembol, minimum emir, kaldıraç ve marjin modu doğrulanmalı.
- Başarısız kontrol durumunda mod değişmemeli.
- Geçiş audit log’a kaydedilmeli.
- Yetkisiz kullanıcı geçiş yapamamalı.

---

### K-03 — API bilgilerinin saklanması güvenlik açısından tanımsız
**Referans:** Satır 2, 5-9

“Borsa API bilgileri klasöre kaydedilsin” ifadesi API anahtarlarının kaynak kodu veya düz dosyada tutulması şeklinde yorumlanabilir.

**Eksikler:**

- API anahtarının kullanıcıya mı, borsaya mı ait olduğu
- Şifreleme ve secret manager kullanımı
- Anahtarların loglarda maskelenmesi
- Trade/withdraw yetkileri
- Anahtar rotasyonu ve silinmesi
- Kullanıcı ve strateji bazlı yetkilendirme

**Gerekli kabul kriteri:** API secret’ları kaynak kodunda veya düz metinde tutulmamalı; şifreli saklama, yalnızca gerekli trade izinleri ve withdrawal yetkisinin reddi tanımlanmalı.

---

### K-04 — Koşul motoru deterministik değil
**Referans:** Satır 20-37, 55-65

Aşağıdaki noktalar tanımsızdır:

- `VE` ve `VEYA` karışık kullanıldığında öncelik ve parantezleme
- Koşulların aynı mumda mı, aynı saniyede mi gerçekleşmesi gerektiği
- Sinyalin mum kapanışında mı, canlı mumda mı üretildiği
- “Yukarı Keser/Aşağı Keser” için önceki ve mevcut değer tanımı
- “Yukarı/Aşağı Yönlü” için eğim hesabı
- Farklı zaman periyotlarındaki indikatörlerin nasıl senkronize edileceği
- Bir sinyalin kaç kez emir üretebileceği
- Unary operatörlerin sağ operandı olmadan, binary operatörlerin sağ operandla kullanılması

Satır 37 VEYA mantığına izin verirken, emir bölümlerindeki “tüm koşullardan ortak sinyal” ifadesi (55, 58-62) tüm koşulların VE olduğu izlenimini veriyor.

**Gerekli kabul kriteri:** Koşul ifadesi ağaç/grup yapısıyla, operatör önceliği ve örnek doğruluk tablolarıyla tanımlanmalı.

---

### K-05 — Emir fiyatı ve piyasa veri kaynağı belirsiz
**Referans:** Satır 55-65

“Anlık gerçek tahta fiyatı” aşağıdakilerden hangisidir belirtilmiyor:

- Son işlem fiyatı
- En iyi alış
- En iyi satış
- Mark price
- Index price
- Mid price

Long ve Short için kullanılacak taraf da belirtilmiyor. Bu durum giriş, stop, take-profit ve P&L sonuçlarını değiştirir.

**Gerekli kabul kriteri:** Her emir ve hesap türü için fiyat kaynağı, veri zaman damgası, kabul edilen veri gecikmesi ve stale-data davranışı tanımlanmalı.

---

### K-06 — Limit, Market ve Post-Only davranışları birbiriyle uyumsuz
**Referans:** Satır 54-64

- Satır 54’te seçenek `Tetikleme Sapması`, satır 60’ta `Tetiklemeli Limit Order`.
- Mevcut “tahta fiyatında” limit emir, emir defterinin karşı tarafına denk gelirse hemen gerçekleşebilir.
- Aynı emir Post-Only seçilmişse borsa tarafından reddedilebilir veya iptal edilebilir.
- Market emri için sinyal fiyatıyla gönderim fiyatının karşılaştırılması tarif ediliyor; emrin ne kadar bekleyeceği ve koşul sağlanmazsa ne olacağı yok.
- Tetiklemeli limit emrinin tetik fiyatı değil, doğrudan hesaplanmış limit fiyatı gönderildiği anlaşılıyor; emir yaşam döngüsü belirsiz.

**Gerekli kabul kriteri:** Emir durumları (`oluşturuldu, gönderildi, açık, kısmi doldu, doldu, iptal, reddedildi, süresi doldu`) ve Post-Only ret/yeniden fiyatlama politikası tanımlanmalı.

---

### K-07 — Simülasyon motoru için gerçekçilik ve doğrulama kriteri yok
**Referans:** Satır 41-44, 55-64, 71-72

Simülasyonun aşağıdakileri nasıl modelleyeceği belirtilmiyor:

- Bid/ask spread
- Emir defteri derinliği ve likidite
- Kısmi dolum
- Slippage
- Maker/taker komisyonu
- Ağ ve borsa gecikmesi
- Funding
- Futures liquidation
- Post-Only retleri
- Minimum miktar ve fiyat adımları

“Gerçekmiş gibi” ifadesi test edilebilir değildir.

**Gerekli kabul kriteri:** Aynı piyasa veri kaydı ve aynı stratejiyle simülasyonun tekrarlanabilir olması; fill algoritması ve ücret modeli açıkça tanımlanmalı.

---

### K-08 — Futures pozisyon büyüklüğü/marjin tanımı hatalı veya yanıltıcı
**Referans:** Satır 51-53

`10 USDT × 5 = 50 USDT pozisyon futures cüzdanından açılacak` ifadesi marjin ile notional pozisyon büyüklüğünü karıştırıyor. Normal yorumda cüzdandan bağlanan marjin 10 USDT, pozisyon nominali 50 USDT’dir; ücret ve marjin kuralları ayrıca uygulanır.

Aynı sorun yüzdelik bakiye örneğinde de bulunuyor.

**Gerekli kabul kriteri:** Alanlar ayrı adlandırılmalı:

- Ayrılan marjin
- Kaldıraç
- Nominal pozisyon büyüklüğü
- Kullanılabilir bakiye
- Gerekli başlangıç/bakım marjini

---

### K-09 — Kâr/zarar formülleri kademeli alım ve ücretleri desteklemiyor
**Referans:** Satır 84-90, 193-253

Kademeli alım ortalama giriş fiyatını ve toplam miktarı değiştirir; ancak detay sayfası hesabı tek bir `Açılış Fiyatı` kullanıyor. Ayrıca komisyon, funding, slippage ve gerçekleşmiş/gerçekleşmemiş P&L yoktur.

`Nihai oran = fiyat değişimi × kaldıraç` ve ardından `işlem tutarı × nihai oran` hesabı, “işlem tutarı” nominal pozisyon ise kaldıracı iki kez uygulayabilir.

**Gerekli kabul kriteri:** Ağırlıklı ortalama giriş, çoklu girişler, çoklu çıkışlar, ücretler, funding ve marjin/notional ayrımıyla tek bir P&L spesifikasyonu oluşturulmalı.

---

### K-10 — Risk limitlerinin davranışı kesin değil
**Referans:** Satır 91-94

“Maksimum zarar gerçekleşince tüm işlemleri durdurabilir” ifadesi zorunlu davranış belirtmiyor.

Belirsiz noktalar:

- Gerçekleşmiş mi, gerçekleşmemiş mi, toplam P&L mi?
- Başlangıç bakiyesi mi, gün başı bakiyesi mi?
- Strateji, kullanıcı veya hesap bazında mı?
- Limit aşılınca yalnızca yeni girişler mi durur?
- Açık emirler iptal edilir mi?
- Açık pozisyonlar kapatılır mı?
- Gün/hafta/ay hangi saat diliminde sıfırlanır?
- Tekrar başlatma manuel mi otomatik mi?

---

### K-11 — Aktif strateji düzenleme/kopyalama/silmenin ticari etkisi tanımlı değil
**Referans:** Satır 107-125, 146-164

Açık emir veya pozisyon varken strateji:

- Düzenlenirse yeni ayarlar mevcut pozisyona uygulanır mı?
- Silinirse emirler iptal veya pozisyonlar kapatılır mı?
- Kopyalanırsa çalışma istatistikleri de kopyalanır mı?
- Borsa çağrısı başarısızken yerel silme yapılır mı?

Gerçek para senaryosunda bu davranışlar kritik önemdedir.

---

# 2. Yüksek öncelikli belirsizlik ve eksikler

### Y-01 — Strateji adı girişi hiç tanımlanmamış
**Referans:** Satır 97-101, 116, 139

Strateji adı listeleniyor ve kopya adına ek yapılıyor; ancak adın girileceği alan, zorunluluk, uzunluk, benzersizlik ve karakter kuralları yok.

---

### Y-02 — Borsa ve indikatör eklenti sözleşmesi eksik
**Referans:** Satır 2, 5, 7-9, 12, 17, 20

Klasör oluşturma tek başına modüler mimari sağlamaz. Şunlar tanımlanmalı:

- Ortak adapter/interface
- Spot/Futures yetenek bildirimi
- Sembol, ticker, candle, balance ve order fonksiyonları
- Hata modeli
- `settings.py` ve `parameters.py` şeması
- Veri tipleri, varsayılan değerler ve validasyon
- Eklentinin yüklenememesi durumundaki davranış

Ayrıca satır 2’de `indikatörler`, satır 12’de `indicators` klasörü kullanılmış.

---

### Y-03 — Ön filtre hacim alanları birbirinden ayırt edilemiyor
**Referans:** Satır 8-9

“Para Birimi Olarak Hacim” ile “24 Saatlik Para Birimi Olarak Hacim” arasındaki fark tanımlı değil. Çoğu borsa ticker API’sindeki quote volume zaten 24 saatliktir.

Ayrıca:

- Minimum/maksimum boş olabilir mi?
- Sınırlar dâhil mi?
- Minimum maksimumdan büyükse ne olur?
- Hacim hangi para birimine dönüştürülür?
- Sıfır ve negatif değerler kabul edilir mi?

---

### Y-04 — Bağımlı alan değişikliklerinde veri bütünlüğü tanımlı değil
**Referans:** Satır 5-9, 48-53

Borsa veya işlem tipi değiştiğinde eski:

- Para birimi
- Sembol filtresi
- Marjin/kaldıraç
- Pozisyon yönü
- Bakiye bazlı tutar

değerlerinin temizlenip temizlenmeyeceği belirtilmiyor.

---

### Y-05 — Grafik/mum türleri teknik olarak tutarsız
**Referans:** Satır 15, 29

“Normal Mum Grafiği” ile “Japon Mum Grafiği” muhtemelen aynı kavramdır. Renko ve çizgi grafik standart zaman bazlı OHLC mumlarından farklıdır. Renko kutu büyüklüğü ve çizgi grafiğin fiyat kaynağı belirtilmemiştir.

---

### Y-06 — İndikatör zaman periyodu ve hazır mum davranışı eksik
**Referans:** Satır 16-18, 30-32

- Borsanın desteklemediği periyotlar nasıl türetilecek?
- Aylık/haftalık mum sınırları hangi zaman diliminde?
- İndikatör için gereken minimum geçmiş mum sayısı nedir?
- Yetersiz veri varsa strateji ne yapar?
- Canlı mum mu kapanmış mum mu kullanılır?

---

### Y-07 — Koşul modalında zorunlu alan ve tip uyumluluğu yok
**Referans:** Satır 20-36

Örneğin `RSI – Yukarı Keser – Fiyat` teknik olarak seçilebilir görünüyor; ancak bütün parametre/operatör kombinasyonları anlamlı değildir. Sayısal, boolean, seri ve kategorik tipler tanımlanmalı.

---

### Y-08 — Tekrarlanan sinyaller ve aynı sembolde pozisyon politikası yok
**Referans:** Satır 37, 55-62, 92

- Aynı koşul açık kaldığı her tick’te yeni emir mi üretir?
- Sinyal edge-triggered mı level-triggered mı?
- Aynı sembolde ikinci pozisyon açılır mı?
- Futures hedge/one-way mode nasıl ele alınır?
- Kapanıştan sonra yeniden giriş için bekleme süresi var mı?

---

### Y-09 — Take Profit emir türü ve yürütme davranışı eksik
**Referans:** Satır 66-72

- TP emirleri limit mi market mi?
- Pozisyon açılınca borsaya önceden mi gönderilir?
- `reduce-only` kullanılacak mı?
- Yüzdelik dilim toplamı tam %100 olmalı mı?
- Kâr oranları artan sırada mı olmalı?
- Borsa miktar hassasiyeti nedeniyle kalan küsurat ne yapılır?
- Kısmi gerçekleşme ve emir reddi nasıl yönetilir?

---

### Y-10 — Stop Loss seçeneklerinin birbiriyle ilişkisi belirsiz
**Referans:** Satır 73-90

Standart Stop, Trailing Stop ve Kademeli Alım:

- Birbirini dışlayan seçenekler mi?
- Birlikte etkinleştirilebilir mi?
- “Kademeli Alım” neden Zarar Durdur altında?
- Short pozisyonda kademeli işlem ek satış mı olacak?
- Her kademeden sonra ortalama maliyet, TP ve stop yeniden hesaplanacak mı?
- Maksimum sermaye gereksinimi kaydetmeden önce kontrol edilecek mi?

---

### Y-11 — Trailing Stop tanımı hatalı/eksik
**Referans:** Satır 81-83

Trailing stop, girişe göre `%3 zarar` değil, long için ulaşılan en yüksek değerden; short için en düşük değerden geri çekilme olarak tanımlanmalıdır. Aktivasyon fiyatı ve izleme başlangıcı belirtilmemiştir.

---

### Y-12 — Borsa kısıtları ve hata yönetimi yok
**İlgili konular:** Satır 5-9, 48-64, 66-94

Eksik gereksinimler:

- Tick size, step size, min/max quantity ve min notional
- Desteklenen kaldıraç aralığının sembol bazında alınması
- Bakiye yetersizliği
- Rate limit
- Timeout/retry
- Idempotency/client order ID
- API bağlantı kesintisi
- Kısmi dolum ve emir reddi
- Clock drift
- Delist/symbol suspension

Satır 50’de sabit 1-100 kaldıraç, borsanın ve sembolün gerçek sınırlarıyla uyuşmayabilir.

---

### Y-13 — Kaydetme validasyonu ve atomiklik eksik
**Referans:** Satır 95-97

- Eksik zorunlu alanlarda ne olur?
- Koşul yokken kaydedilebilir mi?
- TP/SL seçilmeden kaydedilebilir mi?
- İki ayrı listede gösterimden biri başarısız olursa ne olur?
- Çift tıklama mükerrer kayıt üretir mi?
- Eşzamanlı düzenleme/version conflict nasıl ele alınır?
- Kaydetme sırasında kullanıcıya başarı/hata bilgisi nasıl verilir?

---

### Y-14 — Silme için onay, soft-delete ve denetim izi yok
**Referans:** Satır 123-125, 162-164

“Tamamen silme” finansal işlem geçmişi ve audit gereksinimleriyle sakıncalıdır. Strateji tanımı silinse bile gerçekleşmiş işlemler korunmalıdır.

---

### Y-15 — İstatistik tanımları eksik
**Referans:** Satır 169-172

- Kısmi kapanan işlem “kapanan işlem” sayılır mı?
- Break-even işlem kârlı mı zararlı mı?
- Komisyon sonrası mı önce mi?
- Düzenlemede sayaçlar devam eder mi?
- Kopyada sayaçlar sıfırlanır mı?
- Test ve gerçek mod istatistikleri ayrı mı?

---

### Y-16 — İşlem detayları açık/kısmi işlemleri karşılamıyor
**Referans:** Satır 185-206

Açık işlemlerde kapanış tarihi/fiyatı yoktur. Kademeli kapanışın tek satırda mı alt satırlarda mı gösterileceği belirtilmemiştir. İşlem durumu, pozisyon yönü, mod, borsa, ücret, funding ve gerçekleşmemiş P&L alanları eksiktir.

---

### Y-17 — Kademeli kapanış tespit kuralı yanlış
**Referans:** Satır 204-206

“Kapanış adeti toplam pozisyon adetine eşit değil” ifadesi final durumda doğru değildir; kademeli kapanışların **toplam kapanış adedi** pozisyon toplamına eşit olabilir. Tespit, kapanış fill sayısı ve pozisyonun kalan miktarı üzerinden yapılmalıdır.

---

### Y-18 — Sıfır sonuç ve zarar işareti tanımlanmamış
**Referans:** Satır 234-253

Sadece pozitif/negatif ele alınmış, sıfır sonucu yoktur. Zarar oranı negatif gösterilirken zarar miktarı örneği pozitif mutlak değer kullanıyor. Gösterim standardı belirlenmeli.

---

# 3. Tekrarlar ve belge yapısı

### Tam veya tama yakın tekrarlar

- **Mod Geçişi:** Satır 102-106 ile 141-145
- **Düzenle:** Satır 107-110 ile 146-149
- **Kopyala:** Satır 111-122 ile 150-161
- **Sil:** Satır 123-125 ile 162-164
- **Borsaya göre gruplama:** Satır 127-136 içinde aynı gereksinim birkaç kez yineleniyor
- **İkinci indikatör ayar akışı:** Satır 26-34, satır 12-20’nin büyük ölçüde tekrarıdır; ortak “İndikatör Seçici/Ayar Editörü” bileşeni olarak tarif edilmelidir.

**Öneri:** Tek bir “Strateji kartı eylemleri” gereksinimi tanımlanıp hangi sayfalarda kullanıldığı belirtilmeli. Tekrarlar ileride farklı güncellenerek çelişki üretir.

---

# 4. Orta öncelikli kabul kriteri eksikleri

### O-01 — Sekme verilerinin kalıcılık sınırı belirsiz
**Referans:** Satır 3

Sekme geçişinde kaybolmaması belirtilmiş; fakat yenileme, tarayıcı kapanması, oturum süresi dolması, geri tuşu ve ağ hatasında davranış yok. Taslak otomatik kaydetme ve “kaydedilmemiş değişiklik” uyarısı tanımlanmalı.

### O-02 — Sayısal alan standardı yok
**Referans:** Satır 8-9, 50-53, 60-90, 92-94

Virgül/nokta ondalık ayracı, negatif değer, sıfır, üst sınır, hassasiyet, bilimsel gösterim ve yapıştırılan hatalı metin davranışı belirtilmemiş.

### O-03 — Varsayılan değerler eksik
Borsa, işlem tipi, mod, yön, marjin modu, kaldıraç, pozisyon büyüklüğü, emir tipi, TP/SL ve risk alanlarının başlangıç değerleri belirtilmemiş.

### O-04 — Yükleniyor/boş/hata durumları yok
Borsa veya indikatör bulunamadığında, API yanıt vermediğinde, sembol listesi boş olduğunda gösterilecek durumlar tanımlanmamış.

### O-05 — Sıralama gereksinimi çelişmeye açık
**Referans:** Satır 129-134 ile 180-181

Stratejilerin alfabetik sıralanması istenirken tarih ve moda göre özelleştirilebilir sıralama da isteniyor. Kullanıcının seçimi alfabetik varsayılanı geçersiz kılar mı belirtilmeli.

### O-06 — Arama/filtre davranışı eksik
**Referans:** Satır 174-176

Büyük/küçük harf, Türkçe karakter, kısmi eşleşme, debounce, sonuç yok durumu ve çöktürülmüş grupların aramada otomatik açılması tanımlanmamış.

### O-07 — Saat dilimi standardı eksik
**Referans:** Satır 185-192

Sadece açılış/kapanış saati için “Türkiye saati” denmiş. Veri tabanında UTC saklama ve gösterimde `Europe/Istanbul` kullanımı açıkça belirtilmeli. Günlük/haftalık limitlerde de aynı standart uygulanmalı.

### O-08 — Performans/SLA kriteri yok
Gerçek zamanlı izleme, sinyal üretimi ve emir gönderimi için maksimum veri gecikmesi, emir gecikmesi, yeniden bağlanma ve kullanılabilirlik hedefleri tanımlanmamış.

### O-09 — Kullanıcı/yetki modeli yok
Birden fazla kullanıcı, rol, strateji sahipliği, borsa hesabı erişimi ve görüntüleme/düzenleme yetkileri belirtilmemiş.

### O-10 — Bildirim gereksinimleri yok
Emir dolumu/reddi, stop, risk limiti, bağlantı kaybı, Gerçek Moda geçiş ve strateji hatasında kullanıcı bildirim kanalı tanımlanmamış.

### O-11 — Erişilebilirlik ve responsive davranış yok
Toggle, slider, modal, renkli kâr/zarar ve iki satırlı kartların klavye, ekran okuyucu ve mobil görünüm kabul kriterleri bulunmuyor. Kâr/zarar yalnız renkle ifade edilmemeli.

### O-12 — Grafik sayfası tanımsız
**Referans:** Satır 255-256

Grafiğin zaman aralığı, mum tipi, işlem giriş/çıkış işaretleri, veri kaynağı ve yetkilendirmesi belirtilmemiş.

---

# 5. Terminoloji ve yazım sorunları

### Terminoloji tutarsızlıkları

- `borsalar/indikatörler` ↔ `indicators` — satır 2, 12, 26
- `Futures İşlem` ↔ daha uygun ve tutarlı `Vadeli İşlem` veya her yerde `Futures`
- `Cross` ↔ Türkçede `Çapraz Marjin`; tek terim seçilmeli — satır 49
- `Para Birimi` gerçekte `Karşıt Para Birimi (quote asset)` anlamında kullanılıyor — satır 7
- `Tetikleme Sapması` ↔ `Tetiklemeli Limit Order` — satır 54, 60
- `Normal Mum` ↔ `Japon Mum` muhtemel kavramsal tekrar — satır 15, 29
- `Limit Order / Market Order / Take Profit / Stop Loss` ile Türkçe terimler karışık
- `koin` yerine ürün genelinde `coin`, tercihen `varlık` veya `baz varlık`
- `tahta fiyatı` teknik olarak belirsiz; bid/ask/last açıkça yazılmalı
- `işlem`, `emir` ve `pozisyon` yer yer birbirinin yerine kullanılıyor

### Belirgin yazım hataları

- `sonradanda` → `sonradan da` — satır 2
- `içerisinede` → `içerisine de` — satır 2
- `açılr` → `açılır` — satır 8
- `tıklanıncada` → `tıklandığında da` — satır 19, 33
- `parametleri` → `parametreleri` — satır 20
- `yada` → `ya da` — çok sayıda satır
- `olarakta` → `olarak da` — satır 35
- `kaydırmadanda` → `kaydırmadan da` — satır 50
- `noktasıda` → `noktası da` — satır 50
- `değerlerde dahil` → `değerler de dâhil` — satır 51
- `seçeneğide` → `seçeneği de` — satır 56, 63
- `Merket Order` → `Market Order` — satır 57
- `lisletelenen` → `listelenen` — satır 101
- `hemde` → `hem de` — satır 110, 125
- `tamemen` → `tamamen` — satır 125, 164
- Finansal anlamda `kar` → `kâr`
- `API` büyük harfle ve tutarlı kullanılmalı

Belgedeki `**` işaretleri gerçek başlık/liste yapısına dönüştürülmeli; mevcut biçim gereksinim hiyerarşisini zorlaştırıyor.

---

# 6. Belgeye eklenmesi gereken ortak kabul kriterleri

Her özellik için en az şu alanlar bulunmalıdır:

1. **Amaç ve kapsam**
2. **Ön koşullar**
3. **Zorunlu/opsiyonel alanlar**
4. **Varsayılan değerler**
5. **Veri tipi, aralık ve hassasiyet**
6. **Başarılı akış**
7. **Hatalı/boş/veri gelmeyen akış**
8. **Yükleme ve yeniden deneme davranışı**
9. **Yetkilendirme ve güvenlik**
10. **Kalıcı veri ve atomiklik**
11. **Emir/pozisyon durum geçişleri**
12. **Audit log**
13. **Performans ve gecikme sınırı**
14. **Given/When/Then test senaryoları**
15. **Borsa hata kodlarının kullanıcıya ve strateji durumuna etkisi**

---

## Sonuç ve önerilen öncelik

Geliştirmeye başlamadan önce şu konular karara bağlanmalıdır:

1. Strateji yaşam döngüsü ve Gerçek Moda güvenli geçiş
2. Koşul motorunun kesin mantığı ve zaman senkronizasyonu
3. Emir/fill durum makinesi ve kullanılacak fiyat kaynakları
4. Marjin–kaldıraç–nominal tutar ayrımı
5. Simülasyon motorunun fill/ücret modeli
6. Kademeli alım/çıkış dâhil tek ve doğru P&L modeli
7. Risk limitlerinin zorunlu aksiyonları
8. Aktif stratejide düzenleme/silme davranışı
9. API secret güvenliği ve kullanıcı yetkilendirmesi
10. Borsa hassasiyetleri, hata yönetimi ve idempotency

**Dosya durumu:** Hiçbir dosya oluşturulmadı veya değiştirilmedi.
**İnceleme sorunu:** Belge sorunsuz biçimde doğrudan okundu; erişim ya da çıkarım hatası yaşanmadı.