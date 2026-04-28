#!/bin/bash
set -e
LOG_FILE="deploy.log"
SITE=${1:-glukhova-dasha}
REMOTE="ru-3"
BUCKET="storage-data"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой: $SITE ==="

log "1. Commit & Push в GitVerse..."
git add -A
git commit -m "update $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || log "   → нет новых изменений"
git push 2>&1 | tee -a "$LOG_FILE"
log "   ✓ Git push готов"

log "2. Загрузка на S3..."
rclone sync . "$REMOTE:$BUCKET/$SITE" \
  --include "*.html" \
  --include "api/**" \
  --progress \
  >> "$LOG_FILE" 2>&1
log "   ✓ Сайт загружен"

log "3. Проверка..."
COMMIT=$(git log -1 --format='%h %s')
log "   HEAD: $COMMIT"
log "   URL: https://$BUCKET.storage.selcloud.ru/$SITE/index.html"
log "=== Готово ==="
