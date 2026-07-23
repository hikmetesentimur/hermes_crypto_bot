# Kripto Trading Bot Site Senaryosu — Ham Metin

> Bu dosya, kullanıcı tarafından sağlanan Word belgesinin aranabilir metin kopyasıdır. Anlamı değiştirilmeden saklanır; düzenlenmiş gereksinimler ayrı belgelerde tutulur.

KRİPTO TRADİNG BOT SİTE ÖZELLİKLERİ:

Modüler bir yapı oluşturmak ve daha sonradanda kolay bir şekilde eklemeler çıkarmalar yapabilmek için borsalar ve indikatörler için ayrı klasör yapıları oluşturulsun. Örneğin borsalar/binance klasörü içerisine binance borsası ile ilgili api bilgileri kaydedilsin, indikatörler/RSI klasörü içerisinede RSI indikatörü için gereken kodlar kaydedilsin.

“Strateji Oluştur” sayfası: Bu sayfada sayfa yenileme durumu olmaması ve kullanıcı tarafından girilen bilgilerin kaybolmaması için tek sayfa içerisinde sekmeli geçiş sistemi kullanılacak. Sadece aktif olan sekme içeriği gösterilerek diğer sekmeler kullanıcı tarafından girilen bilgiler silinmeden gizlenmiş olacak. Sekmeler arası geçiş yapılabilecek ve geçişlerde sayfa yenilenmeyecek, daha önce girilen bilgiler kullanıcı kendisi silmediği sürece kesinlikle sekmeler arası geçiş esnasında silinmeyecek.

“Ön Filtreleme” sekmesi:

**  “Borsa Seç” başlığı altında bir açılır menü oluştur. Bu açılır menüde, borsalar klasöründe kayıtlı olan borsaların isimlerini listele. Kullanıcı, bu listeden işlem yapmak istediği borsayı seçebilsin ve bu seçim zorunlu olsun.

**  “İşlem Tipi” başlığı altında bir açılır liste oluştur. Bu listede “Spot İşlem” ve “Futures İşlem” seçenekleri yer alsın. Bu seçim de zorunlu olsun.

**  “Para Birimi” adında bir açılır liste oluştur ve daha önceden seçilmiş olan borsa ve işlem tipine göre, borsanın API dosyasından mevcut işlem çiftlerini çek. Bu işlem çiftlerinden karşıt para birimlerini (quote currency) ayıkla ve “Para Birimi” başlığı altında bir açılır menüde göster. Bu strateji için yapılacak diğer işlemlerde sadece bu açılır menüden seçilen karşıt para birimi ile işlem gören işlem çiftlerini kullan.

**  “Para Birimi Olarak Hacim” başlığı altında kullanıcının rakamsal değerler yazabileceği “Minimum Hacim” ve “Maksimum Hacim” adlarında 2 adet text kutucuğu oluştur. Daha önceden seçilmiş olan Borsa ve İşlem Tipi seçeneklerine göre (spot veya futures), seçilen borsa klasörünün içindeki api kodlarındaki hacim verilerini çekip “Para Birimi” başlığı altındaki açılr menüden seçilen karşıt para birimine göre “para_birimi_olarak_hacim” verisini ayıkla ve kullanıcının text kutucuklarına yazdığı değerlere göre bu veriyi filtrele.

**  “24 Saatlik Para Birimi Olarak Hacim” başlığı altında kullanıcının rakamsal değerler yazabileceği “Minimum Hacim” ve “Maksimum Hacim” adlarında 2 adet text kutucuğu oluştur. Daha önceden seçilmiş olan Borsa ve İşlem Tipi seçeneklerine göre (spot veya futures), seçilen borsa klasörünün içindeki api kodlarından hacim verilerini çekip “Para Birimi” başlığı altındaki açılır listeden seçilen para birimine göre 24 saatlik para birimi cinsinden hacim verisini ayıklayıp kullanıcının text kutucuklarına yazdığı değerlere göre bu veriyi filtrele.

** “Kıyaslama Koşulları” sekmesi:

**  Bu sekmenin en başında bir “Kıyaslama Koşulu Ekle” butonu oluştur. Bu butona tıklayınca bir modal pencere açılsın ve bu pencerenin içeriğinde

**  “İndikatör Seç” başlığı altında açılır menü ile indicators klasörü içinde bulunan indikatörlerin listesi sunulsun. Bu listeden bir indikatör seçildiğinde ilgili indikatörün klasörüne bağlanılsın.

** Seçilen indikatörü altta göster ve yanına “Ayar” ikonu ve “Sil” butonu ekle.

**  Ayar ikonuna tıklandığında bir modal daha aç ve bu modal içerisinde;

**  İndikatör sinyallerinin fiyat ve trend takibi yapabilmesi ve doğru kıyaslama koşulları sinyalleri üretebilmesi için “Grafik Mum Tipleri” seçenekleri olan “Normal Mum Grafiği”, “Heikin Ashi Mum Grafiği”, “Japon Mum Grafiği”, “Renko Mum Grafiği”, “Çizgi Grafik” seçenekleri bir açılır menü ile seçilebilsin.

**  İndikatör ve Grafik zaman periyodu seçenekleri olan “1 dakika”, “5 dakika”, “15 dakika”, “30 dakika”, “1 saat”, “4 saat”, “1 gün”, “1 hafta”, “1 ay” seçenekleri bir açılır menü ile seçilebilsin.

** İlgili indikatörün settings.py dosyasında bulunan diğer ayar parametreleri burada görünsün indikatör ayarları buradan yapılsın. (Örneğin; RSI indikatörü için RSI sinyal uzunluk değeri, kaynak, hareketli ortalama tipi (MA, SMA, WMA vb. gibi), hareketli ortalama uzunluk değeri gibi seçilen indikatöre ait ayarlar buradan yapılabilsin.)

**  Bu modal pencerenin en altında “KAYDET” butonu olsun ve bu butona tıklandığında bu pencerede seçilen indikatör ayarları kaydedilip Ayar için açılan modal pencere kapatılsın.

**   Sil butonuna tıklanıncada seçilen indikatör buradan kaldırılsın ve yukarıdaki açılır menüden tekrar bir indikatör seçilebilsin.

**   Bir alt satırda seçilen indikatör için parameters.py dosyasında bulunan parametreler “İndikatör Parametresi Seç” başlığı altında bir açılır menüde sunulsun. Örneğin; yine RSI indikatörü için RSI sinyali ve indikatör ayarlarında seçilen hareketli ortalama tipi örneğin SMA seçilmişse bu ikisi seçilen indikatöre ait kıyaslama parametleri olarak seçilebilecek.

