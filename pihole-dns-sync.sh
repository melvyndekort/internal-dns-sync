#!/bin/bash
set -e

REPO_DIR="/var/lib/internal-dns"
REPO_URL="git@github.com:melvyndekort/internal-dns.git"
DNS_FILE="custom-dns.list"
PIHOLE_DNS="/etc/pihole/hosts/custom.list"
SSH_KEY="/root/.ssh/deploy-key"

export GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=accept-new"

# Clone repo if it doesn't exist
if [ ! -d "$REPO_DIR" ]; then
    git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

# Pull latest changes
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Changes detected, updating DNS entries..."
    git pull origin main
    
    # Backup current DNS
    if [ -f "$PIHOLE_DNS" ]; then
        cp "$PIHOLE_DNS" "$PIHOLE_DNS.backup.$(date +%Y%m%d-%H%M%S)"
    fi
    
    # Copy new DNS entries
    cp "$DNS_FILE" "$PIHOLE_DNS"
    
    echo "DNS entries updated - PiHole will reload automatically"
else
    echo "No changes detected"
fi
