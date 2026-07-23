# Hermes Crypto Bot Agent Talimatları

## Kaynak gerçekliği

Kalıcı proje gerçekliği sohbet hafızası değil, Git deposudur. Çalışmaya başlamadan önce sırayla şunları oku:

1. `docs/README.md`
2. `docs/decisions/DECISION_LOG.md`
3. `docs/requirements/OPEN_QUESTIONS.md`
4. İlgili normalize gereksinim, mimari ve güvenlik belgeleri

## İletişim dili

- Kullanıcıyla bütün soruları, seçenekleri, açıklamaları, uyarıları ve sonuçları açık ve sade Türkçe yaz.
- İngilizce teknik terim kullanmak zorunluysa önce Türkçe karşılığını ver; İngilizce terimi yalnız gerektiğinde parantez içinde belirt.
- Yalnız İngilizce kısaltma veya jargonla seçenek sunma. Örnek: `slippage` yerine “emir fiyat kayması”, `drawdown` yerine “sermayenin zirveden düşüşü”, `fill` yerine “emir gerçekleşmesi”.
- Kod/API tarafından zorunlu İngilizce adları değiştirme; bunları kullanıcıya Türkçe açıklamayla göster.

## Zorunlu çalışma disiplini

- Onaylanmamış varsayımı kesin ürün kararı gibi uygulama.
- Her yeni kullanıcı kararını karar günlüğüne yaz ve ilgili açık soruyu kapat.
- Her gereksinime kimlik ve test edilebilir kabul kriteri ver.
- Kod değişikliklerinde TDD uygula ve gerçek test çıktısı olmadan tamamlandı deme.
- Değişiklikleri conventional commit mesajlarıyla Git'e kaydet ve GitHub'a gönder.
- API anahtarı, secret, özel anahtar veya kullanıcı verisini repoya yazma.
- Para çekme yetkili borsa anahtarlarını hiçbir koşulda kabul etme.

## Canlı işlem güvenlik kapısı

Aşağıdakiler tamamlanmadan canlı emir gönderme yolunu etkinleştirme:

- Kullanıcı tarafından onaylanmış risk politikası
- Şifreli secret yönetimi ve en az ayrıcalık
- Emir idempotency ve borsa mutabakatı
- Kill switch ve güvenli varsayılan durum
- Komisyon, funding, slippage ve borsa filtreleri
- Testnet/sandbox kabul testleri
- İzleme, alarm, audit log ve yedekleme
- Kullanıcının açık canlı pilot onayı

## Dokümantasyon

Özgün kaynaklar `docs/source/` altında değişmeden kalır. Düzeltmeler, ek özellikler ve kesinleştirilen davranışlar normalize gereksinimlere yazılır. Çelişkilerde `docs/README.md` içindeki kaynak önceliğini uygula.
