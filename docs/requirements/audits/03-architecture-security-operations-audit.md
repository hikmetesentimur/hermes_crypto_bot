## Genel sonuç

Kaynak senaryo belgesi doğrudan incelendi. Repo kontrol edildi; yalnızca tek satırlık `README.md` ve ilk commit var, uygulama kodu/şema/test/altyapı henüz bulunmuyor. Belge kapsamlı bir işlem stratejisi arayüzü tarif ediyor; ancak üretimde gerçek para yönetecek bir sistem için gerekli mimari, güvenlik, veri bütünlüğü ve operasyonel kurallar büyük ölçüde tanımlanmamış.

Aşağıdaki konular kodlamadan önce karar kaydına dönüştürülmeli.

---

## P0 — Geliştirmeden önce kapatılması gereken kararlar

1. Ürün yalnızca kullanıcının kendi borsa hesabında çalışan bir otomasyon aracı mı, yoksa kullanıcı adına emir ileten/yöneten bir hizmet mi?
2. İlk sürüm paper trading ile mi sınırlı olacak? Gerçek mod ne zaman ve hangi onaylarla açılacak?
3. Tenant modeli nedir: tek kullanıcı, bireysel çoklu kullanıcı, ekip/kurum?
4. Desteklenen ilk borsa, piyasa ve emir tipleri hangileri?
5. Emir yaşam döngüsü, tekrar deneme ve idempotency kuralları nedir?
6. Maksimum risk için platform tarafından aşılamayan sert sınırlar olacak mı?
7. Borsa API sırları kim tarafından ve nerede saklanacak?
8. Kayıt, piyasa verisi ve denetim izi saklama süreleri nedir?
9. Türkiye’de sunulacak hizmetin SPK/KVHS kapsamına girip girmediğine ilişkin hukuki görüş alındı mı?
10. RPO/RTO, erişilebilirlik ve olay müdahale hedefleri nedir?

---

## 1. Sistem mimarisi

**Eksikler**

- UI, strateji değerlendirme, piyasa verisi, emir yürütme ve simülasyonun servis sınırları yok.
- “Borsa klasöründeki API dosyasına bağlanma” yaklaşımı çalışma zamanı sözleşmesi, sürümleme ve izolasyon tanımlamıyor.
- WebSocket kopması, eksik mum, geç veri, saat sapması, rate limit, borsa bakım modu ve yeniden bağlanma davranışları yok.
- Emir durumu için deterministik state machine tanımlanmamış.
- Aynı sinyalin birden çok instance tarafından işlenmesini engelleyecek sahiplik/locking modeli yok.
- Kill switch, reconciliation ve manuel müdahale akışı yok.

**Önerilen varsayılan**

- Başlangıçta modüler monolit + ayrı worker süreçleri:
  - Web/API
  - market-data ingestion
  - strategy evaluator
  - execution/risk worker
  - paper-trading engine
  - scheduler/reconciliation worker
- PostgreSQL ana kayıt sistemi; Redis yalnızca kuyruk, lock ve kısa ömürlü cache.
- Borsa adaptörleri ortak, sürümlü bir `ExchangeAdapter` sözleşmesi uygulasın.
- Emirler kalıcı state machine ile yönetilsin: `CREATED → RISK_APPROVED → SUBMITTING → ACKNOWLEDGED → PARTIALLY_FILLED → FILLED/CANCELLED/REJECTED/UNKNOWN`.
- Her emir niyetinde idempotency key; her strateji/symbol için tek aktif evaluation lease.
- Paper ve live aynı strateji/risk çekirdeğini kullansın; yalnızca execution adapter değişsin.
- Canlı mod için global, kullanıcı, borsa ve strateji seviyesinde kill switch.

**Karar soruları**

- Hedef eşzamanlı kullanıcı/strateji/symbol sayısı ve kabul edilen sinyal gecikmesi nedir?
- Sinyal yalnızca kapanmış mumda mı, yoksa açık mum üzerinde mi üretilecek?
- Borsa yanıtı bilinmiyorsa emir yeniden gönderilecek mi, önce sorgulanacak mı?
- Borsa ile yerel durum uyuşmazlığında hangi kayıt kaynak kabul edilecek?
- Sistem kesintisinde mevcut pozisyonları yönetmeye devam mı edecek, güvenli duruşa mı geçecek?

