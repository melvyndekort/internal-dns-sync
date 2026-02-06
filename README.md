# Internal DNS Sync

Container image for syncing internal DNS entries from the [internal-dns](https://github.com/melvyndekort/internal-dns) repository to PiHole servers.

## Container Image

Published to `ghcr.io/melvyndekort/internal-dns-sync:latest`

## Usage

The container syncs DNS entries from the private `internal-dns` repository to the local PiHole configuration.

### Environment Variables

- `TZ` - Timezone (default: Europe/Amsterdam)

### Volumes

- `/etc/pihole/hosts` - PiHole hosts directory (must be writable)
- `/root/.ssh/deploy-key` - SSH deploy key for accessing the internal-dns repository (read-only)

## Deployment

See the `deployment/` directory for server-specific configurations:
- `pihole-1/` - Fedora IoT with podman + systemd
- `lmserver/` - Fedora CoreOS with docker compose

## How It Works

1. Clones/pulls the internal-dns repository using the provided SSH key
2. Checks for changes
3. If changes detected, copies `custom-dns.list` to `/etc/pihole/hosts/custom.list`
4. PiHole automatically reloads the DNS entries
