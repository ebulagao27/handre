from PIL import Image, ImageOps;
import struct;
import math;
from numpy import *

def getCharImages(image, imageName = 'segmented'):
    
  mg = image#Image.open(imgname+".png");	
  imgname = imageName
  for y in range(0, mg.size[1]):
    for x in range(0, mg.size[0]):
      if ( mg.getpixel((x,y))[0] > 190 ): mg.putpixel((x,y), (0,0,0));
      else: mg.putpixel((x,y), (255,255,255));

  bb = mg.getbbox();
  img = mg.crop((bb[0], max(bb[1] - 2, 0), bb[2], max(bb[3] + 2, mg.size[1])));

  imw = img.size[0];
  imh = img.size[1];

  imm = [];

  for y in range(0, img.size[1]):
    imm.append([]);
    for x in range(0, img.size[0]):
      if ( img.getpixel((x,y))[0] > 190 ):
        imm[y].append(255);
      else:
        imm[y].append(0);

  dlist = [];
  running = True;
  for x in range(0, img.size[0]):
    pcount = 0;
    for y in range(0, img.size[1]):
      if ( imm[y][x] > 190 ): pcount += 1;

    if ( pcount  == 0 ):
      if ( not running ):
        running = True;
        dlist.append(x);

    else: running = False;

  if not running: dlist.append(img.size[0]);

  # print dlist

  startPixel = 0
  left = 0
  w, h = img.size
  img = ImageOps.invert(img)
  #print 'mg.size=' + str(mg.size)
  i=0
  
  imgArray = [];
  
  for point in dlist:
    right = point
    cropbox = (left, 0, point, h-1)
    #print 'cropbox='+str(cropbox)
    croppedimage = img.crop(cropbox)
    #print 'croppedimage.size=' + str(croppedimage.size)
    croppedimage.save(imgname+'_'+str(i)+'.png')
    imgArray.append(croppedimage)
    left = point+1
    i += 1
 
  return imgArray
