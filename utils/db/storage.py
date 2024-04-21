import sqlite3 as lite


class DatabaseManager(object):

    def __init__(self, path):
        self.conn = lite.connect(path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.query(
            'CREATE TABLE IF NOT EXISTS products (idx text, title text, body text, photo blob, price int, tag text)')
        self.query('CREATE TABLE IF NOT EXISTS orders (cid int, usr_name text, usr_address text, products text)')
        self.query('CREATE TABLE IF NOT EXISTS cart (cid int, idx text, quantity int)')
        self.query('CREATE TABLE IF NOT EXISTS categories (idx text, title text)')
        self.query('CREATE TABLE IF NOT EXISTS wallet (cid int, balance real)')
        self.query('CREATE TABLE IF NOT EXISTS questions (cid int, question text)')

    def insert_dump_data(self):
        # Inserting data into products
        self.query('INSERT INTO products (idx, title, body, price, tag) VALUES (?, ?, ?, ?, ?)',
                   ('1', 'Coffee Mug', 'A large coffee mug.', 10, 'kitchen'))
        self.query('INSERT INTO products (idx, title, body, price, tag) VALUES (?, ?, ?, ?, ?)',
                   ('2', 'Tea Cup', 'A delicate tea cup.', 5, 'kitchen'))

        # Inserting data into orders
        self.query('INSERT INTO orders (cid, usr_name, usr_address, products) VALUES (?, ?, ?, ?)',
                   (1, 'John Doe', '123 Elm St', '1,2'))
        self.query('INSERT INTO orders (cid, usr_name, usr_address, products) VALUES (?, ?, ?, ?)',
                   (2, 'Jane Smith', '456 Oak St', '2'))

        # Inserting data into cart
        self.query('INSERT INTO cart (cid, idx, quantity) VALUES (?, ?, ?)',
                   (1, '1', 2))
        self.query('INSERT INTO cart (cid, idx, quantity) VALUES (?, ?, ?)',
                   (2, '2', 3))

        # Inserting data into categories
        self.query('INSERT INTO categories (idx, title) VALUES (?, ?)',
                   ('kitchen', 'Kitchenware'))
        self.query('INSERT INTO categories (idx, title) VALUES (?, ?)',
                   ('office', 'Office Supplies'))

        # Inserting data into wallet
        self.query('INSERT INTO wallet (cid, balance) VALUES (?, ?)',
                   (1, 100.0))
        self.query('INSERT INTO wallet (cid, balance) VALUES (?, ?)',
                   (2, 150.0))

        # Inserting data into questions
        self.query('INSERT INTO questions (cid, question) VALUES (?, ?)',
                   (1, 'What is the return policy?'))
        self.query('INSERT INTO questions (cid, question) VALUES (?, ?)',
                   (2, 'Do you ship internationally?'))

    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()


'''

products: idx text, title text, body text, photo blob, price int, tag text

orders: cid int, usr_name text, usr_address text, products text

cart: cid int, idx text, quantity int ==> product_idx

categories: idx text, title text

wallet: cid int, balance real

questions: cid int, question text

'''
