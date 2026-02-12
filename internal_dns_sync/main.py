import logging

from internal_dns_sync import config, git, dns_config, pihole

FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def sync_pihole(pihole_config, desired_hosts, desired_cnames):
    logger.info('Syncing PiHole at %s', pihole_config['url'])
    
    api = pihole.PiHoleAPI(pihole_config['url'], pihole_config['password'])
    api.authenticate()
    
    current_hosts = api.get_hosts()
    current_cnames = api.get_cnames()
    
    # Build desired hosts list
    desired_hosts_list = [f"{ip} {domain}" for (ip, domain) in desired_hosts.values()]
    desired_cnames_list = [f"{domain},{target}" for (domain, target) in desired_cnames.values()]
    
    # Check if updates are needed
    hosts_changed = set(current_hosts) != set(desired_hosts_list)
    cnames_changed = set(current_cnames) != set(desired_cnames_list)
    
    changes = 0
    if hosts_changed:
        api.update_hosts(desired_hosts_list)
        changes += abs(len(desired_hosts_list) - len(current_hosts))
    
    if cnames_changed:
        api.update_cnames(desired_cnames_list)
        changes += abs(len(desired_cnames_list) - len(current_cnames))
    
    if changes > 0:
        logger.info('Synced %d changes to %s', changes, pihole_config['url'])
    else:
        logger.info('No changes for %s', pihole_config['url'])
    
    return changes


def main():
    cfg = config.get_config()
    
    repo_dir = git.clone_or_update(cfg['repo_url'], cfg['ssh_key'])
    
    desired_hosts, desired_cnames = dns_config.load_dns_config(repo_dir, cfg['dns_config_path'])
    
    total_changes = 0
    for pihole_config in cfg['piholes']:
        total_changes += sync_pihole(pihole_config, desired_hosts, desired_cnames)
    
    logger.info('Total changes across all PiHoles: %d', total_changes)


if __name__ == "__main__":
    main()
