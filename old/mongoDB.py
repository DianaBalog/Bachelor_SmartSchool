import pymongo


class DB:
    client = pymongo.MongoClient(
        "mongodb+srv://Diana:DianaBalog@clusterschool.xiuru.mongodb.net/SmartSchool?retryWrites=true&w=majority")
