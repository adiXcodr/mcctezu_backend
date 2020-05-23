from flask import Blueprint, jsonify, request
import pymongo
bp = Blueprint("run_model", __name__)
from passlib.hash import pbkdf2_sha256
import constants as const
#-------------MEMBERS HANDLER ROUTES-------------------
@bp.route("/get_members",methods = ["GET"])
@bp.route("/get_members/",methods = ["GET"])
def get_members():
    coll = const.mydb['members']
    member_list=[]
    members_query=coll.find()
    if(members_query):
        for x in members_query:
            if(x["_id"]!=None):
                member_list.append(x)
        status_response='Success'
    else:
        status_response='Faliure'
    return jsonify({"status":status_response,"data":member_list})

@bp.route("/get_members/<_id>",methods = ["GET"])
def get_member(_id):
    coll = const.mydb['members']
    member_query=coll.find_one({"_id":int(_id)})
    result="No Data"
    if(member_query and member_query["_id"]!=None):
        status_response='Success'
        result=member_query
    else:
        status_response='Faliure'
    return jsonify({"status":status_response,"data":result})


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
    user_agent='{}'. format(request.user_agent)
    remote_user='{}'.format(request.remote_addr)
    output=[]
    if query:
        for i in query:
            output.append({"id":i["id"],"evt_org":i["evt_org"],"evt_name":i["evt_name"],"evt_date":i["evt_date"],"evt_time":i["evt_time"],"evt_venue":i["evt_venue"],"evt_image":i["evt_image"],"remote_user":remote_user,"user_agent":user_agent})
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
        img=const.mongo.db.test.find_one({"id":i["id"]})
        output.append({"id":i["id"],"evt_org":i["evt_org"],"evt_name":i["evt_name"],"evt_date":i["evt_date"],"evt_time":i["evt_time"],"evt_venue":i["evt_venue"],"evt_image":i["evt_image"],"evt_image":i['evt_image']})
    else:
        status_response="Failure"
        output="No Data Found"
    return jsonify({"status":status_response,"result":output})
#----------EVENT IMAGE------------
@bp.route('/get-img/<filename>',methods=['GET'])
def get_img(filename):
    return const.mongo.send_file(filename)

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
        query=event.find()
        if query is None:
            id=1
        else:
            big=0
            for x in query:
                big=x["id"]
                for y in query:
                    if y["id"] > big:
                        big=y['id'] 
            id=big+1
            if 'image' in request.files:
                evt_image=request.files['image']
                const.mongo.save_file(evt_image.filename,evt_image)
                const.mongo.db.test.insert_one({"id":id,"image":evt_image.filename})
                event_id=event.insert_one({"id":id,"evt_name":q["evt_name"],"evt_org":q["evt_org"],"evt_date":q["evt_date"],"evt_time":q["evt_time"],"evt_venue":q["evt_venue"],"evt_image":evt_image.filename})
                status_response=event_id.inserted_id
                if status_response:
                    status_response="Success"
                else:
                    status_response="Failure"
                return jsonify({"status": status_response,"result":output})
            event_id=event.insert_one({"id":id,"evt_name":q["evt_name"],"evt_org":q["evt_org"],"evt_date":q["evt_date"],"evt_time":q["evt_time"],"evt_venue":q["evt_venue"],"evt_image":"-"})
            status_response=event_id.inserted_id
            if status_response:
                status_response="Success"
            else:
                status_response="Failure"
            return jsonify({"status": status_response,"result":output})
    return jsonify({"status": status_response,"result":output})

@bp.route('/update_events',methods=['PUT'])
def update_event_handler():
    event=const.mydb.events
    field=request.json["field"]
    field_update=request.json['field_update']
    file=request.files['image']
    update_fields=event.find_one(field)
    if update_fields:
        output="No Data"
        udt=event.update_one(field,{'$set':field_update})
        if update_fields['evt_image']!=file.filename:
            sts=const.mongo.db.test.delete_one(field)
            if sts:
                const.mongo.save_file(file)
                const.mongo.db.test.insert_one({"id":update_fields['id'],"image":file.filename})
                udt=event.update_one(field,{'$set':{"evt_image":file.filename}})
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
    record=event.find_one(q)
    if record:
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
    return jsonify({"status": status_response,"data":"No Data"})

@bp.route("/notifications/fetch",methods = ["GET"])
@bp.route("/notifications/fetch/",methods = ["GET"])
def fetch_all():
    notifications = const.mydb['notifications']
    doc=[]
    mydoc=notifications.find()
    if(mydoc):
        for x in mydoc:
            if(x["_id"]!=None):
                doc.append(x)
        status_response='Success'
    else:
        status_response='Faliure'
    return jsonify({"status":status_response,"data":doc})

@bp.route("/notifications/fetch/<_id>",methods = ["GET"])
def fetch_id(_id):
    notifications = const.mydb['notifications']
    doc="No Data"
    mydoc=notifications.find_one({"_id":int(_id)})
    print(mydoc)
    if(mydoc):
        doc=mydoc
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
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"data":"No Data"})

@bp.route("/notifications/delete_many",methods=["DELETE"])
def delete_many():
    jn=request.json
    notifications = const.mydb['notifications']
    if(notifications.find_one(jn)):
        status_response = notifications.delete_many(jn)
        if(status_response):
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"data":"No Data"})

@bp.route("/notifications/update",methods=["PUT"])
def update():
    field=request.json
    notifications = const.mydb['notifications']
    if(notifications.find_one({"_id":field["_id"]})):
        status_response = notifications.update_one({"_id":field["_id"]},{"$set":field})
        if(status_response):
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"data":"No Data"})
        
#-------------------ADMIN HANDLER ROUTES-------------------
@bp.route("/admin-add",methods=['POST'])
def admin_handler():
    admin=const.mydb.admin_credentials
    username=request.json["username"]
    pwd=request.json["password"]
    full=request.json["fullname"]
    hsh_pwd=pbkdf2_sha256.hash(pwd)
    status_response=admin.insert_one({"username":username,"fullname":full,"password":hsh_pwd})
    if status_response:
        status_response="Success"
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"result":"No Data"})
@bp.route('/admin-view',methods=['GET'])
def admin_view():
    admin=const.mydb.admin_credentials
    output=admin.find()
    result=[]
    if output:
        status_response="Success"
        for i in output:
            result.append({"username":i["username"],"fullname":i["fullname"]})
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"result":result})

@bp.route('/admin-view/<user>',methods=['GET'])
def admin_view_dynamic(user):
    admin=const.mydb.admin_credentials
    output=admin.find_one({"username":user})
    result=[]
    if output:
        result.append({"username":output["username"],"fullname":output["fullname"]})
        status_response="Success"
    else:
        status_response="Failure"
        result="No Data"
    return jsonify({"status":status_response,"result":result})

@bp.route('/admin-view-check/<user>',methods=['GET'])
def admin_view_check(user):
    admin=const.mydb.admin_credentials
    output=admin.find_one({"username":user})
    result=[]
    if output:
        result.append({"username":output["username"],"password":output["password"]})
        status_response="Success"
    else:
        status_response="Failure"
        result="No Data"
    return jsonify({"status":status_response,"result":result})

@bp.route('/admin-remove',methods=['DELETE'])
def admin_remove():
    admin=const.mydb.admin_credentials
    usr=request.json
    output=admin.find_one(usr)
    if output:
        output=admin.delete_one(usr)
        if output:
            status_response="Success"
        else:
            status_response="Failure"
    else:
        status_response="Failure"
    return jsonify({"status":status_response,"result":"No Data"})