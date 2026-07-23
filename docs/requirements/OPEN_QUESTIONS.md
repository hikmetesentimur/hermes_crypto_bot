# Açık Sorular ve Netleştirme Kaydı

Bu dosya, özgün senaryodaki belirsizlikleri, çelişkileri ve eklenmesi önerilen özellikleri izler.

## Kullanım

- Durumlar: `AÇIK`, `CEVAPLANDI`, `ERTELENDİ`, `KAPSAM DIŞI`
- Öncelikler: `P0` (mimari/güvenlik engeli), `P1` (MVP davranışı), `P2` (sonraki sürüm)
- Her cevap `docs/decisions/DECISION_LOG.md` içindeki bir `DEC-*` kaydına bağlanır.
- “Önerilen varsayılan” kullanıcı onayı değildir; yalnızca karar vermeyi kolaylaştırır.

---

## A. Ürün kapsamı ve kullanıcı modeli

### Q-001 — Ürün kimin kullanımına açık olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0001`
- Cevap: İlk sürüm tek kullanıcı için geliştirilecek; mimari ve veri modeli gelecekte çoklu kullanıcıya genişlemeye hazır olacak.
- Soru: Sistem yalnızca Hikmet Esentimur'un kendi hesapları için kişisel/özel bir uygulama mı, yoksa birden fazla müşterinin kayıt olup kendi borsa anahtarlarını bağlayacağı SaaS ürünü mü olacak?
- Neden gerekli: Kimlik doğrulama, tenant izolasyonu, mevzuat, destek, faturalandırma ve güvenlik mimarisini değiştirir.
- Önerilen varsayılan: İlk sürüm tek kullanıcı ve özel erişim; çok kullanıcılı SaaS sonraki faz.

### Q-002 — Uygulama nasıl erişilebilir olacak?
- Durum: ERTELENDİ
- Öncelik: P0
- Karar: `DEC-0004`
- Erteleme gerekçesi: Erişim modeli, hosting altyapısı ve güvenlik yetenekleri görüldükten sonra belirlenecek.
- Soru: Yalnızca özel ağ/VPN üzerinden mi, internete açık alan adı üzerinden mi, yoksa yerel bilgisayarda mı çalışacak?
- Önerilen varsayılan: TLS, kimlik doğrulama ve IP/VPN kısıtı olan özel dağıtım.

### Q-003 — İlk sürümde hangi borsalar ve ürünler desteklenecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0002`
- Cevap: İlk çalışan sürüm Binance ve MEXC borsalarında hem Spot hem Futures işlemleri birlikte destekleyecek.
- Soru: İlk adaptör Binance Spot + Binance USDT-M Futures mı olacak? MEXC veya başka borsa MVP kapsamına girecek mi?
- Önerilen varsayılan: Bir borsa ve iki ürün türüyle başla; adaptör sözleşmesini çoklu borsaya hazır tasarla.

### Q-004 — Deneme ortamı ve gerçek hesap sırası nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0040`
- Cevap: Önce yerel benzetim, sonra her borsanın resmî deneme ortamı, en son gerçek hesap kullanılacak.
- Soru: Geliştirme ve kabul sınamaları hangi sırada ve hangi borsa ortamlarında yapılacak?
- Önerilen varsayılan: Yerel benzetim → resmî borsa deneme ortamı → ayrı onaylı gerçek hesap aşaması.

### Q-005 — İlk sürümde uygulamaya giriş nasıl korunacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0041`
- Cevap: Kullanıcı parola + doğrulama uygulaması kodu veya cihaz parmak izi/yüz tanıma/fiziksel güvenlik anahtarıyla giriş yöntemini seçebilecek.
- Soru: İlk sürümde hangi güçlü kimlik doğrulama yöntemleri desteklenecek?
- Önerilen varsayılan: Parola yolu ikinci doğrulama kodunu zorunlu kılar; cihaz/güvenlik anahtarı yolu ve tek kullanımlık kurtarma kodları da desteklenir.

### Q-006 — Dil, saat dilimi ve sayı biçimi nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Arayüz yalnızca Türkçe mi olacak? Veritabanı UTC, gösterim Europe/Istanbul mı? Ondalık ayırıcı hem virgül hem nokta kabul edecek mi?
- Önerilen varsayılan: UI Türkçe; saklama UTC; gösterim Europe/Istanbul; kullanıcı girişinde virgül/nokta kabul edilip Decimal'a normalize edilir.

---

## B. Piyasa evreni, veri ve indikatörler

### Q-007 — İşlem çifti evreni ne zaman yenilenecek?
- Durum: AÇIK
- Öncelik: P1
- Soru: Borsadaki yeni, askıya alınmış veya delist olmuş çiftler hangi sıklıkta yeniden alınacak; açık stratejiler nasıl etkilenecek?
- Önerilen varsayılan: Başlangıçta ve periyodik yenileme; durdurulmuş/delist çiftte yeni emir yasak, açık risk için alarm ve güvenli kapatma politikası.

### Q-008 — Hacim alanlarının kesin tanımı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: “Para birimi olarak hacim” ve “24 saatlik para birimi olarak hacim” hangi borsa alanlarına karşılık geliyor? İlki mum/periyot hacmi mi, anlık ticker hacmi mi, yoksa farklı bir metrik mi?
- Önerilen varsayılan: Birincisini ayrıca tanımlamadan uygulama; 24 saatlik metrik için quoteVolume kullan.

### Q-009 — Hacim filtrelerinde sınırlar nasıl davranacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Minimum/maksimum boş olabilir mi; sınırlar dahil mi; sıfır ve negatif değerler reddedilecek mi?
- Önerilen varsayılan: İkisi de opsiyonel, sınırlar dahil, negatif reddedilir, minimum maksimumdan büyük olamaz.

### Q-010 — Sinyaller yalnızca kapanmış mumdan mı üretilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0007`
- Cevap: Strateji ayarında “Kapanmış Mum” veya “Canlı Mum” seçilebilecek; varsayılan “Kapanmış Mum” olacak.
- Soru: Devam eden mumdaki değişen indikatör değerleri emir tetikleyebilir mi?
- Önerilen varsayılan: Varsayılan yalnızca kapanmış mum; kullanıcı açıkça seçerse intrabar ve repaint uyarısı.

