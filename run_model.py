from flask import Blueprint, jsonify, request
import pymongo
import constants as const
import json

bp = Blueprint("run_model", __name__)


@bp.route("/add_members",methods=["POST"])
def handle_add_members():
    jn=request.json
    coll = const.mydb['members']
    x = coll.insert_one(jn)
    status_response = x.inserted_id
    if(isinstance(status_response, int)):
        status_response='Success'
    else:
        status_response='Failure'
    response = jsonify({"status": status_response,"data":"No data"})
    return response


#-------------EVENTS HANDLER ROUTES-------------------

@bp.route('/get_events',methods=['GET'])
@bp.route('/get_events/',methods=['GET'])
def get_event_handler():
    event=const.mydb.events
    query=event.find()
    output=[]
    if query:
        for i in query:
            output.append({"evt_org":i["evt_org"],"evt_name":i["evt_name"],"evt_date":i["evt_date"],"evt_time":i["evt_time"],"evt_venue":i["evt_venue"],"evt_image":i["evt_image"]})
        status_response="Success"
    else:
        status_response="Failure"
        output="No Record Found"
    return jsonify({"status":status_response,"result":output})

@bp.route('/get_events/<evt_name>',methods=['GET'])
def get_event_handler_dynamic(evt_name):
    event=const.mydb.events
    i=event.find_one({"evt_name":evt_name})
    output=[]
    if i:
        status_response='Success'
        output.append({"evt_org":i["evt_org"],"evt_name":i["evt_name"],"evt_date":i["evt_date"],"evt_time":i["evt_time"],"evt_venue":i["evt_venue"],"evt_image":i["evt_image"]})
    else:
        status_response="Failure"
        output="No Data Found"
    return jsonify({"status":status_response,"result":output})

@bp.route('/add_events',methods=['POST'])
def add_events_handler():
    event=const.mydb.events
    q=request.json
    query=event.find_one(q)
    if query:
        status_response="Failure"
        output="Record Already Present"
    else:
        output="No Data"
        event_id=event.insert_one(q)
        status_response=event_id.inserted_id
        if status_response:
            status_response="Success"
        else:
            status_response="Failure"
    return jsonify({"status": status_response,"result":output})

@bp.route('/update_events',methods=['PUT'])
def update_event_handler():
    event=const.mydb.events
    field=request.json["field"]
    field_update=request.json['field_update']
    if event.find_one(field):
        output="No Data"
        udt=event.update_one(field,{'$set':field_update})
        if udt:
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
        output="Record Not Found"
    return jsonify({"status":status_response,"result":output})

@bp.route('/delete_events',methods=['DELETE'])
def delete_event_handler():
    event=const.mydb.events
    q=request.json
    if event.find_one(q):
        dlt=event.delete_one(q)
        output='No Data'
        if dlt:
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
        output='No Record Found'
    return jsonify({"status":status_response,"result":output})
    
#-----------Notifications Routes-----------------

@bp.route("/notifications/add",methods=["POST"])
def add_notifications():
    jn=request.json
    notifications = const.mydb['notifications']
    x = notifications.insert_one(jn)
    status_response = x.inserted_id
    print(status_response)
    if(status_response):
        status_response='Success'
    else:
        status_response='Failure'
    response = jsonify({"status": status_response,"data":"No Data"})
    return response

@bp.route("/notifications/delete_one",methods=["DELETE"])
def delete_one():
    jn=request.json
    notifications = const.mydb['notifications']
    if(notifications.find_one(jn)):
        status_response = notifications.delete_one(jn)
        if(status_response):
            status_response="Deleted"
        else:
            status_response="Failure"
        return jsonify({"status":status_response,"data":"nodata"})
    else:
        return jsonify({"status":"No Record Found"})

@bp.route("/notifications/delete_many",methods=["DELETE"])
def delete_many():
    jn=request.json
    notifications = const.mydb['notifications']
    if(notifications.find_one(jn)):
        status_response = notifications.delete_many(jn)
        if(status_response):
            status_response="Deleted"
        else:
            status_response="Failure"
        return jsonify({"status":status_response,"data":"nodata"})
    else:
        return jsonify({"status":"No Record Found"})


@bp.route("/notifications/update_one",methods=["PUT"])
def update_one():
    field=request.json["field"]
    update=request.json['update']
    notifications = const.mydb['notifications']
    if(notifications.find_one(field)):
        status_response = notifications.update_one(field,{"$set":update})
        if(status_response):
            status_response="Updated"
        else:
            status_response="Failure"
        return jsonify({"status":status_response,"data":"nodata"})
    else:
        return jsonify({"status":"No Record Found"})
        
@bp.route("/notifications/update_many",methods=["PUT"])
def update_many():
    field=request.json["field"]
    update=request.json['update']
    notifications = const.mydb['notifications']
    if(notifications.find_one(field)):
        status_response = notifications.update_many(field,{"$set":update})
        if(status_response):
            status_response="Updated"
        else:
            status_response="Failure"
        return jsonify({"status":status_response,"data":"nodata"})
    else:
        return jsonify({"status":"No Record Found"})
        