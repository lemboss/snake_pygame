import sqlite3 as sq

class DBConnector:
    def __init__(self, db_name: str = "score.db"):
        self.db_name = db_name
        self.open_connection()

    def open_connection(self):
        self.con = sq.connect(self.db_name)
        self.cur = self.con.cursor()

    def get_leaders(self, table_name):
        self.table = table_name
        select_leaders = f"select * from {self.table} order by point desc limit 5"
        create_table = f"create table if not exists {self.table} (name text primary key, point integer not null)"
        self.crud(create_table)
        return self.select(select_leaders)
    
    def select(self, sql):
        return self.cur.execute(sql).fetchall()
    
    def crud(self, sql):
        self.cur.execute(sql)
        self.con.commit()
    
    def close_connection(self):
        self.con.close()