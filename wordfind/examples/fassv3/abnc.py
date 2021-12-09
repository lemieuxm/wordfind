'''
Created on Nov 18, 2021

@author: mdl
'''
import copy
import os

from wordfind.WFBuilder import buildFromWords
from wordfind.WFImageRec import create_imagerec
from wordfind.WFRenderer import renderCross
from wordfind.data.import_images import read_image_from_dir
from wordfind.data.mysql_helper import MysqlHelper


IMAGE_ROOT = "/Users/mdl/Documents/XavierFASSV/mots/images"

def build_worksheet_sql(grps):
    mh = MysqlHelper()
    sql = "select word, imageloc, image from study.words"
    if grps:
        sql += " where grp in ('%s')"%("','".join(grps))
    else:
        sql += " limit 100"
    rows = mh.query(sql)
    data = []
    for row in rows:
        dat = copy.deepcopy(row)
        # dat['imageloc'] = os.path.join(IMAGE_ROOT, dat['imageloc'])
        data.append(dat) 
    
    name = os.path.sep.join(grps)
    create_imagerec(data, name)
    print("found %i rows for %s"%(len(data), name))

def get_data(grps):
    data = []
    for grp in grps:
        fullpath = os.path.join(IMAGE_ROOT, grp) 
        if not os.path.exists(fullpath):
            print("WARNING, path does not exist: %s"%fullpath)
            continue
        images = os.listdir(fullpath)
        for image in images:
            im_full = os.path.join(fullpath, image)
            word, imagedata = read_image_from_dir(im_full)
            dat = {'word': word, 'imageloc': im_full, 'image': imagedata}
            data.append(dat)
    return(data)
            
            
def build_cross(grps, width=16, height=16, name=None, key=False):
    data = get_data(grps)
    
    if not name:
        name = os.path.sep.join(grps)
        
    wfdict = buildFromWords(data, width, height, name, fillBlanks=False)
    for r in wfdict['grid']:
        print("%s"%" ".join(r))
    renderCross(wfdict, key=key) 

    print("found %i rows for %s"%(len(data), name))
    

def build_worksheet(grps):
    data = get_data(grps)
    name = '_'.join(grps)
    create_imagerec(data, name)
    print("found %i rows for %s"%(len(data), name))


def main():
    build_worksheet(['7a','7b'])
    build_worksheet(['7b','7c'])
    build_worksheet(['7a','7b','7c'])
    # build_worksheet(['6c_6b'])
    # build_cross(['6a_6b'], width=12, height=12, key=False)
    # build_cross(['6c_6b'], width=12, height=12, key=False)
    # build_cross(['7a','7b','7c'], width=20, height=20, key=False)

if __name__ == '__main__':
    main()

