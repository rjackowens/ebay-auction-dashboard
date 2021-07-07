from pymongo import MongoClient, errors


def add_item(number:str, collection_name="placeholder"):
    """Add item to collection in dummy_db database"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.flaskdb # specify db
    db.collection_name.drop() # delete collection if already exists
    collection = db[collection_name] # create and populate collection

    my_item = {
        "number" : number
    }

    collection.insert_one(my_item).inserted_id


def get_items(collection_name: str) -> list:
    """Retrieves all items in collection"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.dummy_db # specify db
    collection = db[collection_name] # specify collection

    cursor = collection.find({})

    items = []
    for document in cursor:
          items.append(document)

    return items