**  Bir alt satırda “Kıyaslama Parametresi Ekle” başlığı altında standart_parameters.py dosyasındaki parametreler bir açılır menüde listelensin. Bu parametreler; Büyüktür, Küçüktür, Büyük veya Eşit, Küçük veya Eşit, Yukarı Keser, Aşağı Keser, Yukarı Yönlü, Aşağı Yönlü gibi bir üstteki seçilen indikatör parametresini, bir altta seçilen Fiyat, Değer, yada ikinci bir indikatör parametresine göre kıyaslamaya yarayacak olan standart kıyaslama parametreleridir.

** Bir alt satırda radyo düğmeleri şeklinde ve sadece bir tanesi seçilebilen ama seçilmesi zorunlu olmayan “Fiyat”, “Değer”, “İndikatör” seçenekleri olsun.

** Bu seçeneklerden “Fiyat” seçilirse, yukarıda seçilen indikatör parametresi, seçilen kıyaslama parametresi sayesinde fiyat ile kıyaslansın. (Örneğin: İndikatör Parametresi – Büyüktür – Fiyat)

** Bu seçeneklerden “Değer” seçilirse alt tarafta kullanıcıya rakamsal değer girebileceği bir kutucuk oluşsun ve bu sayede yukarıda seçilen indikatör parametresi, seçilen kıyaslama parametresi sayesinde kullanıcının girdiği değer ile kıyaslansın. (Örneğin: İndikatör Parametresi – Küçüktür – Değer)

** Bu seçeneklerden “İndikatör” seçilirse:

**  “İndikatör Seç” başlığı altında açılır menü ile indicators klasörü içinde bulunan indikatörlerin listesi sunulsun. Bu listeden bir indikatör seçildiğinde ilgili indikatörün klasörüne bağlanılsın.

**  Seçilen indikatörü altta göster ve yanına “Ayar” ikonu ve “Sil” butonu ekle.

**  Ayar ikonuna tıklandığında bir modal daha aç ve bu modal içerisinde;

İndikatör sinyallerinin fiyat ve trend takibi yapabilmesi ve doğru kıyaslama koşulları sinyalleri üretebilmesi için “Grafik Mum Tipleri” seçenekleri olan “Normal Mum Grafiği”, “Heikin Ashi Mum Grafiği”, “Japon Mum Grafiği”, “Renko Mum Grafiği”, “Çizgi Grafik” seçenekleri bir açılır menü ile seçilebilsin.

İndikatör ve Grafik zaman periyodu seçenekleri olan “1 dakika”, “5 dakika”, “15 dakika”, “30 dakika”, “1 saat”, “4 saat”, “1 gün”, “1 hafta”, “1 ay” seçenekleri bir açılır menü ile seçilebilsin.

İlgili indikatörün settings.py dosyasında bulunan diğer ayar parametreleri burada görünsün indikatör ayarları buradan yapılsın.

Bu modal pencerenin en altında “KAYDET” butonu olsun ve bu butona tıklandığında bu pencerede seçilen indikatör ayarları kaydedilip Ayar için açılan modal pencere kapatılsın.

**  Sil butonuna tıklanıncada seçilen indikatör buradan kaldırılsın ve yukarıdaki açılır menüden tekrar bir indikatör seçilebilsin.

** Bir alt satırda seçilen indikatöre ait parametreler “İndikatör Parametresi Seç” başlığı altında bir açılır menüde sunulsun. Bu sayede yukarıda seçilen indikatör parametresi yukarıda seçilen kıyaslama parametresi sayesinde kullanıcının burada seçtiği indikatör parametresi ile kıyaslansın. (Örneğin: İndikatör Parametresi1 – Yukarı Keser – İndikatör Parametresi2)

**  Eğer yukarıdaki radyo düğmelerinden hiçbirisi seçilmeden sadece indikatör parametresi ve kıyaslama parametresi seçilerek kıyaslama kaydedilirse sadece bu iki değer kıyaslansın. (Örneğin: indikatör parametresi olarak RSI sinyali ve kıyaslama parametresi olarakta Yukarı Yönlü parametresi kaydedilmişse ikinci bir indikatör parametresi yada değere gerek kalmadan sadece RSI sinyalinin Yukarı Yönlü olduğu durumlar filtrelenir.)

**  Bu modal penceresinin en altında “Kıyaslama Koşullarını Kaydet” butonu olsun. Bu butona tıklayınca modal penceresinde kullanıcı tarafından girilen tüm kıyaslama koşulları kaydedilip “Kıyaslama Koşulu Ekle” butonunun alt tarafında özet parametre bilgileri şeklinde gösterilsin (Örneğin: RSI – Büyüktür – 50) ve modal kapatılsın.

** Bu şekilde birden fazla koşul VE-VEYA mantığı ile oluşturulabilsin. Örneğin 1. Koşul VE 2. Koşul birlikte gerçekleşirse yada 1. Koşul VEYA 2. Koşuldan herhangi biri gerçekleşirse.

**  Kaydedilen ve “Kıyaslama Koşulu Ekle” butonunun altında gösterilen koşulların yanlarına “Düzenle” ve “Sil” butonları eklensin. Sil butonuna tıklayınca ilgili koşullar silinsin. Düzenle butonuna tıklayınca modal penceresi yeniden açılsın ve düzenlenerek tekrar kaydedilebilsin.

** “Pozisyon Emirleri” Sekmesi:

**  Test Mod & Gerçek Mod Geçiş Sistemi: Strateji oluşturma sayfasında, kullanıcıya Test Modu ve Gerçek Mod arasında Geçiş Butonu (Toggle Switch) şeklinde geçiş yapma seçeneği sunulsun.

** Test Modu: Kullanıcı, Test Modu'nda emirleri simüle edebilecek ve borsaya gerçek emir gönderilmeyecek. Bu modda yapılan tüm işlemler, sanki gerçekmiş gibi işlenecek ancak sadece simülasyon amaçlı olacak.

** Simülasyon Motoru: Test Modu'nda, oluşturulan stratejiye göre emirlerin nasıl gerçekleştirileceğini simüle eden bir motor bulunmalıdır. Bu motor, mevcut olan gerçek anlık piyasa verilerini kullanarak emirlerin nasıl gerçekleşeceğini taklit eder.

** Emir Gönderme Simülasyonu: Kullanıcı, emir gönderdiğinde sistem bu emri simüle eder ve sanki borsaya gönderilmiş gibi işleme koyar. Ancak, gerçek borsaya hiçbir emir gönderilmez.

** Pozisyon Durumu İzleme: Simüle edilen emirlerin ve pozisyonların durumu gerçek zamanlı olarak izlenir ve kullanıcının ana ekranında gösterilir. Bu sayede, stratejinin nasıl çalıştığını test edebilir.

** Gerçek Mod: Kullanıcı, Test Modu'nda test ettiği stratejiyi başarılı bulduğunda, Gerçek Mod'a geçiş yapabilecek. Bu geçiş, tüm parametreleri ve ayarları Gerçek Mod'a taşıyacak ve artık gerçek emirler borsaya gönderilecek.

