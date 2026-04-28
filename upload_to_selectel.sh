#!/bin/bash
BUCKET=${1:-glukhova-photos}
rclone sync glukhova-dasha selectel:$BUCKET/glukhova-dasha --progress --s3-endpoint=https://s3.selectel.ru --s3-acl=public-read
echo "Uploaded glukhova-dasha to s3://$BUCKET/glukhova-dasha/"
echo "https://$BUCKET.storage.selectel.ru/glukhova-dasha/originals/xxx.webp"
