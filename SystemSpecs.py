# Libraries used
# Clean up program exit
import atexit
# Communication with server
import ssl
# Database
import pymongo
# VMware SOAP API
from pyvim.connect import SmartConnect, Disconnect
# Server login details
import ConnectionSettings


# Extract virtual machine specs into variables
def get_info(id, vm):
    summary = vm.summary
    name = summary.config.name
    path = summary.config.vmPathName
    guest = summary.config.guestFullName
    annotation = summary.config.annotation
    if annotation is not "None":
        description = annotation
        power_state = summary.runtime.powerState

    if summary.guest.ipAddress is not None:
        ip = summary.guest.ipAddress
        ip_address = ip
    else:
        ip_address = "Unavaliable"

    if summary.quickStats.hostMemoryUsage is not None:
        print("hostMemory               : ", summary.quickStats.hostMemoryUsage)
        host_memory = summary.quickStats.hostMemoryUsage
    else:
        host_memory = 0
    if summary.quickStats.guestMemoryUsage is not None:
        print("guestmemory              : ", summary.quickStats.guestMemoryUsage)
        guest_usage = summary.quickStats.guestMemoryUsage
    else:
        guest_usage = 0

    assigned_storage = summary.storage.unshared
    used_storage = summary.storage.uncommitted

    vm_database(id, name, path, guest, description, power_state, ip_address, host_memory, guest_usage, assigned_storage,
                used_storage)

# Extract system specs into variables
def get_system_specs(vm):
    #Setup data store retrieval
    length = str(vm.datastore)
    number_of_stores = clean_up(length)
    amount = int(len(number_of_stores))

    for number in range(0, amount):
        total_storage = vm.datastore[number].summary.capacity
        remaining_storage = vm.datastore[number].summary.freeSpace

    # CPU
    num_cpu_cores = vm.runtime.host.hardware.cpuInfo.numCpuCores
    num_cpu_sockets = vm.runtime.host.hardware.cpuInfo.numCpuPackages
    num_cpu_threads = vm.runtime.host.hardware.cpuInfo.numCpuThreads
    cpu_mhz = vm.runtime.host.summary.hardware.cpuMhz
    cpu_model = vm.runtime.host.summary.hardware.cpuModel

    # Memory
    memory_size = vm.runtime.host.hardware.memorySize

    # Machine
    vendor = vm.runtime.host.hardware.systemInfo.vendor
    model = vm.runtime.host.hardware.systemInfo.model

    # ServerIP
    server_ip = vm.runtime.host.name

    # vCenterIP
    vcenter_server_ip = vm.summary.runtime.host.summary.managementServerIp

    # Network
    num_of_nics = vm.runtime.host.parent.host[0].summary.hardware.numNics

    host_database(num_cpu_cores, num_cpu_sockets, num_cpu_threads, cpu_mhz, cpu_model, memory_size, vendor, model,
                  server_ip, vcenter_server_ip, num_of_nics, total_storage, remaining_storage)


# Remove whitepace and irrelevant characters from data
def clean_up(len):
    # Main system settings

    stripped = len.strip("(ManagedObject) [")
    strip = stripped.strip()
    replace = strip.replace(" ", "")
    multilines = replace.replace("\n", "")
    nearly = multilines.strip("]")
    done = nearly.replace("'", "")
    stores = list(done.split(","))
    return stores


def vm_database(id_value, name, path, guest, description, power_state, ipaddress, host_memory, guest_usage, assigned_storage,
                used_storage):
    # connect to database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Virtual_Machines"]
    mycol = mydb["Machines"]

    virtual_machine = [
        {"id": id_value, "name": name, "path": path, "guest": guest, "description": description, "power_state": power_state,
         "ipaddress": ipaddress, "host_memory": host_memory, "vm_memory_usage": guest_usage,
         "host_storage_assigned": assigned_storage, "vm_storage_usage": used_storage}]

    mycol.insert(virtual_machine)
    return

# Store system specs into database
def host_database(num_cpu_cores, num_cpu_sockets, num_cpu_threads, cpu_mhz, cpu_model, memory_size, vendor, model,
                  server_ip, vcenter_server_ip, num_of_nics, total_storage, remaining_storage):
    # connect to database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["System_Specs"]
    mycol = mydb["Specs"]

# Database entries
    system_specs = [
        {"_id": 0, "CPU_Cores": num_cpu_cores, "CPU_Sockets": num_cpu_sockets, "CPU_Threads": num_cpu_threads,
         "CPU_Mhz": cpu_mhz, "CPU_Model": cpu_model, "Memory_Size": memory_size, "Vendor": vendor, "Model": model,
         "Server_IP": server_ip, "vCenter_IP": vcenter_server_ip, "Number_of_Network_Interfaces": num_of_nics,
         "Total_Storage:": total_storage, "Remaining_Storage": remaining_storage}]
    #
    x = mycol.insert(system_specs)
    return


# Connect to server
def connect():
    try:
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        si = SmartConnect(host=ConnectionSettings.hostname(),
                          user= ConnectionSettings.username() ,
                          pwd=ConnectionSettings.password(),
                          port=443,
                          sslContext=None)
        if not si:
            return -1
        # Disconnect from server
        atexit.register(Disconnect, si)

        content = si.RetrieveContent()
        return content

    except:
        return "Connection Failed"


# Determine which information is to be updated
def main(target):
    content = connect()

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            # target = False
            if target == "system":
                vm = vmList[0]
                get_system_specs(vm)

            elif target == "vm":
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["Virtual_Machines"]
                mycol = mydb["Machines"]
                mycol.drop()
                id_value = 0
                for vm in vmList:
                    get_info(id_value, vm)
                    id_value = id_value + 1
            else:
                get_system_specs(vm)
                for vm in vmList:
                    get_info(vm)
    return 0


# Start program
if __name__ == "__main__":
    main()