** Modlar Arası Geçiş: Test Modu ve Gerçek Mod arasındaki geçiş sırasında, sistem tüm strateji parametrelerini ve ayarlarını kontrol edecek ve geçişin güvenli olup olmadığını onaylayacak.

** Test Modu ve Gerçek Mod arasındaki geçiş, strateji kaydetme ve güncelleme fonksiyonlarıyla ilişkilendirilecek.

**  “Pozisyon Yönü” Seçimi: Kullanıcı, pozisyonun yönünü (Long/Short) yine bir Geçiş Butonu ile seçebilecek. Kullanıcı eğer Ön Filtreleme sekmesinde İşlem Tipi olarak Spot seçerse, bu buton sadece Long yönünde kilitlenecek ve Short tarafa geçiş yapılamayacak.

**  Marjin Modu: Kullanıcı yine bir Geçiş Butonu ile marjin modunu (İzole/Cross) seçebilecek. Kullanıcı eğer  Ön Filtreleme sekmesinde İşlem Tipi olarak Spot seçerse, bu buton pasif kalacak ve hiçbir seçim yapılamayacak.

**  Kaldıraç Ayarı: Kullanıcı, pozisyon için uygulanacak kaldıraç oranını bir Slider Buton ile belirleyebilecek. Kullanıcı tutma noktasını hareket ettirdikçe adım değeri 1’er değer olarak artacak yada azalacak ve bu değerler 1-100 arası olacak (1 ve 100 dahil). Bu butonun altında tutma noktasının bulunduğu değeri gösteren bir kutucuk bulunacak ve kullanıcı isterse tutma noktasını kaydırmadanda bu kutucuğa 1 ve 100 arası bir değer girebilecek ve tutma noktasıda otomatik olarak bu kutucuğa girilen değerin olduğu noktada konumlanacak. Eğer bu değerlerden daha az yada daha fazla bir değer girilirse bu kabul edilmeyecek, hatalı girişler engellenecek ve kullanıcı bu konuda uyarılacak. Kullanıcı eğer  Ön Filtreleme sekmesinde İşlem Tipi olarak Spot seçerse, bu buton 1 değerinde kilitli şekilde ve pasif olarak kalacak ve kesinlikle değiştirilemeyecek.

**  Pozisyon Büyüklüğü: Kullanıcı, bir pozisyon için bağlamak istediği fon miktarını “Sabit Tutar” ve “Cüzdanın Yüzdelik Dilimi” olarak girebilecek. “Sabit Tutar” ve “Yüzdelik Dilim” arasında bir Geçiş Butonu ile geçiş yapılabilecek. Geçiş Butonunun altında kullanıcının virgüllü değerlerde dahil olmak üzere rakamsal değer girebileceği bir kutucuk olacak.

** “Sabit Tutar” Seçeneği: “Sabit Tutar” seçildiğinde kutucuğun yanında kullanıcının Ön Filtreleme sekmesinde seçtiği “Para Birimi” görünecek ve açılacak her pozisyonda bu para biriminde yine Ön Filtreleme sekmesinde seçilen “İşlem Tipi” seçeneğine göre spot işlem tipi seçilirse Spot cüzdanından kullanıcının kutucuğa girdiği değer kadar miktar bir pozisyon için bağlanacak. (Örneğin: Kullanıcının seçtiği Para Biriminin USDT olduğunu, İşlem Tipinin Spot olduğunu ve kutucuğada 10 rakamını yazdığını varsayalım. Buna göre kutucuğun yanında USDT ibaresi görünecek ve Spot cüzdanından her pozisyon için 10 USDT bağlanacak.) Kaldıraçlı Futures işlemlerde bu kutucuğa girilen değer kaldıraç miktarı ile çarpılacak onun sonucunda çıkan değer kadarlık pozisyon futures cüzdanından açılacak. (Örneğin: Kullanıcı kaldıraç miktarını 5 olarak girdiğini, İşlem Tipinin Futures seçildiğini ve kutucuğada 10 rakamını yazdığını varsayalım. Buna göre Futures cüzdanından 10x5=50 USDT lik pozisyon açılacak.)

** “Yüzdelik Dilim” Seçeneği: “Yüzdelik Dilim” seçildiğinde kutucuğun yanında “%” (Yüzde) ibaresi görünecek ve açılacak her pozisyonda Ön Filtreleme sekmesinde seçilen İşlem Tipine göre Spot işlem tipi seçilirse Spot Cüzdanının içerisinde bulunan yine ön filtreleme sekmesinde seçilen Para Birimi cinsinden toplam bakiyenin kutucuğun içerisine yazılan rakam kadar yüzdelik kısmı kullanılacak. (Örneğin: Ön Filtreleme sekmesinde Para Birimi olarak USDT seçildiğini, İşlem Tipi olarak Spot seçildiğini, Spot cüzdanının USDT bakiyesinin 1000 USDT olduğunu ve kutucuğada 1,5 yazıldığını varsayalım. Buna göre Spot cüzdanın USDT bakiyesi olan 1000 USDT nin %1,5 lik kısmı olan 15 dolar bağlanacak pozisyona.) Kaldıraçlı Futures işlemlerde ise Ön Filtreleme sekmesinde seçilen İşlem Tipine göre Futures işlem tipi seçilirse Futures Cüzdanının içerisinde bulunan yine Ön Filtreleme sekmesinde seçilen Para Birimi cinsinden Toplam Cüzdan bakiyesinin kutucuğa yazılan yüzdelik değerinin ayrıca kaldıraç miktarı ile çarpılması sonucu çıkan rakam kadarlık bir pozisyon açılacak. (Örneğin: Ön Filtreleme sekmesinde Para Birimi olarak USDT seçildiğini, İşlem Tipi olarak Futures seçildiğini, Futures cüzdanının USDT bakiyesinin 1000 USDT olduğunu ve kutucuğada 1,5 yazıldığını ve kaldıraç miktarınında 10 olduğunu varsayalım. Buna göre Futures cüzdanın USDT bakiyesi olan 1000 USDT nin %1,5 lik kısmı olan 15 dolar ayrıca 10 ile çarpılarak 150 USDT lik bir pozisyon açılacak.)

**  Emir Tipi: Kullanıcıların “Emir Tipi” olarak “Limit Order”, “Market Order” ve “Tetikleme Sapması” seçeneklerini seçebileceği bir açılır menü oluştur.

** “Limit Order” Seçeneği: Kullanıcı bu “Limit Order” seçeneğini seçerse, “Kıyaslama Koşulları” sekmesinde kaydedilen tüm koşulların sinyalleri ve anlık fiyatları takip edilsin ve kayıtlı olan tüm koşullardan ortak sinyal alındığı andaki anlık gerçek tahta fiyatı ilgili işlem çiftinin “Limit Order” Fiyatı olarak belirlenip “Test Modu” yada “Gerçek Mod” durumuna göre simüle edilsin yada borsaya gönderilsin.