### Q-011 — “Normal Mum” ve “Japon Mum” farkı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Belgede ayrı seçenekler olarak geçiyorlar fakat genel kullanımda aynı OHLC mumunu ifade edebilirler. Farklı davranış bekleniyor mu?
- Önerilen varsayılan: Tek seçenek olarak “Japon/Standart Mum”.

### Q-012 — Heikin Ashi, Renko ve çizgi verisi nasıl üretilecek?
- Durum: AÇIK
- Öncelik: P1
- Soru: Borsa verisinden istemci/sunucu tarafında mı türetilecek? Renko kutu boyutu ve çizgi kaynağı hangi ayarlara sahip olacak?
- Önerilen varsayılan: Sunucuda deterministik üretim; Renko için ATR/sabit kutu seçimi ve parametreleri; çizgi için varsayılan kapanış.

### Q-013 — Gösterge ekleme ve kullanıcı talep süreci nasıl olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0044`
- Cevap: İlk sürümde göstergeleri yalnız Sahip ekleyecek. Çok kullanıcılı sürümde kullanıcılar ad, isteğe bağlı bağlantı, TradingView kodu ve görsellerle gösterge talebi oluşturabilecek; göstergeyi yine yalnız Sahip inceleyip ekleyecek.
- Soru: Gösterge kodunu kim ekleyip etkinleştirebilir; kullanıcıdan gelen kod ve dosyalar doğrudan çalıştırılabilir mi?
- Önerilen varsayılan: Yalnız Sahip yayımlar; kullanıcı girdisi talep malzemesidir ve doğrudan çalıştırılmaz.

### Q-014 — Eksik veya gecikmiş piyasa verisinde ne yapılacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0045`
- Cevap: Yeni girişler hemen durdurulacak; eksik veri borsadan tamamlanıp doğrulanınca sistem otomatik devam edecek ve kullanıcıya bildirim gönderilecek.
- Soru: Canlı veri bağlantısı koptuğunda, sıra boşluğu, geç mum, saat farkı veya eski fiyat algılandığında strateji nasıl davranacak?
- Önerilen varsayılan: Güvenli duruş; aynı borsadan veri tamamlama ve doğrulama sonrası otomatik devam; kesinti/iyileşme bildirimi.

---

## C. Kıyaslama koşulları ve sinyal semantiği

### Q-015 — VE/VEYA gruplama ve öncelik nasıl olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0008`
- Cevap: İç içe koşul grupları/parantezler desteklenecek; her grup “TÜMÜ (AND)” veya “EN AZ BİRİ (OR)” operatörü kullanacak.
- Soru: Yalnızca düz bir koşul listesi mi, yoksa iç içe gruplar ve parantezler mi desteklenmeli? `A VE B VEYA C` nasıl yorumlanacak?
- Önerilen varsayılan: Açık koşul ağacı; grup bazlı ALL/ANY, UI'da parantezli özet.

### Q-016 — “Yukarı/Aşağı Keser” eşitliği nasıl ele alacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0046`
- Cevap: Her kesişme koşulunda eşitliğin dahil veya hariç olduğu kullanıcı tarafından seçilecek.
- Soru: Önceki ve güncel değerlerle kesişme hesaplanırken eşitlik geçerli taraf değişimi sayılacak mı?
- Önerilen varsayılan: Hazır seçim yok; kullanıcı Eşitlik Dahil veya Eşitlik Hariç seçer; veri adımı başına en fazla bir olay.

### Q-017 — “Yukarı Yönlü/Aşağı Yönlü” nasıl hesaplanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0047`
- Cevap: Son İki Değer, Art Arda Yön ve Dönemsel Değişim Eşiği yöntemleri ayrı seçenekler olarak desteklenecek.
- Soru: Yön yalnız son iki değere mi, seçilen sayıda ardışık harekete mi, yoksa dönem boyunca en az değişim yüzdesine mi göre belirlenecek?
- Önerilen varsayılan: Kullanıcı üç yöntemden birini ve yöntemin zorunlu alanlarını seçer; eşit değer yön üretmez.

### Q-018 — Koşul gerçekleştikten sonra yeniden tetikleme politikası nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Koşul true kaldığı her döngüde emir mi üretir, yalnızca false→true geçişinde mi, cooldown veya aynı sembolde tek pozisyon kuralı var mı?
- Önerilen varsayılan: Kenar tetikleme, sembol/strateji başına idempotent sinyal kimliği ve yapılandırılabilir cooldown.

### Q-019 — Fiyat ile kıyaslamada hangi fiyat kullanılacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Son işlem, mark, index, bid, ask, mid veya mum kapanışı mı?
- Önerilen varsayılan: İndikatör koşulunda ilgili kapanmış mumun close değeri; yürütmede yön bazlı gerçek order-book fiyatı.

### Q-020 — Çoklu zaman dilimleri nasıl hizalanacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Farklı periyotlarda iki indikatör karşılaştırılırsa hangi bar zamanında değerlendirme yapılacak ve look-ahead nasıl engellenecek?
- Önerilen varsayılan: Son ortak kapanmış zaman; yalnızca o anda bilinen değerlerle değerlendirme.

---

## D. Emir yürütme ve pozisyon yönetimi

### Q-021 — Belgede geçen üçüncü emir tipinin adı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0010`
- Cevap: “Geri Çekilme Limit Emri” ile gerçek “Stop-Limit Emir” iki ayrı seçenek olarak desteklenecek; “Tetikleme Sapması” ve belirsiz “Tetiklemeli Limit” adları kullanılmayacak.
- Soru: “Tetikleme Sapması” ile “Tetiklemeli Limit Order” aynı seçenek mi?
- Önerilen varsayılan: Tek ad: “Sinyal Fiyatından Sapmalı Limit Emir”.

