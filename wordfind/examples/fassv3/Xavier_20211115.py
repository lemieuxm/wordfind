'''
Created on Nov 15, 2021

@author: mdl
'''
from wordfind.WFBuilder import buildFromWords
from wordfind.WFRenderer import renderPDF


def main():
    title = "Xavier Study 2021.11.16"
    rows = 25
    cols = 25
    english_sm2wk4 = ['ferocious', 'shine', 'shone', 'doubt', 'stare', 
                      'stared', 'descended', 'relief', 'knowledge', 
                      'disbelief', 'rhythm', 'murmured']
    français = ['un chapeau', 'le ciel', 'dame', 'un dos', 'l\'autre', 'l\'un', 
                'se coucher', 'vieil', 'vieille', 'vieux', 'un boeuf',
                'un géant', 'paysage', 'pied', 'sommeil', 'une main', 
                'un oeil', 'des yeux', 'eux']
    
    words = english_sm2wk4
    words.extend(français)

    wfdict = buildFromWords(words, rows, cols, title)
    renderPDF(wfdict, "/tmp/%s.pdf"%title)
    print("Finished writing words.")


if __name__ == '__main__':
    main()