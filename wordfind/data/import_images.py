'''
Created on Nov 18, 2021

@author: mdl
'''
import os
import re

from wordfind.data.mysql_helper import MysqlHelper


def read_image_from_dir(fullpath):
    word = os.path.basename(fullpath)
    word = re.sub(r'^l_', "l'", word)
    word = re.sub(r'\.png$', '', word)
    word = re.sub(r'\.jpe?g$', '', word)
    word = re.sub(r'^(un|le|une|la|les|des)_', r'\1 ', word)
    word = re.sub('_', ' ', word)
    # print("file=%s | word=%s"%(file, word))
    with open(fullpath, mode='rb') as f:
        imagedata = f.read()
        
    return(word, imagedata)

def read_images(startDir, year='3rd', lang='FR'): 
    pass
    dirs = os.listdir(startDir)
    mh = MysqlHelper()
    i = 0 
    for d in dirs:
        fullpath = os.path.join(startDir, d)
        if os.path.isdir(fullpath):
            files = os.listdir(fullpath)
            for file in files:
                imageloc = os.path.join(d, file)
                word, imagedata = read_image_from_dir(imageloc)

                sql = """insert into words (word, grp, src, lang, imageloc, image) values 
                    ('%s', '%s', '%s', '%s', '%s', %%s) on duplicate key update imageloc='%s' 
                    """%(re.sub("'", "''", word), d, year, lang, imageloc, imageloc)
                print("sql: %s"%sql)
                mh.executetuple(sql, imagedata)
                i += 1
        else:
            print("Ignoring (not directory) %s in %s"%(dir, startDir))

    print("Finished executing %i sql statements."%i)

def main():
    imageRoot = '/Users/mdl/Documents/XavierFASSV/mots/images'
    read_images(imageRoot)
    print("Done reading images")

if __name__ == '__main__':
    main()
    