### Q-022 — “Koşullar gerçekleştiği andaki gerçek tahta fiyatı” hangi fiyat?
- Durum: AÇIK
- Öncelik: P0
- Soru: Long için best ask, short için best bid, son işlem veya mid fiyat mı? Snapshot gecikmesi için tolerans nedir?
- Önerilen varsayılan: Yürütülebilir yön fiyatı (alış=best ask, satış=best bid), timestamp ve maksimum yaş kontrolüyle.

### Q-023 — Market emir kuralı gerçekten bekleyen bir fiyat filtresi mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0009`
- Cevap: Derhal gönderilen korumalı Market Emir ile fiyat koşulunu sonlu süre bekleyen Fiyat Korumalı Tetikleyici iki ayrı emir seçeneği olarak desteklenecek.
- Soru: Belgede Long için emir anı fiyatının sinyal fiyatına eşit/düşük, Short için eşit/yüksek olması bekleniyor. Koşul sağlanmazsa ne kadar beklenecek, sinyal ne zaman iptal olacak? Bu davranış market emrinden çok fiyat korumalı tetikleyiciye benziyor.
- Önerilen varsayılan: Maksimum bekleme süresi ve sapma toleranslı “protected market”; süre dolarsa iptal.

### Q-024 — Limit emir ne kadar açık kalacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: GTC/IOC/FOK seçenekleri, son kullanma süresi, yeniden fiyatlama ve iptal kuralları nedir?
- Önerilen varsayılan: Kullanıcı seçilebilir time-in-force; varsayılan GTC + açık süre limiti + alarm.

### Q-025 — Post-only emir reddedilirse ne olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Borsa emri piyasa alacak diye reddettiğinde iptal mi, bir tick geriden yeniden fiyatlama mı, post-only kapatma mı?
- Önerilen varsayılan: Otomatik taker emrine dönüşme yok; sınırlı yeniden fiyatlama veya iptal, ikisi de açık ayar.

### Q-026 — Kısmi dolumlar nasıl yönetilecek?
- Durum: AÇIK
- Öncelik: P0
- Soru: Kısmen dolan giriş/çıkış emrinde timeout, kalan miktar, TP/SL miktarı ve kullanıcı görünümü nasıl olacak?
- Önerilen varsayılan: Fill bazlı pozisyon muhasebesi; kalan miktar için açık politika; çıkışlar yalnızca gerçekleşmiş miktara göre.

### Q-027 — Emir tekrarları ve ağ hataları nasıl önlenecek?
- Durum: AÇIK
- Öncelik: P0
- Soru: Timeout sonrası emrin borsaya ulaşıp ulaşmadığı belirsizse nasıl mutabakat yapılacak?
- Önerilen varsayılan: Kalıcı clientOrderId/idempotency key, sorgula-uzlaştır, kör yeniden gönderme yapma.

### Q-028 — Spot işlemlerde satış/çıkış kapsamı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Spot “Long” yalnızca yeni alımı mı ifade eder; bot önceden elde bulunan varlığı satabilir mi; borçlu/margin spot tamamen kapsam dışı mı?
- Önerilen varsayılan: Yalnızca botun açtığı miktarı yönet; margin spot kapsam dışı.

### Q-029 — Futures pozisyon modu nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: One-way mi hedge mode mu? Aynı sembolde aynı anda Long ve Short tutulabilir mi?
- Önerilen varsayılan: MVP one-way; hedge mode sonraki faz.

### Q-030 — Marjin ve kaldıraç sınırları nasıl uygulanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Belgede 1–100 sabit aralık var; borsa/sembol/notional katmanına göre daha düşük maksimum varsa ne olacak?
- Önerilen varsayılan: UI ve sunucu etkin maksimumu borsa verisinden alır; sabit 100'e güvenmez.

### Q-031 — Pozisyon büyüklüğündeki “tutar” marjin mi, notional mı?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0005`
- Cevap: Kullanıcı Futures işlemlerde tutar türünü “Marjin Tutarı” veya “Notional Pozisyon Tutarı” olarak seçebilecek; sistem diğer değeri ve maliyetleri hesaplayıp gösterecek.
- Soru: Futures örneğinde 10 USDT × 5 = 50 USDT pozisyon deniyor. Cüzdandan 10 USDT marjin ayrılıp 50 USDT notional mı açılacak, yoksa 50 USDT cüzdandan mı düşecek?
- Önerilen varsayılan: Girilen tutar marjin; notional=tutar×kaldıraç; ücret ve rezerv ayrıca hesaba katılır.

### Q-032 — Yüzdelik boyutlandırma hangi bakiyeyi kullanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0006`
- Cevap: Kullanıcı yüzde hesabının tabanını “Toplam Bakiye”, “Kullanılabilir Bakiye” veya “Strateji Bütçesi” olarak seçebilecek.
- Soru: Toplam bakiye, kullanılabilir bakiye, serbest marjin veya belirlenmiş strateji bütçesi mi? Açık emir rezervleri düşülecek mi?
- Önerilen varsayılan: Stratejiye ayrılmış bütçe içindeki kullanılabilir bakiye; açık emirler ve güvenlik rezervi düşülür.

### Q-033 — Borsa miktar/fiyat kurallarında yuvarlama nasıl olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: tick size, step size, minimum quantity ve minimum notional için yönlü yuvarlama ve reddetme politikası nedir?
- Önerilen varsayılan: Decimal; riski artırmayacak yönde normalize et; minimumları karşılamıyorsa emir üretme ve açıklayıcı hata ver.

### Q-034 — Aynı sembolde birden fazla strateji nasıl etkileşecek?
- Durum: AÇIK
- Öncelik: P0
- Soru: Pozisyonlar borsa tarafında netleştiğinde strateji sahipliği, çıkış emri ve risk hesabı nasıl ayrılacak?
- Önerilen varsayılan: MVP'de hesap+ürün+sembol başına tek aktif strateji/pozisyon; daha sonra sanal lot muhasebesi.

### Q-035 — Strateji durdurma/silme/mod değiştirmede açık pozisyon ne olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Açık emirler iptal mi, pozisyon kapatılır mı, yönetim devam mı eder, kullanıcıya seçim mi sunulur?
- Önerilen varsayılan: Sessizce bırakma yok; kullanıcı açıkça “yalnız yeni girişleri durdur”, “emirleri iptal et ve yönetmeye devam et” veya “güvenli kapat” seçer.

