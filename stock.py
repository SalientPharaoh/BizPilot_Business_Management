from database import *
from datetime import date
from opt_stock import *

#searching for the stock using item code and returning the search result
def SearchStock(db, item_code):
    stock_register = db.stock
    query = {"item_code":item_code}
    data = stock_register.find_one(query)
    try:
        if len(list(data.keys()))!=0 :
            return data
    except:
        return None

#updating the stock collection after a sale
def updateStockSales(db, data):
    stock_register = db.stock
    details = SearchStock(db, data["item_code"])
    rem_quantity = details["quantity"] - data['quantity']
    myquery = { "item_code": data["item_code"] }
    newvalues = { "$set": { "quantity": rem_quantity } }
    stock_register.update_one(myquery, newvalues)

#updating the stock collection after a purchase is made
def updateStockPurchase(db, data):
    stock_register = db.stock
    #showing the purchase amount and getting the selling rate of the product
    print(f"The purchase rate of the product is :- {data['rate']}")
    print(f"The purchase tax rate of the product is :- {data['tax']}")
    rate = float(input(f"Enter the selling rate of the product:-{data['item_code']}\n"))
    tax = float(input(f"Enter the tax rate of the product:-{data['item_code']}\n"))

    #check whether the item exists in the stock collection or not
    check = SearchStock(db, data["item_code"])
    if check is not None: #if it exists, update the entries
        details = check
        rem_quantity = details["quantity"] + data['quantity']
        myquery = { "item_code": data["item_code"] }
        newvalues = { "$set": { "quantity": rem_quantity , "rate":rate, "tax":tax, "amount":rate+tax} }
        stock_register.update_one(myquery, newvalues)
    else: #if does not exist, add the new entry to the stock collection
        values={
            "item_code": data["item_code"],
            "item_name":data["item_name"],
            "rate": rate,
            "tax":tax,
            "amount": rate+tax,
            "quantity":data["quantity"]
        }
        stock_register.insert_one(values)
    
def get_all(db):
    stock_register = db.stock
    all_data = stock_register.find()
    data=[['item code','item name','rate','tax','amount','quantity']]
    for document in all_data:
        if 'item_code' in document:
            data.append([document['item_code'],document['item_name'],document['rate'],document['tax'],document['amount'],document['quantity']])
    
    create_order(db,data)

def create_order(db,data):
    stock_register = db.stock
    d = sorted(data[1:], key=lambda x : int(x[5]))
    cost = int(input("Enter the available amount:- "))
    n = len(d)
    dlist = [[i[-2],i[-3],i[0],i[1]] for i in d]
    process(cost,n,dlist)

    