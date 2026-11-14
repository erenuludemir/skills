# Kullanıcının 14.11.2026 tarihli kurulum rehberindeki operatif talimatlar

Bu belge kullanıcının sağladığı `find-skills` yönergelerini, sırasını ve içerik kapsamını koruyan bir kayıt ve uygulanacak kontrol zinciridir. Tam kullanıcı mesajı, sohbet kaynağında saklıdır. Buradaki yeniden yapılandırılmış sürüm **birebir mesaj kopyası olduğunu iddia etmez**.

## 1 · Ne yapıyor
İsteğin alan ve görevini çözümler; skills.sh sıralamasından başlayarak `npx skills find` ile arar; kurulum sayısı, kaynak ve GitHub yıldızıyla değerlendirme yapar; kullanıcıya sonuç sunar; kullanıcı seçimiyle kurar; eşleşme yoksa bunu belirtir.

## 2 · Gereken iki bileşen
Claude Code ve Node.js >=22.20.0. `node --version` ile kontrol edilir; ChatGPT becerisi ile Claude Code kurulumu ayrı işlemlerdir.

## 3 · Tek komut
`DISABLE_TELEMETRY=1 npx skills add vercel-labs/skills --skill find-skills -g -a claude-code --copy -y`

## 4 · Doğrulama
`$HOME/.claude/skills/find-skills/SKILL.md` kontrol edilir, `DISABLE_TELEMETRY=1 npx skills list -g` çalıştırılır, yeni Claude Code oturumunda skill çağrılması doğrulanır.

## 5 · Altı deneme
1. Instagram/LinkedIn içerikleri için en iyi üç skill'i ve kurulum sayısını ara.
2. React performansı için skill ara.
3. Derin araştırma için skill ara.
4. Kaynak, indirme ve GitHub yıldızı karşılaştırması yap.
5. Kullanıcının seçtiği ilk skill'i yetkili inceleme ve onaydan sonra kur.
6. Kurulu skill'leri listele, güncellemeleri kontrol et.

## 6 · Kurulum öncesi üç ölçü
Tercih: 1000+ kurulum, doğrulanabilir yayımlayıcı, 100+ GitHub yıldızı; mutlaka SKILL.md ve yardımcı betik içerik denetimi.

## 7 · Bakım
`npx skills list -g`; `npx skills check`; `npx skills update -g` (yetkili yazma); `npx skills remove find-skills` (yetkili silme); `npx skills find <query>`; `npx skills use <repo>@<skill>` (harici içerik indirir ve bazı modlarda ajan çalıştırır).

## 8 · Takılırsan
`npx` bulunamıyor → Node kurulumunu ayrıca ele al; sürüm eski → yükseltme planı; skill görünmüyor → konum ve oturum doğrula; skill aranmıyor → arama talebini açık belirt.

## 9 · İkinci kullanıcı rehberi
macOS komutu, `--copy`, telemetri kapatma, global kapsam, altı QuantumAI alanında deney ve Plugin Creator ile ChatGPT entegrasyon ayrımı korunur. Node sürüm denetimi yalnızca string basmakla kalmaz; >=22.20 koşuluyla fail-closed çalışır. Kurulum, izole otonom yapıya değil açık kullanıcı yetkisine bağlıdır.

Kaynak: Bu sohbette kullanıcı tarafından sağlanan iki Türkçe rehber ve Vercel upstream belge içeriği (2026-11-14 erişimi).
