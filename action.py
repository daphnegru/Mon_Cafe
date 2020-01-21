import os
import sqlite3
import sys
import persistence
import printdb


def main(args):
    dbexist = os.path.isfile('moncafe.db')
    if dbexist:
        _conn = sqlite3.connect('moncafe.db')
        rep = persistence.start(_conn)
        inputFile = os.path.abspath(os.path.realpath(sys.argv[1]))
        with open(inputFile) as inputfile:
            for line in inputfile:
                splitline = line.split(',')
                product_id = splitline[0]
                quantity = splitline[1]
                activator_id = splitline[2]
                date = splitline[3]
                q = int(quantity)
                prodQuantity = int(rep.Products.find(product_id))
                if (q < 0):
                    if ((prodQuantity - q) >= 0):
                        amount = prodQuantity + q
                        rep.Products.update(amount,product_id)
                        rep.Activities.insert(persistence.Activity(product_id, quantity, activator_id, date))

                elif (q > 0):
                    amount = prodQuantity+q
                    rep.Products.update(amount, product_id)
                    rep.Activities.insert(persistence.Activity(product_id, quantity, activator_id, date))


    rep.close(_conn)


if __name__ == '__main__':
    main(sys.argv)
    printdb.main()