---

## 2. Veri modeli ve finansal doğruluk

**Eksikler**

- Kullanıcı, tenant, borsa hesabı, strateji sürümü, deployment, sinyal, order intent, exchange order, fill, position, balance snapshot ve audit event modelleri yok.
- Strateji düzenlemenin çalışan stratejiyi geçmişe dönük değiştirmemesi için sürümleme belirtilmemiş.
- Para/adet/fiyat için precision, tick size, lot size, min notional ve yuvarlama politikası yok.
- İşlem ücreti, funding, slippage, spread, kısmi dolum, liquidation, realized/unrealized PnL hesaba katılmıyor.
- Belgede PnL’nin yalnızca fiyat farkı × kaldıraç şeklinde hesaplanması gerçek gerçekleşen kâr/zararı doğru temsil etmez.
- Zamanlar “Türkiye saati” olarak gösteriliyor fakat veri tabanı zaman standardı yok.
- Koşullarda iç içe VE/VEYA, öncelik ve parantez semantiği tanımsız.
- Silme işleminin geçmiş denetim ve işlem kayıtlarına etkisi tanımlanmamış.

**Önerilen varsayılan**

- Tüm zamanlar DB’de UTC; arayüzde kullanıcı saat dilimine çevrilsin.
- Tüm finansal alanlar `Decimal/NUMERIC`; binary float kullanılmasın.
- Her strateji kaydı immutable `strategy_version`; canlı çalıştırma belirli sürüme bağlansın.
- Koşullar tip güvenli ve sürümlü JSON AST olarak saklansın; Python dosyaları/serbest kod DB’den çalıştırılmasın.
- `order_intent`, `exchange_order` ve `fill` ayrı tablolar olsun.
- PnL fill ledger üzerinden; fee, funding ve gerçekleşen miktarlar dahil hesaplanmalı.
- Kullanıcı “silmesi” soft delete/archive olsun; finansal kayıt ve audit izi silinmesin.
- Günlük/haftalık/aylık risk pencereleri için saat dilimi ve reset anı açıkça kaydedilsin.

**Karar soruları**

- Bir strateji güncellendiğinde açık pozisyonlar eski sürümle mi yönetilecek?
- Kademeli alım sonrası stop-loss ve take-profit yeni ağırlıklı maliyete göre yeniden mi hesaplanacak?
- TP yüzdelerinin toplamı tam `%100` olmak zorunda mı?
- Günlük zarar; realized PnL, unrealized PnL, fee ve funding’in hangilerini kapsıyor?
- Piyasa verisi kaynağı ile emir verilen borsa aynı olmak zorunda mı?
- “Normal mum” ve “Japon mum” ayrı kavramlar mı? Renko/çizgi grafikte zaman periyodu ve indikatör semantiği nasıl olacak?

---

## 3. Güvenlik ve işlem emniyeti

**Eksikler**

- Kimlik doğrulama, MFA, oturum güvenliği, CSRF/XSS/SSRF ve rate limiting yok.
- Gerçek moda tek tıkla geçiş son derece riskli; step-up authentication/onay yok.
- Limit order fiyatının yalnız “anlık tahta fiyatı” olması bid/ask tarafını ve price protection’ı tanımlamıyor.
- Market order için belgede tarif edilen fiyat eşitliği kontrolü dolum garantisi vermez.
- API’den gelen sembol/precision değerlerinin güven sınırı ve doğrulaması yok.
- Audit kayıtlarının değiştirilemezliği belirtilmemiş.

**Önerilen varsayılan**

