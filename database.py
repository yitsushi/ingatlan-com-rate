import sqlite3

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
                    "decided integer"      # -1: false, 1: true, 0: na
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
        c = self.db.cursor()
        c.execute(
                "select {0} from {1} where {0} = ?".format(column_name, table_name),
                (value,)
        )
        exists = c.fetchone() != None
        c.close()
        return exists

