from flask import Blueprint, jsonify, request
import pymongo
import constants as const

bp = Blueprint("run_model", __name__)

#-------------MEMBERS HANDLER ROUTES-------------------

@bp.route("/add_members",methods=["POST"])
def handle_add_members():
    jn=request.json
    coll = const.mydb['members']
    status_response = coll.insert_one(jn)
    if (status_response):
            status_response="Success"
    else:
            status_response="Failure"
    response = jsonify({"status": status_response,"data":"No data"})
    return response


@bp.route('/update_members',methods=['POST'])
def handle_edit_members():
    member=const.mydb['members']
    jn=request.json
    member_id=jn["_id"]
    print(member_id)
    search={}
    search["_id"]=member_id
    search_result=member.find_one(search)
    if (search_result):
        output='Record Found'
        delete=member.delete_one(search_result)
        x = member.insert_one(jn)
        status_response = x
        if (status_response):
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
        output='No Record Found'
    return jsonify({"status":status_response,"result":output})

@bp.route('/delete_members',methods=['POST'])
def handle_delete_members():
    member=const.mydb['members']
    jn=request.json
    member_id=jn["_id"]
    print(member_id)
    search={}
    search["_id"]=member_id
    search_result=member.find_one(search)
    if (search_result):
        output='Record Found'
        delete=member.delete_one(search_result)
        status_response = delete
        if (status_response):
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
        output='No Record Found'
    return jsonify({"status":status_response,"result":output})
    

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

@bp.route("/notifications/fetch",methods = ["GET"])
@bp.route("/notifications/fetch/",methods = ["GET"])
def fetch_all():
    notifications = const.mydb['notifications']
    doc=[]
    mydoc=notifications.find()
    if(mydoc):
        for x in mydoc:
            doc.append(x)
        status_response='Success'
    else:
        status_response='Faliure'
    return jsonify({"status":status_response,"data":doc})

@bp.route("/notifications/fetch/<_id>",methods = ["GET"])
def fetch_id(_id):
    notifications = const.mydb['notifications']
    doc=[]
    mydoc=notifications.find_one({"_id":int(_id)})
    print(mydoc)
    if(mydoc):
        doc.append(mydoc)
        status_response='Success'
    else:
        status_response='Faliure'
    return jsonify({"status":status_response,"data":doc})
    
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


@bp.route("/notifications/update",methods=["PUT"])
def update():
    field=request.json
    notifications = const.mydb['notifications']
    if(notifications.find_one({"_id":field["_id"]})):
        status_response = notifications.update_one({"_id":field["_id"]},{"$set":field})
        if(status_response):
            status_response="Updated"
        else:
            status_response="Failure"
        return jsonify({"status":status_response,"data":"nodata"})
    else:
        return jsonify({"status":"No Record Found"})
        
