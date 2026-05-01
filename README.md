# glukhova-dasha.com

Сайт на статическом HTML, раздаётся через Selectel CDN + S3.

## Архитектура

```
Локально                GitVerse                  Selectel
────────               ──────────                 ────────
HTML + api/  ──git──▶  репозиторий  ──workflow──▶  CDN → S3 (странички)

originals/   ──────────── deploy.sh ────────────▶  S3 (картинки)
```

- **HTML + api/** — коммитятся и пушатся в GitVerse. Workflow автоматически заливает в корень S3-бакета.
- **originals/ и thumbs/** — НЕ коммитятся. Загружаются на S3 вручную через `deploy.sh`.

## Как деплоить

### Странички (HTML)
```bash
git add -A
git commit -m "описание изменений"
git push
```
Workflow сам зальёт в S3. Ничего больше делать не нужно.

### Картинки
```bash
./deploy.sh
```
Заливает `originals/` и `thumbs/` (если есть) напрямую в S3.

## DNS

| Домен | Тип | Значение |
|---|---|---|
| `glukhova-dasha.com` | ALIAS | `46434bb5-95ba-4ec8-96e6-35adf8fdd92b.selcdn.net` |
| `www.glukhova-dasha.com` | CNAME | `46434bb5-95ba-4ec8-96e6-35adf8fdd92b.selcdn.net` |

## SSL

Wildcard-сертификат Let's Encrypt (`*.glukhova-dasha.com`), выпускается через:
```bash
certbot certonly --manual --preferred-challenges dns -d "*.glukhova-dasha.com" -d glukhova-dasha.com
```
Сертификат загружается в панель Selectel CDN → ресурс → вкладка «Сертификаты».

## Структура проекта

```
.
├── *.html              # Страницы сайта (коммитятся)
├── api/                # JSON-виджеты (коммитятся)
├── originals/          # Исходные изображения (НЕ коммитятся)
├── deploy.sh           # Ручной деплой картинок на S3
├── .gitverse/          # GitVerse CI/CD workflow
└── .certbot/           # Сертификаты Let's Encrypt (локально)
```
