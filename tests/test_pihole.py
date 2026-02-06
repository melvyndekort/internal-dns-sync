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


def test_update_hosts_success(pihole_api):
    """Test successful hosts update"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        pihole_api.update_hosts(['10.0.0.1 test.local', '10.0.0.2 test2.local'])
        pihole_api.session.put.assert_called_once()


def test_update_hosts_error(pihole_api):
    """Test hosts update with error"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Error")
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.update_hosts(['10.0.0.1 test.local'])


def test_update_cnames_success(pihole_api):
    """Test successful CNAMEs update"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        pihole_api.update_cnames(['alias.local,target.local'])
        pihole_api.session.put.assert_called_once()


def test_update_hosts_empty(pihole_api):
    """Test updating with empty hosts list"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        pihole_api.update_hosts([])
        pihole_api.session.put.assert_called_once()


def test_update_cnames_empty(pihole_api):
    """Test updating with empty CNAMEs list"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        pihole_api.update_cnames([])
        pihole_api.session.put.assert_called_once()


def test_update_cnames_error(pihole_api):
    """Test CNAMEs update with error"""
    pihole_api.sid = 'test-sid'
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Error")
    
    with patch.object(pihole_api.session, 'put', return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            pihole_api.update_cnames(['alias.local,target.local'])


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
