# Türkiye Yerli VPS/VDS Sağlayıcı Araştırması

- Araştırma tarihi: 2026-07-25
- Kapsam: Türkiye içinde hizmet veren yerli firmalar
- Proje: Hermes Crypto Bot
- Durum: Satın alma kararı değildir; Q-002 için ön araştırmadır.

## Amaç ve asgari hedef

İlk sürümde web uygulaması, sürekli çalışan arka plan işçileri, PostgreSQL, Redis, borsa WebSocket bağlantıları, emir/risk motoru ve izleme bileşenleri aynı sunucuda çalışabilecektir. Başlangıç hedefi:

- en az 4 sanal işlemci çekirdeği;
- en az 8 GB RAM;
- SSD/NVMe disk;
- tam `root`/SSH erişimi;
- Docker çalıştırabilme;
- sabit genel IP;
- kaynak yükseltme imkânı;
- DDoS koruması ve hizmet seviyesi beyanı;
- sağlayıcı yedeğinden bağımsız, ayrı arıza alanında proje yedeği.

Paylaşımlı hosting bu kullanım için uygun değildir. Canlı işlem, canlı işlem güvenlik kapıları tamamlanıp ayrıca onaylanana kadar kapalı kalacaktır.

## Kısa sonuç

1. **Ana yerli öneri: Alastyr VDS Pro.** Kaynak izolasyonu, kendi Türkiye veri merkezi, VMware altyapısı, kurumsal geçmiş ve açık sunucu sözleşmesi bakımından en dengeli seçenektir.
2. **Kurumsal alternatif: Radore Disk-Elite.** Daha fazla NVMe disk ve güçlü kurumsal veri merkezi işletmecisi avantajı vardır; fiyatı ABD doları cinsindendir ve yedekleme/koruma kalemleri sipariş öncesinde yazılı teyit edilmelidir.
3. **Kampanyalı alternatif: Turhost VDS TR 4.** Teknik altyapısı güçlüdür fakat reklam fiyatı ilk dönem kampanyasına dayanır; standart yenileme fiyatı ve Anti-DDoS maliyeti nedeniyle toplam sahip olma maliyeti yükselir.
4. **Hostixo, Oweb ve IXirHost:** Fiyatları cazip olsa da yayımlanmış sözleşmelerindeki yatırım/kripto ticareti yasakları nedeniyle yazılı istisna/onay alınmadan kullanılmamalıdır.

## Uygun görülen kısa liste

