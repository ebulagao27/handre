#!/usr/bin/python

from PIL import Image;
import glob, os;
import sys;

im = Image.open("page.png");
imsize = im.size;

pix_thresh = 230;

def lowpass(ar):
	nar = [];
	for i in range(0, len(ar)):
		if ( i >= 12 ): nar.append(2 * nar[i-1] - nar[i-2] + ar[i] - 2 * ar[i-6] + ar[i - 12]);
		elif ( i >= 6 ): nar.append(2 * nar[i-1] - nar[i-2] + ar[i] - 2 * ar[i-6]);
		elif ( i >= 2 ): nar.append(2 * nar[i-1] - nar[i-2] + ar[i]);
		elif ( i >= 1 ): nar.append(2 * nar[i-1] + ar[i]);
		else: nar.append(ar[i]);
	return nar;
			
def highpass(ar):
	nar = [];
	for i in range(0, len(ar)):
		if ( i >= 32 ): nar.append(32 * ar[i-16] - (nar[i-1] + ar[i] - ar[i-32]));
		elif ( i >= 16 ): nar.append(32 * ar[i-16] - (nar[i-1] + ar[i]));
		elif ( i >= 1 ): nar.append(- (nar[i-1] + ar[i]));
		else: nar.append(- ( ar[i]));
	return nar;

def diff(ar):
	nar = [];
	for i in range(0, len(ar)-2):
		if ( i >= 2): nar.append(-ar[i-2] - 2 * ar[i-1] + 2 * ar[i+1] + ar[i + 2]);
		elif ( i >= 1): nar.append(- 2 * ar[i-1] + 2 * ar[i+1] + ar[i + 2]);
		else: nar.append(2 * ar[i+1] + ar[i + 2]);
	return nar;


y_pixels = [];
for i in range(0, imsize[1]):
	pix_tot = 0;
	for j in range(0, imsize[0]):
		pix = im.getpixel((j,i));
		if ( pix[0] < pix_thresh ): pix_tot += 1;
	
	y_pixels.append(pix_tot);

passed = diff(y_pixels);
#passed = diff(highpass(lowpass(y_pixels)));

nar = [];
window = [0,0,0,0];
wpos = 0;

maxs = 0;
for i in range(0, len(passed)):
	sq = abs(passed[i]);# * passed[i];
#	nar.append(sq);
	
	window[wpos % len(window)] = sq;
	wpos += 1;
	s = 0;
	for n in window: s += n;
	s /= len(window);

	nar.append(s);
#	print s;
	if (s > maxs): maxs = s;
	
#nar = y_pixels;

img = Image.new("RGB", imsize, "#FFFFFF");

running = False;
divs = [];
for i in range(0, len(nar)):
	if ( nar[i]*100/maxs > 50 ):
		if running == False: divs.append(i);
		running = True;
	else: running = False;

	for j in range(0, nar[i]*imsize[0]/maxs):
		img.putpixel((j,i), (0,0,255));

last_d = 0;
linec = 0;
for d in divs:
	mi = Image.new("RGB", (imsize[0], d-last_d+5), "#FFFFFF");
	for i in range(0, imsize[0]):
		for j in range(last_d, d+5):
			if ( d+5 >= imsize[1] ): break;
			p = im.getpixel((i,j));
			mi.putpixel((i, j-last_d), p);
	
	mi.save("result/line"+str(linec)+".png", "png");
	os.system("./word.py "+str(linec));
	
	last_d = d;
	linec += 1;
#	for i in range(0, imsize[0]):
#		im.putpixel((i, d), (255,0,0));


img.save("result/salines.png", "png");
im.save("result/pp.png", "png");

	

