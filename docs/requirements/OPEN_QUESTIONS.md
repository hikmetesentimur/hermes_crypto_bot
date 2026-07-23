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

### Q-004 — Testnet/sandbox ve canlı hesap sırası nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Geliştirme ve kabul testleri hangi borsanın testnet/sandbox ortamında yapılacak?
- Önerilen varsayılan: Önce yerel simülasyon, sonra Binance testnet, en son limitli canlı pilot.

### Q-005 — Kullanıcı, rol ve oturum modeli nasıl olmalı?
- Durum: AÇIK
- Öncelik: P0
- Soru: Tek kullanıcıda bile parola, 2FA, oturum süresi ve yeniden doğrulama gerekecek mi? Çok kullanıcıda admin/operatör/izleyici rolleri olacak mı?
- Önerilen varsayılan: Parola + TOTP 2FA; canlı mod ve anahtar değişiminde yeniden doğrulama.

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

### Q-013 — İndikatör eklenti şeması nasıl tanımlanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: `settings.py` ve `parameters.py` içeriğinin güvenli, tipli ve UI tarafından okunabilir sözleşmesi nedir?
- Önerilen varsayılan: Çalıştırılabilir Python dosyasını UI'dan doğrudan keşfetmek yerine sürümlü JSON/Pydantic şeması ve kayıtlı plugin manifesti.

### Q-014 — Eksik/gecikmiş piyasa verisinde davranış nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: WebSocket kopması, sıra boşluğu, geç gelen mum, saat farkı veya stale fiyat halinde strateji duracak mı?
- Önerilen varsayılan: Fail-closed; yeni emirleri durdur, REST ile yeniden eşleştir, veri güncelliği doğrulanınca devam et ve alarm üret.

---

## C. Kıyaslama koşulları ve sinyal semantiği

### Q-015 — VE/VEYA gruplama ve öncelik nasıl olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0008`
- Cevap: İç içe koşul grupları/parantezler desteklenecek; her grup “TÜMÜ (AND)” veya “EN AZ BİRİ (OR)” operatörü kullanacak.
- Soru: Yalnızca düz bir koşul listesi mi, yoksa iç içe gruplar ve parantezler mi desteklenmeli? `A VE B VEYA C` nasıl yorumlanacak?
- Önerilen varsayılan: Açık koşul ağacı; grup bazlı ALL/ANY, UI'da parantezli özet.

### Q-016 — “Yukarı/Aşağı Keser” tam olarak ne zaman true olur?
- Durum: AÇIK
- Öncelik: P0
- Soru: Önceki ve güncel kapanmış mum değerleriyle tek olay mı üretir; eşitlik nasıl ele alınır?
- Önerilen varsayılan: Önceki ve güncel kapanmış bar üzerinden formal iki-nokta tanımı; bar başına en fazla bir olay.

### Q-017 — “Yukarı Yönlü/Aşağı Yönlü” nasıl tanımlanacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Bir önceki değere göre artış/azalış mı, belirli sayıda ardışık bar mı, yoksa eğim eşiği mi?
- Önerilen varsayılan: Parametreli lookback ve minimum eğim; varsayılan 1 kapanmış bar kıyası.

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
- Durum: AÇIK
- Öncelik: P0
- Soru: Belgede fiyat değişimi yüzdesi kaldıraçla çarpılıyor. Gösterilecek getiri notional'a göre mi, başlangıç marjinine göre mi, yoksa toplam sermayeye göre mi?
- Önerilen varsayılan: Ayrı metrikler göster: fiyat getirisi, gerçekleşmiş PnL tutarı, kullanılan marjine göre ROE ve strateji sermayesine göre getiri.

### Q-044 — Komisyon, funding, slippage ve vergi nasıl ele alınacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Net PnL hesaplarında maker/taker ücretleri, funding, borç faizi ve gerçekleşen kayma dahil mi? Vergi raporu kapsamda mı?
- Önerilen varsayılan: Net PnL'a ücret/funding/slippage dahil; vergi tavsiyesi yok, yalnız dışa aktarılabilir işlem kaydı.

### Q-045 — Gerçekleşmemiş ve gerçekleşmiş PnL nasıl ayrılacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Açık ve kısmen kapanmış pozisyonlarda rapor ve limit hesapları hangi değerleri kullanacak?
- Önerilen varsayılan: Realized/unrealized ayrı; risk limitleri için ikisini içeren equity drawdown ve ayrıca realized günlük zarar.

### Q-046 — Risk limitlerinin kapsamı nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Maksimum eşzamanlı işlem ve zarar limitleri kullanıcı, borsa hesabı, strateji veya tüm sistem seviyesinde mi?
- Önerilen varsayılan: Global hard limit + hesap ve strateji alt limitleri; en dar limit kazanır.

