from pymongo import MongoClient, errors

def init_connection():
    try:
        client = MongoClient("mongodb://root:root@localhost") # 27017
        
        database_names = client.list_database_names()

        print("successfully connected to MongoDB!")
        print ("\ndatabases:", database_names)
        print ("server version:", client.server_info()["version"])

    except errors.ServerSelectionTimeoutError as e:
        raise(e)


def create_table():
    client = MongoClient("mongodb://root:root@localhost")

    db = client.new_db
    print("created new db")

    new_col = db.new_col
    print("created new collection")
    
    item = {
        "build_name": "my_build",
        "run_time": 24,
        "status": "success"
    }

    post_id = new_col.insert_one(item).inserted_id
    post_id

    database_names = client.list_database_names()
    print(database_names)
    # client.list_collection_names()

# init_connection()
# create_table()

def get_items_in_collection(collection_name: str) -> list:
    client = MongoClient("mongodb://root:root@localhost") # connect to admin db

    db = client.dummy_db # specify db
    collection = db[collection_name] # specify collection

    cursor = collection.find({})

    collection_name = []
    for document in cursor:
          collection_name.append(document)

    print(collection_name)
    return collection_name

get_items_in_collection("build_1")
