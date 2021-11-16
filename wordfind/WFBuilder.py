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
    (-1,0),  # up 
    (-1,1),  # up right
    (0,1),   # right
    (1,1),   # down right
    (1,0),   # down
    (1,-1),  # down left
    (0,-1),  # left
    (-1,-1), # up left
    ]

def canBeAdded(word, grid, dirTuple, start):
    for i in range(len(word)):
        r = start[0] + dirTuple[0]*i
        c = start[1] + dirTuple[1]*i
        if r>len(grid)-1 or c>len(grid[0])-1:
            print("ERROR: r or c is too big.")
            print("place holder")
        letter = grid[r][c]
        if letter and letter.upper() != word[i].upper():
            return(False)
    # All cells are either empty, or filled and matches the word 
    return(True)
            

def addWord(word, grid):
    wordLen = len(word)
    rows = len(grid)
    cols = len(grid[0])
    directions = [i for i in range(8)]
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
                if canBeAdded(word, grid, DIRECTIONS[i], (j,k)):
                    for m in range(len(word)):
                        r = j + DIRECTIONS[i][0]*m
                        c = k + DIRECTIONS[i][1]*m
                        grid[r][c] = word[m].upper()
                    return(grid, i, j, k)
                
    return(grid, None, None, None)

# list('abcdefghijklmnopqrstuvwxyz')

def fillBlanks(grid):
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
    

def _build(wfdict):
    # Fill the grid with empty strings
    wfdictbackup = copy.deepcopy(wfdict)
    wfgrid = []
    for r in range(wfdict['rows']):
        wfgrid.append([])
        for c in range(wfdict['columns']):  # @UnusedVariable
            wfgrid[r].append('')
    
    word_is = [i for i in range(len(wfdict['words']))]
    random.shuffle(word_is)
    for j in word_is:
        wfword = wfdict['words'][j]
        wfgrid, direction, r, c = addWord(wfword['wfword'], wfgrid)
        if r is None or c is None or direction is None:
            # Unable to build with words added
            for k,v in wfdictbackup.items():
                wfdict[k]=v
            return(False) 
        wfword['start']=(r,c)
        wfword['direction']=direction

    wfgrid = fillBlanks(wfgrid)
        
    wfdict['grid'] = wfgrid
        
    return(True)    
    
def build(wfdict, n=5):
    for i in range(n):   # @UnusedVariable
        if _build(wfdict):
            return(True)
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
    s = s.replace(" ", "")
    s = s.replace("'", "")
    return(s.upper()) 
    
    
def buildFromWords(words, rows, cols, title):
    wfdict = {'title':title, 'rows':rows, 'columns':cols, 'words':[]}

    for word in words:
        wfdict['words'].append({
                'word': word, 'wfword': strip_accents(word),
                # not adding image_file right now
            })

    if build(wfdict):
        return(wfdict)
    
    return(None)

