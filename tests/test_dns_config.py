import tempfile
import os
from internal_dns_sync import dns_config


def test_load_dns_config():
    toml_content = """
[dns]
hosts = [
    { ip = "10.0.0.1", domain = "test1.local" },
    { ip = "10.0.0.2", domain = "test2.local" },
]
cnameRecords = [
    { domain = "alias.local", target = "test1.local" },
]
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.toml')
        with open(config_file, 'w') as f:
            f.write(toml_content)
        
        hosts, cnames = dns_config.load_dns_config(tmpdir)
        
        assert len(hosts) == 2
        assert '10.0.0.1 test1.local' in hosts
        assert hosts['10.0.0.1 test1.local'] == ('10.0.0.1', 'test1.local')
        
        assert len(cnames) == 1
        assert 'alias.local test1.local' in cnames