** “Post-Only” Seçeneği: “Limit Order” seçeneği seçildiğinde bu seçeneğin altında bir tik ile işaretlenebilen “Post-Only” seçeneğide oluşsun. Bu Post-Only seçeneği işaretlendiğinde Limit Order emri borsaya Post-Only (Piyasa Yapıcı) emir olarak gönderilsin.

** “Market Order” Seçeneği: Kullanıcı bu “Merket Order” seçeneğini seçerse, “Pozisyon Yönü” durumuna göre;

** “Long” pozisyonlarda “Kıyaslama Koşulları” sekmesinde kaydedilen tüm koşulların sinyalleri ve anlık fiyatları takip edilsin ve ilgili işlem çiftinin kayıtlı olan tüm koşullardan ortak sinyal alındığı andaki anlık gerçek tahta fiyatıyla ilgili işlem çiftinin emrin verileceği andaki anlık gerçek tahta fiyatının eşit yada anlık fiyatın daha düşük olduğu durumlarda “Market Order” emri verilsin ve “Test Modu” yada “Gerçek Mod” durumuna göre simüle edilsin yada borsaya gönderilsin.

** “Short” pozisyonlarda “Kıyaslama Koşulları” sekmesinde kaydedilen tüm koşulların sinyalleri ve anlık fiyatları takip edilsin ve ilgili işlem çiftinin kayıtlı olan tüm koşullardan ortak sinyal alındığı andaki anlık gerçek tahta fiyatıyla ilgili işlem çiftinin emrin verileceği andaki anlık gerçek tahta fiyatının eşit yada anlık fiyatın daha yüksek olduğu durumlarda “Market Order” emri verilsin ve “Test Modu” yada “Gerçek Mod” durumuna göre simüle edilsin yada borsaya gönderilsin.

** “Tetiklemeli Limit Order” Seçeneği: Kullanıcı bu “Tetiklemeli Limit Order” seçeneğini seçerse, virgüllü rakamsal değer girebileceği bir kutucuk oluşsun ve bu kutucuğa yazılan değer yüzde olarak hesaplansın. Sonra “Pozisyon Yönü” durumuna göre;

** “Long” pozisyonlarda “Kıyaslama Koşulları” sekmesinde kaydedilen tüm koşulların sinyalleri ve anlık fiyatları takip edilsin ve ilgili işlem çiftinin kayıtlı olan tüm koşullardan ortak sinyal alındığı andaki anlık gerçek fiyatı tetikleme fiyatı olarak kabul edilsin ve tetikleme fiyatının yüzde olarak kutucuğa yazılan değer kadar aşağısından Limit Order emri verilsin ve “Test Modu” yada “Gerçek Mod” durumuna göre simüle edilsin yada borsaya gönderilsin. (Örneğin: Kutucuğa 1,5 değeri yazılmışsa tetikleme fiyatının %1,5 daha aşağısından limit order emri verilir.)

** “Short” pozisyonlarda “Kıyaslama Koşulları” sekmesinde kaydedilen tüm koşulların sinyalleri ve anlık fiyatları takip edilsin ve ilgili işlem çiftinin kayıtlı olan tüm koşullardan ortak sinyal alındığı andaki anlık gerçek fiyatı tetikleme fiyatı olarak kabul edilsin ve tetikleme fiyatının yüzde olarak kutucuğa yazılan değer kadar yukarısından Limit Order emri verilsin ve “Test Modu” yada “Gerçek Mod” durumuna göre simüle edilsin yada borsaya gönderilsin. (Örneğin: Kutucuğa 1,5 değeri yazılmışsa tetikleme fiyatının %1,5 daha yukarısından limit order emri verilir.)

**  “Post-Only” Seçeneği: “Tetiklemeli Limit Order” seçeneği seçildiğinde bu seçeneğin altında bir tik ile işaretlenebilen “Post-Only” seçeneğide oluşsun. Bu Post-Only seçeneği işaretlendiğinde Tetiklemeli Limit Order emri borsaya Post-Only (Piyasa Yapıcı) emir olarak gönderilsin.

** Önemli Not: Long veya Short her iki Pozisyon Yönü içinde gereken tüm hesaplamalar site üzerinde gerçekleştirilecek, simülasyon motoruna yada borsaya bu hesaplamaların sonuçları “Limit Order” emri olarak gönderilecek.

** Önemli Not: Yukarıdaki “Kıyaslama Koşulları” sekmesinde “indikatör parametreleri” ve “Kıyaslama Parametreleri” kullanılarak zaman periyodu ve grafik mum tipi verilerine göre koşul sinyalleri üretilerek pozisyon giriş koşulları belirlenmiş olacak. Fakat emir tiplerinin hepsinde pozisyon giriş fiyatı yada tetikleme fiyatı olarak koşulların gerçekleştiği andaki gerçek tahta fiyatı kullanılacak.

**  Take Profit: Kullanıcıların “Take Profit” seçenekleri olarak “Tek Seferde Kapat” ve “Yüzdelik Dilimlere Böl” seçeneklerini seçebileceği bir açılır menü oluştur.

** “Tek Seferde Kapat” Seçeneği: Kullanıcı bu “Tek Seferde Kapat” seçeneğini seçtiğinde seçeneğin altında kullanıcının virgüllü rakamsal değer girebileceği bir kutucuk oluşacak ve bu kutucuğa girilen rakamsal değer yüzde olarak hesaplanacak. Daha sonra Pozisyon Yönü durumuna göre:

** “Long” pozisyonlarda fiyat, pozisyon giriş fiyatından kutucuğa girilen yüzde değer kadar yükseldiğinde pozisyon tamamen kapanacak. (Örneğin: Kullanıcı kutucuğa “1,5” değerini yazmışsa Fiyat “%1,5” yükseldiğinde pozisyon tamamen kapatılır.)

** “Short” pozisyonlarda fiyat, pozisyon giriş fiyatından kutucuğa girilen yüzde değer kadar düştüğünde pozisyon tamamen kapanacak. (Örneğin: Kullanıcı kutucuğa “2,5” değerini yazmışsa Fiyat “%2,5” düştüğünde pozisyon tamamen kapatılır.)

** “Yüzdelik Dilimlere Böl” Seçeneği: Kullanıcı bu “Yüzdelik Dilimlere Böl” seçeneğini seçtiğinde, seçeneğin altında “Yüzdelik Dilim Gir” ve “Kar Oranı Gir” adında virgüllü rakamsal değerler girilebilen yan yana 2 adet kutucuk oluşsun. Bu kutucuklar bir “+” butonu ile çoğaltılabilsin. “+” butonuna her tıklandığında bir alt satırda yine yan yana “Yüzdelik Dilim Gir” ve “Kar Oranı Gir” kutucukları oluşsun. Oluşan bu 2 kutucuğun yanındada bir tane “-“ butonu olsun. “-“ butonuna tıklandığındada ilgili 2 kutucuk silinsin. Pozisyon yönlerine göre bu kutucuklara girilen değerlerin hesaplama şekilleri:

