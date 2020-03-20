import pymongo
from flask import Flask, jsonify
from flask_restful import Api

import GetVMs
import SystemSpecs

# Setup REST API
app = Flask(__name__)
api = Api(app)


# Server GET requests
@app.route('/api/monitoring/status', methods=['GET'])
def test():
    try:
        # print(SystemSpecs.connect())
        if SystemSpecs.connect() == "Connection Failed":
            return jsonify({"message": SystemSpecs.connect()})
        else:
            return jsonify({"message": "Online"})

    except test.exceptions.RequestException as e:
        return e


@app.route('/api/monitoring/host/specs', methods=['GET'])
def specs():
    try:
        SystemSpecs.main("system")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["System_Specs"]
        mycol = mydb["Specs"]
        mycol.drop()
        SystemSpecs.main("system")
        data_query = {"id": 1}
        results = mycol.find(data_query)
        for id in results:
            del id['_id']
            del id['id']
        print(id)
        return jsonify({"specs": id})
    except:
        return jsonify({"message": "An error occurred"})


@app.route('/api/monitoring/vmlist', methods=['GET'])
def vm_list():
    # try:
    #
    #     print(GetVMs.vmstatus())
    #     return jsonify({"message":GetVMs.vmstatus()})
    #
    # except vm_list.exceptions.RequestException as e:
    #     print(e)

    try:

        print(GetVMs.by_ip())
        return jsonify({"message": GetVMs.by_ip()})

    except vm_list.exceptions.RequestException as e:
        print(e)


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
    app.run(host='0.0.0.0', port=5000, debug=True)
