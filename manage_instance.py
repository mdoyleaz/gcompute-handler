from gce_api_calls import GceInstApi

class InstManagement(object):
    def __init__(self, project, zone, instance):
        self.inst_call = GceInstApi(project, zone, instance)
        self.project = project
        self.zone = zone
        self.instance = instance

    def inst_power_control(self, power_option):
        """
        Instance power management controls.
        The following options are supported:
        'start': Starts Instance,
        'stop': Stops Instance,
        'reset': Restarts Instance
        """
        options = ['start', 'stop', 'reset']

        if power_option not in options:
            return f"Invalid Power Option, please use one of the follwing:\n{options}"

        req = self.inst_call.put_inst_power(power_option)

        return f"POWER STATUS: {power_option.upper()} {req['status']}"


### TESTING ###
if __name__ == '__main__':
    inst = InstManagement('gcp-creator', 'us-central1-a', 'instance-1')

    print(inst.inst_power_control('stop'))
