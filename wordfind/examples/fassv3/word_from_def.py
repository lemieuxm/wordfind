'''
Created on Nov 30, 2021

@author: mdl
'''
from wordfind.WFBuilder import buildFromWords
from wordfind.WFRenderer import renderCross
from wordfind.data.util import get_data_for_grps_sql


def render_grid(data):
    pass

def cross(grps):
    data, name = get_data_for_grps_sql(grps)
    width=13
    height=13
    words=[]
    defs=[]
    for r in data:
        words.append(r['word'])
        defs.append(r['def'])
    wfdict = buildFromWords(words, width, height, name, fillBlanks=False, defs=defs)

    for r in wfdict['grid']:
        print("%s"%" ".join(r))

    renderCross(wfdict, key=True) 

    print("found %i rows for %s"%(len(data), name))    

    print("Created crossword.")
    

def main():
    cross(['sm2wk4'])
    

if __name__ == '__main__':
    main()
    