#!/bin/bash
set -e
LOG_FILE="deploy.log"
SITE=${1:-glukhova-dasha}
BUCKET="storage-data"
REMOTE="ru-3"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой: $SITE ==="

log "1. Git pull..."
git pull origin master >> "$LOG_FILE" 2>&1
log "   ✓ Изменения получены"

log "2. Загрузка на S3..."
rclone sync . "$REMOTE:$BUCKET/$SITE" \
  --include "*.html" \
  --include "api/**" \
  --progress \
  >> "$LOG_FILE" 2>&1

# Общие ресурсы (один раз)
if [ "$SITE" = "glukhova-dasha" ]; then
  log "   → Общие модули..."
  rclone sync st-p.rmcdn1.net "$REMOTE:$BUCKET/st-p.rmcdn1.net" --progress >> "$LOG_FILE" 2>&1
  rclone sync c-p.rmcdn.net "$REMOTE:$BUCKET/c-p.rmcdn.net" --progress >> "$LOG_FILE" 2>&1
fi

log "   ✓ Сайт загружен"

log "3. Проверка..."
COMMIT=$(git log -1 --format='%h %s')
log "   HEAD: $COMMIT"
log "   URL: https://$BUCKET.storage.selcloud.ru/$SITE/index.html"
log "=== Готово ==="
