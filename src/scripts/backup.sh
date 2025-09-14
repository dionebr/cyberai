#!/bin/bash

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "[+] Realizando backup de configs e dados..."
cp -r config "$BACKUP_DIR/"
cp -r data "$BACKUP_DIR/"
cp -r models "$BACKUP_DIR/"
cp requirements.txt "$BACKUP_DIR/"
cp package.json "$BACKUP_DIR/"
echo "[+] Backup concluído em $BACKUP_DIR"
