class Coffee_stand(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        s = ("({}, '{}', {})".format(self.id, self.location, self.number_of_employees))
        return s


class Employee(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def __str__(self):
        s = ("({}, '{}', {}, {})".format(self.id, self.name, self.salary, self.coffee_stand))
        return s


class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        s = ("({}, '{}', '{}')".format(self.id, self.name, self.contact_information))
        return s


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        s = ("({}, '{}', {}, {})".format(self.id, self.description, self.price, self.quantity))
        return s


class Activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        s = ("({}, {}, {}, {})".format(self.product_id, self.quantity, self.activator_id, self.date))
        return s


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""INSERT INTO Coffee_stands (id,location,number_of_employees) VALUES(?,?,?)""",
                           [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT id, location, number_of_employees FROM Coffee_stands ORDER BY id
                """).fetchall()
        return [Coffee_stand(*row) for row in all]

    def findBuilding(self, standID):
        c = self._conn.cursor()
        res = c.execute("""
                    SELECT location FROM Coffee_stands
                    WHERE id=?
                """, [standID]).fetchone()
        return res[0]


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""INSERT INTO Employees (id,name,salary,coffee_stand) VALUES(?,?,?,?)""",
                           [employee.id, employee.name.strip(' \n\r\t'), employee.salary, employee.coffee_stand])

    def find(self, id):
        c = self._conn.cursor()
        res = c.execute("""SELECT name, coffee_stand FROM Employees WHERE id = ? ORDER BY name
        """, [id]).fetchone()
        return res[0]

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT id, name, salary, coffee_stand FROM Employees ORDER BY id
                """).fetchall()
        return [Employee(*row) for row in all]


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO Suppliers (id,name,contact_information) VALUES(?,?,?)",
                           [supplier.id, supplier.name.strip(' \n\r\t'), supplier.contact_information.strip(' \n\r\t')])

    def find(self, id):
        c = self._conn.cursor()
        res = c.execute("""SELECT name FROM Suppliers WHERE id = ?
        """, [id]).fetchone()
        return res[0]

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT id, name, contact_information FROM Suppliers ORDER BY id
                """).fetchall()
        return [Supplier(*row) for row in all]


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""INSERT INTO Products (id,description,price,quantity) VALUES(?,?,?,?)""",
                           [product.id, product.description.strip(' \n\r\t'), product.price, 0])

    def find(self, id):
        c = self._conn.cursor()
        res = c.execute("""SELECT quantity FROM Products WHERE id = ?
        """, [id]).fetchone()
        return res[0]

    def update(self, quantity, id):
        c = self._conn.cursor()
        c.execute("""UPDATE Products SET quantity = ? WHERE id = ?
        """, [quantity, id])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT id, description, price, quantity FROM Products ORDER BY id
                """).fetchall()
        return [Product(*row) for row in all]

    def productPrice(self, id):
        c = self._conn.cursor()
        res = c.execute("""SELECT price FROM Products WHERE id= ?
        """, [id]).fetchone()
        return res[0]

    def productName(self, id):
        c = self._conn.cursor()
        res = c.execute("""SELECT description FROM Products WHERE id = ?
        """, [id]).fetchone()
        return res[0]


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""INSERT INTO Activities (product_id,quantity,activator_id,date) VALUES(?,?,?,?)""",
                           [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find(self, product_id):
        c = self._conn.cursor()
        c.execute("""SELECT product_id, stand FROM Activities WHERE product_id = ?
        """, [product_id])
        return Activity(*c.fecthone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT product_id, quantity, activator_id, date FROM Activities ORDER BY date
                """).fetchall()
        return [Activity(*row) for row in all]

    def find_total(self, activator_id):
        total = 0
        rep = start(self._conn)
        for item in rep.Activities.find_all():
            id = item.activator_id
            if id == activator_id:
                total = total + abs((item.quantity * rep.Products.productPrice(item.product_id)))
        return total

    def find_report(self):
        c = self._conn.cursor()
        res = c.execute("""SELECT Activities.date, Products.description, Activities.quantity, Employees.name, Suppliers.name
        FROM Activities LEFT JOIN Products ON Activities.product_id=Products.id LEFT JOIN Employees ON Activities.activator_id = Employees.id LEFT JOIN Suppliers ON Activities.activator_id=Suppliers.id
        ORDER BY Activities.date
                        """).fetchall()
        return res


class _Repository(object):
    def __init__(self, _conn):
        self.Coffee_stands = _Coffee_stands(_conn)
        self.Employees = _Employees(_conn)
        self.Suppliers = _Suppliers(_conn)
        self.Products = _Products(_conn)
        self.Activities = _Activities(_conn)

    def close(self, _conn):
        _conn.commit()
        _conn.close()

    def create_tables(self, _conn):
        _conn.executescript("""
                    CREATE TABLE Employees (
                        id      INTEGER        PRIMARY KEY,
                        name    TEXT        NOT NULL,
                        salary  REAL    NOT NULL,
                        coffee_stand    INTEGER REFERENCES  Coffee_stand(id)
                    );

                    CREATE TABLE Suppliers (
                        id                 INTEGER     PRIMARY KEY,
                        name     TEXT    NOT NULL,
                        contact_information  REAL
                    );

                    CREATE TABLE Products (
                        id      INTEGER     PRIMARY KEY,
                        description  TEXT     NOT NULL,
                        price           REAL     NOT NULL,
                        quantity    INTEGER NOT NULL
                    );

                    CREATE TABLE Coffee_stands (
                        id  INTEGER PRIMARY KEY,
                        location TEXT    NOT NULL,
                        number_of_employees INTEGER
                    );
                    CREATE TABLE Activities (
                        product_id INTEGER  INTEGER REFERENCES  Product(id),
                        quantity INTEGER    NOT NULL,
                        activator_id INTEGER NOT NULL,
                        date    DATE    NOT NULL

                    );
                    """)

def start(_conn):
    repo = _Repository(_conn)
    return repo
