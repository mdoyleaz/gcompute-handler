import pprint # TEMPORARY: FORMATTING FOR BUILDING RETURNS
from gce_api_calls import InstanceManagement

class InstDetailinst_req(object):
    def __init__(self, project, zone, instance):
        ## Creates object to retreive instance details
        inst_call = InstanceManagement(project, zone, instance)

        ## Pulls the 'items' key from the list inst_request
        self.inst_req = inst_call.get_inst_details()
        self.disk_req = inst_call.get_inst_disk()

        ########################################
        # pprint.pprint(self.inst_req) ## Readout for building returns
        ########################################

    def get_inst_tag(self):
        inst_tag = self.inst_req['tags']

        return inst_tag

    def get_inst_name(self):
        inst_name = self.inst_req['name']

        return inst_name

    def get_creation_time(self):
        timestamp = self.inst_req['creationTimestamp']
        date = timestamp[:timestamp.find('T')]
        time = timestamp[(timestamp.find('T') + 1):timestamp.find('.')]

        return {'date': date, 'time': time}

    def get_inst_loc_ip(self):
        inst_loc_ip = self.inst_req['networkInterfaces'][0]['networkIP']

        return inst_loc_ip

    def get_inst_pub_ip(self):
        try:
            pub_ip = self.inst_req['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        except KeyError:
            pub_ip = ""

        return pub_ip

    def get_inst_status(self):
        pwr_status = self.inst_req['status']

        if pwr_status.lower() == 'running':
            inst_status = 'ONLINE'
        elif pwr_status.lower() == 'terminated':
            inst_status = 'OFFLINE'
        elif pwr_status.lower() == 'stopping':
            inst_status = "POWERING DOWN"
        elif pwr_status.lower() == 'starting':
            inst_status = "POWERING ON"
        else:
            inst_status = 'UNKNOWN'

        return inst_status

    def get_inst_cpu_platform(self):
        platform = self.inst_req['cpuPlatform']

        return platform

    def get_inst_disk_size(self):
        disk_size = int(self.disk_req['items'][0]['sizeGb'])

        return f'{disk_size} GB'

    def get_inst_os(self):
        os_lic_url = self.inst_req['disks'][0]['licenses'][0]
        os_type = os_lic_url[(os_lic_url.rfind('/') + 1):]

        return os_type

    def get_inst_machine_type(self):
        machine_type_url = self.inst_req['machineType']
        machine_type = machine_type_url[(machine_type_url.rfind('/') + 1):]

        return machine_type



if __name__ == '__main__':
    instance = input("Enter Instance: ")

    class_inst = InstDetailinst_req(
        'gcp-creator', 'us-central1-a', instance)

    inst_name = class_inst.get_inst_name()
    inst_status = class_inst.get_inst_status()
    inst_creation_date_time = class_inst.get_creation_time()
    inst_intern_ip = class_inst.get_inst_loc_ip()
    inst_pub_ip = class_inst.get_inst_pub_ip()
    inst_cpu_platform = class_inst.get_inst_cpu_platform()
    inst_disk_size = class_inst.get_inst_disk_size()
    inst_os_type = class_inst.get_inst_os()
    inst_machine_type = class_inst.get_inst_machine_type()
    inst_tags = class_inst.get_inst_tag()


    print(f"Instance Name: {inst_name}")
    print(f"Instance Status: {inst_status}")
    print(f"Creation Date: {inst_creation_date_time['date']}")
    print(f"Creation Time: {inst_creation_date_time['time']}")
    print(f"Disk Size: {inst_disk_size}")
    print(f"OS: {inst_os_type}")
    print(f"Internal IP: {inst_intern_ip}")
    print(f"Public IP: {inst_pub_ip}")
    print(f"CPU Platform: {inst_cpu_platform}")
    print(f"Machine Type: {inst_machine_type}")
    print(f'Instance Tags = {inst_tags}')
