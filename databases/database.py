from pymongo import MongoClient

#Connecting to MongoDB
db_con = MongoClient("localhost", 27017)
db = db_con['SinQuo']
user_col = db['Users']

