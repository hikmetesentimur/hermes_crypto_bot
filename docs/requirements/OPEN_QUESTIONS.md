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
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0075`
- Cevap: Arayüz Türkçe olacak; kalıcı zamanlar UTC saklanıp Europe/Istanbul olarak gösterilecek; sayı girişinde virgül veya nokta kabul edilerek ondalık değere dönüştürülecek, belirsiz karışık biçimler reddedilecek.
- Soru: Arayüz yalnızca Türkçe mi olacak? Veritabanı UTC, gösterim Europe/Istanbul mı? Ondalık ayırıcı hem virgül hem nokta kabul edecek mi?
- Önerilen varsayılan: UI Türkçe; saklama UTC; gösterim Europe/Istanbul; kullanıcı girişinde virgül/nokta kabul edilip Decimal'a normalize edilir.

---

## B. Piyasa evreni, veri ve indikatörler

### Q-007 — İşlem çifti evreni ne zaman yenilenecek?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0076`
- Cevap: Çiftler başlangıçta, borsa durum olaylarında, hız sınırına uyan dönemsel yenilemede ve her emir öncesi doğrulanacak; askıya alınan/delist çiftte yeni giriş yasaklanıp açık risk güvenli çıkış ve alarm ile yönetilecek.
- Soru: Borsadaki yeni, askıya alınmış veya delist olmuş çiftler hangi sıklıkta yeniden alınacak; açık stratejiler nasıl etkilenecek?
- Önerilen varsayılan: Başlangıçta ve periyodik yenileme; durdurulmuş/delist çiftte yeni emir yasak, açık risk için alarm ve güvenli kapatma politikası.

### Q-008 — Hacim alanlarının kesin tanımı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0077`
- Cevap: “Para birimi olarak hacim” seçili mumun karşı-varlık hacmi; “24 saatlik para birimi olarak hacim” kayan 24 saatlik karşı-varlık hacmi olacak; temel-varlık hacmi ayrı adla gösterilecek.
- Soru: “Para birimi olarak hacim” ve “24 saatlik para birimi olarak hacim” hangi borsa alanlarına karşılık geliyor? İlki mum/periyot hacmi mi, anlık ticker hacmi mi, yoksa farklı bir metrik mi?
- Önerilen varsayılan: Birincisini ayrıca tanımlamadan uygulama; 24 saatlik metrik için quoteVolume kullan.

### Q-009 — Hacim filtrelerinde sınırlar nasıl davranacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0078`
- Cevap: Alt ve üst sınır ayrı ayrı boş bırakılabilecek ve dâhil olacak; negatif değer, alt sınırın üstü aşması ve sonlu olmayan değer reddedilecek; gerekli hacim yoksa koşul geçmeyecek.
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
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0079`
- Cevap: “Normal Mum” ve “Japon Mum” tek “Standart/Japon Mum” seçeneği olacak; aynı OHLC verisi için iki farklı davranış sunulmayacak.
- Soru: Belgede ayrı seçenekler olarak geçiyorlar fakat genel kullanımda aynı OHLC mumunu ifade edebilirler. Farklı davranış bekleniyor mu?
- Önerilen varsayılan: Tek seçenek olarak “Japon/Standart Mum”.

### Q-012 — Heikin Ashi, Renko ve çizgi verisi nasıl üretilecek?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0080`
- Cevap: Heikin Ashi, Renko ve çizgi serileri ham borsa verisinden sunucuda deterministik üretilecek; çizgide hazır kaynak kapanış, Renko’da sabit tutar/yüzde/ATR seçimi zorunlu olacak; sentetik fiyat emir gerçekleşmesi sayılmayacak.
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

### Q-018 — Koşul doğru kaldığında yeniden sinyal üretilecek mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0048`
- Cevap: Tek Geçiş kullanılacak; koşul yalnız yanlış durumdan doğru duruma geçtiğinde bir kez sinyal üretecek ve yeniden sinyal için önce tekrar yanlış olmalıdır.
- Soru: Koşul doğru kaldığı her değerlendirmede mi, yoksa yalnız yanlış→doğru geçişinde mi sinyal üretilecek?
- Önerilen varsayılan: Yalnız yanlış→doğru geçişi; aynı veri adımı ve sinyal kimliği yeniden emir oluşturmaz.

### Q-019 — Fiyatla kıyaslamada fiyat kaynağı nasıl seçilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0050`
- Cevap: Sistem koşulun amacına göre güvenli fiyat kaynağını otomatik seçecek ve kullanılan fiyat türünü kullanıcıya açıkça gösterecek.
- Soru: Mum/gösterge koşulu, emir yürütme, vadeli işlem riski ve kâr-zarar hesabında hangi fiyat kullanılacak?
- Önerilen varsayılan: Mum koşulunda ilgili mum fiyatı; alış yürütmede en iyi satış, satış yürütmede en iyi alış; vadeli riskte adil fiyat; gerçekleşmiş sonuçta gerçek emir gerçekleşmeleri.

