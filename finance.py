from database import *
from datetime import date

def check_status(db, type="CREDIT"):
    if type == "DEBIT":
        debit = db.debit
        seller = input("Enter the GST Number:-").upper()
        res = debit.find_one({"GSTIN":seller})
        
        if res is None:
            print(f"There is no transaction with the {seller}!")
            return
        
        amt = res["Pending_amount"]
        print(f"Rs.{amt} is due for {seller}!")
    else:
        credit = db.credit
        client = input("Enter the GST Number:-").upper()
        res = credit.find_one({"GSTIN":client})
        
        if res is None:
            print(f"There is no transaction with {client}!")
            return
        
        amt = res["Pending_amount"]
        print(f"Rs.{amt} is due for {client}!")

    return res

def record_debit(db):
    res= check_status(db, "DEBIT")
    if res is None:
        return
    amt = float(input("Enter the amount paid:-"))
    date_ = str(date.today())
    details=input("Enter 1 for cash, for check - enter the check number:-")
    if details == "1":
        details= "CASH"
    transaction(db,res, amt, date_, details,"DEBIT")

def record_credit(db):
    res= check_status(db)
    if res is None:
        return
    amt = float(input("Enter the amount recieved:-"))
    date_=str(date.today())
    details=input("Enter 1 for cash, for check - enter the check number:-")
    if details == "1":
        details= "CASH"
    transaction(db,res, amt, date_, details,"CREDIT")


def transaction(db,res, amt, date, details,type):
    if type=="DEBIT":
        table = db.debit
    else:
        table = db.credit
    fin = db.finance
    data = {
        "GSTIN":res["GSTIN"],
        "Transaction_amount":amt,
        "date":date,
        "details":details,
        "type":type
    }
    fin.insert_one(data)

    query = {"GSTIN":res["GSTIN"]}
    upd = {'$set': {"Pending_amount":res["Pending_amount"]-amt} }
    table.update_one(query,upd)

    print("Transaction recorded succesfully!")


def add_to_debit(db,data):
    debit = db.debit
    seller = data[0]
    amount = data[1]
    query = {"GSTIN":seller}
    res = debit.find_one(query)
    if res is None:
        debit.insert_one({"GSTIN":seller, "Pending_amount":amount})
        print("Added to debits!")
        return
    upd = {'$set': {"Pending_amount":res["Pending_amount"]+amount} }
    debit.update_one(query,upd)
    print("updated the debits!")

def add_to_credit(db,data):
    credit = db.credit
    client = data[0]
    amount = data[1]
    query = {"GSTIN":client}
    res = credit.find_one(query)
    if res is None:
        credit.insert_one({"GSTIN":client, "Pending_amount":amount})
        print("Added to credits!")
        return
    upd = {'$set': {"Pending_amount":res["Pending_amount"]+amount} }
    credit.update_one(query,upd)
    print("updated the credits!")


