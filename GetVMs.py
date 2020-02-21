import requests
import urllib3
def vmstatus():
    # from vmware.vapi.vsphere.client import create_vsphere_client
    # session = requests.session()
    # session.verify = False
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #
    # # Connect to a vCenter Server using username and password
    # vsphere_client = create_vsphere_client(server='192.168.1.153', username='administrator@esxi.local', password='Networking101!', session=session)
    #
    # # List all VMs inside the vCenter Server
    # print(vsphere_client.vcenter.VM.list())
    # print(vsphere_client.vcenter)
    return "API ran"#vsphere_client.vcenter.VM.list()
