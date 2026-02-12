import os
import yaml
import logging

logger = logging.getLogger(__name__)


def get_config():
    # Try config file first (backward compatibility)
    config_file = os.getenv('CONFIG', '/config/config.yml')
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        if cfg is None:
            cfg = {}
    else:
        cfg = {}
    
    # Set defaults
    cfg.setdefault('repo_url', os.getenv('REPO_URL', 'git@github.com:melvyndekort/homelab.git'))
    cfg.setdefault('ssh_key', os.getenv('SSH_KEY', '/ssh-key'))
    cfg.setdefault('dns_config_path', os.getenv('DNS_CONFIG_PATH', 'dns/dns-config.yaml'))
    
    # Parse PiHole configs from env vars if not in file
    if 'piholes' not in cfg:
        pihole_urls = os.getenv('PIHOLE_URLS', '').split(',')
        pihole_passwords = os.getenv('PIHOLE_PASSWORDS', '').split(',')
        
        if pihole_urls and pihole_urls[0]:
            cfg['piholes'] = [
                {'url': url.strip(), 'password': pwd.strip()}
                for url, pwd in zip(pihole_urls, pihole_passwords)
            ]
        else:
            cfg['piholes'] = []
    
    return cfg