- Passkey/WebAuthn veya TOTP MFA; canlı moda geçişte yeniden doğrulama.
- Canlı moda geçiş: ön kontrol özeti + risk uyarısı + yazılı onay + kısa soğuma süresi.
- Yeni kullanıcı ve yeni API hesabı varsayılan olarak paper-only.
- Platform çapında sert sınırlar: maksimum kaldıraç, pozisyon büyüklüğü, günlük zarar, emir frekansı ve fiyat sapması.
- Withdraw yetkili API anahtarları kesinlikle reddedilsin.
- En az ayrı API/worker ağ zonları; egress yalnız izinli borsa uçlarına.
- Append-only audit log; kritik olaylar hash-chain/WORM hedefe aktarılabilir.
- Bağımlılık/SAST/secret/container taraması CI’da zorunlu.

**Karar soruları**

- Kullanıcının belirlediği risk limitlerinin üstünde platform sert tavanları ne olacak?
- Live moda geçiş için yalnız kullanıcı onayı yeterli mi, ekip hesabında çift onay mı gerekli?
- Olağandışı işlemde otomatik durdurma kriterleri nelerdir?
- Manuel pozisyon kapatma ve tüm açık emirleri iptal etme yetkisi kimlerde olacak?

---

## 4. Kullanıcı ve rol yönetimi

**Eksikler**

- Kullanıcı kaydı, doğrulama, parola kurtarma, MFA ve hesap kilitleme yok.
- Tenant izolasyonu tanımlanmamış.
- Destek/admin personelinin kullanıcı sırlarına ve işlemlerine erişimi belirsiz.
- Yetkilendirme yalnız ekran düzeyinde düşünülmüş; kaynak/eylem düzeyi izin modeli yok.

**Önerilen varsayılan**

- Bireysel MVP’de `user` ve sınırlı `support`; kurumsal kullanım varsa `owner`, `admin`, `trader`, `viewer`, `auditor`.
- RBAC + kaynak sahipliği kontrolü; her sorguda `tenant_id`.
- Support varsayılan olarak API sırrını göremez, emir veremez, live moda geçemez.
- Kritik yönetici işlemlerinde MFA, gerekçe ve audit kaydı.
- Kullanıcı/ekip üyeliği iptalinde aktif oturumlar ve ilgili erişimler anında sonlandırılsın.

**Karar soruları**

- Ekip hesapları MVP kapsamına dahil mi?
- Trader strateji oluşturabilir fakat live moda alamaz şeklinde görev ayrımı isteniyor mu?
- Destek ekibi kullanıcı hesabına “impersonation” yapabilecek mi; yapılacaksa onay ve görünür banner olacak mı?
- Kullanıcı hesabı kapatıldığında açık pozisyonlara ne olacak?

---

## 5. Borsa API anahtarları

**Eksikler**

- Belgedeki “borsa klasörüne API bilgileri kaydedilsin” ifadesi sırların kaynak koduna/dosya sistemine yazılması riski taşıyor.
- Anahtar şifreleme, rotasyon, doğrulama, maskeleme ve silme prosedürü yok.
- Testnet/live credential ayrımı ve subaccount desteği yok.
- Borsa yetkilerinin nasıl kontrol edileceği belirtilmemiş.

**Önerilen varsayılan**

- Sırlar repo, config dosyası, log, hata mesajı veya istemci depolamasına asla yazılmasın.
- KMS/Vault ile envelope encryption; DB’de yalnız ciphertext ve metadata.
- Anahtar yalnız execution worker içinde, kısa süreyle plaintext olsun.
- Read + trade izinleri; withdrawal kapalı; mümkünse IP allowlist ve ayrı subaccount.
- Arayüz anahtarı bir kez alır, sonra yalnız maskeli son karakterleri gösterir.
- Eklenirken yetki/canlı-testnet/borsa hesabı doğrulaması yapılsın.
- Periyodik rotasyon hatırlatması ve şüphede anında revoke/runbook.

**Karar soruları**

- Cloud KMS mi, self-hosted Vault mu kullanılacak?
- Kullanıcı kendi anahtarını mı getiriyor, yoksa platform adına borsada OAuth benzeri bağlantı var mı?
- IP allowlist için sabit egress IP sağlanabilecek mi?
- Bir anahtar iptal olduğunda açık pozisyonların güvenli yönetimi nasıl yapılacak?

---

