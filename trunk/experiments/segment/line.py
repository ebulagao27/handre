#!/usr/bin/python

from PIL import Image;
import glob, os;
import sys;

im = Image.open("zpage.png");
imsize = im.size;

pix_thresh = 210;

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

def fill_all(x,y,imx, rd):
	if ( rd > 20 ): return;
	sz = im.size;
	if (x < 0 or y < 0 or x >= sz[0] or y >= sz[1]): return;

	p = im.getpixel((x,y))[0] < pix_thresh;
	if (not p): return;
	else:
		im.putpixel((x,y), (255,255,255));
		fill_all(x, y+1, imx, rd+1);
		fill_all(x+1, y, imx, rd+1);
		fill_all(x-1, y, imx, rd+1);

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
window = [0,0,0,0,0];
wpos = 0;

maxs = 0;
for i in range(0, len(passed)):
	sq = abs(passed[i])/2;# * abs(passed[i];
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
	mi = Image.new("RGB", (imsize[0], d-last_d+7+4), "#FFFFFF");
	for i in range(0, imsize[0]):
		for j in range(max(last_d-4,last_d), d+7):
			if ( d+5 >= imsize[1] ): break;
			p = im.getpixel((i,j));

			if ( p[0] < pix_thresh):
				mi.putpixel((i, j-last_d), (0,0,0));

	misize = mi.size;	

	for y in range(0, misize[1]):
		xtot = 0;
		for x in range(0, misize[0]):
			p = mi.getpixel((x,y));
			if ( p[0] < pix_thresh ): xtot += 1;

		if ( xtot*100/misize[0] > 60 ):
			for i in range(0, misize[0]):
				if ( y <= 0 or y >= misize[1] - 1 ):
					mi.putpixel((i,y), (255,255,255));
					continue;

				pa = mi.getpixel((i,y-1));
				pb = mi.getpixel((i,y+1));
				if ( pa[0] >= pix_thresh or pb[0] >= pix_thresh):
					mi.putpixel((i,y), (255,255,255));
########################################3
	for y in range(0, misize[1]):
		xtot = 0;
		for x in range(0, misize[0]):
			p = mi.getpixel((x,y));
			if ( p[0] < pix_thresh ): xtot += 1;

		if ( xtot*100/misize[0] > 40 ):
			for i in range(0, misize[0]):
				if ( y <= 0 or y >= misize[1] - 1 ):
					mi.putpixel((i,y), (255,255,255));
					continue;

				pa = mi.getpixel((i,y-1));
				pb = mi.getpixel((i,y+1));
				if ( pa[0] >= pix_thresh or pb[0] >= pix_thresh):
					mi.putpixel((i,y), (255,255,255));
############################################
	for y in range(1, misize[1]-1):
		for x in range(1, misize[0] - 1):
			p0 = mi.getpixel((x,y))[0]<pix_thresh;
			pa = mi.getpixel((x,y-1))[0]<pix_thresh;
			pb = mi.getpixel((x,y+1))[0]<pix_thresh;
			pl = mi.getpixel((x-1,y))[0]<pix_thresh;
			pr = mi.getpixel((x+1,y))[0]<pix_thresh;
			if ( pa + pb + pl + pr < 2 ): mi.putpixel((x,y),(255,255,255));

	for x in range(0, imsize[0]):
		fill_all(x,d,im, 0);


	

	mi.save("result/line"+str(linec)+".png", "png");
	os.system("./word.py "+str(linec));
	
	print "Line " + str(linec) + " completed!";
	last_d = d;
	linec += 1;
#	for i in range(0, imsize[0]):
#		im.putpixel((i, d), (255,0,0));


img.save("result/salines.png", "png");
im.save("result/pp.png", "png");

	

