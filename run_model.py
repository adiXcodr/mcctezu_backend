from flask import Blueprint, jsonify, request
import pymongo
import constants as const

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
    