** “Long” Pozisyonlarda “Yüzdelik Dilim Gir” kutucuğuna girilen değerler pozisyonun toplam koin adeti üzerinden hesaplanacak ve hesaplanan adetler ile birlikte Kar Oranı Gir kutucuğuna yazılan yüzdelik rakam oranında fiyat yükseldiğinde site üzerinde kar olarak hesaplanarak simülasyon motoruna veya borsaya sadece kapatılacak adet miktarı ve kar oranı hesaplanmış fiyat bilgisi gönderilecek. (Örneğin; + butonu ile çoğaltılıp 2 kademe yüzdelik dilim ve kar oranı girildiğini ve bu kademelerin 1. Kademe Yüzdelik Dilim= %40, Kar Oranı= %2,5 - 2. Kademe Yüzdelik Dilim= %60, Kar Oranı= %3 - Pozisyon Giriş Fiyatı= 100 USDT, Koin Adeti= 100 adet olduğunu varsayalım. Buna göre 1. Kademe Kapatılacak Adet= 40 adet, Kapanış Fiyatı= 102,5 USDT – 2. Kademe Kapatılacak Adet= 60 adet, Kapanış Fiyatı= 103 USDT olarak pozisyon kapanış emirleri verilir.)

** “Short” Pozisyonlarda “Yüzdelik Dilim Gir” kutucuğuna girilen değerler pozisyonun toplam koin adeti üzerinden hesaplanacak ve hesaplanan adetler ile birlikte Kar Oranı Gir kutucuğuna yazılan yüzdelik rakam oranında fiyat düştüğünde site üzerinde kar olarak hesaplanarak simülasyon motoruna veya borsaya sadece kapatılacak adet miktarı ve kar oranı hesaplanmış fiyat bilgisi gönderilecek. (Örneğin; + butonu ile çoğaltılıp 3 kademe yüzdelik dilim ve kar oranı girildiğini ve bu kademelerin 1. Kademe Yüzdelik Dilim= %35, Kar Oranı= %2,5 - 2. Kademe Yüzdelik Dilim= %35, Kar Oranı= %3 - 3. Kademe Yüzdelik Dilim= %30, Kar Oranı= %3,5 - Pozisyon Giriş Fiyatı= 100 USDT, Koin Adeti= 100 adet olduğunu varsayalım. Buna göre 1. Kademe Kapatılacak Adet= 35 adet, Kapanış Fiyatı= 97,5 USDT – 2. Kademe Kapatılacak Adet= 35 adet, Kapanış Fiyatı= 97 USDT - 3. Kademe Kapatılacak Adet= 30 adet, Kapanış Fiyatı= 96,5 USDT olarak pozisyon kapanış emirleri verilir.)

**  “Zarar Durdur” Seçeneği: "Zarar Durdur" adında, "Aktif" ve "Pasif" edilebilen bir seçenek olsun. Aktif konuma getirildiğinde, aşağıdaki üç seçenek görünsün:

"Standart Stop Loss"

"Trailing Stop Loss"

"Kademeli Alım"

Pasif konuma getirildiğinde, "Zarar Durdur" seçeneği tamamen devre dışı kalsın ve bu üç seçenek de görünmesin.

**  Standart Stop Loss: "Zarar Durdur" seçeneği aktif durumdayken "Standart Stop Loss" seçeneği seçildiğinde, virgüllü rakamsal değer girilebilen bir kutucuk oluşsun.

Bu kutucuğa girilen değer, zarar oranını yüzde olarak hesaplasın.

Örneğin, kutucuğa "2,5" girilirse, pozisyon %2,5 zarar ettiğinde otomatik olarak kapanacaktır.

**  Trailing Stop Loss: "Trailing Stop Loss" seçeneği seçildiğinde, virgüllü rakamsal değer girilebilen bir kutucuk oluşsun.

Bu kutucuğa girilen değer, "yüzde" olarak hesaplanacak şekilde ayarlansın.

Örneğin, kutucuğa "3" girilirse, Trailing Stop Loss pozisyonu %3 geriden takip edecek ve %3 zarar durumunda pozisyon kapanacaktır.

**  Kademeli Alım: "Kademeli Alım" seçeneği seçildiğinde, aşağıdaki üç farklı kutucuk oluşsun:

**   Zarar Yüzdesi: Virgüllü rakamsal değer girilebilen ve "ortalama maliyetin zarar yüzdesi" olarak hesaplanan bir kutucuk.

Örneğin, bu kutucuğa "7,5" yazıldığında, ortalama maliyet üzerinden %7,5 zarar edildiğinde tetikleme yapılır.

**  Kademe Çarpanı: Virgüllü rakamsal değer girilebilen ve "toplam koin adetinin çarpanı" olarak hesaplanan bir kutucuk.

Örneğin, bu kutucuğa "1,5" yazıldığında, pozisyondaki mevcut koin adedinin 1,5 katı kadar ek alım yapılır.

** Kademe Sayısı: Virgülsüz tam sayı girilebilen ve alım yapılacak maksimum kademe sayısını belirten bir kutucuk.

Örneğin, bu kutucuğa "3" yazıldığında, işlemler maksimum 3 kez tekrarlanacaktır.

**  Risk Yönetimi Seçenekleri:

**  Maksimum Eşzamanlı İşlem Sayısı: Kullanıcıların tam sayı olarak rakamsal değer girebileceği bir kutucuk oluştur. Kullanıcının bu kutucuğun içine yazdığı rakamsal değer, aynı anda açık olabilecek maksimum işlem sayısını belirleyecek. Bu kutucuğa herhangi bir değer girilmemişse, yani bu kutucuk boş bırakılmışsa işlem sayısı konusunda herhangi bir kısıtlama uygulanmayacak. (Örneğin; Kullanıcı bu kutucuğa 5 yazmışsa en fazla 5 işlem açık olabilecek. Eğer halihazırda açık olan 5 işlem varsa, gerekli şartlar ve koşullar gerçekleşse bile yeni bir işlem açılmayacak.)

**  Maksimum Zarar Limiti: Kullanıcıların virgüllü rakamsal değer girebileceği bir kutucuk oluştur. Bu kutucuk içine yazılan değerle kullanıcı botun toplam sermayenin ne kadarını kaybetmesine izin verileceğini kontrol eder. (Örneğin; Kutucuğun içine 10 yazıldığında, maksimum zarar limiti %10 olarak ayarlanmış olur ve bot toplam bakiyenin %10’unu kaybederse tüm işlemleri durdurabilir.)