## 6. Gözlemlenebilirlik

**Eksikler**

- Log, metric, trace, alarm, SLO ve olay korelasyonu yok.
- Kullanıcıya “neden işlem açılmadı?” açıklaması sunulmuyor.
- Piyasa verisi gecikmesi veya strateji worker sessizce durduğunda tespit mekanizması yok.

**Önerilen varsayılan**

- OpenTelemetry tabanlı trace; yapılandırılmış JSON log.
- Korelasyon alanları: `tenant_id`, `strategy_version_id`, `signal_id`, `order_intent_id`, `exchange_order_id`; sırlar ve kişisel veriler maskeli.
- Temel metrikler: veri yaşı, websocket yeniden bağlanma, sinyal gecikmesi, order ack latency, reject oranı, reconciliation farkı, queue lag, risk-stop sayısı.
- Alarm öncelikleri ve runbook bağlantıları.
- Kullanıcı arayüzünde strateji heartbeat’i, son veri zamanı, son değerlendirme ve engellenen işlem nedeni.
- Varsayılan SLO önerisi: API `%99,9`; kritik worker heartbeat ve stale-market-data için saniyeler seviyesinde alarm.

**Karar soruları**

- 7/24 nöbet olacak mı; alarmı kim karşılayacak?
- Kabul edilen maksimum piyasa verisi yaşı ve emir onay gecikmesi nedir?
- Kullanıcıya hangi teknik ayrıntılar ve olay geçmişi gösterilecek?
- Log/metric/trace saklama süreleri nedir?

---

## 7. Dağıtım ve operasyon

**Eksikler**

- Ortamlar, CI/CD, migration, rollback, secret injection ve network politikası yok.
- Çoklu instance çalışmada emirlerin iki kez gönderilmesini önleyen dağıtım kuralı yok.
- Sağlık kontrolü yalnız HTTP erişimine indirgenemez; worker ve borsa bağlantı sağlığı tanımsız.

**Önerilen varsayılan**

- Ayrı `dev/staging/prod`; staging yalnız testnet/paper credential kabul etsin.
- Immutable container image, pinlenmiş bağımlılıklar ve SBOM.
- CI: lint, type check, unit/integration/security test, migration dry-run.
- Prod dağıtımında onay, canary/rolling deployment ve otomatik rollback.
- DB migration’ları backward-compatible expand/contract yaklaşımıyla.
- Readiness; DB, queue ve gerekli bağımlılıkları kontrol etsin; liveness yalnız process yaşamını.
- Egress allowlist, özel DB ağı, TLS ve least-privilege servis hesapları.

**Karar soruları**

- Hedef platform managed container mı, Kubernetes mi, tek sunucu mu?
- Hangi bölgede barındırılacak ve veri yurtdışına aktarılacak mı?
- Sıfır kesinti gerekli mi?
- Borsa adaptörü değişiklikleri diğer adaptörlerden bağımsız yayımlanmalı mı?

---

## 8. Yedekleme ve felaket kurtarma

**Eksikler**

- RPO/RTO, yedek kapsamı, şifreleme, restore testi ve bölgesel arıza planı yok.
- Cache/queue içeriği ile DB kaydı arasındaki kurtarma semantiği belirsiz.
- Yedekten dönünce borsadaki gerçek durumla reconciliation süreci yok.

**Önerilen varsayılan**

- PostgreSQL PITR + günlük tam yedek; ayrı hesap/bölgede şifreli ve immutable kopya.
- Başlangıç hedefi: `RPO ≤ 5 dk`, `RTO ≤ 60 dk`; iş ihtiyacına göre onaylanmalı.
- Aylık otomatik restore testi, üç aylık DR tatbikatı.
- KMS anahtarlarının bağımsız kurtarma prosedürü.
- Restore sonrası live trading otomatik başlamasın; önce borsa emir/pozisyon/bakiye reconciliation ve yetkili onayı.

**Karar soruları**

- Finansal/audit kayıtlar için zorunlu saklama süresi kaç yıl?
- Bölge kaybında otomatik failover mı, manuel güvenli geçiş mi?
- Felaket anında açık pozisyonları kim ve hangi kanal üzerinden yönetecek?
- Kullanıcılar strateji verilerini dışa aktarabilecek mi?