### Q-020 — Çoklu zaman aralıkları nasıl hizalanacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0051`
- Cevap: İlgili zaman aralıklarından herhangi birinde yeni mum kapanınca, bütün zaman aralıklarının o anda kesinleşmiş son değerleriyle koşul ağacı yeniden değerlendirilecek; aynı anda kapanan mumlar tek değerlendirmede birleştirilecek.
- Soru: Farklı zaman aralıklarındaki göstergeler hangi anda ve hangi kesinleşmiş veriyle birlikte değerlendirilecek?
- Önerilen varsayılan: Her ilgili mum kapanışı değerlendirme olayıdır; her koşul kendi aralığının o anda kapanmış son değerini kullanır; gelecekteki veri kullanılmaz.

---

## D. Emir yürütme ve pozisyon yönetimi

### Q-021 — Belgede geçen üçüncü emir tipinin adı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0010`
- Cevap: “Geri Çekilme Limit Emri” ile gerçek “Stop-Limit Emir” iki ayrı seçenek olarak desteklenecek; “Tetikleme Sapması” ve belirsiz “Tetiklemeli Limit” adları kullanılmayacak.
- Soru: “Tetikleme Sapması” ile “Tetiklemeli Limit Order” aynı seçenek mi?
- Önerilen varsayılan: Tek ad: “Sinyal Fiyatından Sapmalı Limit Emir”.

### Q-022 — Koşullar gerçekleştiği andaki kullanılabilir emir fiyatı nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0050`
- Cevap: Alış için emir defterindeki en iyi satış fiyatı, satış için en iyi alış fiyatı kullanılacak; kaynak ve zamanı kullanıcıya gösterilecek.
- Soru: Sinyalden emir kararına geçerken o anda gerçekten ulaşılabilir yön fiyatı nasıl belirlenecek?
- Önerilen varsayılan: Alışta en iyi satış, satışta en iyi alış; güncellik ve fiyat farkı güvenlik denetimi zorunlu.

### Q-023 — Market emir kuralı gerçekten bekleyen bir fiyat filtresi mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0009`
- Cevap: Derhal gönderilen korumalı Market Emir ile fiyat koşulunu sonlu süre bekleyen Fiyat Korumalı Tetikleyici iki ayrı emir seçeneği olarak desteklenecek.
- Soru: Belgede Long için emir anı fiyatının sinyal fiyatına eşit/düşük, Short için eşit/yüksek olması bekleniyor. Koşul sağlanmazsa ne kadar beklenecek, sinyal ne zaman iptal olacak? Bu davranış market emrinden çok fiyat korumalı tetikleyiciye benziyor.
- Önerilen varsayılan: Maksimum bekleme süresi ve sapma toleranslı “protected market”; süre dolarsa iptal.

### Q-024 — Limit emir ne kadar açık kalacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0081`
- Cevap: Borsanın desteklediği GTC/IOC/FOK/süreli türler sunulacak; limit için hazır seçim GTC olacak fakat DEC-0054/DEC-0060 yaşam süresi dolunca güvenli iptal uygulanacak; otomatik yeniden fiyatlama olmayacak.
- Soru: GTC/IOC/FOK seçenekleri, son kullanma süresi, yeniden fiyatlama ve iptal kuralları nedir?
- Önerilen varsayılan: Kullanıcı seçilebilir time-in-force; varsayılan GTC + açık süre limiti + alarm.

### Q-025 — Post-only emir reddedilirse ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0082`
- Cevap: Post-only ret taker emrine dönüştürülmeyecek; güncel defter ve özgün fiyat sınırı doğrulanarak en yakın pasif fiyatta en fazla bir bağlı yeniden deneme yapılacak, ikinci rette iptal edilecek.
- Soru: Borsa emri piyasa alacak diye reddettiğinde iptal mi, bir tick geriden yeniden fiyatlama mı, post-only kapatma mı?
- Önerilen varsayılan: Otomatik taker emrine dönüşme yok; sınırlı yeniden fiyatlama veya iptal, ikisi de açık ayar.

### Q-026 — Kısmi gerçekleşen giriş emrinin kalan miktarı nasıl yönetilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0053`
- Cevap: Bekleme süresi dolunca gerçekleşmeyen miktar iptal edilecek; gerçekleşen kısım açık işlem olarak hemen koruyucu emirlerle yönetilecek ve kalan miktar piyasa emriyle tamamlanmayacak.
- Soru: Giriş emri kısmen gerçekleşip kalan miktar bekleme süresini aşarsa ne yapılacak?
- Önerilen varsayılan: Kalanı iptal et, iptali borsayla doğrula, gerçekleşen miktarı koru; belirsiz durumda ikinci emir gönderme.

### Q-027 — Emir tekrarları ve ağ hataları nasıl önlenecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0061`
- Cevap: Her emir niyeti gönderilmeden önce kalıcı ve benzersiz kimlikle kaydedilecek; ağ hatası/zaman aşımında borsa sorgulanıp sonuç kesinleşmeden kör yeniden gönderim veya aynı riski artıran yeni emir yapılmayacak.
- Soru: Zaman aşımı sonrası emrin borsaya ulaşıp ulaşmadığı belirsizse nasıl mutabakat yapılacak?
- Önerilen varsayılan: Kalıcı istemci emir kimliği ve yinelenmeme anahtarı; sorgula-uzlaştır; belirsizlikte yeniden gönderme yapma.

