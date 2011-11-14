#!/usr/bin/python

from PIL import Image;
import glob, os;
import sys;

if (len(sys.argv) < 2):
	print "Enter line*.png number!";
	exit();


im = Image.open("result/line"+sys.argv[1]+".png");
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


x_pixels = [];
for i in range(0, imsize[0]):
	pix_tot = 0;
	for j in range(0, imsize[1]):
		pix = im.getpixel((i,j));
		if ( pix[0] < pix_thresh ): pix_tot += 1;
	
	x_pixels.append(pix_tot);



passed = diff(x_pixels);
#passed = diff(highpass(lowpass(y_pixels)));

nar = [];
window = [0,0,0];
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

if (maxs == 0 ): exit();

img = Image.new("RGB", imsize, "#FFFFFF");

running = False;
divs = [];
for i in range(0, len(nar)):
	if ( nar[i]*1000/maxs < 15 ):
		if running == False: divs.append(i);
		running = True;
	else: running = False;

	for j in range(0, nar[i]*imsize[1]/maxs):
		img.putpixel((i,j), (0,0,255));

img.save("result/sawords.png", "png");

last_d = 0;
linec = 0;
for d in divs:
	mi = Image.new("RGB", (d-last_d, imsize[1]), "#FFFFFF");
	for i in range(0, imsize[1]):
		for j in range(last_d, d):
			p = im.getpixel((j,i));
			mi.putpixel((j-last_d,i), p);
	
	if ( d-last_d > 20):
		mi.save("result/word"+sys.argv[1]+"_"+str(linec)+".png", "png");
		linec += 1;
	
	last_d = d;
	for i in range(0, imsize[1]):
		im.putpixel((d, i), (255,0,0));


im.save("result/pp.png", "png");

	

