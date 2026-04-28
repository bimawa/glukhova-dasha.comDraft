#!/bin/bash
set -e
BUCKET=${1:-storage-data}
REMOTE="ru-3"
echo "Uploading glukhova-dasha to $REMOTE:$BUCKET/glukhova-dasha ..."
rclone sync glukhova-dasha "$REMOTE:$BUCKET/glukhova-dasha" --progress
echo ""
echo "Done!"
echo "Originals: https://$BUCKET.storage.selcloud.ru/glukhova-dasha/originals/"
echo "Thumbs:    https://$BUCKET.storage.selcloud.ru/glukhova-dasha/thumbs/"
echo ""
echo "After upload, update widget URLs:"
echo "  python3 update_urls.py https://$BUCKET.storage.selcloud.ru"
