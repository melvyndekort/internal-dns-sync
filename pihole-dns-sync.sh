#!/bin/bash
set -e

REPO_DIR="/var/lib/internal-dns"
REPO_URL="git@github.com:melvyndekort/internal-dns.git"
DNS_FILE="custom-dns.list"
PIHOLE_DNS="/etc/pihole/hosts/custom.list"
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

# Always copy the file
echo "Deploying DNS entries..."

# Backup current DNS
if [ -f "$PIHOLE_DNS" ]; then
    cp "$PIHOLE_DNS" "$PIHOLE_DNS.backup.$(date +%Y%m%d-%H%M%S)"
fi

# Copy new DNS entries
cp "$DNS_FILE" "$PIHOLE_DNS"

echo "DNS entries updated - PiHole will reload automatically"
