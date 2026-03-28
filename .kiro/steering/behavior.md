# internal-dns-sync

> For global standards, way-of-workings, and pre-commit checklist, see `~/.kiro/steering/behavior.md`

## Role

Python developer and DevOps engineer.

## What This Does

Syncs internal DNS entries from a YAML config to PiHole servers via the PiHole v6 API. Clones a Git repo containing DNS config, parses it, and pushes entries to PiHole.

## Repository Structure

- `internal_dns_sync/` — Application source
- `tests/` — Test suite
- `deployment/` — Deployment configuration
- `config.example.yml` — Example configuration
- `Dockerfile` — Multi-stage Alpine build (includes git + openssh-client)
- `Makefile` — `install`, `test`, `lint` (pylint), `build`, `full-build`, `run`

## Deployment

- Container image: `ghcr.io/melvyndekort/internal-dns-sync:latest` (multi-arch: amd64 + arm64)
- Runs on homelab Docker via Portainer

## Related Repositories

- `~/src/melvyndekort/homelab` — Docker Compose stack that runs this container, also contains the DNS config files in `dns/`