---

## E. Take Profit, Stop Loss ve kademeli alım

### Q-036 — Kademeli TP yüzdeleri toplamı nasıl doğrulanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Kapanış dilimleri tam olarak %100 etmek zorunda mı; aynı kâr oranları ve sırasız hedefler kabul edilir mi?
- Önerilen varsayılan: Toplam tam %100; hedefler yön bazında monoton; miktarlar borsa adımına yuvarlanıp son dilim kalan miktarı kapatır.

### Q-037 — TP/SL hesaplaması hangi giriş fiyatını kullanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: İlk fill, ağırlıklı ortalama fill, kademeli alım sonrası yeni ortalama maliyet veya mark price mı?
- Önerilen varsayılan: Fill'lerden hesaplanan güncel ağırlıklı ortalama giriş; tetikleme fiyat kaynağı ürün türüne göre ayrıca tanımlanır.

### Q-038 — Trailing stop ne zaman aktive olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Pozisyon açılır açılmaz mı, belirli kâr eşiğinden sonra mı; callback oranı hangi fiyatı takip eder; borsanın native emri mi sunucu takibi mi?
- Önerilen varsayılan: Aktivasyon eşiği + callback oranı ayrı; mümkünse native koruma, değilse yüksek erişilebilir sunucu takibi.

### Q-039 — Kademeli alım tetikleri kümülatif mi?
- Durum: AÇIK
- Öncelik: P0
- Soru: Her kademe güncel ortalama maliyetin aynı zarar yüzdesinde mi, ilk girişten sabit seviyelerde mi tetiklenecek?
- Önerilen varsayılan: Belgede söylendiği gibi her dolumdan sonra güncellenen ortalama maliyete göre; seviyeler ve maksimum toplam exposure önceden gösterilir.

### Q-040 — Kademeli alımın maksimum risk sınırı nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Çarpan ve kademe sayısı geometrik büyümeyle bakiyeyi aşarsa ne olacak? Maksimum notional/marjin ve liquidation buffer nedir?
- Önerilen varsayılan: Önceden worst-case exposure hesapla; strateji/cüzdan limitini aşan ayarı kaydetme; hard liquidation-distance kontrolü.

### Q-041 — Stop loss ile kademeli alım birlikte kullanılabilir mi?
- Durum: AÇIK
- Öncelik: P0
- Soru: Belge üç seçeneği alternatif gösteriyor. Aynı stratejide kademeli alımdan sonra nihai stop loss zorunlu mu?
- Önerilen varsayılan: Kademeli alım tek başına sınırsız zarar koruması değildir; zorunlu nihai stop veya hard risk limiti ekle.

### Q-042 — Çıkış emirleri reduce-only olacak mı?
- Durum: AÇIK
- Öncelik: P0
- Soru: Futures TP/SL emirlerinin ters pozisyon açmasını nasıl engelleyeceğiz?
- Önerilen varsayılan: Tüm futures çıkışları reduce-only/close-position semantiğiyle ve gerçekleşmiş miktarla sınırlandırılır.

---

## F. PnL, ücretler ve risk

### Q-043 — Kâr/zarar oranının paydası nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0011`
- Cevap: Fiyat getirisi, brüt PnL, net PnL, kullanılan marjine göre ROE ve strateji sermayesine göre getiri ayrı hesaplanıp gösterilecek.
- Soru: Belgede fiyat değişimi yüzdesi kaldıraçla çarpılıyor. Gösterilecek getiri notional'a göre mi, başlangıç marjinine göre mi, yoksa toplam sermayeye göre mi?
- Önerilen varsayılan: Ayrı metrikler göster: fiyat getirisi, gerçekleşmiş PnL tutarı, kullanılan marjine göre ROE ve strateji sermayesine göre getiri.

### Q-044 — Komisyon, funding, slippage ve vergi nasıl ele alınacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0011`, `DEC-0012`
- Cevap: Net PnL komisyon, funding, slippage ve ilgili gerçekleşmiş maliyetleri içerecek; MVP ayrıca Türkiye'ye özel vergi raporu üretecek. Vergi raporunun resmî/bilgilendirme niteliği ve uzman onay süreci ayrıca kesinleştirilecek.
- Soru: Net PnL hesaplarında maker/taker ücretleri, funding, borç faizi ve gerçekleşen kayma dahil mi? Vergi raporu kapsamda mı?
- Önerilen varsayılan: Net PnL'a ücret/funding/slippage dahil; vergi tavsiyesi yok, yalnız dışa aktarılabilir işlem kaydı.

### Q-045 — Gerçekleşmemiş ve gerçekleşmiş PnL nasıl ayrılacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0021`
- Cevap: Her risk kuralında ölçüm kaynağı Realized Net PnL, Unrealized Net PnL veya Toplam Equity Değişimi olarak seçilebilecek.
- Soru: Açık ve kısmen kapanmış pozisyonlarda rapor ve limit hesapları hangi değerleri kullanacak?
- Önerilen varsayılan: Realized/unrealized ayrı; risk limitleri için ikisini içeren equity drawdown ve ayrıca realized günlük zarar.

### Q-046 — Risk limitlerinin kapsamı nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0016`
- Cevap: Kullanıcı her risk limiti için kapsamı Global, borsa hesabı, strateji veya sembol seviyesinde seçebilecek; çakışan limitlerde en sıkı olan uygulanacak. Platform hard cap'leri atlanamayacak.
- Soru: Maksimum eşzamanlı işlem ve zarar limitleri kullanıcı, borsa hesabı, strateji veya tüm sistem seviyesinde mi?
- Önerilen varsayılan: Global hard limit + hesap ve strateji alt limitleri; en dar limit kazanır.

