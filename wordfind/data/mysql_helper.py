'''
Created on Jun 8, 2018

@author: mdl
'''

import hashlib
from pathlib import Path
import pathlib
import pickle

from cryptography.fernet import Fernet
import pymysql


class MysqlHelper(object): 

    my_config = None
    server = None
    connection = None
    need_tunnel = False
    cache_dir = None
    cursorclass = None

    def __init__(self, config=None):
        # This should create the ssh connection all by itself... and do the connection... 
        #   this should be done at the same time as creating the connection
        if not config:
            key = b'FzdkHKFJGBFYdjxII7W462aBd8sXmnIoPM5xTkx3vpA='
            passcode = b'gAAAAABhlqvvYJw3Asr_R66iHo5k-RiAmWD06vo4xRfL8AKa11yyUiWJ_ur0VKnRHrv34UsYOY347wZ6KUg50AU5p8A5ww2ZHA=='
            f = Fernet(key)
            config = {
                'port': 3343,
                'host': 'localhost',
                'user': 'mdl',
                'pass': f.decrypt(passcode).decode(),
                'db': 'study', 
                }

        self.my_config = config
        self.cursorclass = pymysql.cursors.DictCursor
        self.cache_dir = "/tmp/cache/sql"
        pathlib.Path(self.cache_dir).mkdir(parents=True, exist_ok=True)        
        
    def db_connection(self, force_new=False):
        if force_new and self.connection is not None:
            self.connection.close()
            self.connection = None
        if self.connection is None:

            # self.db=MySQLdb.connect(passwd="yhnscu9",user="mdl",db="ibkr",host="10.0.72.120")
            mysql_port = self.my_config['port']
            self.connection = pymysql.connect(
                host=self.my_config['host'],
                port=mysql_port,                          
                user=self.my_config['user'],
                password=self.my_config['pass'],             
                database=self.my_config['db'],
                # auth_plugin='mysql_native_password',
                # get_warnings=True,
                # buffered=True
                # raise_on_warnings=True
                local_infile=1,
                cursorclass=pymysql.cursors.DictCursor
                )
            # LOGGER.debug("Using port %i for mysql"%mysql_port)
        return(self.connection)
    
    def close_db_connection(self):
        if self.connection is not None:
            self.connection.close()
        if self.need_tunnel:
            self.server.stop()
    
    def execute_sqls(self, sqls):
        connection = self.db_connection()
        rs = []
        cursor = connection.cursor() 
        for sql in sqls:
            rs.append(cursor.execute(sql))
        connection.commit()
        cursor.close()
        return(rs)          

    def executetuple(self, sql, mtup):
        # caller = inspect.stack()[1][3]
        # LOGGER.debug("MYSQL-EXEC(from: %s): %s"%(caller, sql[:30]))
        connection = self.db_connection()
        cursor = connection.cursor(cursor=self.cursorclass)
        r = cursor.execute(sql, mtup)
        connection.commit()
        cursor.close()
        return(r)  
    
    def execute(self, sql):
        # caller = inspect.stack()[1][3]
        # LOGGER.debug("MYSQL-EXEC(from: %s): %s"%(caller, sql[:30]))
        connection = self.db_connection()
        cursor = connection.cursor(cursor=self.cursorclass)
        r = cursor.execute(sql)
        connection.commit()
        cursor.close()
        return(r)    
    
    def executemany(self, sql, many):
        connection = self.db_connection()
        cursor = connection.cursor(cursor=self.cursorclass)
        nsql = sql.replace('?', '%s')
        # manys = [tuple(x) for x in many[:10]]
        for m in many:
            r = cursor.execute(nsql, m)
        # r = cursor.executemany(nsql, manys)
        connection.commit()
        cursor.close()
        return(r)    
    
    def cursor(self):
        connection = self.db_connection()
        cursor = connection.cursor(cursor=self.cursorclass)
        return(cursor)        
    
    def query(self, sql, newConnection=False):
        connection = self.db_connection(force_new=newConnection)
        cursor = connection.cursor(cursor=self.cursorclass)
        cursor.execute(sql)
        return(cursor)    

    def sql_hash(self, sql):
        sqlhash = hashlib.md5(sql.encode('utf-8')).hexdigest()
        return(sqlhash)

    def query_cached(self, sql, force_reload=False):
        sqlhash = self.sql_hash(sql)
        cache_file = self.cache_dir +'/sql_query_'+sqlhash
        cache_path = Path(cache_file)
        with open("%s.sql"%cache_file, 'w') as f:
            f.write(sql+"\n")
        # LOGGER.debug("%s -> %s"%(sqlhash, sql))
        if cache_path.exists() and not force_reload:
            with open(cache_file, 'rb') as fp:
                rows = pickle.load(fp)
            return(rows)
        connection = self.db_connection()
        cursor = connection.cursor(cursor=self.cursorclass)
        cursor.execute(sql)
        rows = cursor.fetchall()
#         for row in cursor:
#             rows.append(row)
        with open(cache_file, 'wb') as fp:
            pickle.dump(rows, fp)
        return(rows)
    
    def insert(self, sql, params):
        connection = self.db_connection()
        cursor = connection.cursor() 
        for param in params:
            cursor.execute(sql,param)
        connection.commit()
        print("done with insert (%i records)"%len(params))
            
            
    def upsert(self, table_name, ds, table_keys, col_name_map): # pass in a list of dicts
        queries = []
        for d in ds:
            ks = list(d.keys())
            updates = []
            transformed_keys = []
            values = []
            for k in ks:
                values.append("'%s'"%d[k] if isinstance(d[k], str) else "%s"%d[k])
                col_name = col_name_map.get(k)
                if col_name is None:
                    col_name = k
                transformed_keys.append(col_name)
                if k in table_keys:
                    continue
                updates.append("%s='%s'"%(col_name,d[k]) if isinstance(d[k], str) else "%s=%s"%(col_name,d[k]))  #pylint: disable=line-too-long
            update_clause = ','.join(updates)
            cols = ','.join(transformed_keys)
            vals =','.join(values)
            sql = 'insert into %s (%s) values (%s) on duplicate key update %s'%(table_name, cols, vals, update_clause)  #pylint: disable=line-too-long
            queries.append(sql)
        self.execute_sqls(queries)

