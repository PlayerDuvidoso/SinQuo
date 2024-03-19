from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from pydantic import BaseModel
from icecream import ic

private_key = os.getenv('private_key')
uri = "mongodb+srv://artuzao97:Cerrano97%21@cluster-sinquo.yigs2wj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-SinQuo"                                          

# -->Connecting to MongoDB<--
db_con = MongoClient(uri, server_api=ServerApi('1'))
db = db_con['SinQuo']
user_col = db['Users']


#   -->User Model<--
class User(BaseModel):
    email: str
    password: str
    username: str
    quote: str


def email_exists(useremail: str):
    email_exist = user_col.find_one({'email': f'{useremail}'})
    return email_exist

def quote_exists(userquote: str):
    quote_exist = user_col.find_one({'quote': f'{userquote}'})
    return quote_exist

def username_exists(username: str):
    username_exist = user_col.find_one({'username': f'{username}'})
    return username_exist

def create_user(useremail: str, userpassword: str, username: str, userquote: str):

    data = User(email=useremail, password=userpassword, username=username, quote=userquote)
    return user_col.insert_one(data.model_dump()).inserted_id
    