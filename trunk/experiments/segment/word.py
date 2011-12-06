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
#passed = diff(highpass(lowpassx_pixels)));

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
	#s /= len(window);

	nar.append(s);
	if (s > maxs): maxs = s;
	
#nar = y_pixels;

if (maxs == 0 ): exit();

img = Image.new("RGB", imsize, "#FFFFFF");

running = False;
divs = [];
for i in range(0, len(nar)):
	if ( nar[i]*1000/maxs < 7 ):
		if running == False: divs.append(i);
		running = True;
	else: running = False;

	for j in range(0, nar[i]*imsize[1]/maxs):
		img.putpixel((i,j), (0,0,255));

img.save("result/sawords"+sys.argv[1]+".png", "png");

last_d = 0;
linec = 0;

for d in divs:
	if ( d <= last_d ): continue;

	mi = Image.new("RGB", (d-last_d, imsize[1]), "#FFFFFF");
	for i in range(0, imsize[1]):
		for j in range(last_d, d):
			p = im.getpixel((j,i));
			mi.putpixel((j-last_d,i), p);
	
	
	mid = imsize[1]/2;
	nempty = False;
	for j in range(0, d - last_d):
		p0 = im.getpixel((j+last_d, mid))[0] < pix_thresh;
		if ( p0 ):
			nempty = True;

	for i in range(1, imsize[1] - 1):
		xsum = 0;
		for j in range(0, d - last_d):
			p0 = im.getpixel((j+last_d, i))[0] < pix_thresh;
			if ( p0 ): xsum += 1;

		if ( (xsum*100)/(d-last_d) > 70 ):
			for j in range(0, d - last_d):
				pa = im.getpixel((j+last_d, i-1))[0] < pix_thresh;
				p0 = im.getpixel((j+last_d, i))[0] < pix_thresh;
				pb = im.getpixel((j+last_d, i+1))[0] < pix_thresh;

				if ( (not pa) or (not p0) or (not pb) ):
					mi.putpixel((j,i), (255,255,255));
	


	if ( d-last_d > 10 and nempty ):
		mi.save("result/word"+sys.argv[1]+"_"+str(linec)+".png", "png");

	print "\t Word" + str(linec) + " completed!";
	linec += 1;
	
	last_d = d+2;
	for i in range(0, imsize[1]):
		im.putpixel((d, i), (255,0,0));


#im.save("result/pp.png", "png");
im.save("result/line_"+sys.argv[1]+".png", "png");

	

