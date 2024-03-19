from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from pydantic import BaseModel
from icecream import ic
from urllib.parse import quote_plus
import dotenv

#   -->Loading and getting the Environment Variables<--
dotenv.load_dotenv(dotenv.find_dotenv())

private_key = os.getenv('private_key')
mongouser = quote_plus(os.getenv('mongouser'))
password= quote_plus(os.getenv('password'))
cluster = os.getenv('uri_cluster')
uri_start = os.getenv('uri_start')
uri_end = os.getenv('uri_end')
uri = f"{uri_start}{mongouser}:{password}{cluster}{uri_end}"

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
    