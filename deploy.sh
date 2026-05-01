#!/bin/bash
set -e
LOG_FILE="deploy.log"
REMOTE="ru-3"
BUCKET="storage-data"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой КАРТИНОК на S3 ==="

log "1. Загрузка картинок (o/)..."
if [ -d o ]; then
  rclone sync o "$REMOTE:$BUCKET/o" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Картинки загружены"
else
  log "   → папка o не найдена"
fi

log "2. Загрузка modules..."
if [ -d modules ]; then
  rclone sync modules "$REMOTE:$BUCKET/modules" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Modules загружены"
else
  log "   → папка modules не найдена"
fi

log "3. Загрузка fonts..."
if [ -d fonts ]; then
  rclone sync fonts "$REMOTE:$BUCKET/fonts" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Fonts загружены"
else
  log "   → папка fonts не найдена"
fi

log "=== Готово ==="
