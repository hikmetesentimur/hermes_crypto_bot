# Proje Dokümantasyonu

Bu klasör, projenin kalıcı ve sürüm kontrollü hafızasıdır. Sohbetlerde alınan bütün kalıcı kararlar ilgili dosyalara işlenir.

## Kaynakların öncelik sırası

Çelişki halinde aşağıdaki sıra uygulanır:

1. `docs/decisions/DECISION_LOG.md` içindeki kullanıcı tarafından onaylanmış kararlar
2. Güncel, normalize edilmiş ürün gereksinimleri ve kabul kriterleri
3. Açık sorular için kaydedilmiş geçici varsayımlar
4. `docs/source/` altındaki özgün kullanıcı belgeleri
5. Sohbet özetleri ve çalışma notları

Özgün kaynak belge değiştirilmez. Düzeltmeler ve yeni özellikler normalize edilmiş gereksinim belgelerine yazılır.

## Dizin yapısı

- `source/`: Özgün belgeler ve anlamı değiştirilmemiş metin çıkarımları
- `requirements/`: Gereksinimler, kapsam denetimi, açık sorular ve kabul kriterleri
  - `requirements/REQUIREMENTS_AUDIT.md`: Birleşik denetim ve düzeltme özeti
  - `requirements/audits/`: Üç bağımsız denetimin eksiksiz ham raporları
- `decisions/`: Kullanıcı tarafından onaylanmış kararların günlüğü
- `architecture/`: Sistem mimarisi, veri modeli ve entegrasyon kararları
- `operations/`: Dağıtım, yedekleme, izleme ve olay müdahalesi
- `security/`: Tehdit modeli, anahtar yönetimi ve canlı işlem güvenlik kapıları

## Değişiklik disiplini

- Her kalıcı kullanıcı kararı karar günlüğüne tarih ve kimlik ile eklenir.
- Açık soru cevaplandığında soru kapatılır ve ilgili karar kimliğine bağlanır.
- Gereksinimler benzersiz kimlik, önem derecesi ve test edilebilir kabul kriteri taşır.
- Gerçek para etkileyen davranışlar yalnızca dokümante edilmiş ve test edilmiş kurallardan üretilir.
- Kod, test, dokümantasyon ve migrasyon değişiklikleri aynı Git geçmişinde tutulur.