---

## 9. Test stratejisi

**Eksikler**

- Hiç test artefaktı veya kabul kriteri yok.
- Simülasyonun fill modeli tanımlanmadığı için test modu yanıltıcı olabilir.
- Race condition, duplicate signal, partial fill ve restart senaryoları kapsanmıyor.

**Önerilen varsayılan**

- Unit: indikatörler, AST, precision, risk ve PnL.
- Property-based test: long/short simetrisi, yuvarlama, TP toplamı, risk limitleri.
- Contract test: her exchange adapter için kayıtlı fixture ve sandbox.
- Integration: DB + queue + mock exchange.
- Deterministik replay/backtest: zaman damgalı market-data fixture’ları.
- Paper modeline spread, fee, slippage, latency, partial fill ve maker/taker davranışı eklensin.
- Failure/chaos testleri: timeout, 429, WebSocket kopması, process restart, duplicate event, unknown order status.
- E2E: strateji oluşturma, taslak koruma, kopyalama, live onayı, silme/arşivleme.
- Finansal çekirdek için yüksek branch coverage; yalnız genel coverage yüzdesine güvenilmesin.

**Karar soruları**

- Paper trading yalnız anlık ticker mı, order book mu kullanacak?
- Backtest kapsamda mı; varsa look-ahead bias ve veri kalitesi nasıl kontrol edilecek?
- Desteklenen borsalar testnet sağlıyor mu?
- Bir sürümün live’a çıkması için zorunlu kabul senaryoları nelerdir?

---

## 10. Mevzuat ve uyum

**Eksikler**

- Hizmetin hukuki niteliği, hedef ülke, kullanıcı sözleşmesi ve risk açıklaması yok.
- KVKK veri envanteri, işleme amacı/hukuki sebep, saklama-imha ve ihlal prosedürü yok.
- KYC/AML, yaptırım taraması ve işlem izleme gerekip gerekmediği belirlenmemiş.
- Pazarlama ifadeleri, yatırım tavsiyesi sınırı ve kullanıcı şikâyet süreci yok.

**Önerilen varsayılan**

- Gerçek emir özelliği açılmadan önce Türkiye’de sermaye piyasası/fintek uzmanından kapsam görüşü alınsın.
- Özellikle “kullanıcı adına emir iletme/yönetme” işlevinin 6362 sayılı Kanun ve SPK’nın 13 Mart 2025 tarihli III-35/B.1 ve III-35/B.2 tebliğleri karşısındaki durumu yazılı değerlendirilmeden varsayılmasın.
- KVKK için veri envanteri, aydınlatma, veri minimizasyonu, tedarikçi sözleşmeleri, saklama-imha ve ihlal müdahale planı oluşturulsun.
- Hizmet KVHS sayılırsa MASAK müşteri tanıma, uzaktan kimlik tespiti, sıkılaştırılmış tedbirler ve Travel Rule yükümlülükleri ayrıca ele alınmalı.
- Finansal kayıtlar mevzuat incelemesi tamamlanana kadar kullanıcı tarafından fiziksel olarak silinmesin; arşivlensin.
- “Kâr garantisi” çağrışımı yapılmasın; risk ve simülasyon sınırlılıkları açık gösterilsin.

**Karar soruları**

- Şirket ve kullanıcılar hangi ülkelerde olacak?
- Sistem yalnız yazılım sağlayıcı mı, emir ileten/yöneten aracı mı?
- Kullanıcı fonuna veya saklama anahtarına hiçbir aşamada erişilecek mi?
- Bireysel tüketici mi, profesyonel müşteri mi hedefleniyor?
- VERBİS, yurtdışı veri aktarımı, KYC/AML ve kayıt saklama yükümlülükleri için hukuk görüşü kimden alınacak?

Referanslar: SPK’nın 13.03.2025 tarihli KVHS duyurusu ve III-35/B.1/B.2 tebliğleri; KVKK Kişisel Veri Güvenliği Rehberi; MASAK KVHS Rehberi.

