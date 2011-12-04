import ImageFont, ImageDraw, ImageOps
from PIL import Image
import struct
import csv
import sys
import tools
import numpy
from numpy import array
import scipy
import os

IMAGE_LOCATION_INDEX = 0
LABEL_INDEX = 1

DEBUG_MODE = True

def readCSV():
  
  # image data
  images = [] 
  # label data
  labels = []

  # read the actual csv file
  data = csv.reader(open('../../data/leslie/data.csv', 'rb'), delimiter=' ', quotechar='|')
  
  # create tmp
  if not os.path.exists('./tmp'):
    os.makedirs('./tmp')


  i = 0
  for row in data:
    image_location = row[IMAGE_LOCATION_INDEX]
    
    sys.stdout.write('Reading: ' + image_location + ' ... ')
    image = Image.open(image_location)
    sys.stdout.write('Done!\n')
    
    if image.mode != 'RGB':
      image = image.convert('RGB')
    print image.format, image.mode
    # get the image name with the extension (.png)
    image_name = image_location[:-4]
    image = ImageOps.invert(image)
    #image.save(image_name + '.inverted.png')
    image.save('./tmp/img' + str(i) + '_inverted.png')

    width, height = image.size
    
    # remove borders
    bbox = image.getbbox()
    print bbox
    
    threshold = 3
    left = max(bbox[0]-threshold, 0) 
    top = max(bbox[1]-threshold, 0)
    right = min(bbox[2]+threshold,width)
    bottom = min(bbox[3]+threshold,height)


    #bbox2 = (bbox[0]-threshold, bbox[1]-threshold, bbox[2]+threshold,  bbox[3]+threshold)
    bbox2 = (left, top, right, bottom)
    image = image.crop(bbox2)
    print bbox2
    image.save('./tmp/img' + str(i) + '_noborder.png')
    
    thumbnail_image = image.copy()
    thumbnail_image.thumbnail((28,28))
    # thumbnail_image.save('img' + str(i) + '_thumbnail.png')
    
    w, h = thumbnail_image.size
    
    image_container = Image.new('RGB', (28,28), 'black')
    image_container.paste(thumbnail_image, (max(0,(28-w)/2),max(0,(28-h)/2)))
    thumbnail_image = image_container
    thumbnail_image.save('./tmp/img' + str(i) + '_thumbnail.png')


    width, height = image.size
    #print image.size

    # crop image
    bounds = tools.cropbbox(width, height, 28, 28)
    #print bounds

    cropped_image = image.crop(bounds)
    # cropped_image.save(image_name + '.normalized.png')
    cropped_image = cropped_image.resize((28, 28))
    cropped_image.convert('1')
    #cropped_image.save(image_name + '.normalized.png')
    cropped_image.save('./tmp/img' + str(i) + '_normalized.png')
    #print 'cropped_image.size=' + str(cropped_image.size)

    # convert to array
    #image_array = numpy.asarray(cropped_image)
    
    pixels = thumbnail_image.load() # cropped_image.load()
    w, h = thumbnail_image.size # cropped_image.size
    print w, h
    image_array = []

    for y in range(h):
      for x in range(w):
        cpixel = pixels[x, y]
        image_array.append(cpixel[0])

    #print 'image_array=' + str(image_array)
    
    np_image_array = numpy.asarray(image_array).reshape((w,h))
    scipy.misc.imsave('./tmp/np_image_array' + str(i) + '.png', np_image_array)    
    #print 'np_image_array=' + str(np_image_array)
    
    # add image to array
    
    images.append(array(numpy.asarray(image_array)))
    labels.append(int(ord(row[LABEL_INDEX])))  
    
    i = i+1
    print 'len(images)=' + str(len(images))
    print 'label=' + str(ord(row[LABEL_INDEX]))

  return images, numpy.array(labels)
images, labels = readCSV()
'''
def mkImage (f, s, r):
	img = Image.new("RGB", (28,28), "#FFFFFF");
	#draw = ImageDraw.Draw(image);

	font = ImageFont.truetype(f, 32);
	t = Image.new('L', (100,100));
	d = ImageDraw.Draw(t);
	size = d.textsize(s, font=font);

	d.text((50,55), " "+s+" ", font=font, fill=255);

	t = t.rotate(r, expand=1);

	xsum = 0;
	ysum = 0;
	minx = 100;
	miny = 100;
	maxx = 0;
	maxy = 0;
	pixcount = 0;
	for i in range (0,t.size[0]):
		for j in range (0, t.size[1]):
			if (t.getpixel((i,j)) > 200):
				if ( minx > i ): minx = i;
				if ( miny > j ): miny = j;
				if ( maxx < i ): maxx = i;
				if ( maxy < j ): maxy = j;

				t.putpixel((i,j), 255);

				xsum += i;
				ysum += j;
				pixcount += 1;
	
#	xavr = xsum / (pixcount);
#	yavr = ysum / (pixcount);

	midx = (minx + maxx)/2;
	midy = (miny + maxy)/2;

#	if ( pixcount == 0 ):
#		print "pixcount == 0 at ", f, s;

	#d.text((14-size[0]/2,14-size[1]/2), s, font=font, fill=255);
	#img.paste(t, (0,0,t.size[0],t.size[1]));
	img.paste(ImageOps.colorize(t,(0,0,0),(0,0,0)), (14-midx,14-midy),t);

	return img;
	#img.save("A.png", "png");
	#draw.text((10,10), "hi", font=font);

fontlist = ["christopher.ttf","star.ttf"];
#fontlist = ["christopher.ttf","star.ttf", "angelina.ttf", "note_this.ttf", "handsean.ttf", "harrison.ttf"];
charlist = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
rotatelist = [-6, -2, 0, 2]; 
#rotatelist = [-16, -14, -12, -10, -8, -6, -4, -2, 0, 
#									2, 4, 6, 8, 10, 12, 14, 16];

#mkImage("christopher.ttf", "H").show();

f = open("img.idx", "wb");
f.write(struct.pack(">I",2051)); #0,0,8,3
f.write(struct.pack(">I", len(charlist)*len(fontlist)*len(rotatelist) ));
f.write(struct.pack(">I", 28 ));
f.write(struct.pack(">I", 28 ));

l = open("label.idx", "wb");
l.write(struct.pack(">I",2049)); #0,0,8,1
l.write(struct.pack(">I", len(charlist)*len(fontlist)*len(rotatelist) ));

for font in fontlist:
	print "Starting font "+ font;
	for c in charlist:
		for r in rotatelist:
			img = mkImage(font,c, r);
			l.write(c);

			for y in range(0,img.size[1]):
				for x in range(0,img.size[0]):
					if ( img.getpixel((x,y))[0] < 180 ):
						f.write(struct.pack(">B", 255));
					else:
						f.write(struct.pack(">B", 0));
f.close();
l.close();
'''
