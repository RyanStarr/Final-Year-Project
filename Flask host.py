import GetVMs
from flask import Flask, jsonify
from flask_restful import Api, Resource

# Setup REST API
app = Flask(__name__)
api = Api(app)

#Server API requests
@app.route('/api/monitoring/status', methods=['GET'])
def test():
    try:
        result = "Status Online"
        return jsonify({"message": result})

    except test.exceptions.RequestException as e:
        print(e)


@app.route('/api/monitoring/vmlist', methods=['GET'])
def vm_list():
    try:

        print(GetVMs.vmstatus())
        return jsonify({"message":GetVMs.vmstatus()})

    except vm_list.exceptions.RequestException as e:
        print(e)


#Server Post requests
@app.route('/api/request/create-vm', methods=['post'])
def create_vm():
    try:
         result = "Online"
         return jsonify({"message": result})

    except create_vm.exceptions.RequestException as e:
        print(e)

#Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        result = "Online"
        return jsonify({"message": result})

    except dashboard.exceptions.RequestException as e:
        print(e)
if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True)