### Q-047 — Zarar limiti aşılınca tam olarak ne olur?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0017`
- Cevap: Her risk kuralında “Uyar”, “Yeni Girişleri Durdur”, “Bekleyen Giriş Emirlerini İptal Et” veya “Pozisyonları Acil Kapat” aksiyonu seçilebilecek. Platform hard limitleri minimum güvenli aksiyonu zorunlu kılabilecek.
- Soru: Yalnız yeni girişler mi durur, açık emirler iptal mi, pozisyonlar otomatik kapanır mı? Manuel yeniden başlatma mı gerekir?
- Önerilen varsayılan: Yeni girişleri durdur, bekleyen girişleri iptal et, koruyucu çıkış yönetimini sürdür, alarm üret; otomatik piyasa kapatma ayrı acil politika.

### Q-048 — Günlük/haftalık/aylık limitlerin sıfırlanması nasıl olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0018`
- Cevap: Her risk kuralında Takvim Penceresi veya Kayan Pencere ile IANA saat dilimi seçilebilecek; takvim haftası başlangıcı ve kayan süre açıkça yapılandırılacak.
- Soru: Europe/Istanbul takvim dönemi mi, kayan pencere mi? Dönem başı equity nasıl sabitlenecek?
- Önerilen varsayılan: Europe/Istanbul takvim dönemleri; dönem başı equity snapshot; transferler PnL'dan ayrılır.

### Q-049 — Maksimum drawdown ve liquidation güvenliği eklensin mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0019`
- Cevap: Maksimum Drawdown ve Liquidation Mesafesi kuralları kullanıcı tarafından açılıp kapatılabilecek; varsayılan aktif olacak. Platformun atlanamayan hard safety cap'leri ayrı kalacak.
- Soru: Belgede doğrudan yer almıyor. Peak equity drawdown, maksimum hesap kullanımı ve liquidation mesafesi limitleri zorunlu olacak mı?
- Önerilen varsayılan: Evet; canlı modun zorunlu hard limitleri.

### Q-050 — Fiyat sapması ve spread limiti eklensin mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0020`
- Cevap: Maksimum spread ve slippage/fiyat sapması limitleri varsayılan aktif olacak; kullanıcı uyarı/MFA/audit ile kapatabilecek. Borsa ve platform hard fiyat/veri güvenliği ayrı kalacak.
- Soru: Sinyalden yürütmeye kadar maksimum slippage/spread aşıldığında emir iptal edilmeli mi?
- Önerilen varsayılan: Evet; sembol/strateji bazlı maksimum bps toleransı.

---

## G. Simülasyon, backtest ve strateji yaşam döngüsü

### Q-051 — Deneme benzetiminde emir gerçekleşmesi ne kadar gerçekçi olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0023`
- Cevap: Kullanıcı Temel, Orta veya İleri benzetim düzeyini kendisi seçebilecek. Sonuçlarda seçilen düzey ve kullanılan varsayımlar açıkça gösterilecek.
- Soru: Yalnız son fiyatın emre dokunması yeterli mi; piyasa derinliği, gecikme, emrin parça parça gerçekleşmesi, emir sırası, işlem ücreti ve fiyat kayması hesaba katılmalı mı?
- Önerilen varsayılan: Orta düzey; alış-satış fiyatları, işlem ücreti, fiyat kayması, piyasa derinliği, gecikme ve parçalı gerçekleşme hesaba katılır.

### Q-052 — Geçmiş piyasa verileriyle sınama eklensin mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0024`
- Cevap: İlk sürümde ayrıntılı geçmiş veri sınaması bulunacak.
- Soru: Strateji geçmiş veriler üzerinde çalıştırılsın mı; farklı dönemlerde tekrar sınama, alışılmamış piyasa koşulları ve ayrıntılı başarı/risk raporu isteniyor mu?
- Önerilen varsayılan: Evet; ilk sürümde ayrıntılı geçmiş veri sınaması ve açık varsayım raporu.

### Q-053 — Strateji düzenlenirken çalışan sürüm ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0014`
- Cevap: Her düzenleme yeni değişmez sürüm oluşturacak; kaydederken “Yalnız Yeni İşlemler” veya “Eski Pozisyonlara Uygula” seçilebilecek. Eski pozisyon uygulaması yalnız güvenli ve ileriye dönük yönetim ayarlarını kontrollü migrate edecek.
- Soru: Ayarlar anında çalışan örneğe mi uygulanacak, yoksa yeni sürüm oluşturulup kontrollü yeniden başlatma mı yapılacak?
- Önerilen varsayılan: Immutable strategy version; kaydetme yeni taslak/sürüm üretir, explicit activate ile devreye alınır.

### Q-054 — Testten gerçeğe geçişte hangi kontroller zorunlu?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0015`
- Cevap: Zorunlu paper süresi/işlem sayısı/performans eşiği olmayacak; kullanıcı risk uyarısı ve MFA sonrası istediği zaman canlıya geçebilecek. Atlanamayan teknik güvenlik ve risk kontrolleri yine zorunlu olacak.
- Soru: Minimum test süresi/işlem sayısı, max drawdown, API yetkisi, bakiye, açık emir ve risk kontrolü eşikleri nedir?
- Önerilen varsayılan: Sunucu taraflı checklist, 2FA/re-auth, özet risk ekranı, yazılı onay ve başlangıçta capped pilot.

### Q-055 — Kopyalanan stratejinin geçmişi nasıl davranacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Ayarlar kopyalanırken işlem istatistikleri sıfırdan mı başlamalı? İsim çakışmaları nasıl çözülmeli?
- Önerilen varsayılan: Yeni kimlik ve sıfır istatistik; güvenli benzersiz ad; her zaman taslak/test modu.

### Q-056 — Strateji silme soft-delete mi olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Denetim ve işlem geçmişi için kayıt korunacak mı? Açık pozisyon varken silmeye izin verilecek mi?
- Önerilen varsayılan: Soft-delete/arşiv; işlem/audit geçmişi korunur; açık risk çözülmeden kalıcı silme yok.

---

## H. Güvenlik, gözlemlenebilirlik ve operasyon

### Q-057 — API anahtarları nerede ve nasıl saklanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Hosting sağlayıcının secret manager'ı mı, şifreli veritabanı mı? Ana şifre/KMS nerede olacak?
- Önerilen varsayılan: Platform secret manager/KMS; veritabanında yalnız şifreli değer; log ve Git'te asla secret yok.

