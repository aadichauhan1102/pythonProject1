import pymongo


class db_connection:
    def connect_to_mongodb(self):
        connection_string = "mongodb+srv://travel_db:project%40123@cluster0.cmk1l.mongodb.net/travel_db?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["travel_db"]
        return db
