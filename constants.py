import pymongo


# Generic constants
STATUS = 'status'
SUCCESS = 'success'
ERROR = 'error'
DATA = 'data'

#Creating DB
client = pymongo.MongoClient("mongodb+srv://mcc_admin:admin123@mcc-tezu-c1-qluij.gcp.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["mcc_tezu"]    

#DB FOR IMAGES