---

## 11. UX ve güvenli kullanım

**Eksikler**

- Çok uzun tek form, iç içe modallar ve tek tık live toggle hata riskini artırıyor.
- Sekme verisinin yalnız istemci belleğinde tutulması tarayıcı kapanması/çökmesinde kayıp doğurur.
- Klavye erişimi, ekran okuyucu, mobil kullanım ve renk körlüğü düşünülmemiş.
- Kritik işlem sonuçları, bekleyen emirler ve kısmi dolumlar görünür değil.
- “İşlem açılmadı” nedenleri ve validation özeti yok.

**Önerilen varsayılan**

- Üç aşamalı wizard + otomatik sunucu taraflı taslak kaydı ve sürüm çakışması kontrolü.
- Live mode toggle yerine açık eylem: “Canlıya al”; etkilerin özeti ve MFA onayı.
- İleri seviye ayarları progressive disclosure ile aç.
- Stratejiyi insan tarafından okunabilir özet ve koşul ağacıyla göster.
- Kaydetmeden önce exchange capability, precision, risk ve çelişkili koşul doğrulaması.
- Silme için impact özeti; açık pozisyon varsa doğrudan silme yerine durdur/arşivle.
- Renk tek gösterge olmasın; metin/ikon kullanılsın.
- Kullanıcı panelinde: veri güncelliği, strateji durumu, son sinyal, engellenme nedeni, açık emir/pozisyon ve acil durdurma.

**Karar soruları**

- Mobilde yalnız izleme mi, canlı işlem yönetimi de olacak mı?
- Taslaklar cihazlar arasında senkronize edilecek mi?
- Stratejiyi silmek açık emir ve pozisyonları nasıl etkileyecek?
- Kullanıcı live moda geçmeden önce paper trading süresi/işlem sayısı şartı olacak mı?
- Uyarılar uygulama içi, e-posta, SMS veya push kanallarından hangileriyle verilecek?

---

## 12. Belgede düzeltilmesi gereken alan kuralları

- Futures pozisyon büyüklüğünde “teminat × kaldıraç” notional değerdir; gerçek bakiye etkisi, fee, maintenance margin ve liquidation ayrıca modellenmeli.
- Market order belirtilen fiyattan gerçekleşmez; fiyat koruması/slippage limiti veya marketable limit yaklaşımı kararlaştırılmalı.
- Post-only emir, fiyat piyasayı çaprazlarsa reddedilebilir; yeniden fiyatlama politikası gerekli.
- Kaldıraç her borsa/symbol için 1–100 olmayabilir; capability API’sinden sınır alınmalı.
- Spot her zaman “Long” gibi modellenebilir, fakat short/margin spot ayrı ürün olarak açıkça kapsam dışı bırakılmalı.
- “Maksimum işlem sayısı boşsa sınırsız” ve stop-loss’un pasif olabilmesi tehlikeli varsayılanlardır. Canlı modda platform sert sınırı ve zorunlu risk kontrolü önerilir.
- “Tüm stratejiyi tamamen sil” denetim/finans kayıtlarıyla çelişir; arşiv ve saklama politikası uygulanmalı.
- Testten gerçeğe parametreleri aynen taşımak yeterli değildir; bakiye, precision, leverage, permission, symbol availability ve açık pozisyon kontrolleri yapılmalı.

---

## Teslim özeti

- **Yapılan:** Kaynak DOCX’in tamamı, repo içeriği ve Git durumu incelendi; eksikler 12 alanda varsayılanlar ve uygulanabilir karar sorularına dönüştürüldü.
- **Bulgu:** Repo henüz boş başlangıç durumunda (`README.md` dışında uygulama yok). En kritik boşluklar execution state machine, risk sınırları, API sırrı yönetimi, strateji sürümleme, reconciliation ve hukuki kapsam.
- **Dosya değişikliği:** Yok.
- **Sorun:** Teknik uygulama mevcut olmadığı için analiz gereksinim/risk incelemesi düzeyindedir; kod doğrulaması yapılamadı.