import requests
import logging

logger = logging.getLogger(__name__)


class PiHoleAPI:
    def __init__(self, base_url, password):
        self.base_url = base_url.rstrip('/')
        self.password = password
        self.session = requests.Session()
        self.sid = None
        self.csrf = None
    
    def authenticate(self):
        logger.info('Authenticating with PiHole API')
        response = self.session.post(
            f'{self.base_url}/api/auth',
            json={'password': self.password}
        )
        response.raise_for_status()
        data = response.json()
        self.sid = data['session']['sid']
        self.csrf = data['session']['csrf']
        self.session.headers.update({
            'X-FTL-SID': self.sid,
            'X-FTL-CSRF': self.csrf
        })
    
    def get_hosts(self):
        logger.info('Fetching current DNS hosts')
        response = self.session.get(
            f'{self.base_url}/api/config/dns/hosts',
            params={'sid': self.sid}
        )
        response.raise_for_status()
        return response.json().get('config', {}).get('dns', {}).get('hosts', [])
    
    def get_cnames(self):
        logger.info('Fetching current DNS CNAMEs')
        response = self.session.get(
            f'{self.base_url}/api/config/dns/cnameRecords',
            params={'sid': self.sid}
        )
        response.raise_for_status()
        return response.json().get('config', {}).get('dns', {}).get('cnameRecords', [])
    
    def update_hosts(self, hosts):
        logger.info('Updating hosts list (%d entries)', len(hosts))
        response = self.session.put(
            f'{self.base_url}/api/config/dns/hosts',
            params={'sid': self.sid},
            json={'hosts': hosts}
        )
        response.raise_for_status()
    
    def update_cnames(self, cnames):
        logger.info('Updating CNAME list (%d entries)', len(cnames))
        response = self.session.put(
            f'{self.base_url}/api/config/dns/cnameRecords',
            params={'sid': self.sid},
            json={'cnameRecords': cnames}
        )
        response.raise_for_status()