### Q-028 — Spot çıkışta hangi varlık miktarı satılabilir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0062`
- Cevap: Bot yalnız kendi doğrulanmış işlemleriyle ilgili strateji için aldığı ve ayırdığı spot miktarı satabilecek; kullanıcının mevcut/sonradan yatırılan varlıkları ve diğer stratejilerin payları korunacak.
- Soru: Spot çıkış cüzdanın tamamını mı, yalnız ilgili stratejiye doğrulanmış bot miktarını mı satabilir?
- Önerilen varsayılan: Yalnız ilgili stratejinin bot tarafından doğrulanmış ve ayrılmış miktarını yönet; kullanıcı varlıklarını koru.

### Q-029 — Vadeli işlemlerde pozisyon modu nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0064`
- Cevap: İlk sürüm tek yönlü pozisyon modunu kullanacak; aynı hesap ve işlem çiftinde eşzamanlı uzun/kısa tutulmayacak, ters girişten önce mevcut pozisyonun ve çakışan emirlerin güvenli biçimde kapanıp net sıfır olduğu doğrulanacak.
- Soru: Aynı vadeli işlem çiftinde eşzamanlı uzun ve kısa pozisyon tutulabilecek mi?
- Önerilen varsayılan: İlk sürüm tek yönlü; karşıt sinyalde önce tam kapatma ve borsa mutabakatı; çift yönlü mod yalnız gelecekte ayrı onayla değerlendirme.

### Q-030 — Marjin ve kaldıraç sınırları nasıl uygulanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0068`
- Cevap: Sabit 1–100 aralığına güvenilmeyecek; etkin azami kaldıraç platform, kullanıcı, borsa, hesap, sözleşme ve pozisyon büyüklüğü kademelerindeki sınırların en düşüğü olacak, uygun olmayan yeni giriş sessiz düzeltme yerine gerekçeli olarak engellenecek.
- Soru: Belgede 1–100 sabit aralık var; borsa/sembol/pozisyon büyüklüğü katmanına göre daha düşük azami değer varsa ne olacak?
- Önerilen varsayılan: Güncel borsa sınırlarını al; bütün sınırların en düşüğünü uygula; risk azaltan çıkışları engelleme.

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
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0069`
- Cevap: Para/fiyat/miktarda ondalık aritmetik kullanılacak; değerler emir amacına göre riski artırmayan ve koruyucu tetiği geciktirmeyen yönde borsa adımlarına indirgenecek; minimumu karşılamayan emir otomatik büyütülmeyip gerekçeli olarak engellenecek.
- Soru: Fiyat adımı, miktar adımı, asgari miktar ve asgari işlem değeri için yuvarlama/reddetme politikası nedir?
- Önerilen varsayılan: Ondalık aritmetik; risk artırmayan yön; minimumu karşılamıyorsa emir üretme.

### Q-034 — Aynı sembolde birden fazla strateji nasıl etkileşecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0070`
- Cevap: Normal spotta her strateji yalnız kendi doğrulanmış sanal varlık payını yönetebilecek; tek yönlü vadeli işlemlerde aynı hesap–çift için yalnız bir sahip strateji bulunacak ve diğer stratejilerin girişleri engellenecek.
- Soru: Aynı işlem çiftinde strateji sahipliği, çıkış ve risk hesabı ürün türüne göre nasıl ayrılacak?
- Önerilen varsayılan: Spotta ayrılmış sanal pay; vadeli işlemlerde tek sahip strateji.

### Q-035 — Strateji durdurma/silme/mod değiştirmede açık pozisyon ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0083`
- Cevap: Duraklatma girişleri kesip korumayı sürdürecek; durdurma onaylı “koru veya güvenli kapat” seçimini kullanacak; açık riskte silme arşivle sınırlı olacak, mod değişimi yeni sürüm oluşturacak.
- Soru: Açık emirler iptal mi, pozisyon kapatılır mı, yönetim devam mı eder, kullanıcıya seçim mi sunulur?
- Önerilen varsayılan: Sessizce bırakma yok; kullanıcı açıkça “yalnız yeni girişleri durdur”, “emirleri iptal et ve yönetmeye devam et” veya “güvenli kapat” seçer.

---

## E. Take Profit, Stop Loss ve kademeli alım

### Q-036 — Kademeli TP yüzdeleri toplamı nasıl doğrulanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0071`
- Cevap: Kâr alma kapanış dilimleri tam `%100` olacak; hedefler pozisyon yönünde sıkı artan ve tekrarsız sıralanacak; miktarlar borsa adımına indirgenecek ve son dilim doğrulanmış kalan miktarı kapatacak.
- Soru: Kapanış dilimleri tam `%100` etmek zorunda mı; aynı veya sırasız hedefler kabul edilir mi?
- Önerilen varsayılan: Toplam tam `%100`; hedefler sıkı sıralı; son dilim yuvarlama artığını kapatır.

### Q-037 — TP/SL hesaplaması hangi giriş fiyatını kullanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0072`
- Cevap: Kâr alma ve zarar durdurma fiyatlarının maliyet tabanı, borsadan doğrulanmış gerçekleşmelerin miktar ağırlıklı ortalama giriş fiyatı olacak; adil fiyat yalnız ürünün onaylı tetik/risk kaynağıdır ve giriş maliyetinin yerine geçmeyecek.
- Soru: İlk gerçekleşme, ağırlıklı ortalama gerçekleşme veya adil fiyat mı kullanılacak?
- Önerilen varsayılan: Doğrulanmış gerçekleşmelerden miktar ağırlıklı ortalama giriş; tetik kaynağını ayrı tut.

