import subprocess
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def clone_or_update(repo_url, ssh_key):
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key} -o StrictHostKeyChecking=accept-new'
    
    repo_dir = tempfile.mkdtemp()
    logger.info('Cloning repository to %s', repo_dir)
    
    subprocess.run(
        ['git', 'clone', repo_url, repo_dir],
        env=env,
        check=True
    )
    
    return repo_dir
