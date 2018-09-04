import requests
from inst_app_auth import receive_token

import pprint  # TESTING


class GceInstApi(object):
    def __init__(self, project, zone, instance):
        api_creds = receive_token()
        self.project = project
        self.zone = zone
        self.instance = instance
        # Structures API URL for requests
        self.headers = {'Authorization': f'Bearer {api_creds}'}
        self.base_url = "https://www.googleapis.com/compute/v1/projects"
        self.inst_url = "{}/{}/zones/{}/instances/{}/".format(
            self.base_url, self.project, self.zone, self.instance)

    def get_inst_details(self):
        """
        Returns instance details
        """
        endpoint = self.inst_url
        req = requests.get(endpoint, headers=self.headers).json()

        return req

    def put_inst_power(self, power_option):
        """
        Initiates power option
        Supports: ['start', 'stop', 'reset']
        """
        endpoint = f'{self.inst_url}{power_option}/'
        req = requests.post(endpoint, headers=self.headers).json()

        return req




### TESTING ###
if __name__ == '__main__':
    inst = GceInstApi('gcp-creator', 'us-central1-a', 'instance-1')

    print(inst.inst_power_controls('start'))