### Q-038 — Trailing stop ne zaman aktive olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0073`
- Cevap: Aktivasyon eşiği ve geri çekilme oranı ayrı strateji alanları olacak; gerçek işlemlerde yalnız borsanın doğrulanmış yerel takip eden zarar durdurma emri kullanılacak, bağdaştırıcı gerekli davranışı güvenilir desteklemiyorsa özellik canlıda kullanılamayacak.
- Soru: Aktivasyon eşiği, geri çekilme oranı, takip fiyatı ve borsa/sunucu sorumluluğu nasıl belirlenecek?
- Önerilen varsayılan: Ayrı eşik/oran; gerçek modda yerel borsa koruması; destek yoksa canlıda reddet.

### Q-039 — Kademeli alım tetikleri kümülatif mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0084`
- Cevap: İlk sürümde spot veya vadeli açık pozisyona kademeli alım/ortalama düşürme yapılmayacak; kümülatif ya da ortalama maliyete bağlı kademe tetiği bulunmayacak.
- Soru: Her kademe güncel ortalama maliyetin aynı zarar yüzdesinde mi, ilk girişten sabit seviyelerde mi tetiklenecek?
- Önerilen varsayılan: Belgede söylendiği gibi her dolumdan sonra güncellenen ortalama maliyete göre; seviyeler ve maksimum toplam exposure önceden gösterilir.

### Q-040 — Kademeli alımın maksimum risk sınırı nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0085`
- Cevap: Kademeli alım kapalı olduğundan kademe kaynaklı ek itibari tutar/marjin oluşmayacak; gelecekte ancak en kötü durum toplam risk, teminat ve tasfiye mesafesi sert sınırlarla doğrulanırsa değerlendirilecek.
- Soru: Çarpan ve kademe sayısı geometrik büyümeyle bakiyeyi aşarsa ne olacak? Maksimum notional/marjin ve liquidation buffer nedir?
- Önerilen varsayılan: Önceden worst-case exposure hesapla; strateji/cüzdan limitini aşan ayarı kaydetme; hard liquidation-distance kontrolü.

### Q-041 — Stop loss ile kademeli alım birlikte kullanılabilir mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0086`
- Cevap: Kademeli alım ilk sürümde olmayacak ve gelecekte de zarar durdurmanın yerine sayılmayacak; eklenirse borsa-yerel nihai zarar durdurma ve sert tasfiye mesafesi sınırı zorunlu olacak.
- Soru: Belge üç seçeneği alternatif gösteriyor. Aynı stratejide kademeli alımdan sonra nihai stop loss zorunlu mu?
- Önerilen varsayılan: Kademeli alım tek başına sınırsız zarar koruması değildir; zorunlu nihai stop veya hard risk limiti ekle.

### Q-042 — Çıkış emirleri reduce-only olacak mı?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0074`
- Cevap: Bütün vadeli kâr alma, zarar durdurma, normal çıkış ve acil kapatma emirleri yalnız pozisyonu azaltan/kapatma anlamıyla ve borsada doğrulanmış net miktarla sınırlandırılacak; hiçbir çıkış ters veya daha büyük pozisyon açamayacak.
- Soru: Vadeli çıkış emirlerinin ters pozisyon açması nasıl engellenecek?
- Önerilen varsayılan: Bütün vadeli çıkışları yalnız-azaltan/kapatma anlamı ve doğrulanmış miktarla sınırla.

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
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0087`
- Cevap: Kopya yeni kimlik/benzersiz adla, sıfır istatistikle ve taslak/test durumunda oluşturulacak; canlı yetki, çalışan örnek, açık risk ve geçmiş kopyalanmayacak.
- Soru: Ayarlar kopyalanırken işlem istatistikleri sıfırdan mı başlamalı? İsim çakışmaları nasıl çözülmeli?
- Önerilen varsayılan: Yeni kimlik ve sıfır istatistik; güvenli benzersiz ad; her zaman taslak/test modu.

### Q-056 — Strateji silme soft-delete mi olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0088`
- Cevap: Silme yumuşak silme/arşivleme olacak; açık emir, pozisyon veya araştırılan durum varken tamamlanmayacak; işlem ve denetim geçmişi değişmez bağlantıyla korunacak.
- Soru: Denetim ve işlem geçmişi için kayıt korunacak mı? Açık pozisyon varken silmeye izin verilecek mi?
- Önerilen varsayılan: Soft-delete/arşiv; işlem/audit geçmişi korunur; açık risk çözülmeden kalıcı silme yok.

---

## H. Güvenlik, gözlemlenebilirlik ve operasyon

### Q-057 — API anahtarları nerede ve nasıl saklanacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0089`
- Cevap: Tercih barındırma gizli bilgi yöneticisi/KMS olacak; veritabanında yalnız zarf şifreli değer bulunacak, ana anahtar veritabanı/Git/log dışında kalacak; sağlayıcı dağıtım kararıyla seçilecek.
- Soru: Hosting sağlayıcının secret manager'ı mı, şifreli veritabanı mı? Ana şifre/KMS nerede olacak?
- Önerilen varsayılan: Platform secret manager/KMS; veritabanında yalnız şifreli değer; log ve Git'te asla secret yok.

