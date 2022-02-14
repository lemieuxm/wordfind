'''
Created on Nov 15, 2021

@author: mdl
'''
'''
    wfdict = {'title':<title>, 'rows':<number rows>,
              'columns':<number of columns>,
              'words':[<wdict>, <wdict>, ..., <wdict>],
              'grid':[ <row>, <row>, ..., <row>]
              }
              
    <row> = [<letter>, <letter>, ..., <letter>]
              
    wdict = {'word':<word with articles and accents>, 
             'wfword':<word find word, no articles or accents>,
             'image_file':<if desired an image file can be used instead of word text>,
             }
'''

import copy
import random
import re
import unicodedata


DIRECTIONS = [ 
    (-1,0),  # up 0
    (-1,1),  # up right 1
    (0,1),   # right 2
    (1,1),   # down right 3
    (1,0),   # down 4
    (1,-1),  # down left 5
    (0,-1),  # left 6
    (-1,-1), # up left 7
    ]

BLANK = '_'

def canBeAdded(word, grid, dirTuple, start, requireIntersect=False):
    hasIntersect = False
    
    # Don't start words with another letter before the starting 
    #      letter in the same direction
    r = start[0]-dirTuple[0]
    c = start[1]-dirTuple[1]
    if r>=0 and c>=0 and r<len(grid) and c<len(grid[r]) and grid[r][c]:
        return(False)
    # Don't end words with another letter after the ending 
    #      letter in the same direction
    r = start[0] + dirTuple[0]*len(word)
    c = start[1] + dirTuple[1]*len(word)
    if r<len(grid) and c<len(grid[0]) and grid[r][c]:
        return(False)

    for i in range(len(word)):
        r = start[0] + dirTuple[0]*i
        c = start[1] + dirTuple[1]*i
        if r>len(grid)-1 or c>len(grid[0])-1:
            # This should never happen, it is here to detect a bug
            print("ERROR: r or c is too big.")
            return(False)
        letter = grid[r][c]
        if letter:
            if letter.upper() != word[i].upper():
                return(False)
            hasIntersect = True

            
    # All cells are either empty, or filled and matches the word 
    return(not requireIntersect or hasIntersect)
            

def addWord(word, grid, directions=[i for i in range(8)], requireIntersect=False):
    wordLen = len(word)
    rows = len(grid)
    cols = len(grid[0])
    random.shuffle(directions)
    for i in directions: # iterate over the directions
        minrow = -min(0,wordLen*DIRECTIONS[i][0])
        maxrow = min(rows, rows-wordLen*DIRECTIONS[i][0])
        rows_j = [x for x in range(minrow, maxrow)]
        random.shuffle(rows_j)
        for j in rows_j:
            mincol = -min(0,wordLen*DIRECTIONS[i][1])
            maxcol = min(cols, cols-wordLen*DIRECTIONS[i][1])
            cols_j = [x for x in range(mincol, maxcol)]
            random.shuffle(cols_j)
            for k in cols_j:
                if canBeAdded(word, grid, DIRECTIONS[i], (j,k), requireIntersect):
                    for m in range(len(word)):
                        r = j + DIRECTIONS[i][0]*m
                        c = k + DIRECTIONS[i][1]*m
                        grid[r][c] = word[m].upper()
                    return(grid, i, j, k)
                
    return(grid, None, None, None)


def isEmpty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]:
                return(False)
    return(True)

def intersection(lst1, lst2):
    lst3 = [list(filter(lambda x: x in lst1, sublist)) for sublist in lst2]
    return lst3


def addWordForCW(word, grid):
    wordLen = len(word)
    rows = len(grid)
    cols = len(grid[0])
    directions = [2,4]
    random.shuffle(directions)
    
    if isEmpty(grid):
        grid, i, j, k = addWord(word, grid, directions)
        r = j-DIRECTIONS[i][0]
        c = k-DIRECTIONS[i][1]
        if r>=0 and c>=0 and not grid[r][c]:
            grid[r][c] = BLANK
        # Don't end words with another letter after the ending 
        #      letter in the same direction
        r = j+DIRECTIONS[i][0]*len(word)
        c = k+DIRECTIONS[i][1]*len(word)
        if r<len(grid) and c<len(grid[0]) and not grid[r][c]:
            grid[r][c] = BLANK  
        return(grid, i, j, k)
    
    # intersectChars = intersection(list(word), grid)
    
    for i in directions:
        minrow = -min(0,wordLen*DIRECTIONS[i][0])
        maxrow = min(rows, rows-max(1,wordLen*DIRECTIONS[i][0]))
        rows_j = [x for x in range(minrow, maxrow+1)]
        random.shuffle(rows_j)
        for j in rows_j:
            mincol = -min(0,wordLen*DIRECTIONS[i][1])
            maxcol = min(cols, cols-max(1,wordLen*DIRECTIONS[i][1]))
            cols_j = [x for x in range(mincol, maxcol+1)]
            random.shuffle(cols_j)
            for k in cols_j:
                #if grid[j][k] and grid[j][k] in word:                
                if canBeAdded(word, grid, DIRECTIONS[i], (j,k), requireIntersect=True):
                    r = j-DIRECTIONS[i][0]
                    c = k-DIRECTIONS[i][1]
                    if r>=0 and c>=0 and not grid[r][c]:
                        grid[r][c] = BLANK
                    # Don't end words with another letter after the ending 
                    #      letter in the same direction
                    r = j+DIRECTIONS[i][0]*len(word)
                    c = k+DIRECTIONS[i][1]*len(word)
                    if r<len(grid) and c<len(grid[0]) and not grid[r][c]:
                        grid[r][c] = BLANK                    
                    for m in range(len(word)):
                        r = j + DIRECTIONS[i][0]*m
                        c = k + DIRECTIONS[i][1]*m
                        grid[r][c] = word[m].upper()
                    return(grid, i, j, k)
                   
    return(grid, None, None, None)

