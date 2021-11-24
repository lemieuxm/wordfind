'''
Created on Nov 15, 2021

@author: mdl
'''
from wordfind.WFBuilder import buildFromWords
from wordfind.WFRenderer import renderPDF


def main():
    title = "Xavier Study 2021.11.17"
    rows = 18
    cols = 18
    english_sm2wk4 = ['ferocious', 'shine', 'shone', 'doubt', 'stare', 
                      'stared', 'descended', 'relief', 'knowledge', 
                      'disbelief', 'rhythm', 'murmured']
    français = ['un chapeau', 'le ciel', 'dame', 'un dos', 'l\'autre', 'l\'un', 
                'se coucher', 'vieil', 'vieille', 'vieux', 'un boeuf',
                'un géant', 'paysage', 'pied', 'sommeil', 'une main', 
                'un oeil', 'des yeux', 'eux']
    
    words = english_sm2wk4
    words.extend(français)
    words.sort()

    wfdict = buildFromWords(words, rows, cols, title)
    if not wfdict:
        print("Unable to build after several tries.  Either try again or make the grid larger.")
        exit(1)
    else:
        outfile = "/tmp/%s.pdf"%title
        renderPDF(wfdict, outfile)
        print("Finished writing to %s"%outfile)


if __name__ == '__main__':
    main()