import logging

from internal_dns_sync import config, git, dns_config, pihole

FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def sync_entries(api, current, desired, delete_func, add_func):
    current_set = set(current)
    desired_set = set(desired.keys())
    
    to_delete = current_set - desired_set
    to_add = desired_set - current_set
    
    for entry in to_delete:
        delete_func(entry)
    
    for entry in to_add:
        add_func(*desired[entry])
    
    return len(to_delete) + len(to_add)


def sync_pihole(pihole_config, desired_hosts, desired_cnames):
    logger.info('Syncing PiHole at %s', pihole_config['url'])
    
    api = pihole.PiHoleAPI(pihole_config['url'], pihole_config['password'])
    api.authenticate()
    
    current_hosts = api.get_hosts()
    current_cnames = api.get_cnames()
    
    changes = 0
    changes += sync_entries(api, current_hosts, desired_hosts, api.delete_host, api.add_host)
    changes += sync_entries(api, current_cnames, desired_cnames, api.delete_cname, api.add_cname)
    
    if changes > 0:
        logger.info('Synced %d changes to %s', changes, pihole_config['url'])
    else:
        logger.info('No changes for %s', pihole_config['url'])
    
    return changes


def main():
    cfg = config.get_config()
    
    repo_dir = git.clone_or_update(cfg['repo_url'], cfg['ssh_key'])
    
    desired_hosts, desired_cnames = dns_config.load_dns_config(repo_dir)
    
    total_changes = 0
    for pihole_config in cfg['piholes']:
        total_changes += sync_pihole(pihole_config, desired_hosts, desired_cnames)
    
    logger.info('Total changes across all PiHoles: %d', total_changes)


if __name__ == "__main__":
    main()