### Q-058 — Borsa anahtarı izin politikası nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Trade-only, IP allowlist ve sub-account zorunlu mu?
- Önerilen varsayılan: Para çekme kapalı, yalnız gereken ürünlerde işlem, IP allowlist, mümkünse ayrı sub-account.

### Q-059 — Canlı moda geçişte UI dışında hangi güvenlik olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Toggle tek başına yeterli mi; 2FA, tekrar parola, yazılı risk özeti ve bekleme süresi gerekli mi?
- Önerilen varsayılan: Toggle yalnız talep oluşturur; sunucu doğrulaması + re-auth/2FA + açık onay olmadan aktif olmaz.

### Q-060 — Bildirim kanalları neler olacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Telegram, e-posta veya web push ile hangi olaylar bildirilecek?
- Önerilen varsayılan: Telegram + uygulama içi; emir/fill, hata, veri kesintisi, limit ihlali, live mode ve kill switch olayları.

### Q-061 — Audit log kapsamı ve saklama süresi nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Ayar değişiklikleri, girişler, anahtar işlemleri, mod değişimleri, sinyal/emir kararları ve manuel müdahaleler kaç yıl saklanacak?
- Önerilen varsayılan: Append-only audit; hassas veri maskeli; süre hukuki/operasyonel gereksinime göre, ilk varsayım 1 yıl.

### Q-062 — Veri saklama ve silme politikası nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Mum/tick/order-book, strateji, işlem ve kullanıcı verileri ne kadar tutulacak?
- Önerilen varsayılan: Veri sınıfı bazlı süre; ham yüksek frekans verisi kısa, işlem/audit verisi uzun; kullanıcı talebi ve yasal yükümlülükler belgelenir.

### Q-063 — Yedekleme ve felaket kurtarma hedefleri nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Kabul edilen veri kaybı (RPO) ve hizmet dönüş süresi (RTO) nedir?
- Önerilen varsayılan: Günlük şifreli tam + sık artımlı yedek; düzenli restore testi; canlı işlemde RPO/RTO daha sıkı.

### Q-064 — Sistem yeniden başlarken nasıl uzlaşacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Açık emir/pozisyonlar borsadan çekilip yerel durumla uyuşmazsa hangi kaynak kazanacak?
- Önerilen varsayılan: Borsa execution gerçeği kazanır; strateji sahipliği ve audit ile reconcile; belirsizlikte yeni emir fail-closed.

### Q-065 — Kill switch kapsamı nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Global, hesap, borsa ve strateji bazlı düğmeler olacak mı; açık pozisyonu kapatmak ayrı seçenek mi?
- Önerilen varsayılan: Katmanlı kill switch; “yeni girişi durdur” ile “acil kapat” ayrı ve açıkça etiketli.

### Q-066 — İzleme/SLO hedefleri nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Veri gecikmesi, emir gecikmesi, hata oranı, bakiye mutabakatı ve uptime için eşikler nedir?
- Önerilen varsayılan: İlk yük testlerinden sonra ölçülebilir SLO; kritik alarm Telegram'a.

---

## I. UX, raporlama ve mevzuat

### Q-067 — Mobil ve erişilebilirlik kapsamı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Responsive mobil web, klavye erişimi ve WCAG seviyesi gerekli mi?
- Önerilen varsayılan: Responsive web + temel WCAG 2.1 AA.

### Q-068 — Taslak ve otomatik kaydetme olacak mı?
- Durum: AÇIK
- Öncelik: P1
- Soru: Sekmeler arası state korunmasına ek olarak tarayıcı kapanması/oturum süresi dolmasında taslak kurtarılacak mı?
- Önerilen varsayılan: Sunucu taraflı sürümlü taslak + belirgin kaydedildi durumu.

### Q-069 — Rapor dışa aktarma gerekli mi?
- Durum: AÇIK
- Öncelik: P1
- Soru: İşlemler ve PnL CSV/Excel/PDF olarak dışa aktarılacak mı?
- Önerilen varsayılan: CSV MVP; diğer formatlar sonraki faz.

### Q-070 — Grafik sağlayıcısı ve veri lisansı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: TradingView bileşeni mi, açık kaynak grafik mi; ticari kullanım/lisans koşulları kabul ediliyor mu?
- Önerilen varsayılan: Lisansı doğrulanmış açık kaynak grafik; TradingView kullanılacaksa lisans kararı kaydedilir.

### Q-071 — Ürün kişisel araç mı, üçüncü kişilere hizmet mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0003`
- Cevap: MVP tek kullanıcıyla başlayacak; uzun vadede kullanıcıların kendi borsa hesaplarını bağladığı abonelik/SaaS ürünü olacak. Platform kullanıcı fonlarını saklamayacak ve para çekme yetkisi almayacak.
- Soru: Başkaları adına işlem, sinyal satışı, saklama/custody veya fon yönetimi hedefleniyor mu?
- Önerilen varsayılan: Yalnız kullanıcının kendi hesabında kişisel araç; üçüncü kişi fonu/saklama/yatırım tavsiyesi kapsam dışı.

### Q-072 — Risk açıklaması ve kullanım koşulları gerekli mi?
- Durum: AÇIK
- Öncelik: P1
- Soru: İnternete açık/çok kullanıcılı üründe kullanıcı sözleşmesi, gizlilik politikası, risk bildirimi ve mevzuat incelemesi yapılacak mı?
- Önerilen varsayılan: Çok kullanıcılı veya ticari yayından önce hukuk uzmanı incelemesi zorunlu.

---

## J. Strateji yaşam döngüsü, validasyon ve performans

### Q-073 — Strateji kaydedildiğinde çalışma nasıl başlatılacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0025`
- Cevap: Kaydederken “Taslak Olarak Kaydet” veya “Kaydet ve Başlat” seçenekleri sunulacak. Başlatma, zorunlu doğrulamalar geçildikten sonra gerçekleşecek.
- Soru: Kaydetmek yalnız taslak mı oluşturur, yoksa kullanıcı isterse aynı işlemde stratejiyi başlatabilir mi?
- Önerilen varsayılan: İki ayrı seçenek; Taslak Olarak Kaydet ve Kaydet ve Başlat.

