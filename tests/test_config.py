import pytest
import tempfile
import os
from internal_dns_sync import config


def test_get_config_success():
    """Test successful config loading"""
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


def test_get_config_missing_file():
    """Test config file not found"""
    os.environ['CONFIG'] = '/nonexistent/config.yml'
    try:
        with pytest.raises(FileNotFoundError):
            config.get_config()
    finally:
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']


def test_get_config_invalid_yaml():
    """Test invalid YAML syntax"""
    config_content = """
piholes:
  - url: http://test1
    password: pass1
  invalid yaml: [unclosed
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(config_content)
        config_file = f.name
    
    try:
        os.environ['CONFIG'] = config_file
        with pytest.raises(Exception):  # yaml.YAMLError
            config.get_config()
    finally:
        os.unlink(config_file)
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']


def test_get_config_empty_file():
    """Test empty config file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("")
        config_file = f.name
    
    try:
        os.environ['CONFIG'] = config_file
        cfg = config.get_config()
        # Empty YAML returns None, but we add defaults
        assert cfg == {
            'repo_url': 'git@github.com:melvyndekort/internal-dns.git',
            'ssh_key': '/config/deploy-key'
        }
    finally:
        os.unlink(config_file)
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']


def test_get_config_missing_piholes():
    """Test config without piholes section"""
    config_content = """
repo_url: git@github.com:test/repo.git
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(config_content)
        config_file = f.name
    
    try:
        os.environ['CONFIG'] = config_file
        cfg = config.get_config()
        assert 'piholes' not in cfg or cfg.get('piholes') is None
    finally:
        os.unlink(config_file)
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']


def test_get_config_custom_defaults():
    """Test custom repo_url and ssh_key"""
    config_content = """
piholes:
  - url: http://test1
    password: pass1
repo_url: git@github.com:custom/repo.git
ssh_key: /custom/key
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(config_content)
        config_file = f.name
    
    try:
        os.environ['CONFIG'] = config_file
        cfg = config.get_config()
        assert cfg['repo_url'] == 'git@github.com:custom/repo.git'
        assert cfg['ssh_key'] == '/custom/key'
    finally:
        os.unlink(config_file)
        if 'CONFIG' in os.environ:
            del os.environ['CONFIG']
