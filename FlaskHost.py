# Libraries for API
from flask import Flask, request, jsonify
from flask_restful import Api
# Database
import pymongo
# External programs
import GetVMs
import SystemSpecs

# Setup REST API
app = Flask(__name__)
api = Api(app)


# Server GET requests
# Check status of server connection
@app.route('/api/monitoring/status', methods=['GET'])
def test():
    try:
        # Attempt to connect to server
        if SystemSpecs.connect() == "Connection Failed":
            return jsonify({"System": SystemSpecs.connect()})
        else:
            return jsonify({"System": "Online"})

    except test.exceptions.RequestException:
        return jsonify({"System": "An Error occurred"})

# Get latest server system specification
@app.route('/api/monitoring/host/specs', methods=['GET'])
def specs():
    try:
        # Update database to verify connection is fine
        SystemSpecs.main("system")
        # Connect to database
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["System_Specs"]
        mycol = mydb["Specs"]

        # Clear database
        mycol.drop()

        # Update database
        SystemSpecs.main("system")

        # Retrieve data from database
        data_query = {"id": 0}
        results = mycol.find(data_query)
        for id in results:
            del id['_id']
            del id['id']

        # Export as JSON
        return jsonify(id)

    except test.exceptions.RequestException:
        ''' In the case the server is having issues. The archived database can be read.
        System specs are unlikely to change.
        '''
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["System_Specs"]
            mycol = mydb["Specs"]

            # Request the system specs
            results = mycol.find({"_id": 0})
            for id in results:
                del id['_id']
            # Output as JSON
            return jsonify(id)

        except test.exceptions.RequestException:
            return jsonify({"message": "An error occurred"})

# Get latest virtual machine list
@app.route('/api/monitoring/vmlist', methods=['GET'])
def vm_list():
    try:
        machines = []
        # Update virtual machines
        SystemSpecs.main("vm")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Virtual_Machines"]
        mycol = mydb["Machines"]

        # Read entire database
        results = mycol.find({})
        for virtual_machines in results:
            del virtual_machines['_id']
            machines.append(virtual_machines)
        # Output as JSON
        return jsonify(machines)

    except test.exceptions.RequestException:
        return jsonify({"message": "An error occurred"})

    # try:
    #
    #     print(GetVMs.by_ip())
    #     return jsonify({"message": GetVMs.by_ip()})
    #
    # except vm_list.exceptions.RequestException as e:
    #     print(e)


# @app.route('/api/monitoring/ip-address', methods=['GET'])
# def ip_address():
#     try:
#
#         print(GetIPs.vmstatus())
#         return jsonify({"message":GetIPs.vmstatus()})
#
#     except vm_list.exceptions.RequestException as e:
#         print(e)
#
# #Server Post requests
# @app.route('/api/request/create-vm', methods=['post'])
# def create_vm():
#     try:
#          result = "Online"
#          return jsonify({"message": result})
#
#     except create_vm.exceptions.RequestException as e:
#         print(e)
#
# Dashboard
# @app.route('/status/dashboard', methods=['GET'])
# def dashboard():
#     try:
#         result = "Online"
#         return jsonify({"message": result})
#
#     except dashboard.exceptions.RequestException as e:
#         print(e)
if __name__ == '__main__':
    app.run(port=5000)