### Q-047 — Zarar limiti aşılınca tam olarak ne olur?
- Durum: AÇIK
- Öncelik: P0
- Soru: Yalnız yeni girişler mi durur, açık emirler iptal mi, pozisyonlar otomatik kapanır mı? Manuel yeniden başlatma mı gerekir?
- Önerilen varsayılan: Yeni girişleri durdur, bekleyen girişleri iptal et, koruyucu çıkış yönetimini sürdür, alarm üret; otomatik piyasa kapatma ayrı acil politika.

### Q-048 — Günlük/haftalık/aylık limitlerin sıfırlanması nasıl olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Europe/Istanbul takvim dönemi mi, kayan pencere mi? Dönem başı equity nasıl sabitlenecek?
- Önerilen varsayılan: Europe/Istanbul takvim dönemleri; dönem başı equity snapshot; transferler PnL'dan ayrılır.

### Q-049 — Maksimum drawdown ve liquidation güvenliği eklensin mi?
- Durum: AÇIK
- Öncelik: P0
- Soru: Belgede doğrudan yer almıyor. Peak equity drawdown, maksimum hesap kullanımı ve liquidation mesafesi limitleri zorunlu olacak mı?
- Önerilen varsayılan: Evet; canlı modun zorunlu hard limitleri.

### Q-050 — Fiyat sapması ve spread limiti eklensin mi?
- Durum: AÇIK
- Öncelik: P0
- Soru: Sinyalden yürütmeye kadar maksimum slippage/spread aşıldığında emir iptal edilmeli mi?
- Önerilen varsayılan: Evet; sembol/strateji bazlı maksimum bps toleransı.

---

## G. Simülasyon, backtest ve strateji yaşam döngüsü

### Q-051 — Simülasyon dolum modeli ne kadar gerçekçi olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Last price dokunması yeterli mi; order-book, gecikme, kısmi fill, maker queue, ücret ve slippage modellenmeli mi?
- Önerilen varsayılan: MVP'de muhafazakâr bid/ask + ücret + slippage + kısmi fill modeli; sonuçlarda simülasyon varsayımları açıkça gösterilir.

### Q-052 — Tarihsel backtest eklensin mi?
- Durum: AÇIK
- Öncelik: P1
- Soru: Belgede yalnız canlı piyasa verili test modu var. Stratejiyi geçmiş veride çalıştırma, walk-forward ve performans raporu isteniyor mu?
- Önerilen varsayılan: Evet; canlı pilot öncesi zorunlu fakat MVP'nin ilk dikey diliminden sonra.

### Q-053 — Strateji düzenlenirken çalışan sürüm ne olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Ayarlar anında çalışan örneğe mi uygulanacak, yoksa yeni sürüm oluşturulup kontrollü yeniden başlatma mı yapılacak?
- Önerilen varsayılan: Immutable strategy version; kaydetme yeni taslak/sürüm üretir, explicit activate ile devreye alınır.

### Q-054 — Testten gerçeğe geçişte hangi kontroller zorunlu?
- Durum: AÇIK
- Öncelik: P0
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

### Q-073 — Strateji yaşam döngüsü nasıl olacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Kaydetmek stratejiyi yalnız taslak mı yapar? Ayrı Başlat, Duraklat, Durdur ve Arşivle eylemleri olacak mı? Restart sonrası otomatik devam edilecek mi?
- Önerilen varsayılan: Taslak → Doğrulanıyor → Hazır → Çalışıyor ↔ Duraklatıldı → Durduruldu/Arşivlendi; hata durumu ayrı; restart sonrası canlı strateji fail-closed ve mutabakat/onay sonrası devam.

### Q-074 — Strateji adı kuralları nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Ad zorunlu ve kullanıcı/borsa kapsamında benzersiz mi; uzunluk/karakter sınırı nedir?
- Önerilen varsayılan: Zorunlu, trim edilmiş 3–80 karakter; kullanıcı kapsamında case-insensitive benzersiz; kopya adına güvenli sıra numarası eklenir.

### Q-075 — Borsa veya işlem tipi değişince bağımlı alanlar ne olacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Önceki quote asset, sembol, yön, marjin, kaldıraç ve boyut ayarları otomatik temizlenecek mi?
- Önerilen varsayılan: Geçersiz hale gelen alanlar atomik sıfırlanır; kullanıcıya değişiklik özeti gösterilir; sessizce eski değer kullanılmaz.