### Q-058 — Borsa anahtarı izin politikası nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0090`
- Cevap: Para çekme izni değişmez biçimde yasak olacak; yalnız gereken okuma ve spot/vadeli işlem izinleri kabul edilecek; destekleniyorsa IP izin listesi ve ayrı alt hesap kullanılacak.
- Soru: Trade-only, IP allowlist ve sub-account zorunlu mu?
- Önerilen varsayılan: Para çekme kapalı, yalnız gereken ürünlerde işlem, IP allowlist, mümkünse ayrı sub-account.

### Q-059 — Canlı moda geçişte UI dışında hangi güvenlik olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0091`
- Cevap: Arayüz düğmesi yalnız talep oluşturacak; sunucu teknik/risk kontrolleri, yakın güçlü doğrulama ve açık risk özeti onayı olmadan canlı yolu açmayacak.
- Soru: Toggle tek başına yeterli mi; 2FA, tekrar parola, yazılı risk özeti ve bekleme süresi gerekli mi?
- Önerilen varsayılan: Toggle yalnız talep oluşturur; sunucu doğrulaması + re-auth/2FA + açık onay olmadan aktif olmaz.

### Q-060 — Bildirim kanalları neler olacak?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0092`
- Cevap: İlk sürüm Telegram ve uygulama içi bildirim kullanacak; emir/gerçekleşme, ret-belirsizlik, veri kesintisi, risk, koruma kaybı, canlı mod, acil durdurma ve kurtarma olayları önem düzeyiyle bildirilecek.
- Soru: Telegram, e-posta veya web push ile hangi olaylar bildirilecek?
- Önerilen varsayılan: Telegram + uygulama içi; emir/fill, hata, veri kesintisi, limit ihlali, live mode ve kill switch olayları.

### Q-061 — Audit log kapsamı ve saklama süresi nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0093`
- Cevap: Kimlik doğrulama, ayar/sürüm, anahtar, mod, sinyal/karar/emir, risk ve manuel işlemler eklemeli ve bütünlük korumalı kayda yazılacak; kesin saklama süresi Q-105’e bırakılacak.
- Soru: Ayar değişiklikleri, girişler, anahtar işlemleri, mod değişimleri, sinyal/emir kararları ve manuel müdahaleler kaç yıl saklanacak?
- Önerilen varsayılan: Append-only audit; hassas veri maskeli; süre hukuki/operasyonel gereksinime göre, ilk varsayım 1 yıl.

### Q-062 — Veri saklama ve silme politikası nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0094`
- Cevap: Ham piyasa, türetilmiş, taslak, işlem, denetim, kullanıcı ve sır verileri ayrı yaşam döngüsüne sahip olacak; aktif risk ve hukuki kayıt silinmeyecek; kesin süreler Q-106’ya bırakılacak.
- Soru: Mum/tick/order-book, strateji, işlem ve kullanıcı verileri ne kadar tutulacak?
- Önerilen varsayılan: Veri sınıfı bazlı süre; ham yüksek frekans verisi kısa, işlem/audit verisi uzun; kullanıcı talebi ve yasal yükümlülükler belgelenir.

### Q-063 — Yedekleme ve felaket kurtarma hedefleri nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0095`
- Cevap: Şifreli tam+artımlı/noktasal kurtarma, ayrı arıza alanı ve düzenli geri yükleme testi zorunlu olacak; sayısal RPO/RTO Q-107’ye bırakılacak.
- Soru: Kabul edilen veri kaybı (RPO) ve hizmet dönüş süresi (RTO) nedir?
- Önerilen varsayılan: Günlük şifreli tam + sık artımlı yedek; düzenli restore testi; canlı işlemde RPO/RTO daha sıkı.

### Q-064 — Sistem yeniden başlarken nasıl uzlaşacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0096`
- Cevap: Gerçekleşme, açık emir, pozisyon ve bakiye için borsa yürütme gerçeği; niyet/sahiplik/audit için yerel değişmez kayıt birlikte uzlaştırılacak.
- Soru: Açık emir/pozisyonlar borsadan çekilip yerel durumla uyuşmazsa hangi kaynak kazanacak?
- Önerilen varsayılan: Borsa execution gerçeği kazanır; strateji sahipliği ve audit ile reconcile; belirsizlikte yeni emir fail-closed.

### Q-065 — Kill switch kapsamı nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0097`
- Cevap: Global, borsa, hesap, strateji ve işlem çifti düzeyi durdurma bulunacak; “yeni girişleri durdur” ile “acil kapat” ayrı eylem olacak.
- Soru: Global, hesap, borsa ve strateji bazlı düğmeler olacak mı; açık pozisyonu kapatmak ayrı seçenek mi?
- Önerilen varsayılan: Katmanlı kill switch; “yeni girişi durdur” ile “acil kapat” ayrı ve açıkça etiketli.

### Q-066 — İzleme/SLO hedefleri nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0098`
- Cevap: Veri yaşı, hesaplama, emir hazırlama/yanıt, hata, mutabakat, bildirim ve hizmet sürekliliği ölçülecek; sayısal hedef ve alarm eşikleri Q-089 ölçümleriyle belirlenecek.
- Soru: Veri gecikmesi, emir gecikmesi, hata oranı, bakiye mutabakatı ve uptime için eşikler nedir?
- Önerilen varsayılan: İlk yük testlerinden sonra ölçülebilir SLO; kritik alarm Telegram'a.

