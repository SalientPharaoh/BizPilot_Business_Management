from database import *
from datetime import date
from stock import *
from finance import *

#adding purchases made
def addPurchase(db):

    #getting required database collections
    p_register = db.purchase
    b_register = db.bills
    f_register = db.finance

    seller = input("Enter seller gst number:-").upper()
    name = input("Seller name:-").upper()
    bill_no = input("Enter bill number:-").upper()

    bill_content={}
    bill_content['date'] = str(date.today())
    total = 0
    i=0
    #Getting each bill entry for the bill
    choice = 1
    while True:
        if choice == 0:
            break
        data={}
        data["item_code"] = input("Enter item code:-").upper() #item code
        data["item_name"] = input("Enter item name:-").upper() #item name
        data["rate"] = float(input("Enter the rate:-")) #purchase rate
        data["tax"] = float(input("Enter the tax amount:-")) #rate of tax
        data["quantity"] = int(input("Enter quantity:-")) #purchased quantity
        data["amount"] = (data['rate']+(data["tax"])*0.01*data['rate'])*data['quantity'] #calculating the item amount
        total+=data["amount"] #updating total bill value
        bill_content[str(i)] = data #adding the entry to bill
        i+=1


        #updating the stock register for the newly added product entry
        updateStockPurchase(db, data)

        choice = int(input("0.Done \n 1.Add more items\n"))

    total+=float(input("Enter miscellaneous amount:-")) #total bill value after all expenses

    bill_content['amount']=total #adding final payable amount by the user

    #adding the purchase entry to purchase collection
    p_data ={"GSTIN":seller,"Name":name, "Bill_Number": bill_no, "amount" : total}
    x = p_register.insert_one(p_data)

    #adding the detailed bill to the bill collection
    b_data = {"GSTIN":seller,"Bill_Number": bill_no,"bill_type": "PURCHASE","id":x.inserted_id, "bill_content":bill_content}
    b_register.insert_one(b_data)

    #to update the finance collection
    #adding functions to accept payments and handling finances
    add_to_debit(db, [seller,total])


