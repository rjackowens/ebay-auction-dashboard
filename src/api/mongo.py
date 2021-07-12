from pymongo import MongoClient, errors


def delete_collection(collection_name:str):
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db
    db = client.flaskdb # specify db
    db[collection_name].drop()
    client.close()


def add_item(brand:str, price:str, bids:str, url:str, time_left:str, collection_name="", is_auction=True): # bids:str
    """Add item to collection in flaskdb database"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.flaskdb # specify db

    collection = db[collection_name]

    # # create and populate collection
    # if is_auction:
    #     collection = db[collection_name]
    # else:
    #     print("using bit collections")
    #     collection = db[collection_name] + "-bit"

    db_item = {
        "brand" : brand,
        "price" : price,
        "url" : url,
        "time_left" : time_left
    }

    if is_auction: # property only used for auctions
        db_item["bids"] = bids

    collection.insert_one(db_item).inserted_id
    client.close()


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
