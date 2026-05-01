# glukhova-dasha.com

Сайт на статическом HTML, раздаётся через Selectel CDN + S3.

## Архитектура

```
Локально                                   Selectel
────────                                   ────────
HTML + api/ + o/ + modules/ + fonts/ ────────────▶  S3 → CDN
                      ↑
                  deploy.sh
```

Всё деплоится через `./deploy.sh` локально.

## Как деплоить

```bash
./deploy.sh
```
Заливает всё: HTML-страницы, api/, картинки (o/), модули (modules/), шрифты (fonts/).

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
├── originals/          # Исходные изображения (НЕ коммитятся, деплой в папку o/)
├── o/                  # Изображения на S3 (НЕ коммитятся)
├── modules/            # JS вьювер Readymag (НЕ коммитятся)
├── fonts/              # Шрифты (НЕ коммитятся)
├── deploy.sh           # Ручной деплой o/ + modules/ + fonts/ на S3
├── .gitverse/          # GitVerse CI/CD workflow
└── .certbot/           # Сертификаты Let's Encrypt (локально)
```
