import yaml
import logging

logger = logging.getLogger(__name__)


def load_dns_config(repo_dir, dns_config_path='dns-config.yaml'):
    config_file = f'{repo_dir}/{dns_config_path}'
    logger.info('Loading DNS config from %s', config_file)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Handle empty file
    if data is None:
        data = {}
    
    hosts = {}
    for entry in data.get('hosts', []):
        hosts[f"{entry['ip']} {entry['domain']}"] = (entry['ip'], entry['domain'])
    
    cnames = {}
    for entry in data.get('cnames', []):
        cnames[f"{entry['domain']},{entry['target']}"] = (entry['domain'], entry['target'])
    
    return hosts, cnames
