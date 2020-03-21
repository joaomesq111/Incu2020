from flask import render_template, jsonify, request
from pymongo import ReturnDocument


from app import app, collection
from app.Schemas.InterfaceSchema import InterfaceSchema


@app.route('/interfacesHTML/<string:switch>', methods=['GET'])
def get_interfaces_from_switch_html(switch):
    interfaces_list = collection.find({"Switch name": switch})

    if interfaces_list.count() != 0:
        return \
            render_template("routes_templates/switch_interfaces.html", switch_name=switch, interfaces=interfaces_list)
    else:
        return render_template('error_templates/invalid_parameter.html')


@app.route('/interfacesHTML/<string:switch>/<string:interface>', methods=['GET'])
def get_interface_detail_html(switch, interface):
    details = collection.find_one({"Switch name": switch, "Interface name": interface})

    if details:
        return \
            render_template("routes_templates/interface_detail.html",
                            switch_name=switch,
                            interface_name=interface,
                            interface_details=details)
    else:
        return render_template('error_templates/invalid_parameter.html')


@app.route('/interfacesJSON/<string:switch>', methods=['GET'])
def get_interfaces_from_switch_json(switch):
    interfaces_list = collection.find({"Switch name": switch})

    dic = {switch: {}}

    for interface in interfaces_list:
        dic[switch][interface['Interface name']] = \
            {'Description': interface['Description'], 'state': interface['state']}

    return jsonify(dic)


@app.route('/interfacesJSON/<string:switch>/<string:interface>', methods=['GET'])
def get_interface_detail_json(switch, interface):
    details = collection.find_one({"Switch name": switch, "Interface name": interface})

    dic = {details['Interface name']: {'Switch name': details['Switch name'],
                                       'Description': details['Description'],
                                       'state': details['state']
                                       }
           }

    return jsonify(dic)


# PATCH ROUTE BY INTERFACE NAME
"""@app.route('/interfaces/<string:switch>/<string:interface>', methods=['PATCH'])
def patch_interface_description(switch, interface):
    payload = request.json
    dic = {"$set": payload}
    query_filter = {"Switch name": switch, "Interface name": interface}

    result = collection.find_one_and_update(query_filter,
                                            dic,
                                            upsert=False,
                                            return_document=ReturnDocument.AFTER)

    res = {'Switch name': result['Switch name'],
           'Interface name': result['Interface name'],
           'Description': result['Description'],
           'state': result['state']}

    return jsonify(res)"""


# PATCH ROUTE BY ID
@app.route('/interfaces/<string:switch>/<ObjectId:_id>', methods=['PATCH'])
def patch_interface_description_id(switch, _id):
    payload = request.json
    dic = {"$set": payload}
    query_filter = {"Switch name": switch, "_id": _id}

    result = collection.find_one_and_update(query_filter,
                                            dic,
                                            upsert=False,
                                            return_document=ReturnDocument.AFTER)
    print(result)
    res = {'Switch name': result['Switch name'],
           'Interface name': result['Interface name'],
           'Description': result['Description'],
           'state': result['state']}

    return jsonify(res)


@app.route('/add_interface', methods=['POST'])
def add_interface():
    payload = request.json
    schema = InterfaceSchema()
    interface = schema.load(payload)
    print(interface)
