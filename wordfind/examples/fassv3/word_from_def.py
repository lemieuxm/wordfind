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
    # grps = ['sm3wk2', 'sm3wk3', 'sm3wk1']
    grps = ['sm2wk6', 'sm2wk7']
    grps = ['sm3wk1', 'sm3wk2']
    rows=18
    cols=18
    # cross_sql(grps, rows=rows, cols=cols)

    #grps = ['sm3wk2', 'sm3wk3', 'sm3wk1', 'sm3wk4']
    rows=16
    cols=rows
    word_find_sql(grps, cols=cols, rows=rows)

    # grps = ['wk4', 'wk3']
    # worksheet_sql(grps, blank=True)
#    print("Finished creating crossword puzzles for %s"%("|".join(grps)))
    

          

if __name__ == '__main__':
    main()
    
    
    
    
    
    # grp, lang, count(1), min(wordid)
# 'adjective', '3rd', '5', '1468'
# 'verb', '3rd', '8', '1474'
# 'adverb', '3rd', '7', '1488'
# 'phrase', '3rd', '1', '1508'
# 'noun', '3rd', '2', '1544'
# 'sm2wk4', 'EN', '14', '12'
# 'wk2', 'EN', '8', '22'
# 'wk3', 'EN', '9', '30'
# 'wk4', 'EN', '9', '39'
# 'wk5', 'EN', '9', '48'
# 'wk6', 'EN', '9', '57'
# 'wk7', 'EN', '9', '66'
# 'sm2wk1', 'EN', '20', '75'
# 'sm2wk2', 'EN', '10', '85'
# 'sm2wk3', 'EN', '10', '95'
# 'sm2wk6', 'EN', '10', '587'
# 'sm2wk7', 'EN', '15', '1062'
# 'sm2rev', 'EN', '21', '1318'
# 'sm3wk1', 'EN', '10', '1457'
# 'sm3wk2', 'EN', '10', '1467'
# 'unkwk1', 'EN', '10', '1837'
# 'sm3wk3', 'EN', '10', '2266'
# 'sm3wk4', 'EN', '10', '2435'
# '6c_6b', 'FR', '9', '205'
# '6a_6b', 'FR', '12', '214'
# '7c', 'FR', '5', '1204'
# '7b', 'FR', '9', '1209'
# '7a', 'FR', '10', '1230'
# '8a', 'FR', '6', '1798'
# '8c', 'FR', '5', '1816'
# '8b', 'FR', '7', '1820'
# '9b', 'FR', '6', '2006'
# '9c', 'FR', '9', '2012'
# '9a', 'FR', '2', '2050'
# '10c', 'FR', '9', '2170'
# '10b', 'FR', '7', '2179'
# '10a', 'FR', '7', '2226'
# ' fit', 'wk3', '1', '1576'
# ' OK', 'wk6', '1', '1598'
