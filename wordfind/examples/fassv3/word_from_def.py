'''
Created on Nov 30, 2021

@author: mdl
'''
from wordfind import WorkSheetRenderer, WFRenderer
from wordfind.WFBuilder import buildFromWords, strip_accents
from wordfind.data.util import get_data_for_grps_sql, get_data_for_grps_csv


def render_grid(data):
    pass
    
def cross_sql(grps, rows=20, cols=20):
    data, name = get_data_for_grps_sql(grps)
    return(cross(data, name))    

def cross_csv(grps, filename, rows=20, cols=20):
    data, name = get_data_for_grps_csv(grps, filename)
    return(cross(data, name))    

def cross(data, name, rows=20, cols=20):
    wfdict = buildFromWords(data, rows, cols, name, fillBlanks=False, trim=True)
    if not wfdict:
        print("Unable to find a valid layout.  Try making the grid bigger.")
        return
    for r in wfdict['grid']:
        print("%s"%" ".join(r))

    WFRenderer.renderCross(wfdict, key=False) 

    print("found %i rows for %s"%(len(data), name))    

    print("Created crossword.")


def word_find_sql(grps, cols=12, rows=12):
    data, name = get_data_for_grps_sql(grps)
    return(word_find(data, name, cols=cols, rows=rows))    

def word_find_csv(grps, filename, title=None, cnt=1, cols=15, rows=15):
    data, name = get_data_for_grps_csv(grps, filename)
    if not title:
        title = name
    return(word_find(data, title, cnt=cnt, cols=cols, rows=rows))    

def word_find(data, name, cnt=1, cols=17, rows=17):
    print("Starting word_find.")
    for i in range(cnt):
        wfdict = buildFromWords(data, rows, cols, name, fillBlanks=True, trim=False)
        if not wfdict:
            print("Unable to find a valid layout.  Try making the grid bigger.")
            return
        for r in wfdict['grid']:
            print("%s"%" ".join(r))
    
        outFileName = "/tmp/wordfind_%s_%i.pdf"%(name, i)
        WFRenderer.renderPDF(wfdict, outFileName=outFileName) 
    
        print("found %i rows for %s"%(len(data), name))    

    print("Created %i crossword(s)."%(i+1))

def worksheet_sql(grps, blank=True):
    words, name = get_data_for_grps_sql(grps)
    return(worksheet(words, name, blank))

def worksheet(words, name, blank):
    wfdict = {'title':name, 'words':[]}
    for word_dict in words:
        splits = [' | ', ' - ']
        already_used = set()
        for split in splits:
            ws = word_dict['word'].split(split)
            for w in ws:
                w = w.strip()
                if w in already_used:
                    continue
                word_dict['wfword'] = strip_accents(w)
                already_used.add(w)
                wfdict['words'].append(word_dict)
    WorkSheetRenderer.renderPDF(wfdict, showWord=not blank, showPos=not blank, showDef=True, showGrid=blank)
    print("finished with worksheets: %i words for %s"%(len(wfdict['words']), name))
    
    

def main():
    # cross([
    #     # 'sm2wk6', 
    #     # 'sm2wk7',
    #     # 'sm2wk3',
    #     'sm2rev',
    #     ])
    # filename = "/Users/mdl/Documents/XavierFASSV/ValentinesWords2022"
    # word_find_csv(['vd'], filename, "Valentine's Day 2022", cnt = 20, cols=12, rows=11)
    #     exit(0)
    # grps = ['sm3wk4']
    # worksheet_sql(grps, blank=True)
    # print("Finished creating worksheet for %s"%("|".join(grps)))

    # grps = ['sm3wk2']
    # worksheet_sql(grps, blank=True)
    # print("Finished creating worksheet for %s"%("|".join(grps)))

    # exit(0)    
    #filename = "/Users/mdl/Documents/XavierFASSV/mots/3rdGradeVocab.csv"
    # cross_csv(grps, filename)
    grps = ['sm3wk4', 'sm3wk2']
    rows=14
    cols=14
    
    cross_sql(grps, rows=rows, cols=cols)
    word_find_sql(grps, cols=cols, rows=rows)
    grps = ['sm3wk4', 'sm3wk3']
    worksheet_sql(grps, blank=True)
#    print("Finished creating crossword puzzles for %s"%("|".join(grps)))
    

          

if __name__ == '__main__':
    main()
    
    
    