---

## I. UX, raporlama ve mevzuat

### Q-067 — Mobil ve erişilebilirlik kapsamı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0099`
- Cevap: İlk sürüm duyarlı mobil web ve WCAG 2.2 AA hedefleyecek.
- Soru: Responsive mobil web, klavye erişimi ve WCAG seviyesi gerekli mi?
- Önerilen varsayılan: Responsive web + temel WCAG 2.1 AA.

### Q-068 — Taslak ve otomatik kaydetme olacak mı?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0100`
- Cevap: Taslaklar sunucuda sürümlü otomatik kaydedilecek; durum görünür olacak, eşzamanlı çakışma sessiz ezilmeyecek ve taslak kendiliğinden başlamayacak.
- Soru: Sekmeler arası state korunmasına ek olarak tarayıcı kapanması/oturum süresi dolmasında taslak kurtarılacak mı?
- Önerilen varsayılan: Sunucu taraflı sürümlü taslak + belirgin kaydedildi durumu.

### Q-069 — Rapor dışa aktarma gerekli mi?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0101`
- Cevap: İşlem, gerçekleşme, ücret, fonlama ve kâr-zarar kayıtları ilk sürümde UTF-8 CSV olarak dışa aktarılacak; Excel/PDF sonraya bırakılacak.
- Soru: İşlemler ve PnL CSV/Excel/PDF olarak dışa aktarılacak mı?
- Önerilen varsayılan: CSV MVP; diğer formatlar sonraki faz.

### Q-070 — Grafik sağlayıcısı ve veri lisansı nedir?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0102`
- Cevap: İlk sürümde resmî kaynakta Apache 2.0 lisanslı olduğu doğrulanan TradingView Lightweight Charts kullanılacak; NOTICE/atıf ve TradingView bağlantısı korunacak.
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
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0103`
- Cevap: Dış, çok kullanıcılı veya ticari yayın öncesi kullanım koşulları, gizlilik politikası ve risk bildirimi hukuk uzmanı onayından geçecek.
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

### Q-092 — Strateji başlatıldığında koşul zaten doğruysa sinyal üretilecek mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0049`
- Cevap: İlk doğru durum sinyal üretmeyecek; önce koşulun yanlış olması, sonra doğruya geçmesi beklenecek.
- Soru: Yeni strateji sürümü ilk değerlendirmesinde giriş koşulunu doğru bulursa bunu yanlış→doğru geçişi sayıp hemen sinyal mi üretmeli, yoksa önce koşulun en az bir kez yanlış olması mı beklenmeli?
- Önerilen varsayılan: İlk doğru durum yalnız başlangıç değeri olarak kaydedilir; gözlenmiş yanlış→doğru geçişi olmadan sinyal üretilmez.

### Q-093 — Canlı Mum modunda çoklu zaman aralıkları ne sıklıkta değerlendirilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0052`
- Cevap: Kullanıcı strateji için 1, 2, 5, 10 veya 30 saniyelik değerlendirme aralığı seçecek; hazır değer 5 saniye olacak ve aradaki veri değişiklikleri en güncel görüntüde birleştirilecek.
- Soru: Kapanmamış mumlar kullanılırken her veri değişimi ayrı mı, yoksa seçilen kısa aralıkta birleştirilerek mi değerlendirilecek?
- Önerilen varsayılan: En düşük 1 saniye; hazır değer 5 saniye; aralık sonunda yalnız en güncel zaman uyumlu veri görüntüsü tek kez değerlendirilir.

### Q-094 — Kısmi giriş emrinin kalan miktarı ne kadar beklenecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0054`
- Cevap: Hızlı gerçekleşmesi beklenen emirlerde hazır süre 5 saniye ve seçilebilir aralık 1–30 saniye; fiyat bekleyen limit türlerinde hazır süre 60 saniye ve seçilebilir aralık 5–300 saniye olacak. Süre ilk doğrulanmış kısmi gerçekleşmede başlayacak.
- Soru: Kısmen gerçekleşen giriş emrinin kalan miktarı iptal edilmeden önce hangi süre ve sınırlar uygulanacak?
- Önerilen varsayılan: Emir sınıfına göre 5/60 saniye; kullanıcı yalnız güvenli sınırlar içinde değiştirebilir.

### Q-095 — Kısmi kâr alma ile zarar durdurma/acil kapatma nasıl yönetilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0055`
- Cevap: Kısmi kâr almada kalan emir iptal edilip kalan pozisyonun koruması sürdürülecek; zarar durdurma veya acil kapatmada kalan açık miktar yalnız pozisyonu azaltan, fiyat kayması korumalı emirle kapatılmaya çalışılacak.
- Soru: Kâr alma ve risk sonlandırma çıkışları kısmen gerçekleşirse kalan miktara aynı mı, amaca göre farklı mı davranılacak?
- Önerilen varsayılan: Kâr almada fiyatı zorlamadan korumayı sürdür; zarar durdurma/acil kapatmada doğrulanmış kalan riski güvenli biçimde azalt.