| Sıra | Firma / paket | Kamuya açık kaynaklar | İlan edilen fiyat | Güçlü yanlar | Önemli eksiler / teyitler |
|---:|---|---|---|---|---|
| 1 | [Alastyr VDS Pro](https://www.alastyr.com/vds) | 4 çekirdek, 8 GB RAM, 60 GB SSD, limitsiz trafik, İzmir | Yıllık alımda aylık birim **1.211,33 TL** | VMware, tam izole kaynak, DDoS koruması beyanı, %99,9 hizmet sürekliliği, 7/24 Türkçe destek, ISO 27001/9001, kendi veri merkezi | Satış sayfasındaki günlük imaj yedeği tanıtımına rağmen sözleşme yedek sorumluluğunu müşteriye bırakır. Bağımsız dış yedek zorunludur. Kripto işlem botu için satın alma öncesi yazılı uygunluk teyidi alınmalıdır. |
| 2 | [Radore Disk-Elite](https://radore.com/tr/hizmetler/bulut-sunucu) | 4 çekirdek, 8 GB RAM, 300 GB NVMe SSD | **29,5 USD/ay** | Yerli kurumsal veri merkezi işletmecisi, geniş disk, esnek bulut paneli, 7/24 destek, otomatik yedekleme seçeneği | TL maliyeti kura bağlıdır. Genel IP, trafik, DDoS, yedek kapsamı/fiyatı, KDV ve kripto botu uygunluğu yazılı teyit edilmelidir. |
| 3 | [Turhost VDS TR 4](https://www.turhost.com/sunucu/vps-tr-sunucu/) | 4 vCPU, 8 GB RAM, 200 GB SSD, 200 Mbit, aylık 3 TB adil kullanım | İlk 3 ay **24,99 USD / 1.180,78 TL/ay**; sayfada standart **72,79 USD/ay**; KDV hariç | İstanbul Türk Telekom Gayrettepe veri merkezi, günlük yedek ve 30 günlük zaman makinesi beyanı, güçlü disk/trafik | Kampanya sonrası maliyet yüksektir; Anti-DDoS ek özellik olarak sunulmaktadır. Yenileme, yedek geri dönüşü, sabit IP ve kripto botu uygunluğu yazılı teyit edilmelidir. |
| 4 | [Güzel Hosting TR-VPS-5](https://www.guzel.net.tr/public-cloud.php) | 4 CPU, 8 GB RAM, 100 GB SSD, aylık 10 TB trafik, 100 Mbit | **1.862,90 TL/ay** | Günlük imaj yedeği beyanı, Türkçe destek, kolay ölçekleme ve root erişimi | OpenVZ 7, KVM/VMware kadar güçlü izolasyon sağlamaz; fiyat/performans oranı ilk üçten zayıftır. Kripto botu uygunluğu yazılı teyit edilmelidir. |
| 5 | [Natro XCloud Pro](https://www.natro.com/sunucu-kiralama/vds-sunucu) | 4 vCPU, 8 GB RAM, 200 GB SSD, 100 Mbit sınırsız trafik | İlk 3 ay **1.417,02 TL/ay**; sayfada standart **3.401,51 TL/ay** | Ayrılmış kaynak beyanı, DDoS koruması, %99,9 ağ hizmet seviyesi, geniş disk | İndirim yalnız ilk 3 ay; sonrasında fiyat yüksektir. NVMe yerine SSD belirtilmiştir. Yedekleme, sabit IP ve kripto botu uygunluğu yazılı teyit edilmelidir. |

> Fiyatlar sağlayıcıların kamuya açık sayfalarında araştırma tarihinde görülen değerlerdir. Kampanya, KDV, ödeme dönemi ve döviz kuru nedeniyle ödeme ekranında değişebilir. Satın alma öncesinde toplam ilk yıl ve yenileme maliyeti yazılı olarak doğrulanmalıdır.

## Fiyatı iyi görünmesine rağmen elenen veya şartlı adaylar

### Hostixo VDS S120 — sözleşme engeli

- [Paket](https://www.hostixo.com/sunucu/vds-sunucu/): 8 çekirdek, 8 GB ECC RAM, 120 GB NVMe, 100 Mbit limitsiz trafik, haftalık yedekleme, KVM, DDoS; yıllık alımda aylık birim 1.051,54 TL; KDV ödeme sırasında eklenir.
- [Sunucu sözleşmesi](https://www.hostixo.com/yasal/sozlesmeler/) madde 4.10, sunucu hizmetlerinde “Yatırım siteleri (FOREX, E-Altın Borsası...)” kullanımını yasaklar.
- Sonuç: Projenin web arayüzü ve otomatik işlem amacı bu kapsama alınabilir. Sağlayıcıdan açık yazılı izin alınmadan satın alınmamalıdır.

### Oweb Linux VPS 4 / TR Cloud v4 — açık kripto yasağı

- [Linux VPS 4](https://www.oweb.net.tr/linux-sanal-sunucu-vps): 4 çekirdek, 8 GB RAM, 80 GB NVMe, 1 Gbit sınırsız trafik; ilan edilen kampanyalı fiyat 601,33 TL/ay.
- [TR Cloud v4](https://www.oweb.net.tr/vds-sanal-sunucu): 4 çekirdek, 8 GB RAM, 100 GB NVMe, haftalık yedek; ilan edilen kampanyalı fiyat 1.318,18 TL/ay.
- [Genel kullanım koşulları](https://www.oweb.net.tr/genel-kullanim-sozlesmesi) madde 3.33, “Bitcoin vb. madencileri, takas, değişim, ticareti ile ilgili siteleri” açıkça yasaklar.
- Sonuç: Fiyat avantajına rağmen bu proje için uygun değildir.

### IXirHost Cloud — sözleşme belirsizliği/engeli

- Cloud sunucu teknik olarak paylaşımlı Developer Hosting paketinden daha uygundur.
- Ancak yayımlanmış hizmet koşullarındaki “yatırım siteleri” kısıtı kripto botunu kapsayabilir.
- Sonuç: Sağlayıcıdan açık ve yazılı uygunluk onayı olmadan satın alınmamalıdır.

### EclitGO VPS Pro — satışta değil

- 4 çekirdek, 8 GB RAM, 200 GB SSD, sınırsız trafik, anlık görüntü ve 7 günlük yedekleme alanı için yıllık alımda 11,49 USD/ay ilan edilmiştir.
- Resmî sipariş bağlantısı araştırma tarihinde `Unavailable` (satışta değil) görünmektedir.
- Sonuç: Aktif olarak satın alınabilir olmadığı için kısa listeye alınmamıştır.

### IHS ve Veridyen — karşılaştırılabilir kamu fiyatı doğrulanamadı

- IHS, güçlü Türkiye veri merkezi ve VMware altyapısı sunmaktadır; ancak 4 çekirdek/8 GB yapılandırmasının toplam fiyatı dinamik seçim ekranında net, sabit paket olarak yayımlanmamaktadır.
- Veridyen’in ilgili paket sayfası araştırma sırasında web güvenlik duvarı tarafından engellendiğinden ayrıntılar resmî kaynaktan doğrulanamadı.
- Sonuç: Yazılı teklif alınırsa daha sonra yeniden karşılaştırılabilir.

## Satın alma öncesi zorunlu yazılı sorular

Seçilecek sağlayıcıdan aşağıdaki konuların tamamı destek talebi/e-posta ile yazılı doğrulanmalıdır:

1. Kişisel kullanım için Binance ve MEXC API’lerine bağlanan, para çekme yetkisi olmayan otomatik kripto alım-satım yazılımı VDS üzerinde çalıştırılabilir mi?
2. Sürekli çalışan Docker konteynerleri, PostgreSQL, Redis ve WebSocket bağlantıları için herhangi bir süreç/CPU kısıtı var mı?
3. Tek ve değişmeyen genel IPv4 adresi pakete dahil mi?
4. DDoS koruması pakete dahil mi; kapasitesi ve kapsamı nedir?
5. İlan edilen CPU çekirdekleri ayrılmış mı, paylaşımlı mı; sürekli kullanım politikası nedir?
6. Sağlayıcı yedeği hangi sıklıkta, kaç gün, hangi ayrı arıza alanında tutuluyor; geri dönüş ücretli mi?
7. Paket büyütmede IP veya disk değişiyor mu; yeniden başlatma/kesinti gerekiyor mu?
8. İlan edilen fiyatın KDV dahil toplamı, kampanya sonrası aylık yenilemesi ve bir yıllık toplam maliyeti nedir?
9. Ubuntu 24.04, `root` erişimi, özel güvenlik duvarı ve Docker kurulumu destekleniyor mu?
10. Hizmet sonlandırma/askıya alma halinde veri dışa aktarma ve yedek alma için ne kadar süre tanınıyor?

## Güvenlik ve operasyon notu

Sağlayıcının “ücretsiz yedek” beyanı tek başına yeterli değildir. Üretim mimarisinde:

- PostgreSQL noktasal kurtarma kayıtları ve şifreli tam yedekler ayrı sağlayıcı/arıza alanına gönderilecek;
- geri yükleme düzenli olarak test edilecek;
- canlı emir gönderme kapalı başlayacak;
- sunucu güvenlik duvarında yalnız gerekli girişler açılacak;
- borsa API anahtarlarında para çekme kapalı ve mümkünse sabit IP izin listesi kullanılacak;
- sunucu sağlayıcısı arızası veya sözleşme feshi için taşınabilir Docker yapılandırması ve kurtarma kılavuzu tutulacaktır.

## Karar durumu

Bu belge bir sağlayıcı satın alma/onay kararı değildir. Q-002; bütçe, erişim modeli, yazılı sağlayıcı uygunluk teyidi ve kullanıcının ticari satın alma seçimi tamamlanana kadar `AÇIK` kalır.
