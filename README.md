# Internal DNS Sync

Container image for syncing internal DNS entries from the [internal-dns](https://github.com/melvyndekort/internal-dns) repository to PiHole servers via the PiHole v6 API.

## Container Image

Published to `ghcr.io/melvyndekort/internal-dns-sync:latest`

Built with:
- Alpine Linux
- Python 3.15
- Git, OpenSSH

## Usage

The container syncs DNS entries from the private `internal-dns` repository to PiHole using the REST API.

### Configuration

Mount a config file at `/config/config.yml`:

```yaml
piholes:
  - url: http://10.204.10.2
    password: password1
  - url: http://10.204.10.3
    password: password2
```

Optional settings (with defaults):
- `repo_url`: `git@github.com:melvyndekort/internal-dns.git`
- `ssh_key`: `/root/.ssh/deploy-key`

### Volumes

- `/config/config.yml` - Configuration file (required)
- `/config/deploy-key` - SSH deploy key for accessing the internal-dns repository (read-only)

## Deployment

Runs on lmserver via docker + scheduler (every 5 minutes), syncing to both PiHole instances.

Configuration file location: `/var/mnt/storage/docker/internal-dns-sync/config.yml`

See `deployment/lmserver/` for scheduler job configuration and example config file.

## How It Works

1. Clones/pulls the `internal-dns` repository using the provided SSH key
2. Reads `dns-config.toml` from the repository
3. Authenticates with PiHole API
4. Fetches current DNS hosts and CNAME records
5. Syncs changes (adds new entries, removes old ones)
6. Changes apply immediately via API - no restart needed
