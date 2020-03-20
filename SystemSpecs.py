#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the vms on an ESX / vCenter host
"""

from __future__ import print_function

import atexit
import ssl

import pymongo
from pyVmomi import vim
from pyvim.connect import SmartConnect, Disconnect


def GetArgs():
    #  """
    # Supports the command-line arguments listed below.
    # """
    #  parser = argparse.ArgumentParser(
    #      description='Process args for retrieving all the Virtual Machines')
    #  parser.add_argument('-s', '--host', required=True, action='store',
    #                      help='Remote host to connect to')
    #  parser.add_argument('-o', '--port', type=int, default=443, action='store',
    #                      help='Port to connect on')
    #  parser.add_argument('-u', '--user', required=True, action='store',
    #                      help='User name to use when connecting to host')
    #  parser.add_argument('-p', '--password', required=False, action='store',
    #                      help='Password to use when connecting to host')
    #  args = parser.parse_args()
    #  return args
    return


def get_info(vm, depth=1):
    """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
    maxdepth = 10
    run = False
    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vm_list = vm.childEntity
        for c in vm_list:
            get_info(c, depth + 1)
        return

    # if this is a vApp, it likely contains child VMs
    # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
    if isinstance(vm, vim.VirtualApp):
        vm_list = vm.vm
        for c in vm_list:
            get_info(c, depth + 1)
        return
    summary = vm.summary

    print("Name                     : ", summary.config.name)
    name = summary.config.name
    print("Path                     : ", summary.config.vmPathName)
    path = summary.config.vmPathName
    print("Guest                    : ", summary.config.guestFullName)
    guest = summary.config.guestFullName
    annotation = summary.config.annotation
    if annotation is not None and annotation != "":
        print("Annotation               : ", annotation)
    description = annotation
    print("State                    : ", summary.runtime.powerState)
    power_state = summary.runtime.powerState
    if summary.guest is not None:
        ip = summary.guest.ipAddress
        if ip is not None and ip != "":
            print("IP                       : ", ip)
        ip_address = ip
    if summary.runtime.question is not None:
        print("Question              : ", summary.runtime.question.text)
    print("")
    if summary.quickStats is not None:
        print("hostMemory               : ", summary.quickStats.hostMemoryUsage)
        host_memory = summary.quickStats.hostMemoryUsage
        print("guestmemory              : ", summary.quickStats.guestMemoryUsage)
        guest_usage = summary.quickStats.guestMemoryUsage
    if summary.storage is not None:
        print("Guesttotalstorage        : ", summary.storage.unshared)
        assigned_storage = summary.storage.unshared
        print("guestusedstorage         : ", summary.storage.uncommitted)
        used_storage = summary.storage.uncommitted
        print("Systemstorage            : ", summary.storage.unshared)

    vm_database(name, path, guest, description, power_state, ip_address, host_memory, guest_usage, assigned_storage,
                used_storage)


def get_system_specs(vm):
    length = str(vm.datastore)
    number_of_stores = clean_up(length)
    print(clean_up(length))
    amount = int(len(number_of_stores))
    print(amount)
    print("SYSTEM DETAILS")
    for number in range(0, amount):
        print(vm.datastore[number].summary.name)
        sopa = vm.datastore[number].summary.name
        print(vm.datastore[number].summary.capacity)

        print(vm.datastore[number].summary.freeSpace)

    # CPU
    print(vm.runtime.host.hardware.cpuInfo.numCpuCores)
    num_cpu_cores = vm.runtime.host.hardware.cpuInfo.numCpuCores

    print(vm.runtime.host.hardware.cpuInfo.numCpuPackages)
    num_cpu_sockets = vm.runtime.host.hardware.cpuInfo.numCpuPackages

    print(vm.runtime.host.hardware.cpuInfo.numCpuThreads)
    num_cpu_threads = vm.runtime.host.hardware.cpuInfo.numCpuThreads

    # not clear print(vm.runtime.host.hardware.cpuInfo.hz
    print(vm.runtime.host.parent.host[0].summary.hardware.cpuMhz)
    cpu_mhz = vm.runtime.host.parent.host[0].summary.hardware.cpuMhz

    print(vm.runtime.host.parent.host[0].summary.hardware.cpuModel)
    cpu_model = vm.runtime.host.parent.host[0].summary.hardware.cpuModel

    # Memory
    print(vm.runtime.host.hardware.memorySize)
    memory_size = vm.runtime.host.hardware.memorySize

    # Machine
    print(vm.runtime.host.hardware.systemInfo.vendor)
    vendor = vm.runtime.host.hardware.systemInfo.vendor

    print(vm.runtime.host.hardware.systemInfo.model)
    model = vm.runtime.host.hardware.systemInfo.model

    # ServerIP
    print(vm.runtime.host.name)
    server_ip = vm.runtime.host.name

    # vCenterIP
    print(vm.summary.runtime.host.summary.managementServerIp)
    vcenter_server_ip = vm.summary.runtime.host.summary.managementServerIp

    # Network
    print(vm.runtime.host.parent.host[0].summary.hardware.numNics)
    num_of_nics = vm.runtime.host.parent.host[0].summary.hardware.numNics

    host_database(num_cpu_cores, num_cpu_sockets, num_cpu_threads, cpu_mhz, cpu_model, memory_size, vendor, model,
                  server_ip, vcenter_server_ip, num_of_nics)

    # if summary.vm.datastore is not None:


# database(name, path, guest, description, power_state, ip_address)

def clean_up(len):
    # Main system settings

    #  print(json.loads(len))
    stripped = len.strip("(ManagedObject) [")
    strip = stripped.strip()
    replace = strip.replace(" ", "")
    multilines = replace.replace("\n", "")
    nearly = multilines.strip("]")
    done = nearly.replace("'", "")
    stores = list(done.split(","))
    return stores


def vm_database(name, path, guest, description, power_state, ipaddress, host_memory, guest_usage, assigned_storage,
                used_storage):
    # connect to database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Virtual_Machines"]
    mycol = mydb["Machines"]
    # f description = :

    virtual_machine = [
        {id: 1, "name": name, "path": path, "guest": guest, "description": description, "power_state": power_state,
         "ipaddress": ipaddress, "host memory": host_memory, "vm memory usage": guest_usage,
         "host storage assigned": assigned_storage, "vm storage used": used_storage}]
    x = mycol.insert_many(virtual_machine)


def host_database(num_cpu_cores, num_cpu_sockets, num_cpu_threads, cpu_mhz, cpu_model, memory_size, vendor, model,
                  server_ip, vcenter_server_ip, num_of_nics):
    # connect to database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["System_Specs"]
    mycol = mydb["Specs"]
    # f description = :

    system_specs = [
        {"id": 1, "CPU Cores": num_cpu_cores, "CPU Sockets": num_cpu_sockets, "CPU Threads": num_cpu_threads,
         "CPU Mhz": cpu_mhz, "CPU Model": cpu_model, "Memory Size": memory_size, "Vendor": vendor, "Model": model,
         "Server IP": server_ip, "vCenter IP": vcenter_server_ip, "Number of Network Interfaces": num_of_nics}]
    x = mycol.insert_many(system_specs)


def connect():
    try:
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        si = SmartConnect(host="192.168.1.190",
                          user="root",
                          pwd="Networking101!",
                          port=443,
                          sslContext=None)
        if not si:
            print("Could not connect to the specified host using specified username and password")
            return -1
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()
        return content

    except:
        print("failed")
        return "Connection Failed"


def main(target):
    """
   Simple command-line program for listing the virtual machines on a system.
   """

    # args = GetArgs()
    # if args.password:
    #    password = args.password
    # else:
    #    password = getpass.getpass(prompt='Enter password for host %s and '
    #                                      'user %s: ' % (args.host,args.user))
    #
    # context = None
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
                for vm in vmList:
                    get_info(vm)
            else:
                get_system_specs(vm)
                for vm in vmList:
                    get_info(vm)

    return 0


# Start program
if __name__ == "__main__":
    main()
