'''
Created on Nov 15, 2021

@author: mdl
'''

from math import floor
from textwrap import wrap

from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.para import Paragraph

from wordfind.WFBuilder import DIRECTIONS, BLANK


def renderPDF(wfdict, outFileName=None):
    # units in points (1 point = 1/72nd inch
    pageSize = (8.5,11.0)
    if not outFileName:
        outFileName = "/tmp/%s.pdf"%wfdict['title']
    print("width=%.1f; height=%.1f"%(pageSize[0]*inch, pageSize[1]*inch))
    canvas = Canvas(outFileName, pagesize=(pageSize[0]*inch, pageSize[1]*inch))

    canvas.setFont("Helvetica", 28)
    canvas.drawCentredString(pageSize[0]*inch/2, pageSize[1]*inch - inch, wfdict['title'])
    titleHeight = 28*2
    canvas.setFont("Helvetica", 12)
    margin = 1*inch
    width_area = pageSize[0]*inch - 2*margin
    height_area = width_area
    g = wfdict['grid']
    x_delta = width_area / len(g[0])
    y_delta = height_area / len(g)

    for r in range(len(g)): # rows
        y = pageSize[1]*inch - margin - r*y_delta - titleHeight
        for c in range(len(g[r])): # cols
            x = margin + c*x_delta
            canvas.drawString(x,y,g[r][c])
            
    y_line = pageSize[1]*inch - margin - len(g)*y_delta - titleHeight
    canvas.line(margin,y_line,pageSize[0]*inch-margin,y_line)
    
    word_columns = 4
    colDelta = width_area / word_columns
    words_height = 19
    y_line -= words_height
    canvas.setFont("Helvetica", 12)
    def getwfword(w):
        return(w['wfword'])
    
    words = sorted(wfdict['words'], key=getwfword)
    for i in range(len(words)):
        word = words[i]
        dmod = divmod(i, word_columns)
        x = margin + dmod[1]*colDelta
        y = y_line - dmod[0]*words_height
        canvas.drawString(x,y,word['word']) 
    
    canvas.showPage()
    canvas.save()
    
    return(canvas)

def isTouching(wr,wc,grid,mincnt=1):
    cnt = 0
    if grid[wr][wc]:
        cnt += 1
    for d in DIRECTIONS:
        r = wr+d[0]
        c = wc+d[1]
        if r>=0 and c>=0 and r<len(grid) and c<len(grid[0]) and grid[r][c] and grid[r][c] != BLANK:
            cnt += 1
    return(cnt>=mincnt)
            
# from: https://stackoverflow.com/questions/51541570/how-to-draw-a-paragraph-from-top-to-bottom-on-canvas            
def draw_paragraph(canvas, msg, x, y, max_width, max_height):
    message_style = ParagraphStyle('Normal')
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)  # @UnusedVariable
    message.drawOn(canvas, x, y - h)
    
    
