import os
import time
import googleapiclient.discovery
import sys

def list_instance(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    # print('list===', result)

    if 'items' in result:#item有存在才算有vm
        instances = result['items']
        print('total instance==', len(instances))
        for tmp in instances:
            print('instance//', tmp['name'])

def create_instance(compute, project, zone):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-9').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup_sh'), 'r').read()

    config = {
        'name': 'python-instance-test',
        'machineType': machine_type,
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(project=project, zone=zone, body=config).execute()

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

# print( len(sys.argv) )
# print('=====')
if len(sys.argv) <= 1:
    print('請輸入projectid and zone!')
else:
    if len(sys.argv)==2 or sys.argv[2] is None:
        print('請輸入zone')
    elif sys.argv[1] is None:
        print('請輸入projectid')
    else:
        project = sys.argv[1]
        zone = sys.argv[2]
        print('zone=' + zone)
        print('projectid=' + project)
        compute = googleapiclient.discovery.build('compute', 'v1')
        print('query running')
        list_instance(compute, project, zone)
        # print('query done!')
        # operation = create_instance(compute, project, zone)
        # wait_for_operation(compute, project, zone, operation['name'])
        # print('create ok!')
        # list_instance(compute, project, zone)
        print('。')



