from flask import Flask, Blueprint,jsonify
from flask_cors import CORS
import pymongo
import run_model
import constants as CONST
from waitress import serve
import os
from flask_pymongo import PyMongo

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(run_model.bp, url_prefix='/run-model')
app.config['MONGO_URI']='mongodb+srv://admin:nydqqzuy1324@cluster0-oobol.mongodb.net/test?retryWrites=true&w=majority'
mongo=PyMongo(app)

# endpoint to check service status
@app.route("/status")
def check_status():
    return jsonify({CONST.STATUS: CONST.SUCCESS, CONST.DATA: None})


if __name__ == "__main__":  #Local
    app.run(host="localhost", port="3434", debug=True, use_reloader=True)

else:     #Production (Heroku)
    port = int(os.environ.get('PORT', 33507))
    serve(app,port=port)