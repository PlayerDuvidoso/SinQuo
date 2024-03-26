from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from pydantic import BaseModel
from icecream import ic
from urllib.parse import quote_plus
import dotenv
from flask_login import UserMixin

#   -->Loading and getting the Environment Variables<--
dotenv.load_dotenv(dotenv.find_dotenv())

private_key = os.getenv('private_key')
mongouser = quote_plus(os.getenv('mongouser'))
password = quote_plus(os.getenv('password'))
cluster = os.getenv('uri_cluster')
uri_start = os.getenv('uri_start')
uri_end = os.getenv('uri_end')
uri = f"{uri_start}{mongouser}:{password}{cluster}"

# -->Connecting to MongoDB<--
db_con = MongoClient(uri, server_api=ServerApi('1'))
db = db_con['SinQuo']
user_col = db['Users']


#   -->User Model<--
class User(BaseModel, UserMixin):
    id: str = ''
    email: str
    password: str
    username: str
    quote: str

    def get_id(self):
        return super().get_id()


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

def get_user(email: str):
    user_data = user_col.find_one({'email': f'{email}'})
    ic(user_data)
    user = User(id=str(user_data['_id']), email=user_data['email'], password=user_data['password'], username=user_data['username'], quote=user_data['quote'])
    return  user
    