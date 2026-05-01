#!/bin/bash
set -e
LOG_FILE="deploy.log"
REMOTE="ru-3"
BUCKET="storage-data"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Деплой на S3 ==="

log "1. Страницы (HTML)..."
rclone sync . "$REMOTE:$BUCKET" \
  --include "*.html" \
  --exclude ".git/**" --exclude ".certbot/**" --exclude ".playwright-mcp/**" \
  --exclude "o/**" --exclude "modules/**" --exclude "fonts/**" --exclude "originals/**" \
  --exclude "*.md" --exclude "*.py" --exclude "*.sh" --exclude "*.log" \
  --exclude "*.png" --exclude "*.yml" --exclude ".env" \
  --ignore-times --no-update-modtime \
  --progress >> "$LOG_FILE" 2>&1
log "   ✓ Страницы загружены"

log "2. API..."
rclone sync api "$REMOTE:$BUCKET/api" --progress >> "$LOG_FILE" 2>&1
log "   ✓ API загружено"

log "3. Картинки (o/)..."
if [ -d o ]; then
  rclone sync o "$REMOTE:$BUCKET/o" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Картинки загружены"
else
  log "   → папка o не найдена (уже на S3)"
fi

log "4. Modules..."
if [ -d modules ]; then
  rclone sync modules "$REMOTE:$BUCKET/modules" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Modules загружены"
else
  log "   → папка modules не найдена"
fi

log "5. Fonts..."
if [ -d fonts ]; then
  rclone sync fonts "$REMOTE:$BUCKET/fonts" --progress >> "$LOG_FILE" 2>&1
  log "   ✓ Fonts загружены"
else
  log "   → папка fonts не найдена"
fi

log "=== Готово ==="