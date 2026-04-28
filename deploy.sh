#!/bin/bash
set -e
LOG_FILE="deploy.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой сайта ==="

log "1. Git pull..."
git pull origin master >> "$LOG_FILE" 2>&1
log "   ✓ Изменения получены"

log "2. Загрузка на S3..."
rclone sync . ru-3:storage-data \
  --include "*.html" \
  --include "api/**" \
  --progress \
  >> "$LOG_FILE" 2>&1
log "   ✓ Сайт загружен"

log "3. Проверка..."
COMMIT=$(git log -1 --format='%h %s')
log "   HEAD: $COMMIT"
log "   URL: https://glukhova-dasha.com"
log "=== Готово ==="
