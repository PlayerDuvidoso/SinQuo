from pymongo import MongoClient
from config import private_key

#Connecting to MongoDB
db_con = MongoClient("localhost", 27017)
db = db_con['SinQuo']
user_col = db['Users']


def email_exists(useremail: str):
    email_exist = user_col.find_one({'email': f'{useremail}'})
    return email_exist

def create_user(useremail: str, userpassword: str, username: str, userquote: str):

    data = {'email': f'{useremail}', 'password': f'{userpassword}', 'username': f'{username}', 'quote': f'{userquote}'}

    if not email_exists(useremail):
        user_col.insert_one(data)
        return True
    
    return False