### Q-096 — Hiç gerçekleşmeyen giriş emri ne kadar açık kalacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0060`
- Cevap: Hızlı girişte hazır süre 5 saniye (1–30), limit türlerinde 60 saniye (5–300) olacak; sayaç borsa kabulünde başlayacak ve süre dolarsa veya giriş koşulu daha önce geçersizleşirse gerçekleşmemiş kısım iptal edilecek.
- Soru: Sıfır miktarı gerçekleşen giriş emrinin süre, başlangıç ve erken iptal kuralı nedir?
- Önerilen varsayılan: Kısmi girişle aynı 5/60 saniye sınıfları; borsa kabulünde başlangıç; koşul geçersizliğinde erken iptal; piyasa emriyle tamamlama yok.

### Q-097 — Kısmi çıkış emri için bekleme süreleri nedir?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0056`
- Cevap: Kâr almada hazır süre 60 saniye ve seçilebilir aralık 15–300 saniye; zarar durdurma/acil kapatmada hazır süre 5 saniye ve seçilebilir aralık 1–15 saniye olacak. Süre ilk doğrulanmış kısmi çıkışta başlayacak ve sonraki gerçekleşmelerle sıfırlanmayacak.
- Soru: Kâr alma, zarar durdurma ve acil kapatma emirleri ilk kısmi gerçekleşmeden sonra hangi süre ve sınırlarla beklenecek?
- Önerilen varsayılan: Kâr alma 60 saniye (15–300); zarar durdurma/acil kapatma 5 saniye (1–15).

### Q-098 — Normal strateji çıkış sinyali hangi kısmi çıkış politikasına girecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0057`
- Cevap: Normal strateji çıkışı ayrı bir Tam Kapatma sınıfı olacak; hazır süre 30 saniye, seçilebilir aralık 5–120 saniye olacak ve süre sonunda kalan miktar yalnız pozisyonu azaltan, fiyat kayması korumalı emirle kapatılmaya çalışılacak.
- Soru: Normal strateji çıkışı kısmen gerçekleşirse kalan pozisyon açık mı tutulacak, yoksa tamamen kapatılacak mı?
- Önerilen varsayılan: Normal çıkış pozisyonu bitirir; 30 saniye hazır süre (5–120) sonrasında güvenli tam kapatma uygulanır.

### Q-099 — Fiyat koruması risk çıkışını engellerse son çare ne olacak?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0058`
- Cevap: Zarar durdurma/acil kapatmada fiyat kayması sınırı kontrollü basamaklarla genişletilecek; yine kapanmazsa canlı işlem açılırken güçlü doğrulamayla önceden onaylanan, yalnız pozisyonu azaltan son çare piyasa kapatması uygulanacak.
- Soru: Risk çıkışı fiyat korumasına takılırsa pozisyon açık mı bırakılacak, yoksa önceden onaylı son çareyle kapatılacak mı?
- Önerilen varsayılan: Basamaklı fiyat koruması; ardından önceden onaylı yalnız-azaltan piyasa kapatması; başarısızlıkta yeni girişleri durdur ve acil alarm üret.

### Q-100 — Hiç gerçekleşmeyen normal veya risk çıkışı ne kadar beklenecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0059`
- Cevap: Normal çıkışta 30 saniye (5–120), zarar durdurma/acil kapatmada 5 saniye (1–15) uygulanacak; sıfır gerçekleşmede sayaç borsanın emri kabul ettiğini doğruladığı anda başlayacak.
- Soru: Normal çıkış, zarar durdurma veya acil kapatma emrinde sıfır miktar gerçekleşirse hangi süre ve başlangıç olayı uygulanacak?
- Önerilen varsayılan: Kısmi çıkışlarla aynı süreler; başlangıç borsa kabulünün doğrulandığı an.

### Q-102 — Borçlanmalı spot işlemleri ürün kapsamına girecek mi?
- Durum: CEVAPLANDI
- Öncelik: P1
- Karar: `DEC-0063`
- Cevap: İlk sürümde kapsam dışı olacak; ileride eklenmesi otomatik olmayacak ve ancak ayrı gereksinim, güvenlik incelemesi, testler ve kullanıcının yeni açık onayıyla değerlendirilebilecek.
- Soru: Borsadan varlık borçlanılan marjin spot işlemleri ilk sürümde desteklenecek mi?
- Önerilen varsayılan: İlk sürümde kapsam dışı; yalnız normal spot ve vadeli işlemler; gelecekte yalnız ayrı onayla değerlendirme.

### Q-103 — Tek yönlü vadeli pozisyonda çoklu strateji sahipliği nasıl yönetilecek?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0065`
- Cevap: İlk sürümde her hesap–vadeli işlem çiftinde yalnız bir sahip strateji olacak; sahiplik sürerken diğer stratejilerin aynı/karşıt sinyalleri engellenecek, sıraya alınmayacak ve alan boşaldıktan sonra yeni bir yanlış→doğru sinyali gerekecek.
- Soru: Aynı hesap ve vadeli işlem çiftinde birden fazla strateji aynı veya karşıt yönde sinyal üretirse tek net pozisyon kime ait sayılacak; bir strateji diğerinin payını kapatabilecek mi?
- Önerilen varsayılan: Tek sahip strateji; diğer stratejileri engelle ve sıraya alma; hiçbir strateji diğerinin pozisyonunu otomatik büyütmesin veya kapatmasın.

