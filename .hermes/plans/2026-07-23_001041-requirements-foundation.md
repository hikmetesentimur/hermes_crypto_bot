# Hermes Crypto Bot — Gereksinimden Ürüne Geçiş Planı

> **For Hermes:** Uygulamayı görev görev, test odaklı ve her aşamada gereksinim uyumu denetimiyle yürüt.

**Goal:** Kullanıcı senaryosunu eksiksiz, test edilebilir ve güvenli bir ürün gereksinimine dönüştürüp kontrollü bir MVP geliştirmek.

**Architecture:** Borsa adaptörleri ve indikatör eklentileri çekirdek strateji motorundan ayrılacak. Simülasyon ve canlı emir yürütme aynı emir niyeti modelini kullanacak ancak canlı yürütme bağımsız güvenlik kapıları, mutabakat ve kill switch ile korunacak.

**Tech Stack:** Açık sorular cevaplandıktan sonra ADR ile seçilecek; seçim yapılana kadar teknoloji varsayılmayacak.

---

## Aşama 1 — Gereksinim normalizasyonu

1. Özgün DOCX dosyasını değişmez kaynak olarak sakla.
2. İşlevsel gereksinimleri benzersiz `FR-*` kimliklerine ayır.
3. İşlevsel olmayan gereksinimleri `NFR-*` kimliklerine ayır.
4. Her gereksinime öncelik, bağımlılık ve test edilebilir kabul kriteri ekle.
5. Tekrarları birleştir; yazım ve terminoloji hatalarını anlamı koruyarak düzelt.
6. Çelişkileri ve eksik kararları `OPEN_QUESTIONS.md` içine taşı.
7. Kullanıcı cevaplarını `DECISION_LOG.md` dosyasına işle.

**Tamamlanma ölçütü:** Her kaynak madde en az bir gereksinime veya açık soruya izlenebilir; cevapsız konu kesin davranış gibi uygulanmaz.

## Aşama 2 — Güvenlik ve domain tasarımı

1. Spot/futures emir, pozisyon, bakiye, komisyon, funding ve PnL kavramlarını tanımla.
2. Borsa filtrelerini (tick size, step size, minimum notional) adaptör sözleşmesine ekle.
3. Anahtar yönetimi ve yetki modelini tasarla; para çekme yetkisini yasakla.
4. Emir idempotency, retry, timeout ve borsa mutabakat kurallarını tanımla.
5. Risk motoru, kill switch ve canlı moda geçiş kontrol listesini oluştur.
6. Simülasyon gerçekçilik seviyesini ve canlı modla beklenen farkları tanımla.

**Tamamlanma ölçütü:** Gerçek para etkileyen her akış için tehdit, başarısızlık davranışı ve otomatik test senaryosu tanımlanmıştır.

## Aşama 3 — Mimari ve veri modeli

1. Sistem bağlamı ve bileşen diyagramlarını oluştur.
2. Strateji, koşul ağacı, indikatör yapılandırması, emir, fill ve pozisyon şemalarını tasarla.
3. Borsa ve indikatör eklenti sözleşmelerini tanımla.
4. Olay kaydı, denetim izi ve zaman serisi veri saklama politikasını belirle.
5. API ve gerçek zamanlı iletişim sözleşmelerini yaz.

**Tamamlanma ölçütü:** Kritik veri varlıkları ve durum geçişleri şema, invariant ve örneklerle belgelenmiştir.

## Aşama 4 — MVP uygulaması

1. Proje iskeleti ve CI kalite kapılarını kur.
2. Kullanıcı/kimlik doğrulama ve şifreli borsa bağlantılarını uygula.
3. Binance testnet/sandbox adaptörünü uygula.
4. RSI ile ilk indikatör eklentisini uygula.
5. Strateji oluşturucu ve doğrulama katmanını uygula.
6. Simülasyon motoru ve emir yaşam döngüsünü uygula.
7. Kayıtlı stratejiler ve işlem detaylarını uygula.
8. Risk motoru ve acil durdurmayı uygula.

**Tamamlanma ölçütü:** Uçtan uca test modunda, gerçek piyasa verisi üzerinde deterministik ve denetlenebilir bir strateji çalışır; hiçbir canlı emir yolu etkin değildir.

## Aşama 5 — Canlı işlem hazırlığı

1. Borsa sandbox/testnet kabul testlerini tamamla.
2. Property-based ve hata enjeksiyon testlerini tamamla.
3. Yedekleme/geri yükleme ve felaket kurtarma tatbikatını yap.
4. İzleme, alarm ve olay müdahale runbook'larını doğrula.
5. Kısıtlı tutarlı canlı pilot için kullanıcı onayı al.
6. Canlı modu özellik bayrağı ve çift onayla etkinleştir.

**Tamamlanma ölçütü:** Canlı işlem kontrol listesinin tüm maddeleri kanıt bağlantılarıyla geçmiştir ve kullanıcı yazılı olarak onaylamıştır.

## Test yaklaşımı

- Birim: hesaplamalar, validasyon, koşul operatörleri
- Sözleşme: borsa ve indikatör adaptörleri
- Entegrasyon: veri akışı, emir/fill/pozisyon yaşam döngüsü
- Property-based: fiyat, miktar, kaldıraç ve PnL invariantları
- Replay/backtest: kayıtlı piyasa verisinde tekrar üretilebilirlik
- Sandbox: borsa testnet emirleri
- E2E: strateji oluşturma, simülasyon, raporlama
- Güvenlik: secret sızıntısı, yetki yükseltme, rate limit ve bağımlılık taraması

## Başlıca riskler

- Simülasyon ile gerçek yürütme arasındaki fark
- Borsa API ve ürün kurallarının değişmesi
- Double order/retry kaynaklı yinelenen emirler
- Yanlış kaldıraç/PnL ve kademeli alım hesapları
- API anahtarı sızıntısı
- Eksik veya gecikmiş piyasa verisi
- Belirsiz mevzuat, vergi ve sorumluluk kapsamı
