import sqlite3
import persistence


def main():
    _conn = sqlite3.connect('moncafe.db')
    rep = persistence.start(_conn)
    list = rep.Activities.find_all()
    print("Activities")
    for item in list:
        print(item.__str__())
    list = rep.Coffee_stands.find_all()
    print("Coffee stands")
    for item in list:
        print(item.__str__())
    list = rep.Employees.find_all()
    print("Employees")
    for item in list:
        print(item.__str__())
    list = rep.Products.find_all()
    print("Products")
    for item in list:
        print(item.__str__())
    list = rep.Suppliers.find_all()
    print("Suppliers")
    for item in list:
        print(item.__str__())
    list = rep.Activities.find_all()
    print()
    list = rep.Employees.find_all()
    print("Employees report")
    for item in list:
        name = item.name
        salary = item.salary
        building = rep.Coffee_stands.findBuilding(item.coffee_stand)
        total = rep.Activities.find_total(item.id)
        s = ("{} {} {} {}".format(name, salary, building, total))
        print(s)
    list = rep.Activities.find_all()
    if (len(list) > 0):
        print()
        print("Activities")
        s = rep.Activities.find_report()
        for report in s:
            if report[3] is None:
                r = ("({}, '{}', {}, {}, '{}')".format(report[0], report[1], report[2], report[3], report[4]))
            elif report[4] is None:
                r = ("({}, '{}', {}, '{}', {})".format(report[0], report[1], report[2], report[3],report[4]))
            print(r)

    rep.close(_conn)

if __name__ == '__main__':
    main()
