'''
Created on Nov 15, 2021

@author: mdl
'''
import unittest

from wordfind.WFBuilder import buildFromWords
from wordfind.WFRenderer import renderPDF


class TestWordBuilding(unittest.TestCase):

    words = ['géant', 'turkey', 'absolutely', 'FunStuff', 'Noël', 'Merry Christmas', 'God Jul']
    def testWFBuild(self):
        
        title = "TestWFBuild"
        rows = 16
        cols = 16
        wfdict = buildFromWords(self.words, rows, cols, title)
        # assert(wfdict is not None)
        for i in range(wfdict['rows']):
            line = ""
            for j in range(wfdict['columns']):
                line += "%s "%wfdict['grid'][i][j] 
            print("%s"%line)
        print("\n")
        print("title=%s; rows=%i, cols=%i"%(title,rows,cols))
        print("words=[%s]"%','.join(self.words))
        print("END")

    def testWFRender(self):
        title = "TestWFRender"
        rows = 16
        cols = 16
        wfdict = buildFromWords(self.words, rows, cols, title)
        renderPDF(wfdict, "/tmp/testWFRender.pdf")
        
        print("END")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWFBuild']
    unittest.main()
    