**  Günlük/Haftalık/Aylık Zarar Limiti: “Günlük”, “Haftalık” ve “Aylık” olacak şekilde yan yana 3 adet virgüllü rakamsal değerler girilebilecek kutucuklar oluştur. Bu kutucukların içlerine yazılan değerler Günlük, Haftalık ve Aylık zaman dilimleri içinde izin verilen maksimum zarar miktarını belirlesin. Bu ayar, belirlenen sürede zarar limiti aşıldığında botun işlem yapmasını durdursun.

**  “STRATEJİYİ KAYDET” Butonu:

**  Strateji Oluştur sayfasının "Pozisyon Emirleri" sekmesinin en altında bir "STRATEJİYİ KAYDET" butonu bulunmalıdır.

**  Kullanıcı bu butona tıkladığında, strateji aşağıda detayları belirtilen şekilde hem "Kayıtlı Stratejiler" sayfasına kaydedilmeli hem de "Strateji Oluştur" sayfasında özet bilgi olarak belirtilmelidir.

**  Kayıtlı Stratejilerin Görüntülenmesi:

**  Kaydedilen strateji, "Strateji Oluştur" sayfasında sekmelerin üst kısmında bir yatay ayırma çizgisi ile ayrılmış bir alanda görünecek şekilde listelenmelidir.

**  Bu alanda, strateji adı özet bilgi şeklinde görüntülenmelidir.

**  Strateji Adı ile lisletelenen her stratejinin yanında “Mod Geçiş Butonu”, “Düzenle” butonu, “Kopyala” butonu ve “Sil” butonu oluşturulsun.

**  Mod Geçiş Butonu:

**  Her strateji adının yanında, "Pozisyon Emirleri" sekmesinde bulunan Test Mod / Gerçek Mod geçiş butonu yer almalıdır.

**  Bu buton, stratejinin kaydedildiği modu (Test Modu veya Gerçek Mod) gösterecek şekilde ayarlanmalıdır.

**  Kullanıcı, bu butonu kullanarak stratejiyi tekrar düzenlemeye gerek kalmadan tek bir tıklama ile modlar arasında hızlıca geçiş yapabilmelidir.

**  Strateji oluştur sayfasında herhangi bir güncelleme yapılmadığı sürece, kaydedilen stratejinin tüm detayları ve ayarları aynı kalmalıdır. Yani aynı ayarlar üzerinde sadece Mod Geçiş işlemi yapılmalıdır.

**  “Düzenle” Butonu:

**  Her strateji adının yanında bir Düzenle butonu bulunmalıdır.

**  Bu butona tıklandığında Strateji Oluştur sayfasındaki sekmeler içerisinde ilgili stratejiye ait kaydedilmiş olan tüm ayarlar sekmelerdeki aynı yerlerine geri çağırılarak düzenlenip tekrar kaydederek güncellenebilmelidir.

**  Böylece bu düzenleme ile hem Kayıtlı Stratejiler sayfasında listelenen, hemde Strateji Oluştur sayfasında Strateji Adı ile özet bilgi şeklinde listelenen ilgili strateji güncellenmiş olur.

**  “Kopyala” Butonu:

**  "Strateji Oluştur" sayfasında kayıtlı her stratejinin yanında bir "Kopyala" butonu bulunmalıdır.

**  Kullanıcı "Kopyala" butonuna tıkladığında, seçilen stratejinin tüm sekmelerde kaydedilmiş tüm ayarları ile birlikte bir kopyası oluşturulmalıdır.

**  Kopya Stratejinin Oluşturulması:

**  Oluşturulan kopya strateji, hem "Kayıtlı Stratejiler" sayfasına hem de "Strateji Oluştur" sayfasında sekmelerin üzerindeki özet bilgi alanına eklenmelidir.

**  Kopya strateji, orijinal stratejiden farklı bir strateji adıyla (örneğin "Strateji Adı - Kopya") kaydedilmelidir.

**  Kopya Stratejinin Mod Ayarı:

**  Kopyalanan strateji, orijinal stratejinin modu ne olursa olsun, her zaman “Test Modu” olarak kaydedilmelidir.

**  Kopya strateji için "Test Modu" aktif olarak ayarlanmalı ve mod geçiş butonunun konumu "Test Modu" olarak görüntülenmelidir.

**  Kopya Stratejinin Özellikleri:

**  Kopya strateji, orijinal stratejinin tüm parametrelerini, ayarlarını, indikatör koşullarını ve pozisyon emirlerini birebir aynı şekilde içermelidir.

**  Kullanıcı, kopya stratejiyi düzenleyebilir, güncelleyebilir ve dilediği zaman "Test Modu"ndan "Gerçek Mod"a geçiş yapabilir.

**  “Sil” Butonu:

**   "Strateji Oluştur" sayfasında kayıtlı her stratejinin yanında bir "Sil" butonu bulunmalıdır.

**  Kullanıcı “Sil” butonuna tıkladığında, ilgili stratejinin tüm sekmelerde kaydedilmiş tüm ayarları ile birlikte hem “Strateji Oluştur” Sayfasından, hemde “Kayıtlı Stratejiler” sayfasından tamemen silinmelidir.

**  “Kayıtlı Stratejiler” Sayfası Tasarımı:

**  Stratejilerin Gruplandırılması:

**  Stratejiler, seçilen borsalara göre gruplandırılmalıdır.

**  Her borsa grubu, kendi başlığı altında alfabetik olarak sıralanmalıdır.

**  Borsa başlıkları da alfabetik olarak sıralanmalı ve ilgili stratejiler kendi borsa grubu altında listelenmelidir.

**  Borsa Başlıklarının Görüntülenmesi:

**  Sayfa, borsa isimlerine göre alfabetik sıralanmış başlıklar içermelidir.

**  Her borsa başlığı, o borsaya ait tüm stratejileri içerir.

**  Örneğin, önce "Binance" başlığı altında o borsaya ait stratejiler, ardından "MEXC" başlığı altında MEXC borsasına ait stratejiler alfabetik olarak sıralanmalıdır.

**  Strateji Gruplarının Görüntülenmesi:

**  Her borsa başlığının altında, ilgili borsaya ait stratejiler listelenmelidir.

**  Her strateji, 2 satır halinde gösterilmelidir:

**  Birinci Satır:

**  Strateji Adı: Sola hizalı şekilde gösterilmeli.

**  Sağa hizalı şekilde, sırasıyla Mod Geçiş Butonu (Test Mod/Gerçek Mod), Düzenle, Kopyala, Sil butonları yan yana yer almalıdır.

**  Mod Geçiş Butonu:

**  Her strateji adının yanında, "Pozisyon Emirleri" sekmesinde bulunan Test Mod / Gerçek Mod geçiş butonu yer almalıdır.

