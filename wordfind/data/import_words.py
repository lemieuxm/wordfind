'''
Created on Nov 18, 2021

@author: mdl
'''
import csv
import re

from cryptography.fernet import Fernet

from wordfind.data.mysql_helper import MysqlHelper


def import_from_file(filename, config, sep="\t", dbcols=['word'], quotechar='"'):
    mysqlh = MysqlHelper(config)
    sqls = []
    with open(filename, 'r') as f:
        csvf = csv.DictReader(f, delimiter=sep, quotechar=quotechar)
        
        for row in csvf:
            words = []
            if re.match(r'(-ed|-d|-s)$', row['word']):
                ws = row['word'].strip().split('-')
                words.append(ws[0])
                words.append(ws[0]+ws[1])
            elif re.match(r'|', row['word']):
                ws = row['word'].strip().split('|')
                for w in ws:
                    words.append(w)
            else:
                words.append(row['word'].strip()) 
            # print("iterating over columns for these words: %s"%(str(words)))
            # print("")
            for w in words:
                sql = "insert into words (%s) values ("%(','.join(dbcols))
                for i in range(len(dbcols)):
                    col = dbcols[i]
                    if i>0:
                        sql += ', '
                    if dbcols[i] == 'image':
                        sql += "I don't know how to encode an image yet. TODO"
                    elif dbcols[i] == 'word':
                        sql += "'%s'"%w
                    else:
                        sql += "'%s'"%row[col]
                sql += ')'
                sql += "on duplicate key update pos='%s', def='%s'"%(row['pos'],row['def'].replace("'", "''"))
                sqls.append(sql)
        print("Executing %i sql statements."%len(sqls))
        # mysqlh.execute_sqls(sqls)
        for sql in sqls:
            print("sql: %s"%sql)
            mysqlh.execute(sql)
        print("Completed executing %i sql statements."%len(sqls))
    mysqlh.close_db_connection()
             
def main():
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
    filename = '/Users/mdl/Documents/XavierFASSV/mots/3rdGradeVocab.csv'
    # TODO: upgrade to read the columns from the file (not super urgent since I have only 1 format)
    import_from_file(filename, config, dbcols=['word', 'def', 'pos', 'lang', 'grp', 'src'], sep=',', quotechar='"')
    print("Imported file: %s"%filename)
    

if __name__ == '__main__':
    main()
    
