import pytest
from unittest.mock import patch, Mock
import subprocess
from internal_dns_sync import git


def test_clone_or_update_success():
    """Test successful git clone"""
    mock_run = Mock()
    
    with patch('subprocess.run', mock_run):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            repo_dir = git.clone_or_update(
                'git@github.com:test/repo.git',
                '/path/to/key'
            )
            
            assert repo_dir == '/tmp/test-repo'
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert 'git' in call_args[0][0]
            assert 'clone' in call_args[0][0]


def test_clone_or_update_invalid_repo():
    """Test clone with invalid repository"""
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(128, 'git')):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            with pytest.raises(subprocess.CalledProcessError):
                git.clone_or_update(
                    'git@github.com:invalid/repo.git',
                    '/path/to/key'
                )


def test_clone_or_update_network_error():
    """Test clone with network error"""
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'git')):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            with pytest.raises(subprocess.CalledProcessError):
                git.clone_or_update(
                    'git@github.com:test/repo.git',
                    '/path/to/key'
                )


def test_clone_or_update_invalid_ssh_key():
    """Test clone with invalid SSH key"""
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(128, 'git')):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            with pytest.raises(subprocess.CalledProcessError):
                git.clone_or_update(
                    'git@github.com:test/repo.git',
                    '/nonexistent/key'
                )


def test_clone_or_update_ssh_command():
    """Test that SSH command is properly configured"""
    mock_run = Mock()
    
    with patch('subprocess.run', mock_run):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            git.clone_or_update(
                'git@github.com:test/repo.git',
                '/path/to/key'
            )
            
            call_kwargs = mock_run.call_args[1]
            env = call_kwargs['env']
            assert 'GIT_SSH_COMMAND' in env
            assert '/path/to/key' in env['GIT_SSH_COMMAND']
            assert 'StrictHostKeyChecking=accept-new' in env['GIT_SSH_COMMAND']


def test_clone_or_update_permission_denied():
    """Test clone with permission denied"""
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(128, 'git')):
        with patch('tempfile.mkdtemp', return_value='/tmp/test-repo'):
            with pytest.raises(subprocess.CalledProcessError):
                git.clone_or_update(
                    'git@github.com:test/repo.git',
                    '/path/to/key'
                )
