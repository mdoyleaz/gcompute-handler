import requests
from google.auth import compute_engine

META_URL = 'http://metadata.google.internal/computeMetadata/v1/'
META_HEADERS = {'Metadata-Flavor': 'Google'}
SERVICE_ACCOUNT = 'default'

def receive_token():
    url = '{}instance/service-accounts/{}/token'.format(
        META_URL, SERVICE_ACCOUNT)

    # Auth token request
    auth_req = requests.get(url, headers=META_HEADERS)
    auth_req.raise_for_status()

    auth_token = auth_req.json()['access_token']

    return auth_token
