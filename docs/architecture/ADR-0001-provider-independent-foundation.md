# ADR-0001 — Sağlayıcıdan Bağımsız Modüler Monolit ve Teknoloji Temeli

- **Durum:** Kabul edildi
- **Tarih:** 2026-07-25
- **Karar dayanağı:** Kullanıcının barındırma sağlayıcısı kesinleşmeden geliştirmeye devam etme talimatı; DEC-0001, DEC-0002, DEC-0004, DEC-0067, DEC-0089 ve DEC-0104

## Bağlam

OVHcloud ve Alastyr değerlendirmeleri sürmektedir. Sağlayıcı seçimi; ağ erişim modeli, sabit çıkış IP'si, güvenlik duvarı, gizli bilgi yöneticisi, yedekleme hedefleri ve sayısal hizmet seviyelerini etkiler. Buna karşılık strateji, risk, emir niyeti, simülasyon, muhasebe ve API sözleşmeleri belirli bir sağlayıcıya bağlı olmamalıdır.

İlk sürüm tek kullanıcı, en fazla 50 çalışan strateji ve strateji başına 200 işlem çifti hedefler. Bu ölçekte erken mikroservis ayrımı; dağıtım, gözlemleme, veri tutarlılığı ve hata ayıklama yükünü gereksiz artırır.

## Karar

1. İlk sürüm **modüler monolit** olarak geliştirilecektir. Web/API, piyasa verisi, strateji değerlendirme, risk, simülasyon, yürütme ve mutabakat sınırları kod içinde açık modüller ve portlar üzerinden ayrılacaktır.
2. Uzun süren veya sürekli işler aynı kod tabanından ayrı worker süreçleri olarak çalıştırılabilecektir; modüller arası finansal gerçeklik gizli ağ çağrılarıyla parçalanmayacaktır.
3. Backend Python `>=3.12,<3.14` ve FastAPI üzerinde kurulacaktır. Alan çekirdeği FastAPI, ORM ve borsa SDK'larından bağımsız saf Python olacaktır.
4. Kalıcı kayıt sistemi PostgreSQL olacaktır. Fiyat, miktar, para, oran, ücret ve kâr/zarar alanları ondalık/NUMERIC olarak saklanacaktır.
5. Redis yalnız kuyruk, kısa süreli önbellek, hız sınırı ve dağıtık kilit gibi yeniden üretilebilir görevlerde kullanılacaktır. Emir, gerçekleşme, pozisyon, bakiye veya denetim gerçeğinin tek kaynağı olmayacaktır.
6. Yönetim paneli React + TypeScript ile geliştirilecektir. UI hiçbir canlı güvenlik kararının yetkili kaynağı olmayacaktır.
7. Yerel ve test ortamı Docker Compose ile yeniden üretilebilir olacaktır. Uygulama belirli OVHcloud/Alastyr ürününe veya özel API'sine bağlanmayacaktır.
8. Sağlayıcıya özgü KMS/gizli bilgi yöneticisi, yedekleme, ağ ve gözlemleme entegrasyonları port/adapter olarak dağıtım katmanında seçilecektir.
9. Canlı emir gönderme yolu özellik bayrağıyla varsayılan kapalı olacak; bu başlangıç paketinde gerçek borsa anahtarı veya canlı yürütme kodu bulunmayacaktır.

## Sonuçlar

### Olumlu

- Sağlayıcı seçimi beklenmeden çekirdek geliştirme ve testler ilerler.
- Finansal alan mantığı altyapı bağımlılıkları olmadan birim test edilebilir.
- Tek dağıtım birimi, ilk sürümde mutabakat ve operasyon karmaşıklığını azaltır.
- PostgreSQL/Redis/Docker her iki aday sağlayıcıda da taşınabilir biçimde çalışabilir.

### Olumsuz / ödünleşimler

- Modüler sınırlar disiplinle korunmazsa monolit içinde sıkı bağımlılık oluşabilir.
- Çok yüksek ölçek veya yüksek hızlı işlem hedefi ileride ayrı servis/altyapı kararı gerektirebilir.
- KMS, sabit IP, yedekleme sıklığı, RPO/RTO ve dış erişim modeli sağlayıcı seçimine kadar tamamlanamaz.

## Güvenlik sınırı

Bu karar üretime dağıtım veya canlı işlem onayı değildir. Q-002, Q-089, Q-101 ve Q-105–Q-107 açık kalır. Canlı işlem güvenlik kapısının bütün maddeleri tamamlanmadan gerçek emir yolu etkinleştirilemez.