**  Bu buton, stratejinin kaydedildiği modu (Test Modu veya Gerçek Mod) gösterecek şekilde ayarlanmalıdır.

**  Kullanıcı, bu butonu kullanarak stratejiyi tekrar düzenlemeye gerek kalmadan tek bir tıklama ile modlar arasında hızlıca geçiş yapabilmelidir.

**  Strateji oluştur sayfasında herhangi bir güncelleme yapılmadığı sürece, kaydedilen stratejinin tüm detayları ve ayarları aynı kalmalıdır. Yani aynı ayarlar üzerinde sadece Mod Geçiş işlemi yapılmalıdır.

**  “Düzenle” Butonu:

**  Her strateji adının yanında bir Düzenle butonu bulunmalıdır.

**  Bu butona tıklandığında Strateji Oluştur sayfasındaki sekmeler içerisinde ilgili stratejiye ait kaydedilmiş olan tüm ayarlar sekmelerdeki aynı yerlerine geri çağırılarak düzenlenip tekrar kaydederek güncellenebilmelidir.

**  Böylece bu düzenleme ile hem Kayıtlı Stratejiler sayfasında listelenen, hemde Strateji Oluştur sayfasında Strateji Adı ile özet bilgi şeklinde listelenen ilgili strateji güncellenmiş olur.

**  “Kopyala” Butonu:

**  "Strateji Oluştur" sayfasında kayıtlı her stratejinin yanında bir "Kopyala" butonu bulunmalıdır.

**  Kullanıcı "Kopyala" butonuna tıkladığında, seçilen stratejinin tüm sekmelerde kaydedilmiş tüm ayarları ile birlikte bir kopyası oluşturulmalıdır.

**  Kopya Stratejinin Oluşturulması:

**  Oluşturulan kopya strateji, hem "Kayıtlı Stratejiler" sayfasına hem de "Strateji Oluştur" sayfasında sekmelerin üzerindeki özet bilgi alanına eklenmelidir.

**  Kopya strateji, orijinal stratejiden farklı bir strateji adıyla (örneğin "Strateji Adı - Kopya") kaydedilmelidir.

**  Kopya Stratejinin Mod Ayarı:

**  Kopyalanan strateji, orijinal stratejinin modu ne olursa olsun, her zaman “Test Modu” olarak kaydedilmelidir.

**  Kopya strateji için "Test Modu" aktif olarak ayarlanmalı ve mod geçiş butonunun konumu "Test Modu" olarak görüntülenmelidir.

**  Kopya Stratejinin Özellikleri:

**  Kopya strateji, orijinal stratejinin tüm parametrelerini, ayarlarını, indikatör koşullarını ve pozisyon emirlerini birebir aynı şekilde içermelidir.

**  Kullanıcı, kopya stratejiyi düzenleyebilir, güncelleyebilir ve dilediği zaman "Test Modu"ndan "Gerçek Mod"a geçiş yapabilir.

**  “Sil” Butonu:

**   "Strateji Oluştur" sayfasında kayıtlı her stratejinin yanında bir "Sil" butonu bulunmalıdır.

**  Kullanıcı “Sil” butonuna tıkladığında, ilgili stratejinin tüm sekmelerde kaydedilmiş tüm ayarları ile birlikte hem “Strateji Oluştur” Sayfasından, hemde “Kayıtlı Stratejiler” sayfasından tamemen silinmelidir.

**  İkinci Satır:

**  İşlem Tipi: (Spot/Futures)

**  Pozisyon Yönü: (Long/Short)

**  Para Birimi: (Karşıt Para Birimi)

**  Toplam İşlem Adeti: Stratejinin kaydedildiği andan itibaren açılmış toplam işlem sayısını gösterir.

**  Kapanan İşlem Adeti: Stratejinin kaydedildiği andan itibaren açılan ve sonrasında kapatılmış toplam işlem sayısını gösterir.

**  Karlı İşlem Adeti: Karla kapatılmış işlem sayısını gösterir.

**  Zararlı İşlem Adeti: Zararla kapatılmış işlem sayısını gösterir.

**  Detaylı Gör Butonu: İlgili stratejiye ait işlemlerin detaylı listelendiği sayfaya yönlendirme linki içerir.

**  Dinamik Filtreleme ve Arama:

**  Sayfa üzerinde kullanıcıların belirli bir borsadaki stratejileri hızla bulabilmesi için dinamik bir arama ve filtreleme özelliği eklenmelidir.

**  Kullanıcı, borsa adını veya strateji adını yazarak ilgili stratejiye hızla ulaşabilmelidir.

**  Görsel Ayırıcılar ve Arayüz Tasarımı:

**  Her borsa başlığı ve strateji grubu arasında görsel ayırıcılar veya çerçeveler olmalıdır, böylece kullanıcılar her borsa ve strateji grubunu kolayca ayırt edebilir.

**  Kullanıcı deneyimini artırmak için her strateji grubunun başlığının yanında bir çökertme (expand/collapse) düğmesi bulunmalıdır. Kullanıcılar, bu düğmeye tıklayarak borsa gruplarını genişletebilir veya daraltabilir.

**  Özelleştirilebilir Sıralama:

Kullanıcıların stratejileri isteğe bağlı olarak oluşturulma tarihine, son güncelleme tarihine veya mod durumuna göre de sıralayabilmesi için bir sıralama seçeneği eklenmelidir.

**  “Strateji Detay” Sayfası Tasarımı:

**  Detaylı Gör Sayfasına Yönlendirme:

**  Detaylı Gör butonuna tıklandığında, kullanıcı ilgili stratejiye ait işlemlerin listelendiği “Strateji Detay” sayfasına yönlendirilmelidir.

**  İşlemler, açılış tarih ve saatine göre en son açılan en üstte olacak şekilde yeniden eskiye doğru listelenmelidir.

**  İşlemler Listesi:

**  Her işlem satırı aşağıdaki bilgileri içermelidir:

**  İşlem Çifti: (Örneğin; BTC/USDT)

**  Açılış Tarihi: (İşlemin açıldığı tarih)

**  Açılış Saati: (İşlemin Türkiye saatine göre açıldığı saat)

**  Kapanış Tarihi: (İşlemin kapatıldığı tarih)

**  Kapanış Saati: (İşlemin Türkiye saatine göre kapatıldığı saat)

**  İşlem Tutarı: Pozisyon Emirleri sekmesindeki “Pozisyon Büyüklüğü” seçeneğine göre yatırılan tutar.

**  Kaldıraç: Kullanılan kaldıraç miktarı.

**  “Kar Oranı” ve “Zarar Oranı”: “Kar Oranı” ve “Zarar Oranı” yan yana iki ayrı sütun olarak oluşturulacak. Her iki oran içinde ortak hesaplama yapılacak fakat bu hesaplamanın sonucuna göre en son Sonuçların Gösterilmesi maddesinde tarif edildiği gibi Kar Oranı ve Zarar Oranı ayrı ayrı olarak gösterilecek.

