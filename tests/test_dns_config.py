import pytest
import tempfile
import os
from internal_dns_sync import dns_config


def test_load_dns_config_success():
    """Test successful DNS config loading"""
    yaml_content = """
hosts:
  - ip: "10.0.0.1"
    domain: "test1.local"
  - ip: "10.0.0.2"
    domain: "test2.local"
cnames:
  - domain: "alias.local"
    target: "test1.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        hosts, cnames = dns_config.load_dns_config(tmpdir)
        
        assert len(hosts) == 2
        assert '10.0.0.1 test1.local' in hosts
        assert hosts['10.0.0.1 test1.local'] == ('10.0.0.1', 'test1.local')
        
        assert len(cnames) == 1
        assert 'alias.local,test1.local' in cnames


def test_load_dns_config_missing_file():
    """Test missing dns-config.yaml file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError):
            dns_config.load_dns_config(tmpdir)


def test_load_dns_config_invalid_yaml():
    """Test invalid YAML in dns-config.yaml"""
    yaml_content = """
hosts:
  - ip: "10.0.0.1"
    domain: "test1.local"
  invalid: [unclosed
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        with pytest.raises(Exception):  # yaml.YAMLError
            dns_config.load_dns_config(tmpdir)


def test_load_dns_config_empty_file():
    """Test empty dns-config.yaml"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write("")
        
        hosts, cnames = dns_config.load_dns_config(tmpdir)
        assert hosts == {}
        assert cnames == {}


def test_load_dns_config_missing_hosts():
    """Test config without hosts section"""
    yaml_content = """
cnames:
  - domain: "alias.local"
    target: "test1.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        hosts, cnames = dns_config.load_dns_config(tmpdir)
        assert hosts == {}
        assert len(cnames) == 1


def test_load_dns_config_missing_cnames():
    """Test config without cnames section"""
    yaml_content = """
hosts:
  - ip: "10.0.0.1"
    domain: "test1.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        hosts, cnames = dns_config.load_dns_config(tmpdir)
        assert len(hosts) == 1
        assert cnames == {}


def test_load_dns_config_malformed_host():
    """Test host entry missing required fields"""
    yaml_content = """
hosts:
  - ip: "10.0.0.1"
  - domain: "test2.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        with pytest.raises((KeyError, TypeError)):
            dns_config.load_dns_config(tmpdir)


def test_load_dns_config_malformed_cname():
    """Test cname entry missing required fields"""
    yaml_content = """
cnames:
  - domain: "alias.local"
  - target: "test1.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        with pytest.raises((KeyError, TypeError)):
            dns_config.load_dns_config(tmpdir)


def test_load_dns_config_duplicate_hosts():
    """Test duplicate host entries"""
    yaml_content = """
hosts:
  - ip: "10.0.0.1"
    domain: "test.local"
  - ip: "10.0.0.1"
    domain: "test.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        hosts, _ = dns_config.load_dns_config(tmpdir)
        # Should only have one entry (last one wins)
        assert len(hosts) == 1


def test_load_dns_config_invalid_ip():
    """Test invalid IP address format"""
    yaml_content = """
hosts:
  - ip: "not.an.ip.address"
    domain: "test.local"
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, 'dns-config.yaml')
        with open(config_file, 'w') as f:
            f.write(yaml_content)
        
        # Should still load but with invalid IP
        hosts, _ = dns_config.load_dns_config(tmpdir)
        assert len(hosts) == 1
