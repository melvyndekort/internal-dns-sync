import tempfile
import os
from internal_dns_sync import config


def test_get_config():
    config_content = """
piholes:
  - url: http://test1
    password: pass1
  - url: http://test2
    password: pass2
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(config_content)
        config_file = f.name
    
    try:
        os.environ['CONFIG'] = config_file
        cfg = config.get_config()
        
        assert len(cfg['piholes']) == 2
        assert cfg['piholes'][0]['url'] == 'http://test1'
        assert cfg['piholes'][0]['password'] == 'pass1'
        assert cfg['repo_url'] == 'git@github.com:melvyndekort/internal-dns.git'
    finally:
        os.unlink(config_file)
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']
