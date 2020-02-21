import sys
#sys.path.insert(0, '/usr/lib/python2.7/site-packages')
from pyvim import connect

my_cluster = connect.SmartConnectNoSSL(host="192.168.1.153", user="administrator@esxi.local", pwd="Networking101!", port=443)
# Get a searchIndex object
searcher = my_cluster.content.searchIndex

# Find a VM
vm_name = searcher.FindByIp(ip="192.168.1.192", vmSearch=True)
#vm_specs = vm
for pool in my_cluster.RetrieveContent().rootFolder.childEntity[0].hostFolder.childEntity[4].resourcePool.resourcePool:
    print(pool.name)
# Print out vm name
print(vm_name.config.name)
