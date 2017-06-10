import sqlite3

(53.0, 250000.0, 1, 25000.0, 1, 1, 2)

class Database():
    def __init__(self):
        self.db = sqlite3.connect('ingatlancom.db')
        self._create_table(
                "properties",
                [
                    "id text",
                    "area real",
                    "price real",
                    "elevator integer",
                    "utility_cost real",
                    "appliances integer",
                    "furnished integer",
                    "rooms integer",
                    "rooms_half integer",
                    "location text",
                    "view_center_x real",
                    "view_center_y real",
                    "predicted integer",   # -1: false, 1: true, 0: na
                    "decided integer",      # -1: false, 1: true, 0: na
                    "done integer"
                ]
        )

    def _create_table(self, name, fields):
        c = self.db.cursor()
        query = "create table if not exists {} ({})".format(name, ", ".join(str(x) for x in fields))
        c.execute(query)
        self.db.commit()
        c.close()

    def insert(self, table_name, data):
        c = self.db.cursor()
        c.execute(
                "insert into {} values ({})".format(table_name, ", ".join(["?"] * len(data.to_value_list()))),
                data.to_value_list()
        )
        self.db.commit()
        c.close()

    def is_exists(self, table_name, column_name, value):
        return self.find_one(table_name, column_name, value) != None

    def find_one(self, table_name, column_name, value):
        c = self.db.cursor()
        c.execute(
                "select * from {1} where {0} = ?".format(column_name, table_name),
                (value,)
        )
        item = c.fetchone()
        c.close()
        return item

    def update_decision(self, table_name, column_name, find_value, decision):
        c = self.db.cursor()
        c.execute(
                "update {0} set decided = ? where {1} = ?".format(table_name, column_name),
                (decision, find_value)
        )
        self.db.commit()
        c.close()
        return self.find_one(table_name, column_name, find_value)

    def update_prediction(self, table_name, column_name, find_value, prediction):
        c = self.db.cursor()
        c.execute(
                "update {0} set predicted = ? where {1} = ?".format(table_name, column_name),
                (prediction, find_value)
        )
        self.db.commit()
        c.close()
        return self.find_one(table_name, column_name, find_value)

    def fetch_all(self, table_name, predicted=(-1,0,1), decided=(-1,0,1), done=(0,1), order=""):
        c = self.db.cursor()
        c.execute(
                "select * from {} where predicted in {} and decided in {} and done in {} {}".format(
                    table_name, predicted, decided, done, order
                )
        )
        rows = c.fetchall()
        c.close()
        return rows

