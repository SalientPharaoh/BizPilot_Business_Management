from database import *
from stock import *
from datetime import date
from finance import *


#adding purchases made
def addSales(db):

    #getting requied collections
    s_register = db.sales
    b_register = db.bills
    f_register = db.finance
    stock_details = db.stock
    
    #getting customer details
    try:
        cust = input("Enter client gst number:-").upper()
    except:
        cust = " "

    name = input("Client name:-").upper()
    bill_no = input("Enter bill number:-").upper()

    bill_content={}
    bill_content['date'] = str(date.today())
    total = 0
    i=0

    #getting each bill entry
    while True:
        choice = int(input("0.Done \n 1.Add more items\n"))
        if choice == 0:
            break

        data={}
        code =input("Enter item code:-").upper()

        #checking if item is availabel or not
        stock_details = SearchStock(db, code)

        if stock_details is not None: #if item is available get corresponding details from the stock collection
            data["item_code"] = code
            data["item_name"] = stock_details["item_name"]
            data["rate"] = stock_details["rate"]
            data["tax"] = stock_details["tax"]
            available_quantity = stock_details["quantity"]

            if available_quantity == 0:
                print("No stock available !")
                continue

            required_quantity =  int(input("Enter quantity:-"))

            #checking if quantity in stock is enough or not
            if available_quantity<required_quantity:
                print("Available stock is less than the required stock!")
                select = int(input("1.Proceed with available quantity.\n 2. Skip this item\n"))
                if select==2: #skipping this entry and not updating any collection
                    continue
                else:
                    required_quantity = available_quantity

            data["quantity"] = required_quantity
            data["amount"] = (data["rate"]+(data["tax"])*0.01*data["rate"])*required_quantity
            total+=data["amount"]
            #adding the product entry in the bill
            bill_content[str(i)] = data
            i = i+1
            #updating the stock based on the product sold
            updateStockSales(db, data)

    #adding miscellaneous charges including transport, etc to the bill
    total+=float(input("Enter miscellaneous amount:-"))

    bill_content['amount']=total


    #updating the sales collection
    s_data ={"GSTIN":cust,"Name":name, "Bill_Number": bill_no, "amount" : total}
    x = s_register.insert_one(s_data)
    
    #updating the bills collection
    b_data = {"GSTIN":cust,"Bill_Number": bill_no,"bill_type": "SALES","id":x.inserted_id, "bill_content":bill_content}
    b_register.insert_one(b_data)

    #whether the bill is paid or is on credit
    paid = int(input("Enter 0 if not paid else enter 1:-"))

    if paid ==0:
        add_to_credit(db, [cust,total])
    else:
        fin = db.finance
        details = input("Enter 1 for cash, for cheque - Enter the cheque number:-")
        if details=="1":
            details="CASH"
        data = {
            "GSTIN":cust,
            "Transaction_amount":total,
            "date":str(date.today()),
            "details":details,
            "type":"CREDIT"
        }
        fin.insert_one(data)
