import constants as const

def create_table():
    #Creating Table/Collection
    coll_name=input("Enter Table Name : ")
    collist = const.mydb.list_collection_names()
    #Dropping old collection and creating a new one
    if coll_name in collist: 
      print('Collection Already Present. Recreating...')
      coll = const.mydb[coll_name]
      coll.drop()

    coll = const.mydb[coll_name]
    #Inserting Columns
    col_len=int(input('Enter the number of columns : '))
    print('Enter column names : ')
    col_names=[]
    for i in range(col_len):
      col_names.append(input())
    columns={}
    columns["_id"]=None
    for i in col_names: 
      columns[i] = None
    x = coll.insert_one(columns)

def delete_table():
    coll_name=input("Enter Table Name : ")
    coll = const.mydb[coll_name]
    coll.drop()
    print('Deleted!')

def display_tables():
    collist = const.mydb.list_collection_names()
    print(collist)

def display_table_values():
    coll_name=input("Enter Table Name : ")
    coll = const.mydb[coll_name]
    for x in coll.find():
        print(x)


choice=-1
while(choice!=0):
    choice=int(input( ('1. Create Table\n2. Delete Table\n3. Display Tables\n4. Display values of a table\n0. Exit termination\n') ))
    if(choice==1):
      create_table()
    elif(choice==2):
      delete_table()
    elif(choice==3):
      display_tables()
    elif(choice==4):
      display_table_values()