### Q-104 — Sahip strateji açık vadeli pozisyona ilave giriş yapabilir mi?
- Durum: CEVAPLANDI
- Öncelik: P0
- Karar: `DEC-0066`
- Cevap: İlk sürümde açık vadeli pozisyona ilave giriş, kademeli büyütme veya ortalama düşürme yapılmayacak; ilk girişin özgün onaylı miktarına kadar olan kısmi gerçekleşmeler dışında pozisyon tamamen kapanmadan yeni risk eklenmeyecek.
- Soru: Aynı stratejide pozisyon açıkken yeni giriş sinyali oluşursa pozisyon büyütülebilecek mi?
- Önerilen varsayılan: İlk sürümde ilave giriş ve ortalama düşürme yok; tamamen kapanma ve yeni yanlış→doğru sinyali gerekir.

---

## K. En sona bırakılan kullanıcı/ölçüm soruları

Bu bölüm yalnız asistanın ölçmeden veya kullanıcının/uzmanın tercihi olmadan sorumlu biçimde cevaplayamayacağı konuları içerir. Bunlar tamamlanana kadar ilgili canlı/üretim kapıları kapalı kalır.

### Q-002 — Uygulama nasıl erişilebilir olacak?
- Durum: AÇIK
- Öncelik: P0
- Önceki süreç kararı: `DEC-0004`
- Neden sona bırakıldı: Erişim modeli, hosting altyapısı, bütçe ve kişisel kullanım tercihi görüldükten sonra kullanıcı tarafından belirlenecek.
- Soru: Yalnızca özel ağ/VPN üzerinden mi, internete açık alan adı üzerinden mi, yoksa yerel bilgisayarda mı çalışacak?
- Önerilen varsayılan: TLS, kimlik doğrulama ve IP/VPN kısıtı olan özel dağıtım.

### Q-089 — İlk sürümün sayısal hız ve hizmet sürekliliği sınırları nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Gerçek hosting ve Binance/MEXC denemelerinde kabul edilecek en yüksek piyasa verisi yaşı, sinyal hesaplama süresi, sistem içi emir hazırlama süresi, borsa yanıt bekleme süresi ve aylık hizmet sürekliliği hedefleri ne olmalı?
- Önerilen varsayılan: Önce ölçüm yapılır; normal hız kapsamına uygun gerçekçi sınırlar ölçüm sonuçlarıyla önerilir ve canlı işlem açılmadan önce kullanıcı tarafından ayrıca onaylanır. Eski veri güvenlik sınırı performans hedefinden bağımsız ve atlanamaz olur.
- Neden sona bırakıldı: Gerçek hosting ile Binance/MEXC deneme ölçümleri olmadan güvenilir sayısal eşik seçilemez.

### Q-101 — Acil risk çıkışının fiyat kayması basamakları nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Normal fiyat kayması sınırından son çare piyasa kapatmasına geçmeden önce kaç basamak, hangi bekleme aralıkları, hangi artış yöntemi ve hangi mutlak üst sınır uygulanacak?
- Önerilen varsayılan: Borsa/ürün emir defteri ölçümlerine dayalı az sayıda kısa basamak; her basamakta mutabakat; platform düzeyinde aşılamaz üst sınır ve sonrasında yalnız önceden onaylı son çare piyasa kapatması.
- Neden sona bırakıldı: Borsa, ürün ve emir defteri ölçümleri olmadan fiyat kayması basamakları güvenilir biçimde belirlenemez.

### Q-105 — Denetim ve finansal kayıtların kesin saklama süresi nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Hukuki, vergi, güvenlik ve işletme ihtiyaçları dikkate alındığında denetim, emir, gerçekleşme ve finansal rapor kayıtları kaç yıl saklanmalı?
- Neden sona bırakıldı: Hukuk/mali müşavir görüşü ve ürünün faaliyet modeli gerekir; rastgele süre seçilemez.

### Q-106 — Ham piyasa ve kullanıcı verilerinin kesin saklama/silme süreleri nedir?
- Durum: AÇIK
- Öncelik: P1
- Soru: Ham mum/tick/emir defteri, türetilmiş gösterge, taslak ve kullanıcı verileri depolama maliyeti, gizlilik ve araştırma ihtiyacına göre ne kadar tutulmalı?
- Neden sona bırakıldı: Barındırma kapasitesi, maliyet, gizlilik ve kullanım ihtiyacı gerekir.

### Q-107 — Kabul edilebilir veri kaybı ve hizmet dönüş hedefleri nedir?
- Durum: AÇIK
- Öncelik: P0
- Soru: Üretim barındırması seçildikten sonra kabul edilebilir en yüksek veri kaybı süresi (RPO) ve hizmeti geri getirme süresi (RTO) ne olmalı?
- Neden sona bırakıldı: Barındırma mimarisi, bütçe ve işletme tercihi olmadan güvenilir sayı seçilemez.

## En son ele alınacak sıra

1. `Q-002` — Dağıtım ve erişim modeli (barındırma/kişisel tercih)
2. `Q-089` — Sayısal hız ve hizmet sürekliliği eşikleri (gerçek ölçüm)
3. `Q-101` — Acil fiyat kayması basamakları (borsa/ürün ölçümü)
4. `Q-105` — Denetim ve finansal kayıt saklama süresi (hukuk/mali müşavir)
5. `Q-106` — Ham piyasa ve kullanıcı verisi saklama süresi (maliyet/gizlilik)
6. `Q-107` — Veri kaybı ve hizmet dönüş hedefleri (barındırma/bütçe)