### Q-074 — Strateji adı kuralları nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0028`
- Cevap: Her kullanıcının strateji adları benzersiz olacak; aynı ad ikinci kez kullanılamayacak.
- Soru: Aynı kullanıcıda ad benzersiz mi, uzunluk/karakter sınırı ne, büyük-küçük harf duyarlı mı? Kopya adı nasıl üretilir?
- Önerilen varsayılan: Kullanıcı içinde büyük-küçük harfe duyarsız benzersiz ad; boşluklar düzeltilir; kopyaya benzersiz sayı eklenir.

### Q-075 — Borsa veya işlem türü değişince bağlı ayarlar ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0029`
- Cevap: Değişiklikten önce etkilenecek ayarlar kullanıcıya gösterilecek; kullanıcı onayladığında uyumsuz ayarlar temizlenecek.
- Soru: Eski işlem çifti, emir türü, marjin, kaldıraç, yön ve borsaya özel ayarlar sessizce korunacak mı, sıfırlanacak mı?
- Önerilen varsayılan: Önce etki özeti ve onay; yalnız uyumsuz alanlar temizlenir, çalışan stratejide yeni sürüm oluşur.

### Q-076 — Riskli alanların hazır değerleri ve gerçek mod denetimi nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0030`
- Cevap: Pozisyon tutarı, kaldıraç, zarar durdurma ve risk sınırları boş gelecek; kullanıcı bu alanları zorunlu olarak dolduracak.
- Soru: Sistem kullanıcı adına pozisyon tutarı, kaldıraç, zarar durdurma veya risk sınırı seçmeli mi? Gerçek modda hangi alanlar boş bırakılamaz?
- Önerilen varsayılan: Riskli finansal alanlarda hazır değer yok; kullanıcı açıkça girer ve sunucu tarafı denetimden geçer.

### Q-077 — Başarı ve risk ölçümlerinin kesin kapsamı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0031`
- Cevap: Net kâr/zarar, başarı oranı, işlem sayısı, sermayenin en yüksek noktadan düşüşü, kazanç-kayıp oranı, ortalama işlem sonucu, ücretler, fonlama maliyeti, açık kalma süresi ve art arda kayıplar gösterilecek.
- Soru: Sonuç ekranında hangi ölçümler zorunlu olacak ve bunların dönem/para birimi/işlem kümesi nasıl belirtilecek?
- Önerilen varsayılan: Ayrıntılı ölçüm kümesi; hesaplama kapsamı ve yöntemi her raporda açıkça belirtilir.

### Q-078 — Emir işlem aşamaları nasıl kaydedilip gösterilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0032`
- Cevap: Sistem bütün ayrıntılı emir aşamalarını kaydedecek; ana ekranda sade durum, ayrıntı sayfasında tüm aşamalar gösterilecek.
- Soru: Gönderilmeden önceki hazırlık, borsa kabulü, parçalı gerçekleşme, iptal bekleme, ret, zaman aşımı ve durumu araştırma ayrı tutulacak mı?
- Önerilen varsayılan: Ayrıntılı iç kayıt; ana ekranda sade özet, ayrıntıda zaman sıralı tam geçmiş.

### Q-079 — Koruyucu emirler borsada mı, sistemde mi tutulacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0033`
- Cevap: Öncelik borsadaki koruyucu emirler olacak; borsa desteklemiyorsa açık kesinti uyarısıyla sistem tarafından takip seçeneği sunulacak.
- Soru: Kâr alma ve zarar durdurma emirleri mümkün olduğunda doğrudan borsaya mı yerleştirilecek? Destek yoksa gerçek işlem engellenecek mi, sistem takibi seçilebilir mi?
- Önerilen varsayılan: Önce borsa; destek yoksa kullanıcı açıkça onaylarsa yüksek görünürlüklü sistem takibi.

### Q-080 — Geçmiş sınama, deneme ve gerçek işlem sonuçları ayrı mı tutulacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0034`
- Cevap: Üç sonuç türü kesin biçimde ayrı tutulacak; kullanıcı isterse yan yana karşılaştırabilecek.
- Soru: Geçmiş sınama, sanal bakiyeyle deneme ve gerçek para sonuçları tek toplamda birleşecek mi?
- Önerilen varsayılan: Ayrı kayıt ve rapor; aynı dönem/sürüm için yan yana karşılaştırma, birleşik finansal toplam yok.

### Q-081 — İlk sürümün işlem hızı sınıfı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0035`
- Cevap: İlk sürüm normal hızda olacak; yüksek hızlı işlemler daha sonra ayrı bir çalışma olarak eklenecek.
- Soru: İlk sürüm 1 dakika ve üzeri strateji aralıklarına mı odaklanacak, yoksa saniyenin çok küçük bölümlerinde emir yarışına dayalı yüksek hızlı işlemler mi hedeflenecek?
- Önerilen varsayılan: İlk sürüm normal hız ve güvenilirlik odaklı; yüksek hız sonraki sürüm kapsamı.

### Q-082 — Sinyal verisi ile emir borsası aynı mı olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0036`
- Cevap: Sinyal ve emir aynı borsada olacak.
- Soru: Fiyat ve gösterge verisi bir borsadan alınırken emir başka bir borsaya gönderilebilecek mi?
- Önerilen varsayılan: Hayır; her stratejide piyasa verisi, gösterge hesabı ve emir yürütme aynı borsa/ürün/işlem çifti kaynağına bağlıdır.

### Q-083 — İlk sürümün hedef çalışma ölçeği nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0037`
- Cevap: Geniş kişisel kullanım hedeflenecek: 1 kullanıcı, en fazla 50 çalışan strateji ve strateji başına 200 işlem çifti.
- Soru: İlk sürüm aynı anda kaç kullanıcı, çalışan strateji ve strateji başına kaç işlem çiftini desteklemeli?
- Önerilen varsayılan: 1 kullanıcı; 50 çalışan strateji; strateji başına 200 işlem çifti; ortak piyasa verisi bağlantıları paylaşılır.

