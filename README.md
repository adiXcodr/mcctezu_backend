<h1 align="center" >MCC TEZU BACKEND</h1>
<h3 align="center">An API for handling GET/POST requests for the MCC TEZU Website</h3>

## Technologies used
* Python
* MongoDB
* FLASK

### Live Server Status
https://mcctezu-backend.herokuapp.com/status


### Github Steps
Follow the steps for working on this repository strictly :
1. Fork the repository to your Github account
2. Copy the link (ends with a .git) of your forked repository
3. In a folder of your choice in your local machine, run `git clone thelinkyoujustcopied.git`
4. `cd mcctezu_backend`
5. `git remote add upstream https://github.com/adiXcodr/mcctezu_backend.git` 
6. When ever you want to push your change, do `git add .` and `git commit -m "did a change"` and then do `git pull upstream master`. Then finally, do `git push origin master`.
7. After pushing, go to your forked repository on Github and create a pull request.



### Steps to run the application

1. `cd mcctezu_backend`
   
2. `pip install -r requirements.txt` (only for the first time) then `python app.py`

3. To manipulate/view tables(collections) do `python handle_tables.py`

4. Add or Edit the routes and functions in the file run_model.py




### Testing the API

1. Locally, eg: http://localhost:9999/run-model/add_members
2. With LIVE Heroku Server, eg: https://mcctezu-backend.herokuapp.com/run-model/add_members
3. Test the API with POSTMAN. 

Example Input for add_members and edit members (ALL FIELDS MUST BE SENT):  

```json
    { 
        "_id": 1, 
        "name": "Adittya Dey", 
        "dept": "CSE", 
        "linkedin": "somelink", 
        "phone": "somenumber", 
        "email": "someemail", 
        "image": "somelink",
        "interest": "Full Stack"
    }
```

Example Input for delete members (Send ID):  

```json
    { 
        "_id": 1
    }
```


Example for GET EVENTS :  
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/get_events`
OR `https://mcctezu-backend.herokuapp.com/run-model/get_events/` to get all the records.
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/get_events/<event_name>` to get record for specified event only. 

Example input for ADD EVENTS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/add_events`
INPUT:
```json
    {
        "evt_name":"Codeathon",
        "evt_org":"MCC_TEZU",
        "evt_date":"04/09/2020",
        "evt_time":"3:00pm",
        "evt_venue":"Dean's Building",
        "evt_image":"none"
    }
```
Example input for UPDATE EVENTS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/update_events`
INPUT:
```json
    {
        "field": {
            "evt_name": "Code Hack"
        },
        "field_update": {
            "evt_org": "MCC_TEZU"
        }
    }
```
In `field` attribute give the column name to identify the record to update. In `field_update` specify the column to be updated and give the new value to it.

Example input for DELETE EVENTS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/delete_events`
INPUT:
```json
    {
    "evt_name":"Codathon"
    }
```
Specify the column to identify and delete the record.

Example input for ADD NOTIFICATIONS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/notifications/add`
INPUT:
```json
    {
        "_id":3,
        "date":"27/04/2020",
        "title":"Events",
        "notification":"sample text"
    }
```

Example input for UPDATE NOTIFICATIONS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/notifications/update_one` to Update Single Record OR
Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/notifications/update_many` to Update More Than One Records

INPUT:
```json
    {
        "field": {
            "_id": 3
        },
        "update": {
            "title": "Notifications"
        }
    }
```
In `field` attribute give the column name to identify the record to update. In `update` specify the column to be updated and give the new value to it.

Example input for UPDATE NOTIFICATIONS :
* Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/notifications/delete_one` to Delete Single Record OR
Set the URL TO `https://mcctezu-backend.herokuapp.com/run-model/notifications/delete_many` to Delete More Than One Records
INPUT:
```json
    {

        "_id": 3
    
    }
```

<hr>

## Author

#### [Adittya Dey](https://github.com/adiXcodr)

[<img src="https://image.flaticon.com/icons/svg/185/185964.svg" width="35" padding="10">](https://www.linkedin.com/in/adittya-dey-3966b916b/)
[<img src="https://image.flaticon.com/icons/svg/185/185981.svg" width="35" padding="10">](https://www.facebook.com/adittya.d