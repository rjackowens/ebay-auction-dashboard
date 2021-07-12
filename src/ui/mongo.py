from pymongo import MongoClient, errors


def get_items(collection_name: str) -> list:
    """Retrieves all items in collection"""
    client = MongoClient("mongodb://root:root@mongodb") # connect to admin db

    db = client.flaskdb # specify db
    collection = db[collection_name] # specify collection

    cursor = collection.find({})

    items = []
    for document in cursor:
          items.append(document)

    return items
