import requests
from googleapiclient import discovery

from pprint import pprint  # TESTING

# Constructor/Master class for API Calls


class ApiInit:
    """
    - ApiInit -
    Class Description: Handles call errors and
    initiates GCE Authentication from provided json
    Parameter Details: No Parameters Required
    Required Parameters: None
    Optional Parameters: None
    """

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

    def param_zone_project(self, kwargs):
        if len(kwargs) < 2:
            raise ValueError("Required Parameters: [project, zone, instance]")
        try:
            project = kwargs.pop('project')
            zone = kwargs.pop('zone')
        except KeyError as e:
            return f'Error: {e}'

        return project, zone

    def param_zone_project_inst(self, kwargs):
        if len(kwargs) < 3:
            raise ValueError("Required Parameters: [project, zone, instance]")
        try:
            project = kwargs.pop('project')
            zone = kwargs.pop('zone')
            instance = kwargs.pop('instance')
        except KeyError as e:
            return f'Error: {e}'

        if not self.instance_verification(project, zone, instance):
            raise Exception(f"{instance} NOT FOUND!")

        return project, zone, instance


class InstanceManagement(ApiInit):
    """
    - Instance Management -
    Class Description: Manages instances (ex. Details, Power)
    Parameter Details class may be initiated or methods called individually
    Required Parameters:
    Optional Parameters:
    'project': GCE project
    'zone': GCE zone
    'instance': GCE instance
    """

    def __init__(self, project=None, zone=None, instance=None):
        ApiInit.__init__(self)  # Inhertis ApiInit class for errors and auth

        if project is zone is instance is not None:
            if not self.instance_verification(project, zone, instance):
                raise Exception(f"{self.instance} NOT FOUND!")

        self.project = project
        self.zone = zone
        self.instance = instance

    def get_inst_details(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.instances().get(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def get_inst_disk(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.disks().list(
            project=self.project, zone=self.zone, filter=f'(name={self.instance})').execute()

        return req

    def start_instance(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.instances().start(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def stop_instance(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.instances().stop(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def reset_instance(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.instances().reset(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req

    def reset_instance(self, **kwargs):
        if self.zone is self.project is self.instance is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        req = self.apicall.instances().reset(
            project=self.project, zone=self.zone, instance=self.instance).execute()

        return req


class DiskManagement(ApiInit):
    """
    - DiskManagement -
    Class Description: Class to manage storage devices on GCE
    Parameter Details: Class may be initiated or methods called individually
    Required Parameters: None
    Optional Parameters:
    'project': GCE project
    'zone': GCE zone
    """

    def __init__(self, project=None, zone=None):
        ApiInit.__init__(self)  # Inhertis ApiInit class for errors and auth

        self.project = project
        self.zone = zone

    def get_disks(self, **kwargs):
        req = self.apicall.disks().list(
            project=self.project, zone=self.zone).execute()

        return req


class NetworkManagement(ApiInit):
    """
    - NetworkManagement -
    Class Description: Manages Network Options
    Parameter Details: Class may be initiated or methods called individually
    Required Parameters: None
    Optional Parameters:
    'project': GCE project
    'zone': GCE zone
    'instance': GCE instance
    """

    def __init__(self, project=None, zone=None, instance=None):
        ApiInit.__init__(self)  # Inhertis ApiInit class for errors and auth

        if project is zone is instance is not None:
            if not self.instance_verification(project, zone, instance):
                raise Exception(f"{self.instance} NOT FOUND!")

        self.project = project
        self.zone = zone
        self.instance = instance

    def add_network_tags(self, new_item, **kwargs):
        if self.zone is None or self.project is None:
            self.project, self.zone, self.instance = self.param_zone_project_inst(
                kwargs)

        get_fingerprint_req = self.apicall.instances().get(
            project=project, zone=zone, instance=instance).execute()

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


class InstanceBuilder(ApiInit):
    """
    - InstanceBuilder -
    Class Description: Create and upgrade instances on GCE
    Parameter Details: Class may be initiated or methods called individually
    Required Parameters: NONE
    Optional Parameters:
    'project': GCE project
    'zone': GCE zone
    """

    def __init__(self, project=None, zone=None):
        ApiInit.__init__(self)  # Inhertis ApiInit class for errors and auth

        self.project = project
        self.zone = zone

    def creation_limits(self, **kwargs):
        if self.zone is None or self.project is None:
            self.project, self.zone = _zone_project(kwargs)

        req = self.apicall.machineTypes().list(
            project=self.project, zone=self.zone).execute()

        return req['items']


### TESTING ###
if __name__ == '__main__':
    inst = InstanceManagement()
    # pprint(inst.get_inst_details(project='gcp-creator',
    #                                     zone='us-central1-a', instance='instance-1'))
    pprint(inst.get_inst_disk(project='gcp-creator',
                              zone='us-central1-a', instance='instance-1'))