### Q-084 — “Neden işlem açılmadı?” kaydı ne zaman tutulacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0038`
- Cevap: Yalnız sinyal oluştuğu hâlde risk, bakiye, borsa, veri veya emir kuralı nedeniyle açılamayan işlemler saklanacak.
- Soru: Her gösterge değerlendirmesi mi, yoksa yalnız geçerli giriş sinyali sonrasındaki engelleme nedenleri mi kaydedilecek?
- Önerilen varsayılan: Sinyal sonrası engellemeler neden kodu ve karar anı özetiyle saklanır; her başarısız koşul hesabı süresiz tutulmaz.

### Q-085 — Açık ve kısmi işlemler ayrıntı sayfasında nasıl gösterilecek?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0039`
- Cevap: Her işlem tek özet satırında gösterilecek; açıldığında giriş ve çıkış gerçekleşmeleri alt satırlarda görülecek.
- Soru: Açık, kısmen gerçekleşmiş ve kapanmış işlemlerde özet, emirler ve her gerçekleşme nasıl sıralanmalı?
- Önerilen varsayılan: İşlem özet satırı + açılır zaman sıralı giriş/çıkış gerçekleşme alt satırları; kalan miktar ve kâr-zarar ayrımı görünür.

### Q-086 — Türkiye vergi raporunun hukuki niteliği nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0013`
- Cevap: MVP raporu bilgilendirme ve mali müşavir çalışma dosyası niteliğinde olacak; resmî beyanname veya vergi tavsiyesi olarak sunulmayacak.
- Soru: Rapor yalnız bilgilendirme/mali müşavire veri hazırlama amacıyla mı, yoksa uzman onayından sonra beyanname hazırlığına doğrudan esas olacak doğrulanmış rapor olarak mı hedefleniyor?
- Önerilen varsayılan: MVP'de bilgilendirme ve mali müşavir çalışma dosyası; uzman tarafından onaylanmış kural seti olmadan resmî beyanname iddiası yok.

### Q-087 — Duraklatma ve durdurma sırasında emirler ve açık işlemler ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0026`
- Cevap: Duraklatma yeni girişleri durduracak ve bekleyen giriş emirlerini iptal edecek; açık işlemlerin kâr alma ve zarar durdurma korumaları devam edecek. Durdururken kullanıcı açık işlemleri korumayı veya kapatmayı seçecek.
- Soru: Duraklatma ve durdurma sırasında yeni sinyaller, bekleyen giriş emirleri, açık işlemler ve koruyucu çıkış emirleri ne olacak?
- Önerilen varsayılan: Duraklatma yeni girişleri keser ve koruyucu yönetimi sürdürür; durdurma için kullanıcı açık işlemleri koru veya kapat seçer.

### Q-088 — Sunucu yeniden başladığında çalışan stratejiler nasıl devam edecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0027`
- Cevap: Deneme modundaki stratejiler kayıtlı durumdan otomatik devam edecek. Gerçek moddakiler borsa hesabı karşılaştırıldıktan sonra kullanıcı onayı bekleyecek.
- Soru: Deneme ve gerçek moddaki stratejiler sunucu yeniden açıldığında otomatik devam mı etmeli, yoksa emirler, işlemler ve bakiyeler borsayla karşılaştırılıp kullanıcı onayı mı beklenmeli?
- Önerilen varsayılan: Deneme modu kayıtlı durumdan devam eder; gerçek modda borsa hesabı karşılaştırması ve kullanıcı onayı tamamlanmadan yeni giriş üretilmez.

### Q-089 — İlk sürümün sayısal hız ve hizmet sürekliliği sınırları nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Gerçek hosting ve Binance/MEXC denemelerinde kabul edilecek en yüksek piyasa verisi yaşı, sinyal hesaplama süresi, sistem içi emir hazırlama süresi, borsa yanıt bekleme süresi ve aylık hizmet sürekliliği hedefleri ne olmalı?
- Önerilen varsayılan: Önce ölçüm yapılır; normal hız kapsamına uygun gerçekçi sınırlar ölçüm sonuçlarıyla önerilir ve canlı işlem açılmadan önce kullanıcı tarafından ayrıca onaylanır. Eski veri güvenlik sınırı performans hedefinden bağımsız ve atlanamaz olur.

### Q-090 — Oturum süresi ve hassas işlemlerde yeniden doğrulama nasıl olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0042`
- Cevap: Oturum kullanıcı tarayıcıyı kapatana kadar açık kalacak; yalnız hassas işlemlerde yeniden güçlü doğrulama istenecek.
- Soru: Oturum ne zaman sona erecek ve hangi işlemler yeni doğrulama gerektirecek?
- Önerilen varsayılan: Kalıcı olmayan tarayıcı oturumu; para/güvenlik etkili işlemlerde yakın zamanda yapılmış güçlü doğrulama zorunlu.

### Q-091 — Gelecekteki çok kullanıcılı sürümde roller nasıl ayrılacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0043`
- Cevap: Sahip rolü sabit olacak; diğer roller sayfa ve işlem yetkileri seçilerek özel oluşturulabilecek.
- Soru: Çok kullanıcılı sürümde hangi yetkiler sabit sahip rolünde kalacak, özel roller hangi sayfa ve işlemlere erişebilecek?
- Önerilen varsayılan: Tek sabit Sahip; diğer roller en az yetki ilkesiyle seçilebilir izinlerden oluşur.

---

## Önce cevaplanacak karar sırası

1. Q-001 — Tek kullanıcı mı, SaaS mı?
2. Q-003 — İlk borsa ve ürünler
3. Q-071 — Kişisel araç mı, üçüncü kişilere hizmet mi?
4. Q-002 — Dağıtım/erişim modeli
5. Q-031 — Futures tutarının marjin/notional anlamı
6. Q-010 — Kapanmış mum/intrabar sinyali
7. Q-015 — Koşul gruplama modeli
8. Q-023 — Market emir fiyat filtresi
9. Q-043 — PnL metriklerinin tanımı
10. Q-053/Q-054 — Strateji sürümü ve canlı moda geçiş
