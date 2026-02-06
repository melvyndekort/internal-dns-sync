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

# Backup current config if it exists
if [ -f "$PIHOLE_TOML" ]; then
    cp "$PIHOLE_TOML" "$PIHOLE_TOML.backup.$(date +%Y%m%d-%H%M%S)"
fi

# Use Rust toml-merge to update DNS entries while preserving comments
toml-merge

echo "DNS entries updated in pihole.toml - PiHole will reload automatically"
