from database import *
from purchases import *
from sales import *

gst = input("Enter you GST Number:-").upper()
db = database(gst)

while True:
    choice = int(input("1.Add purchase\n 2.Add Sales\n"))
    if choice == 1:
        addPurchase(db)
    elif choice==2:
        addSales(db)
    else:
        break
