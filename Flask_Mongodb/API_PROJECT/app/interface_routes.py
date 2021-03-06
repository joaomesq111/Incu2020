from flask import render_template, jsonify, request
from pymongo import ReturnDocument
from app import app, collection


@app.route('/<string:switch>/interfaces.html', methods=['GET'])
def get_interfaces_from_switch_html(switch):
    interfaces_list = collection.find({"switch": switch})

    if interfaces_list.count() != 0:
        return \
            render_template("routes_templates/switch_interfaces.html", switch_name=switch, interfaces=interfaces_list)
    else:
        return render_template('error_templates/invalid_parameter.html')


@app.route('/<string:switch>/<string:interface>/details.html', methods=['GET'])
def get_interface_detail_html(switch, interface):
    details = collection.find_one({"switch": switch, "interface": interface})

    if details:
        return \
            render_template("routes_templates/interface_detail.html",
                            switch_name=switch,
                            interface_name=interface,
                            interface_details=details)
    else:
        return render_template('error_templates/invalid_parameter.html')


@app.route('/<string:switch>/interfaces.json', methods=['GET'])
def get_interfaces_from_switch_json(switch):
    interfaces_list = collection.find({"switch": switch})

    dic = {switch: {}}

    for interface in interfaces_list:
        dic[switch][interface['interface']] = \
            {'Description': interface['description'], 'State': interface['state']}

    return jsonify(dic)


@app.route('/<string:switch>/<string:interface>/details.json', methods=['GET'])
def get_interface_detail_json(switch, interface):
    details = collection.find_one({"switch": switch, "interface": interface})

    dic = {details['interface']: {'Switch name': details['switch'],
                                  'Description': details['description'],
                                  'State': details['state']
                                  }
           }

    return jsonify(dic)


# PATCH ROUTE BY INTERFACE NAME
"""@app.route('/interfaces/<string:switch>/<string:interface>', methods=['PATCH'])
def patch_interface_description(switch, interface):
    payload = request.json
    dic = {"$set": payload}
    query_filter = {"switch": switch, "Interface name": interface}
    

    result = collection.find_one_and_update(query_filter,
                                                dic,
                                                upsert=False,
                                                return_document=ReturnDocument.AFTER)
    
    res = {'Switch name': result['switch'],
               'Interface name': result['interface'],
               'Description': result['description'],
               'State': result['state']}
    
    return jsonify(res)"""


# PATCH ROUTE BY ID
@app.route('/<string:switch>/<ObjectId:_id>', methods=['PATCH'])
def patch_interface_description_id(switch, _id):
    payload = request.json
    dic = {"$set": payload}
    query_filter = {"switch": switch, "_id": _id}

    result = collection.find_one_and_update(query_filter,
                                            dic,
                                            upsert=False,
                                            return_document=ReturnDocument.AFTER)

    res = {'Switch name': result['switch'],
           'Interface name': result['interface'],
           'Description': result['description'],
           'State': result['state']}

    return jsonify(res)


@app.route('/add_interface', methods=['POST'])
def add_interface():
    payload = request.json

    post_id = collection.insert_one(payload).inserted_id

    result = collection.find_one({"_id": post_id})

    res = {'Switch name': result['switch'],
           'Interface name': result['interface'],
           'Description': result['description'],
           'State': result['state']}

    return jsonify(res)
