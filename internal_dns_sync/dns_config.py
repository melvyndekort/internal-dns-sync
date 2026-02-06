import yaml
import logging

logger = logging.getLogger(__name__)


def load_dns_config(repo_dir):
    config_file = f'{repo_dir}/dns-config.yaml'
    logger.info('Loading DNS config from %s', config_file)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    hosts = {}
    for entry in data.get('hosts', []):
        hosts[f"{entry['ip']} {entry['domain']}"] = (entry['ip'], entry['domain'])
    
    cnames = {}
    for entry in data.get('cnames', []):
        cnames[f"{entry['domain']},{entry['target']}"] = (entry['domain'], entry['target'])
    
    return hosts, cnames
