


import sqlite3
import numpy as np


class SQL():
    
    def __init__(self, filename):
        
        self.conn = sqlite3.connect(filename)
        self.curs = self.conn.cursor()
        
        
    def print_tables(self, pprint=False):
        tables = self.get_tables()
        if pprint:
            for table in tables: print table;
        else:
            print tables
        
        
    def get_tables(self):
        self.curs.execute("""
        SELECT name FROM sqlite_master WHERE type = "table" ORDER BY name;
        """)
        tables = [name[0] for name in self.curs.fetchall()]
        return tables
    
    
    def describe_table(self, table, verbose=0):
        self.curs.execute("""
        SELECT sql FROM sqlite_master WHERE type='table' AND name='%s';
        """ % table)
        description = self.curs.fetchone()[0]
        
        self.curs.execute("""
        SELECT count(*) FROM '%s';
        """ % table)
        nEntries = int(self.curs.fetchone()[0])
        
        if verbose == 1:
            print table + ", # entries: ", nEntries
            print description
            print
        
        return description, nEntries
    
    
    def describe_all_tables(self):
        for table in self.get_tables():
            self.describe_table(table, verbose=1)
            
            
    def get_column(self, table, column):
        dType = self.get_dtype(table, column)
        
        self.curs.execute("""
        SELECT %s FROM %s;
        """ % (column, table))
        
        if dType.upper() == 'INT':
            #print self.curs.fetchall()
            col = [int(x[0]) for x in self.curs.fetchall()]
            #print col
            return np.array(col)
        else:
            raise Exception("Unsupported data type: %s; aborting." % dType)
        
        
        
        
    def get_dtype(self, table, column):
        self.curs.execute("""
        PRAGMA table_info(%s);
        """ % table)
        for col in self.curs.fetchall():
            if col[1].upper() == column.upper():
                dType = col[2]
                return dType
        # Fall through indicates key not found
        raise Exception("Column %s in table %s not found")
            


        