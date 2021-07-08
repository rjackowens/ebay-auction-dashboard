from pymongo import MongoClient, errors


def delete_collection(collection_name:str):
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db
    db = client.flaskdb # specify db
    db[collection_name].drop()


def add_item(brand:str, price:str, bids:str, collection_name=""):
    """Add item to collection in flaskdb database"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.flaskdb # specify db
    collection = db[collection_name] # create and populate collection

    my_item = {
        "brand" : brand,
        "price" : price,
        "bids" : bids
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
