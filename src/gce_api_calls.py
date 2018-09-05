import requests
from googleapiclient import discovery

import pprint  # TESTING

# Constructor class for API Calls
class ApiInit:
    def __init__(self):
        self.apicall = discovery.build('compute', 'beta')

    def instance_verification(self, project, zone, instance):
        req = self.apicall.instances().list(
            project=project, zone=zone, filter=f'name={instance}').execute()

        try:
            req['items']
            return True
        except KeyError:
            return False

class InstanceManagement(ApiInit):
    def __init__(self, project, zone, instance):
        ApiInit.__init__(self)

        self.project = project
        self.zone = zone
        self.instance = instance

        if not self.instance_verification(project, zone, instance):
            print(f"{self.instance} NOT FOUND!") ## Temp until errors are built


    def get_inst_details(self):
        req = self.apicall.instances().get(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def start_instance(self):
        req = self.apicall.instances().start(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return(req)

    def stop_instance(self):
        req = self.apicall.instances().stop(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return(req)

    def reset_instance(self):
        req = self.apicall.instances().reset(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return(req)

class DiskManagement(ApiInit):
    def __init__(self, project, zone, instance):
        ApiInit.__init__(self)
        self.project = project
        self.zone = zone
        self.instance = instance

### TESTING ###
if __name__ == '__main__':
    inst = InstanceManagement('gcp-creator','us-central1-a', 'instance-1')

    pprint.pprint(inst.start_instance())
