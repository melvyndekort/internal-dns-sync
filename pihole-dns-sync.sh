#!/bin/bash
set -e

REPO_DIR="/var/lib/internal-dns"
REPO_URL="git@github.com:melvyndekort/internal-dns.git"
DNS_CONFIG="dns-config.toml"
PIHOLE_TOML="/etc/pihole/pihole.toml"
SSH_KEY="/root/.ssh/deploy-key"

export GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=accept-new"

# Clone or update repo
if [ ! -d "$REPO_DIR" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
else
    echo "Updating repository..."
    cd "$REPO_DIR"
    git pull origin main
fi

cd "$REPO_DIR"

echo "Deploying DNS entries to pihole.toml..."

# Calculate checksum before changes
CHECKSUM_BEFORE=""
if [ -f "$PIHOLE_TOML" ]; then
    CHECKSUM_BEFORE=$(sha256sum "$PIHOLE_TOML" | cut -d' ' -f1)
    cp "$PIHOLE_TOML" "$PIHOLE_TOML.backup.$(date +%Y%m%d-%H%M%S)"
fi

# Use Rust toml-merge to update DNS entries while preserving comments
toml-merge

# Calculate checksum after changes
CHECKSUM_AFTER=$(sha256sum "$PIHOLE_TOML" | cut -d' ' -f1)

if [ "$CHECKSUM_BEFORE" != "$CHECKSUM_AFTER" ]; then
    echo "DNS entries changed"
    touch /etc/pihole/.reload-required
else
    echo "No changes detected"
fi