# list('abcdefghijklmnopqrstuvwxyz')

def doFillBlanks(grid):
    rows = len(grid)
    cols = len(grid[0])
    letters = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j]:
                letters.append(grid[i][j].upper())

    for i in range(rows):
        for j in range(cols):
            if not grid[i][j]:
                grid[i][j] = random.choice(letters)
    
    return(grid) 

def removeBlanks(grid):
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == BLANK:
                grid[i][j] = ""
    return(grid)

def clipEdgeBlanks(wfdict):
    wfgrid = wfdict['grid']
            # remove blank top rows        
    cnt = 0
    for r in range(wfdict['rows']):
        for c in range(wfdict['columns']):
            cnt += 1 if wfgrid[r][c] else 0
        if cnt > 0:
            print("r=%i"%r)
            break
    # clip first r rows r is the index of teh first non blank row
    if r > 0:
        wfgrid = wfgrid[r:]
        for word in wfdict['words']:
            word['start'] = (word['start'][0]-r, word['start'][1])
        wfdict['rows'] = len(wfgrid)
    
    # remove blank bottom rows        
    cnt = 0
    for r in range(wfdict['rows']-1,-1,-1):
        for c in range(wfdict['columns']):
            cnt += 1 if wfgrid[r][c] else 0
        if cnt > 0:
            print("r=%i"%r)
            break
    # clip first r rows
    if r < wfdict['rows']-1:
        wfgrid = wfgrid[:r+1]
        wfdict['rows'] = len(wfgrid)
        
    cnt = 0
    for c in range(wfdict['columns']):
        for r in range(wfdict['rows']):
            cnt += 1 if wfgrid[r][c] else 0
        if cnt > 0:
            print("c=%i"%c)
            break
    if c > 0:
        for r in range(wfdict['rows']):
            wfgrid[r] = wfgrid[r][c:]
        for word in wfdict['words']:
            word['start'] = (word['start'][0], word['start'][1]-c)
        wfdict['columns'] = len(wfgrid[0])
        
    cnt = 0
    for c in range(wfdict['columns']-1,-1,-1):
        for r in range(wfdict['rows']):
            cnt += 1 if wfgrid[r][c] else 0
        if cnt > 0:
            print("c=%i"%c)
            break     
    if c < wfdict['columns']-1:
        for r in range(wfdict['rows']):
            wfgrid[r] = wfgrid[r][:c+1]
        wfdict['columns'] = len(wfgrid[0])
    
    wfdict['grid'] = wfgrid
    
    #return(wfdict)
    
    print ("Finished clipping Edge Blanks")
         

def _build(wfdict, fillBlanks=True, trim=False):
    # Fill the grid with empty strings
    wfdictbackup = copy.deepcopy(wfdict)
    wfgrid = []
    for r in range(wfdict['rows']):
        wfgrid.append([])
        for c in range(wfdict['columns']):  # @UnusedVariable
            wfgrid[r].append('')
    
    word_is = [i for i in range(len(wfdict['words']))]
    random.shuffle(word_is)
    wordnum = 0
    starts_used = {}
    for j in word_is:
        wfword = wfdict['words'][j]
        if fillBlanks:
            wfgrid, direction, r, c = addWord(wfword['wfword'], wfgrid)
        else:
            wfgrid, direction, r, c = addWordForCW(wfword['wfword'], wfgrid)

        if r is None or c is None or direction is None:
            print("Unable to complete puzzle")
            for k,v in wfdictbackup.items():
                wfdict[k]=v
            return(False) 
        wfword['start']=(r,c)
        wfword['direction']=direction
        if wfword['start'] in starts_used.keys():
            wfword['wordnum'] = starts_used[wfword['start']]
        else:            
            wordnum += 1
            wfword['wordnum'] = wordnum
            starts_used[wfword['start']] = wordnum

    wfdict['grid'] = wfgrid
    wfdict['numwords'] = wordnum

    
    if fillBlanks:
        wfgrid = doFillBlanks(wfgrid)
    else:
        wfgrid = removeBlanks(wfgrid)

    if trim:
        clipEdgeBlanks(wfdict)
        
    return(True)    

    
def build(wfdict, n=10000, fillBlanks=True, trim=False):
    for i in range(n):   # @UnusedVariable
        if _build(wfdict, fillBlanks=fillBlanks, trim=trim):
            return(True)
        print("No puzzle after %i tries"%(i+1))
    return(False)

def strip_accents(s):
    '''
    From https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    '''
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
    s = re.sub('^un ', '', s)
    s = re.sub('^une ', '', s)
    s = re.sub('^le ', '', s)
    s = re.sub('^les ', '', s)
    s = re.sub('^la ', '', s)
    s = re.sub('^l\'', '', s)
    s = re.sub('^des ', '', s)
    s = re.sub('-ed$', 'ed', s)
    s = re.sub('-d$', 'd', s)
    s = re.sub('-s$', 's', s)
    s = re.sub('-', '', s)
    s = s.replace(" ", "")
    s = s.replace("'", "")
    return(s.upper()) 
    
    
def buildFromWords(words, rows, cols, title, fillBlanks=True, trim=False):
    wfdict = {'title':title, 'rows':rows, 'columns':cols, 'words':[]}
    
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

    if build(wfdict, fillBlanks=fillBlanks, trim=trim):
        return(wfdict)
    
    return(None)

