import os
import yaml
import logging

logger = logging.getLogger(__name__)


def get_config():
    config_file = os.getenv('CONFIG', '/config/config.yml')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    
    # Set defaults
    cfg.setdefault('repo_url', 'git@github.com:melvyndekort/internal-dns.git')
    cfg.setdefault('ssh_key', '/config/deploy-key')
    
    return cfg
