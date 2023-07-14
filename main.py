from database import *
from purchases import *
from sales import *
from finance import *

gst = input("Enter you GST Number:-").upper()
db = database(gst)

while True:
    choice = int(input("1.Add purchase\n 2.Add Sales\n3.check debit\n4.check credit\n5.record debit\n6.record credit"))
    if choice == 1:
        addPurchase(db)
    elif choice==2:
        addSales(db)
    elif choice==3:
        print(check_status(db,"DEBIT"))
    elif choice==4:
        print(check_status(db,"CREDIT"))
    elif choice==5:
        record_debit(db)
    elif choice==6:
        record_credit(db)
    else:
        break
