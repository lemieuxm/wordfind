'''
Created on Nov 18, 2021

@author: mdl
'''
import io
from math import ceil
import random

import PIL.Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


PAGE_SIZE = (11.0*inch, 8.5*inch)
BLANK_HEIGHT = 30
MIN_WIDTH = 60
NUM_ROWS = 2
IMAGES_PER_ROW = 9
MARGIN = inch
ROW_HEIGHT = (PAGE_SIZE[1]-MARGIN-MARGIN) / NUM_ROWS
COL_WIDTH = (PAGE_SIZE[0]-MARGIN-MARGIN) / IMAGES_PER_ROW
MAX_IMAGE_WIDTH = COL_WIDTH
MAX_IMAGE_HEIGHT = ROW_HEIGHT-BLANK_HEIGHT
IMAGE_AREA_RATIO = MAX_IMAGE_WIDTH / float(MAX_IMAGE_HEIGHT)


def layout(data):
    for dat in data:
        im_file = io.BytesIO(dat['image'])
        im = PIL.Image.open(im_file)
        dat['size'] = (im.width, im.height)
        dat['format'] = im.format
        dat['pilim'] = im  # -- only if needed
        # print("read in the image for %s."%dat['word'])
    
    walk = [i for i in range(len(data))]
    row_starts = [0 for _ in range(NUM_ROWS)]
    random.shuffle(walk)
    
    for i in walk:
        dat = data[i]
        # size = dat['size']
        cur_row = 0
        
        # if IMAGE_AREA_RATIO > size[0] / float(size[1]):
        #     # height is limiting
        #     dat['r_size'] = (IMAGE_AREA_RATIO * size[0], MAX_IMAGE_HEIGHT)
        # else:
        #     dat['r_size'] = (MAX_IMAGE_WIDTH, size[0] )

        while MARGIN+row_starts[cur_row]+MAX_IMAGE_WIDTH+MARGIN-2 > PAGE_SIZE[0]:
            cur_row += 1
        dat['r_xy'] = (MARGIN+row_starts[cur_row], PAGE_SIZE[1]-MARGIN-(cur_row*ROW_HEIGHT)-ROW_HEIGHT)
        # print("%i: %s"%(i, str(dat['r_xy'])))
        # row_starts[cur_row] += dat['r_size'][0]
        row_starts[cur_row] += MAX_IMAGE_WIDTH

    return(data)



def render(data, name, outFileName=None):
    if not outFileName:
        outFileName = "/tmp/imagerec_%s.pdf"%(name)

    canvas = Canvas(outFileName, pagesize=PAGE_SIZE)
    
    rdat = [i for i in range(len(data))]
    random.shuffle(rdat)
    for i in rdat:
        dat = data[i]
        canvas.line(dat['r_xy'][0]+5, dat['r_xy'][1], 
                    dat['r_xy'][0]+MAX_IMAGE_WIDTH-5, 
                    dat['r_xy'][1])
        ir = ImageReader(dat['pilim'])
        canvas.drawImage(ir, dat['r_xy'][0], dat['r_xy'][1]+BLANK_HEIGHT, 
                         width=MAX_IMAGE_WIDTH, height=MAX_IMAGE_HEIGHT,
                         anchor='c', preserveAspectRatio=True)
    
    canvas.drawCentredString(PAGE_SIZE[0]/2, PAGE_SIZE[1]-MARGIN+10, "%s"%(name)) # , mode, charSpace, direction, wordSpace)
    
    canvas.showPage()
    canvas.save()
    print("Saved image to %s"%outFileName)
    return(canvas)

def create_imagerec(data, name):
    global NUM_ROWS, IMAGES_PER_ROW, COL_WIDTH, MAX_IMAGE_WIDTH, IMAGE_AREA_RATIO, ROW_HEIGHT, MAX_IMAGE_HEIGHT
    while len(data)/NUM_ROWS > 6:
        NUM_ROWS += 1
    IMAGES_PER_ROW=ceil(len(data)/NUM_ROWS)
    COL_WIDTH = (PAGE_SIZE[0]-MARGIN-MARGIN) / IMAGES_PER_ROW
    MAX_IMAGE_WIDTH = COL_WIDTH
    ROW_HEIGHT = (PAGE_SIZE[1]-MARGIN-MARGIN) / NUM_ROWS
    MAX_IMAGE_HEIGHT = ROW_HEIGHT-BLANK_HEIGHT
    IMAGE_AREA_RATIO = MAX_IMAGE_WIDTH / float(MAX_IMAGE_HEIGHT)
    data = layout(data)
    render(data, name)
    print("Finished create_imagerec.")

    
    