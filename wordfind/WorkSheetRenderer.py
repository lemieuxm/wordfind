'''
Created on Jan 10, 2022

@author: mdl
'''
import random

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.para import Paragraph


# from: https://stackoverflow.com/questions/51541570/how-to-draw-a-paragraph-from-top-to-bottom-on-canvas            
def draw_centered_paragraph(canvas, msg, x, y, max_width, max_height):
    # canvas.rect(x,y-max_height, max_width, max_height)
    # Paragraph creation
    currentFontName = canvas._fontname
    currentFontSize = canvas._fontsize
    fontSize = currentFontSize
    #canvas.getAvailableFonts()
    leading = fontSize
    h = max_height + 2
    while h > max_height:
        # canvas.setFont(currentFontName, fontSize)
        message_style = ParagraphStyle('Normal', alignment=TA_CENTER, fontSize=fontSize, fontName=currentFontName, leading=leading)
        message = msg.replace('\n', '<br />')
        message = Paragraph(message, style=message_style)
        w, h = message.wrap(max_width, max_height)  # @UnusedVariable
        if h > max_height:
            fontSize -= 1
            leading -= 1
            print("Paragraph is too big, trying smaller font size: %i"%fontSize)
        else:
            message.drawOn(canvas, x, y - min(max_height, h))
    canvas.setFont(currentFontName, currentFontSize)

def renderPDF(wfdict, outFileName=None, showWord=False, showPos=False, showDef=True, showGrid=True):
    # units in points (1 point = 1/72nd inch
    pageSize = (8.5,11.0)
    if not outFileName:
        blankText = "blank" if showGrid else "match"
        outFileName = "/tmp/%s_worksheet_%s.pdf"%(wfdict['title'], blankText)
    print("Starting WorkSheetRenderer.renderPDF width=%.1f; height=%.1f"%(pageSize[0]*inch, pageSize[1]*inch))
    canvas = Canvas(outFileName, pagesize=(pageSize[0]*inch, pageSize[1]*inch))
    titleFontSize = 20
    canvas.setFont("Helvetica", titleFontSize)
    canvas.drawCentredString(pageSize[0]*inch/2, pageSize[1]*inch - inch, wfdict['title'])
    fontSize = 12
    titleHeight = titleFontSize*2+fontSize
    canvas.setFont("Helvetica", fontSize)
    margin = 0.8*inch
    width_area = pageSize[0]*inch - 2*margin
    height_area = pageSize[1]*inch - 2*margin - titleHeight
    wordWidth = width_area*0.27
    posWidth = width_area*0.19
    row_height = height_area / len(wfdict['words'])
    maxDefWidth = width_area-wordWidth-posWidth

    
    # draw lines  # canvas.line(x1,y1,x2,y2)
    ### outside box
    left = margin
    right = pageSize[0]*inch-margin
    top = pageSize[1]*inch-margin-titleHeight
    bottom = margin
    canvas.line(left, top, right, top)
    canvas.line(right, top, right, bottom)
    canvas.line(right, bottom, left, bottom)
    canvas.line(left, bottom, left, top)
    if showGrid:
        x_def = margin+wordWidth
        canvas.line(x_def, top, x_def, bottom)
        x_pos = pageSize[0]*inch-margin-posWidth
        canvas.line(x_pos, top, x_pos, bottom)
    
    cellMargin = inch / 18.0
    
    idxs = [x for x in range(len(wfdict['words']))] 
    
    y_title_row = pageSize[1]*inch - margin - titleHeight + cellMargin
    canvas.drawString(margin+cellMargin, y_title_row, "word")
    canvas.drawCentredString(((margin+wordWidth)+(pageSize[0]*inch-margin-posWidth))/2.0, y_title_row, "definition")
    canvas.drawRightString(pageSize[0]*inch-margin-cellMargin, y_title_row, "pos")
    
    if not showGrid:
        jdxs = [x for x in range(len(wfdict['words']))]
        random.shuffle(jdxs)
        kdxs = [x for x in range(len(wfdict['words']))]
        random.shuffle(kdxs)
    
    for a in range(len(idxs)):
        i = idxs[a]
        w = wfdict['words'][i]
        y = pageSize[1]*inch - margin - titleHeight - (i+0.5)*row_height - fontSize/2.0
        
        if showWord:
            usew = w
            if not showGrid:
                usew = wfdict['words'][jdxs[a]]
            x = margin+cellMargin
            canvas.drawString(x,y,usew['word'])
        
        if showDef:
            x = ((margin+wordWidth)+(pageSize[0]*inch-margin-posWidth))/2.0
            # canvas.drawCentredString(x, y, w['def'])
            x = margin+wordWidth+cellMargin
            y_def = y+fontSize+fontSize/2.0
            if len(w['word']) > 49:
                y_def += fontSize
            draw_centered_paragraph(canvas, w['def'], x, y_def, maxDefWidth-2*cellMargin, row_height-2*cellMargin)
            
        if showPos:
            usew = w
            if not showGrid:
                usew = wfdict['words'][kdxs[a]]
            x = pageSize[0]*inch - margin - cellMargin
            canvas.drawRightString(x,y,usew['pos'])
            
        if i<(len(idxs)-1) and showGrid:
            y = pageSize[1]*inch - margin - titleHeight - (i+1)*row_height
            canvas.line(left, y, right, y)
            
        print("Finished: %s"%str(w))

    canvas.showPage()
    canvas.save()
    print("Saved canvas to %s"%(outFileName))
    return(canvas)


