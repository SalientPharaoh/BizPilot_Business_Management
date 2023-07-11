from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv('USERDATA')
password = os.getenv('DATAPASSKEY')

uri = f"mongodb+srv://{username}:{password}@bizpilot.jot7bhn.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

class database():
    def __init__(self, GSTIN):
        try:
            client.admin.command('ping')
        except Exception as e:
            print(e)
            return
        
        temp = client.list_databases()
        dblist = [i['name'] for i in temp]
        
        self.gstin = GSTIN.upper()
        db = client[self.gstin]
        self.sales = db['sales'] #contains all sales made
        self.purchase = db['purchases'] #contains all purchases made
        self.stock = db['stock'] #contains the details and rate of items
        self.finance = db['finance'] #contains all financial transaction details
        self.bills = db['bills'] #contains all sales and purchase bills

        if GSTIN.upper() not in dblist:
            self.sales.insert_one({'description':"All details about sales"})
            self.purchase.insert_one({'description':"All details about purchases"})
            self.stock.insert_one({'description':"All details about stock"})
            self.finance.insert_one({'description':"All details about finances"})
            self.bills.insert_one({'description':"All details about bills"})