**  Kapanış Verilerinin Çekilmesi:

**  API'den veya simülasyon motorundan gelen aşağıdaki verileri al:

Kapanış Fiyatları

Kapanış Adetleri

Açılış Fiyatı

Pozisyondaki Toplam Adet

Kaldıraç

**  Bu veriler her kapanış dilimi için çekilir.

**  Kapanışın Tek Seferde mi Yoksa Kademeli mi Olduğunun Tespiti:

**  Tek Seferde Kapanış: Eğer pozisyonun tamamı tek bir kapanışta gerçekleştiyse, kapanış adeti toplam pozisyon adetine eşittir.

**  Kademeli Kapanış: Eğer pozisyon farklı fiyat ve adetlerle kademeli olarak kapandıysa, kapanış adeti toplam pozisyon adetine eşit değil ve birden fazla kapanış fiyatı vardır.

**  Pozisyon Yönünü Dikkate Alarak Hesaplama:

**  Long Pozisyonlar için Kar/Zarar Hesaplaması:

**  Tek Seferde Kapanış Olmuşsa: Yani pozisyonun kapanış adeti toplam adete eşit olacak şekilde tek seferde pozisyon kapanmışsa

Kar/Zarar Oranı Hesaplama Formülü:

**  Kar/Zarar Oranı = ((Kapanış Fiyatı - Açılış Fiyatı) / Açılış Fiyatı) * 100

Kaldıraçlı Nihai Kar/Zarar Hesaplama Formülü:

**  Nihai Kar/Zarar Oranı = Kar/Zarar Oranı * Kaldıraç

**   Kademeli Kapanış Olmuşsa: Yani pozisyonun kapanış adetleri toplam adetin dilimlere bölünmesi şeklinde kademeli olarak aynı pozisyona ait birden fazla kapanış gerçekleşmiş ise

Ağırlıklı Ortalama Kapanış Fiyatı Hesaplama Formülü:

**  Ağırlıklı Ortalama Kapanış Fiyatı = (Kapanış Fiyatı1 * Kapanış Adedi1 + Kapanış Fiyatı2 * Kapanış Adedi2 + ... + Kapanış FiyatıN * Kapanış AdediN) / (Toplam Kapanış Adedi)

Ağırlıklı Ortalama Kar/Zarar Oranı Hesaplama Formülü:

**  Kar/Zarar Oranı = ((Ağırlıklı Ortalama Kapanış Fiyatı - Açılış Fiyatı) / Açılış Fiyatı) * 100

Kaldıraçlı Nihai Kar/Zarar Hesaplama Formülü:

**  Nihai Kar/Zarar Oranı = Kar/Zarar Oranı * Kaldıraç

**  Short Pozisyonlar için Kar/Zarar Hesaplaması:

**  Tek Seferde Kapanış Olmuşsa: Yani pozisyonun kapanış adeti toplam adete eşit olacak şekilde tek seferde pozisyon kapanmışsa

Kar/Zarar Oranı Hesaplama Formülü:

**  Kar/Zarar Oranı = ((Açılış Fiyatı - Kapanış Fiyatı) / Açılış Fiyatı) * 100

Kaldıraçlı Nihai Kar/Zarar Hesaplama Formülü:

**  Nihai Kar/Zarar Oranı = Kar/Zarar Oranı * Kaldıraç

**  Kademeli Kapanış Olmuşsa: Yani pozisyonun kapanış adetleri toplam adetin dilimlere bölünmesi şeklinde kademeli olarak aynı pozisyona ait birden fazla kapanış gerçekleşmiş ise

Ağırlıklı Ortalama Kapanış Fiyatı Hesaplama Formülü:

**  Ağırlıklı Ortalama Kapanış Fiyatı = (Kapanış Fiyatı1 * Kapanış Adedi1 + Kapanış Fiyatı2 * Kapanış Adedi2 + ... + Kapanış FiyatıN * Kapanış AdediN) / (Toplam Kapanış Adedi)

Ağırlıklı Ortalama Kar/Zarar Oranı Hesaplama Formülü:

**  Kar/Zarar Oranı = ((Açılış Fiyatı - Ağırlıklı Ortalama Kapanış Fiyatı) / Açılış Fiyatı) * 100

Kaldıraçlı Nihai Kar/Zarar Hesaplama Formülü:

**  Nihai Kar/Zarar Oranı = Kar/Zarar Oranı * Kaldıraç

**  Sonuçların Gösterilmesi:

**  Sonuç Pozitif İse:

**  Kar Oranı:

**  Yukarıda Pozisyon yönü ve pozisyon kapanış şekillerine göre formüllerle hesaplanan “Nihai Kar/Zarar Oranı” değeri eğer Pozitif ise bu değer “Kar Oranı” sütununda “yeşil renk” ile gösterilecek.

Yeşil Renkli “Kar Oranı” = Nihai Kar/Zarar Oranı

** Zarar Oranı:

**  Yukarıda Pozisyon yönü ve pozisyon kapanış şekillerine göre formüllerle hesaplanan “Nihai Kar/Zarar Oranı” değeri eğer Pozitif ise “Zarar Oranı” sütununda “siyah renk” ile “0” (Sıfır) değeri gösterilecek.

Siyah Renkli “Zarar Oranı” = 0

** Sonuç Negatif İse:

**  Kar Oranı:

**  Yukarıda Pozisyon yönü ve pozisyon kapanış şekillerine göre formüllerle hesaplanan “Nihai Kar/Zarar Oranı” değeri eğer Negatif ise “Kar Oranı” sütununda “siyah renk” ile “0” (Sıfır) değeri gösterilecek.

Siyah Renkli “Kar Oranı” = 0

**  Zarar Oranı:

**  Yukarıda Pozisyon yönü ve pozisyon kapanış şekillerine göre formüllerle hesaplanan “Nihai Kar/Zarar Oranı” değeri eğer Negatif ise bu değer “Zarar Oranı” sütununda “kırmızı renk” ile gösterilecek.

Kırmızı Renkli “Zarar Oranı” = Nihai Kar/Zarar Oranı

**  Kar Miktarı:

**  İşlem tutarı ile kar oranı çarpılarak hesaplanır (Örneğin; 100 USDT x %15 = 15 USDT).

**  Yeşil renkli rakamlarla gösterilmelidir.

**   Zarar Miktarı:

**  İşlem tutarı ile zarar oranı çarpılarak hesaplanır (Örneğin; 100 USDT x %25 = 25 USDT).

**  Kırmızı renkli rakamlarla gösterilmelidir.

**  Grafiği Gör Butonu:

**  İlgili işlem çiftinin grafik sayfasına yönlendirme linki içerir.
