""" database test """
from common.db_connection import DbEngine
import common
'''
db_engine = DbEngine()
conn = db_engine.get_connection()

# c = conn.connect()

result = conn.execute("select * from tbl_config")
for row in result:
    print(row['class'], row['config'], row['config_value'],)
conn.close()'''
print(common.__file__)
import os
path = os.path.dirname(common.__file__)
print(path)