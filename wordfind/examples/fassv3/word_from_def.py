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
    cols=24
    rows=24
    wfdict = buildFromWords(data, rows, cols, name, fillBlanks=False, trim=True)
    if not wfdict:
        print("Unable to find a valid layout.  Try making the grid bigger.")
        return
    for r in wfdict['grid']:
        print("%s"%" ".join(r))

    renderCross(wfdict, key=False) 

    print("found %i rows for %s"%(len(data), name))    

    print("Created crossword.")
    

def main():
    cross([
        'sm2wk6', 
        'sm2wk7',
        # 'sm2wk3',
        ])
    

if __name__ == '__main__':
    main()
    