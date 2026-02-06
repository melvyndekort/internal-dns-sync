# Internal DNS Sync

Container image for syncing internal DNS entries from the [internal-dns](https://github.com/melvyndekort/internal-dns) repository to PiHole servers.

## Container Image

Published to `ghcr.io/melvyndekort/internal-dns-sync:latest`

Built with:
- Alpine Linux
- Git, Bash, OpenSSH
- Rust binary using `toml_edit` crate (preserves comments and formatting)

## Usage

The container syncs DNS entries from the private `internal-dns` repository to PiHole's configuration file.

### Volumes

- `/etc/pihole` - PiHole configuration directory (must be writable)
- `/root/.ssh/deploy-key` - SSH deploy key for accessing the internal-dns repository (read-only)

## Deployment

See the `deployment/` directory for server-specific configurations:
- `pihole-1/` - Fedora IoT with podman + systemd timer (every 5 minutes)
- `lmserver/` - Fedora CoreOS with docker + scheduler (every 5 minutes)

## How It Works

1. Clones/pulls the `internal-dns` repository using the provided SSH key
2. Reads `dns-config.toml` from the repository
3. Updates `dns.hosts` and `dns.cnameRecords` in `/etc/pihole/pihole.toml`
4. Preserves all comments, formatting, and other PiHole settings
5. PiHole automatically reloads the DNS entries

## Technical Details

Uses Rust's `toml_edit` crate to parse and modify TOML files while preserving:
- Comments
- Formatting
- All other configuration sections