### Q-076 — Varsayılan değerler ve canlı mod validasyonu nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Mod, yön, marjin, kaldıraç, emir, TP/SL ve risk alanlarının başlangıç değerleri ne olacak? Canlı modda stop/risk alanları boş bırakılabilir mi?
- Önerilen varsayılan: Paper mode; Spot/Long; kaldıraç 1; canlı modda pozisyon/risk hard cap ve koruyucu çıkış zorunlu; boş değer sınırsız sayılmaz.

### Q-077 — Performans istatistiklerinin kesin tanımı nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Kısmi kapanış, break-even, komisyon sonrası sonuç, test/live ayrımı, strateji düzenleme ve kopyalama sayaçları nasıl ele alınacak?
- Önerilen varsayılan: İşlem kapanışı position lifecycle bazlı; net PnL sonrası kârlı/zararlı/break-even ayrı; paper/live kesin ayrılır; yeni strateji sürümü aynı strateji ailesinde fakat sürüm bazlı raporlanır; kopya sıfırdan başlar.

### Q-078 — Emir durum makinesi hangi durumları destekleyecek?
- Durum: AÇIK
- Öncelik: P0
- Soru: Created, risk-approved, submitting, acknowledged, partial, filled, cancel-pending, cancelled, rejected, expired ve unknown durumları ile geçiş/retry kuralları onaylanıyor mu?
- Önerilen varsayılan: Bu durumların tamamı kalıcı state machine; bilinmeyen durumda yeni emir yok, önce reconcile.

### Q-079 — Koruyucu emirler borsada native mi tutulacak?
- Durum: AÇIK
- Öncelik: P0
- Soru: Borsa desteklediğinde TP/SL/OCO/bracket ve reduce-only kullanılacak mı? Native destek yoksa yalnız site takibine izin verilecek mi?
- Önerilen varsayılan: Native koruma öncelikli; destek yoksa bu sınırlama açıkça gösterilir, yüksek erişilebilir takip ve acil politika olmadan live'a izin verilmez.

### Q-080 — Test ve canlı istatistikleri tamamen ayrı mı tutulacak?
- Durum: AÇIK
- Öncelik: P1
- Soru: Aynı strateji mod değiştirdiğinde geçmiş paper işlemleri canlı performans özetine dahil edilecek mi?
- Önerilen varsayılan: Hayır; paper/backtest/live portföyleri ve performans metrikleri ayrı, yalnız karşılaştırma ekranında yan yana.

### Q-081 — Performans ve gecikme hedefleri nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Kabul edilen maksimum piyasa verisi yaşı, sinyal değerlendirme gecikmesi, emir ACK süresi ve API uptime hedefi nedir?
- Önerilen varsayılan: İlk yük/sandbox testlerinde ölçülüp borsa ve strateji sınıfına göre SLO belirlenir; stale-data eşiği ayrı hard safety limitidir.

### Q-082 — Sinyal verisi ile emir borsası aynı olmak zorunda mı?
- Durum: AÇIK
- Öncelik: P0
- Soru: Bir borsanın verisiyle başka borsada işlem açmaya izin verilecek mi?
- Önerilen varsayılan: MVP'de hayır; sinyal ve execution aynı borsa/ürün/sembol verisini kullanır. Cross-exchange sonraki faz ve ayrı basis/latency riski gerektirir.

### Q-083 — Hedef ölçek nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Eşzamanlı kullanıcı, aktif strateji, takip edilen sembol ve indikatör sayısı için ilk yıl hedefi nedir?
- Önerilen varsayılan: Tek kullanıcı MVP ölçümleriyle başla; mimari sınırlar yük testiyle belgelenir, gereksiz erken mikroservisleşme yapılmaz.

### Q-084 — Kullanıcıya “neden işlem açılmadı?” kaydı gösterilecek mi?
- Durum: AÇIK
- Öncelik: P1
- Soru: Her değerlendirmede koşul, risk veya borsa kuralı nedeniyle engellenen işlemin açıklaması saklanıp gösterilsin mi?
- Önerilen varsayılan: Evet; maskelenmiş, insan tarafından okunabilir reason code + detay + timestamp + veri sürümü.

### Q-085 — Açık/kısmi işlemler detay sayfasında nasıl gösterilecek?
- Durum: AÇIK
- Öncelik: P1
- Soru: Fill'ler alt satırlarda mı; kapanmamış alanlar boş mu; unrealized PnL ve kalan miktar gösterilsin mi?
- Önerilen varsayılan: Position üst satırı + giriş/çıkış fill alt satırları; durum, kalan miktar, realized/unrealized PnL, fee, funding, mod, borsa ve yön görünür.

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
