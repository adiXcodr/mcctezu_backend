import pymongo
from app import app
from flask_pymongo import PyMongo
app.config['MONGO_URI']='mongodb+srv://admin:nydqqzuy1324@cluster0-oobol.mongodb.net/test?retryWrites=true&w=majority'
mongo=PyMongo(app)
# Generic constants
STATUS = 'status'
SUCCESS = 'success'
ERROR = 'error'
DATA = 'data'

#Creating DB
client = pymongo.MongoClient("mongodb+srv://mcc_admin:admin123@mcc-tezu-c1-qluij.gcp.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["mcc_tezu"]    

#DB FOR IMAGES
