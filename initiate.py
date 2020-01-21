import os
import sqlite3
import sys
import persistence


def main(args):
    if os.path.isfile('moncafe.db'):
        os.remove('moncafe.db')
    _conn = sqlite3.connect('moncafe.db')
    rep = persistence.start(_conn)
    inputFile = os.path.abspath(os.path.realpath(sys.argv[1]))
    rep.create_tables(_conn)
    with open(inputFile) as inputfile:
        for line in inputfile:
            line = line.strip()
            words = line.split(',')
            if words[0] == 'C':
                id = words[1].strip(' \n\r\t')
                location = words[2].strip(' \n\r\t')
                num = words[3].strip(' \n\r\t')
                rep.Coffee_stands.insert(persistence.Coffee_stand(id, location, num))
            if words[0] == 'E':
                id = words[1].strip(' \n\r\t')
                name = words[2].strip(' \n\r\t')
                salary = words[3].strip(' \n\r\t')
                stand = words[4].strip(' \n\r\t')
                rep.Employees.insert(persistence.Employee(id, name, salary, stand))
            if words[0] == 'S':
                id = words[1].strip(' \n\r\t')
                name = words[2].strip(' \n\r\t')
                info = words[3].strip(' \n\r\t')
                rep.Suppliers.insert(persistence.Supplier(id, name, info))
            if words[0] == 'P':
                id = words[1].strip(' \n\r\t')
                info = words[2].strip(' \n\r\t')
                price = words[3].strip(' \n\r\t')
                quantity = 0
                rep.Products.insert(persistence.Product(id, info, price, quantity))

    rep.close(_conn)


if __name__ == '__main__':
    main(sys.argv)
