import pytest
from unittest.mock import Mock, patch
from internal_dns_sync.pihole import PiHoleAPI
import requests


@pytest.fixture
def pihole_api():
    return PiHoleAPI('http://pihole.local', 'testpass')


def test_authenticate_success(pihole_api):
    """Test successful authentication"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'session': {'sid': 'test-sid', 'csrf': 'test-csrf'}
    }
    
    with patch.object(pihole_api.session, 'post', return_value=mock_response):
        pihole_api.authenticate()
        
        assert pihole_api.sid == 'test-sid'
        assert pihole_api.csrf == 'test-csrf'
        assert pihole_api.session.headers['X-FTL-SID'] == 'test-sid'
        assert pihole_api.session.headers['X-FTL-CSRF'] == 'test-csrf'


def test_authenticate_network_error(pihole_api):
    """Test authentication with network error"""
    with patch.object(pihole_api.session, 'post', side_effect=requests.ConnectionError):
        with pytest.raises(requests.ConnectionError):
            pihole_api.authenticate()


def test_authenticate_invalid_password(pihole_api):
    """Test authentication with wrong password"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
    
    with patch.object(pihole_api.session, 'post', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.authenticate()


def test_get_hosts_success(pihole_api):
    """Test successful host retrieval"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.json.return_value = {
        'config': {'dns': {'hosts': ['10.0.0.1 test.local']}}
    }
    
    with patch.object(pihole_api.session, 'get', return_value=mock_response):
        hosts = pihole_api.get_hosts()
        assert hosts == ['10.0.0.1 test.local']


def test_get_hosts_empty(pihole_api):
    """Test getting hosts when none exist"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.json.return_value = {'config': {'dns': {'hosts': []}}}
    
    with patch.object(pihole_api.session, 'get', return_value=mock_response):
        hosts = pihole_api.get_hosts()
        assert hosts == []


def test_get_hosts_network_error(pihole_api):
    """Test get hosts with network error"""
    pihole_api.sid = 'test-sid'
    
    with patch.object(pihole_api.session, 'get', side_effect=requests.ConnectionError):
        with pytest.raises(requests.ConnectionError):
            pihole_api.get_hosts()


def test_get_cnames_success(pihole_api):
    """Test successful CNAME retrieval"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.json.return_value = {
        'config': {'dns': {'cnameRecords': ['alias.local,target.local']}}
    }
    
    with patch.object(pihole_api.session, 'get', return_value=mock_response):
        cnames = pihole_api.get_cnames()
        assert cnames == ['alias.local,target.local']


def test_delete_host_success(pihole_api):
    """Test successful host deletion"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'delete', return_value=mock_response):
        pihole_api.delete_host('10.0.0.1 test.local')
        pihole_api.session.delete.assert_called_once()


def test_delete_host_not_found(pihole_api):
    """Test deleting non-existent host"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    
    with patch.object(pihole_api.session, 'delete', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.delete_host('10.0.0.1 nonexistent.local')


def test_delete_cname_success(pihole_api):
    """Test successful CNAME deletion"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'delete', return_value=mock_response):
        pihole_api.delete_cname('alias.local,target.local')
        pihole_api.session.delete.assert_called_once()


def test_add_host_success(pihole_api):
    """Test successful host addition"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'post', return_value=mock_response):
        pihole_api.add_host('10.0.0.1', 'test.local')
        pihole_api.session.post.assert_called_once()


def test_add_host_duplicate(pihole_api):
    """Test adding duplicate host"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("409 Conflict")
    
    with patch.object(pihole_api.session, 'post', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.add_host('10.0.0.1', 'test.local')


def test_add_cname_success(pihole_api):
    """Test successful CNAME addition"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'post', return_value=mock_response):
        pihole_api.add_cname('alias.local', 'target.local')
        pihole_api.session.post.assert_called_once()


def test_base_url_trailing_slash(pihole_api):
    """Test that trailing slash is removed from base URL"""
    api = PiHoleAPI('http://pihole.local/', 'testpass')
    assert api.base_url == 'http://pihole.local'


def test_session_timeout(pihole_api):
    """Test handling of session timeout"""
    pihole_api.sid = 'expired-sid'
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
    
    with patch.object(pihole_api.session, 'get', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.get_hosts()
