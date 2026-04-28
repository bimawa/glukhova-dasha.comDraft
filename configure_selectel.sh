#!/bin/bash
set -e

ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found. Create it with:"
  echo "  SELECTEL_ACCESS_KEY=your_key"
  echo "  SELECTEL_SECRET_KEY=your_secret"
  exit 1
fi

source "$ENV_FILE"

if [ -z "$SELECTEL_ACCESS_KEY" ] || [ -z "$SELECTEL_SECRET_KEY" ]; then
  echo "Error: SELECTEL_ACCESS_KEY and SELECTEL_SECRET_KEY must be set in $ENV_FILE"
  exit 1
fi

rclone config create ru-3 s3 \
  provider Selectel \
  env_auth false \
  access_key_id "$SELECTEL_ACCESS_KEY" \
  secret_access_key "$SELECTEL_SECRET_KEY" \
  region ru-3 \
  endpoint s3.ru-3.storage.selcloud.ru \
  --all

echo "rclone configured: ru-3"
echo ""
echo "Create bucket (if needed):"
echo "  rclone mkdir ru-3:storage-data"
echo ""
echo "Upload site:"
echo "  rclone sync glukhova-dasha ru-3:storage-data/glukhova-dasha --progress"
echo ""
echo "After upload, update URLs:"
echo "  python3 update_urls.py https://ru-3.storage.selcloud.ru/storage-data"
