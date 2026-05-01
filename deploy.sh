#!/bin/bash
set -e
LOG_FILE="deploy.log"
REMOTE="ru-3"
BUCKET="storage-data"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой КАРТИНОК на S3 ==="

log "1. Загрузка originals..."
if [ -d originals ]; then
  rclone sync originals "$REMOTE:$BUCKET/originals" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Originals загружены"
else
  log "   → папка originals не найдена"
fi

log "=== Готово ==="
