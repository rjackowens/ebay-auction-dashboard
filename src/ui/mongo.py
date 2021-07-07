from pymongo import MongoClient, errors


def init_connection():
    try:
        client = MongoClient("mongodb://root:root@mongodb") # 27017
        
        database_names = client.list_database_names()

        print("successfully connected to MongoDB!")
        print ("\ndatabases:", database_names)
        print ("server version:", client.server_info()["version"])

    except errors.ServerSelectionTimeoutError as e:
        raise(e)


def populate_dummy_data():
    """Add 3 dummy build collections to dummy_db database"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.dummy_db # create db

    def build_1():
        db.build_1.drop() # delete collection if exists
        new_col = db.build_1 # create and populate collection

        from dummy_data import build_1
        for build in build_1:
            new_col.insert_one(build).inserted_id

    def build_2():
        db.build_2.drop() # delete collection if exists
        new_col = db.build_2 # create and populate collection

        from dummy_data import build_2
        for build in build_2:
            new_col.insert_one(build).inserted_id

    def build_3():
        db.build_3.drop() # delete collection if exists
        new_col = db.build_3 # create and populate collection

        from dummy_data import build_3
        for build in build_3:
            new_col.insert_one(build).inserted_id

    build_1()
    build_2()
    build_3()


def get_items(collection_name: str) -> list:
    """Retrieves all items in collection"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.dummy_db # specify db
    collection = db[collection_name] # specify collection

    cursor = collection.find({})

    collection_name = []
    for document in cursor:
          collection_name.append(document)

    return collection_name