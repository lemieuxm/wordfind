'''
Created on Nov 18, 2021

@author: mdl
'''
import copy
import csv
import re

from wordfind.data.mysql_helper import MysqlHelper


DEFAULT_IMAGE_ROOT = '/Users/mdl/Documents/XavierFASSV/mots/images'
DEFAULT_CSV_ROOT = '/Users/mdl/Documents/XavierFASSV/mots/3rdGradeVocab.csv'


def get_data_for_grps_sql(grps):
    mh = MysqlHelper()
    # sql = "select word, imageloc, image from study.words"
    sql = "select * from study.words"
    if grps:
        sql += " where grp in ('%s')"%("','".join(grps))
    else:
        sql += " limit 1000"
    rows = mh.query(sql)
    data = []
    for row in rows:
        dat = copy.deepcopy(row)
        # dat['imageloc'] = os.path.join(IMAGE_ROOT, dat['imageloc'])
        data.append(dat) 
    
    name = "|".join(grps)

    return(data, name)

def get_data_for_grps_csv(grps, filename, quotechar = '"', delimiter=','):
    wordobjs = []
    with open(filename, 'r') as f:
        csvf = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for row in csvf:
            words = []
            if re.match(r'(-ed|-d|-s)$', row['word']):
                ws = row['word'].strip().split('-')
                words.append(ws[0])
                words.append(ws[0]+ws[1])
            # elif re.match(r'|', row['word']):
            elif '|' in row['word']:
                ws = row['word'].strip().split('|')
                for w in ws:
                    words.append(w)
            else:
                words.append(row['word'].strip())            
            for w in words:
                word = {'word': w}
                word.update(row)
            wordobjs.append(word)
    name = '|'.join(grps)
    return(wordobjs, name)

