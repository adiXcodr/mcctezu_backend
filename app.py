from flask import Flask, Blueprint,jsonify
from flask_cors import CORS
import pymongo
import run_model
import constants as CONST

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(run_model.bp, url_prefix='/run-model')

# endpoint to check service status
@app.route("/status")
def check_status():
    return jsonify({CONST.STATUS: CONST.SUCCESS, CONST.DATA: None})


if __name__ == "__main__":
    app.run(host="localhost", port="9999", debug=True, use_reloader=True)