# Karar Günlüğü

Bu dosya yalnızca kullanıcı tarafından açıkça onaylanmış kalıcı kararları içerir. Öneriler ve varsayımlar burada kesin karar olarak kaydedilmez.

## Durum değerleri

- `ONAYLANDI`: Uygulama için bağlayıcı karar
- `DEĞİŞTİRİLDİ`: Daha yeni bir karar tarafından geçersiz kılındı
- `İPTAL`: Kapsamdan çıkarıldı

## Kararlar

### DEC-0001 — MVP tek kullanıcı, mimari çoklu kullanıcıya hazır

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-001
- Karar: İlk ürün sürümü Hikmet Esentimur'un kullanımına yönelik tek kullanıcı olarak geliştirilecek. Sistem sınırları, veri modeli ve yetkilendirme tasarımı gelecekte birden fazla kullanıcının kendi borsa hesaplarını güvenli ve izole biçimde bağlayabileceği yapıya geçişi engellemeyecek.
- Uygulama sonuçları:
  - MVP arayüzünde self-service kayıt, ekip üyeliği, faturalandırma ve çoklu kullanıcı yönetimi bulunmayacak.
  - Sahiplik gerektiren temel kayıtlarda gelecekte tenant/user ayrımına geçişi engelleyecek global varsayımlar yapılmayacak.
  - Borsa hesapları, stratejiler, emir niyetleri, işlemler ve audit olayları sahiplik sınırıyla tasarlanacak.
  - Tek kullanıcı olması kimlik doğrulama, MFA, oturum güvenliği, secret izolasyonu veya audit gereksinimlerini kaldırmayacak.
  - Çoklu kullanıcı özelliği sonraki fazda ayrıca onay ve migration planıyla etkinleştirilecek.
- Gerekçe: İlk sürümün karmaşıklığını ve geliştirme süresini azaltırken, daha sonra pahalı veri modeli/mimari yeniden yazımını önlemek.
- Ödünleşimler: MVP'de bazı tenant-aware alanlar ve sınırlar gelecekteki ihtiyaç için korunacak; ancak kullanılmayan SaaS özellikleri geliştirilmeyecek.
- Önceki karar: Yok

### DEC-0002 — MVP Binance ve MEXC Spot + Futures desteği

- Tarih: 2026-07-23
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili sorular: Q-003; Q-004 henüz açık
- Karar: İlk çalışan sürümde Binance ve MEXC borsalarının hem Spot hem Futures ürünleri desteklenecek.
- Uygulama sonuçları:
  - `ExchangeAdapter` ortak sözleşmesi en az market metadata, semboller, mum/ticker/order-book, bakiye, emir, fill, pozisyon, kaldıraç/marjin ve reconciliation yeteneklerini kapsayacak.
  - Binance ve MEXC ayrı adaptörler olacak; ortak çekirdekte borsaya özel koşul dalları biriktirilmeyecek.
  - Her adaptör desteklediği ürün, emir tipi, time-in-force, post-only, native TP/SL, hedge/one-way, periyot ve test ortamını capability olarak bildirecek.
  - UI yalnız seçilen borsa/ürünün gerçekten desteklediği seçenekleri gösterecek.
  - Ortak davranış sözleşme testleriyle, borsaya özel davranışlar fixture ve uygun sandbox/testnet veya kontrollü mock testleriyle doğrulanacak.
  - Borsalardan birinin özelliği eksikse diğer adaptörün yeteneği yapay olarak kısıtlanmayacak; güvenli fallback veya açık “desteklenmiyor” durumu kullanılacak.
- Gerekçe: Kullanıcı ilk sürümden itibaren iki borsa ve iki işlem türünü birlikte kullanmak istiyor.
- Ödünleşimler: MVP kapsamı, test matrisi, hata yönetimi ve bakım yükü tek borsa yaklaşımına göre belirgin biçimde büyür.
- Önceki karar: Yok

<!--
### DEC-XXXX — Karar başlığı

- Tarih: YYYY-MM-DD
- Durum: ONAYLANDI
- Karar sahibi: Hikmet Esentimur
- İlgili gereksinimler: FR-..., NFR-...
- Karar: ...
- Gerekçe: ...
- Sonuçları / ödünleşimler: ...
- Önceki karar: Yok
-->
