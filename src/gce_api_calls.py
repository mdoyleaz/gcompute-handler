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
            # Temp until errors are built
            raise Exception(f"{self.instance} NOT FOUND!")

    def get_inst_details(self):
        req = self.apicall.instances().get(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def get_inst_disk(self):
        req = self.apicall.disks().list(
            project=self.project, zone=self.zone, filter=f'(name={self.instance})').execute()

        return req

    def start_instance(self):
        req = self.apicall.instances().start(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def stop_instance(self):
        req = self.apicall.instances().stop(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def reset_instance(self):
        req = self.apicall.instances().reset(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def reset_instance(self):
        req = self.apicall.instances().reset(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

## 'add_network_tags()'' will be moved to network manager
    def add_network_tags(self, new_item):
        get_fingerprint_req = self.apicall.instances().get(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        new_tags = get_fingerprint_req['tags']

        try:
            new_tags['items'].append(new_item)
        except KeyError:
            new_tags['items'] = [new_item]

        try:
            req = self.apicall.instances().setTags(
                project=self.project, zone=self.zone, instance=self.instance, body=new_tags).execute()
            return req
        except Exception as e:
            error = str(e)
            return error[error.find('. ') + 2:-2]


class DiskManagement(ApiInit):
    def __init__(self, project, zone):
        ApiInit.__init__(self)
        self.project = project
        self.zone = zone
        self.instance = instance

    def get_disks(self):
        req = self.apicall.disks().list(
            project=self.project, zone=self.zone).execute()

        return req



### TESTING ###
if __name__ == '__main__':
    inst = InstanceManagement('gcp-creator', 'us-central1-a', 'instance-builder')

    pprint.pprint(inst.add_network_tags("steve"))