def renderCross(wfdict, outFileName=None, key=False):
    pageSize = (8.5,11.0)
    if not outFileName:
        outFileName = "/tmp/cross_%s.pdf"%wfdict['title'].replace("/","_")
        
    print("width=%.1f; height=%.1f"%(pageSize[0]*inch, pageSize[1]*inch))
    canvas = Canvas(outFileName, pagesize=(pageSize[0]*inch, pageSize[1]*inch))

    canvas.setFont("Helvetica", 28)
    canvas.drawCentredString(pageSize[0]*inch/2, pageSize[1]*inch - inch, wfdict['title'])
    titleHeight = 28*2
    canvas.setFont("Helvetica", 12)
    margin = 1*inch
    width_area = pageSize[0]*inch - 2*margin
    height_area = width_area*0.8
    g = wfdict['grid']
    x_delta = width_area / len(g[0])
    y_delta = height_area / len(g)
    font_size = floor(x_delta * 0.6)

    {'word': 'un dos', 'wfword': 'DOS', 
     'imageloc': '/Users/mdl/Documents/XavierFASSV/mots/images/6a_6b/un_dos.jpg', 
     'start': (1, 1), 'direction': 4}

    color_c=0.0
    color_m=0.0
    color_y=0.0
    color_k=0.95

    for wordct in wfdict['words']:
        r, c = wordct['start']
        wordnum_label_size = 9
        canvas.setFont("Helvetica", wordnum_label_size)
        y = pageSize[1]*inch - margin - r*y_delta - titleHeight
        x = margin + c*x_delta
        canvas.setStrokeColor(black)
        canvas.setFillColor(black)
        canvas.drawString(x+1,y+y_delta-wordnum_label_size+1,"%s"%wordct['wordnum'])
        for _ in range(len(wordct['wfword'])):
            y = pageSize[1]*inch - margin - r*y_delta - titleHeight
            x = margin + c*x_delta
            canvas.setFont("Helvetica", font_size)
            # this needs to be commented out for the final version
            if key:
                canvas.setStrokeColor(black)
                canvas.setFillColor(black)
                canvas.drawCentredString(x+x_delta/2,y-font_size*0.3+y_delta/2,g[r][c])
            canvas.setFillColorCMYK(color_c, color_m, color_y, color_k)
            canvas.setStrokeColorCMYK(color_c, color_m, color_y, color_k)
            canvas.setStrokeColor(black)
            canvas.setFillColor(black)
            canvas.rect(x,y,x_delta,y_delta)
            r += DIRECTIONS[wordct['direction']][0]
            c += DIRECTIONS[wordct['direction']][1]
            
    for word in wfdict['words']:
        d = DIRECTIONS[word['direction']]
        s = word['start']
        w = word['wfword']
        r = s[0] + d[0]*(len(w)+1)
        c = s[1] + d[1]*(len(w)+1)
        if r>0 and c>0 and r<len(g) and c<len(g) and g[r][c]:
            r = s[0] + d[0]*(len(w))
            c = s[1] + d[1]*(len(w))
            x = margin + c*x_delta
            y = pageSize[1]*inch - margin - r*y_delta - titleHeight
            canvas.setFillColorCMYK(color_c, color_m, color_y, color_k)
            canvas.setStrokeColorCMYK(color_c, color_m, color_y, color_k)
            canvas.rect(x,y,x_delta,y_delta,fill=1)            
        
    canvas.setStrokeColor(black)
    canvas.setFillColor(black)    
    canvas.setFont("Helvetica", font_size)
    
    y_line = pageSize[1]*inch - margin - len(g)*y_delta - titleHeight
    canvas.line(margin,y_line,pageSize[0]*inch-margin,y_line)
    
    def getwordnum(w):
        return(w['wordnum'])
    words = sorted(wfdict['words'], key=getwordnum)

    font_size = 12
    canvas.setFont("Helvetica", font_size)    
    labels = ["Down | Verticalement", "Across | Horizontalement"]
    dis = {4:0,2:1}
    section_height = (y_line-margin)/2
    tops = [y_line,y_line-section_height]
    MAX_PER_ROW = 10
    cnts = [0,0]
    section_title_height = font_size*1.3
    for i in range(len(labels)):
        canvas.drawString(margin, tops[i]-section_title_height-font_size/2, labels[i])
        tops[i] -= font_size
    for word in words:
        cnts[dis[word['direction']]] += 1
    
    canvas.setFont("Helvetica", font_size)
    num_rows = []
    words_heights = []
    word_columns = []
    colDeltas = []
    for i in [0,1]:
        q,rem = divmod(cnts[i], MAX_PER_ROW)
        num_rows.append(q+1 if rem>0 else q)
        words_heights.append((section_height-font_size*1.2) / num_rows[i])
        word_columns.append(min(cnts[i],MAX_PER_ROW))
        colDeltas.append(width_area / word_columns[i])

    cnts = [0,0]  # Down, Across 
    msgs = ["", ""]
    
    for i in range(len(words)):
        word = words[i]
        di = 0
        if word['direction'] == 2:
            di = 1
        elif word['direction'] != 4:
            print("SERIOUS ERROR WRONG DIRECTION: %i"%(word['direction']))
        
        dmod = divmod(cnts[di], word_columns[di])
        x = margin + dmod[1]*colDeltas[di]
        y = tops[di] - section_title_height - dmod[0]*words_heights[di]
        wdef = word.get('def')
        wiml = word.get('imageloc') 
        if wdef:
            wdef = "[%i] %s | "%(cnts[di], wdef)
            # wy = y
            # for line in wrap(wdef, 10):
            #     # canvas.drawString(x, wy, line)
            #     wy -= 15
            msgs[di] += wdef
                
        elif wiml:
            ir = ImageReader(wiml)
            canvas.drawString(x, y-font_size, "%i"%word['wordnum'])
            canvas.drawImage(ir, x+font_size, y-words_heights[di], 
                             width=colDeltas[di]-font_size, 
                             height=words_heights[di], anchor='c', 
                             preserveAspectRatio=True)            
        cnts[di] += 1
        
    # for i in [0,1]:
    #     pass
    #     x
        
    
    canvas.showPage()
    canvas.save()
    
    print("Saved CrossWord in %s"%outFileName)

    