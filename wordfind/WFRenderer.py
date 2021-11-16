'''
Created on Nov 15, 2021

@author: mdl
'''
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas


def renderPDF(wfdict, outFileName=None):
    # units in points (1 point = 1/72nd inch
    pageSize = (8.5,11.0)
    if not outFileName:
        outFileName = "%s.pdf"%wfdict['title']
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


    for i in range(len(g)): # rows
        y = pageSize[1]*inch - margin - i*y_delta - titleHeight
        for j in range(len(g[i])): # cols
            x = margin + j*x_delta
            canvas.drawString(x,y,g[i][j])
    
    y_line = pageSize[1]*inch - margin - len(g)*y_delta - titleHeight
    canvas.line(margin,y_line,pageSize[0]*inch-margin,y_line)
    
    word_columns = 4
    colDelta = width_area / word_columns
    words_height = 19
    y_line -= words_height
    canvas.setFont("Helvetica", 12)
    for i in range(len(wfdict['words'])):
        word = wfdict['words'][i]
        dmod = divmod(i, word_columns)
        x = margin + dmod[1]*colDelta
        y = y_line - dmod[0]*words_height
        canvas.drawString(x,y,word['word']) 
    
    canvas.showPage()
    canvas.save()
    
    return(canvas)
    
    