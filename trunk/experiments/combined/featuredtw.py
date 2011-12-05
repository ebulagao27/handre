#!/usr/bin/python

from PIL import Image, ImageOps;
import struct;
import math;
import sys;

def matprint(a):
	for i in a:
		print "";
		for j in i:
			if j > 190: print 1,
			else: print 0,

def dtw(a, b, w):
	al = len(a);
	bl = len(b);
	m = [];
	D = [];
	for ai in range(0, al):
		m.append([]);
		D.append([]);
		for bi in range(0, bl):
			diff = abs(a[ai] - b[bi]);

			m[ai].append(math.pow(diff,2));
			D[ai].append(999999999);
#			if a[ai] < b[bi]: m[ai].append(8);
#			elif a[ai] > b[bi]: m[ai].append(8);
#			else: m[ai].append(0);
			
#			if ( ai > 0 and bi > 0 and ai - bi > w ): m[ai][bi] = 999999999; 
#			if ( ai > 0 and bi > 0 and bi - ai > w ): m[ai][bi] = 999999999; 
	

#	for ai in range(0, al):
#		for bi in range(1, bl):
#			D[ai][bi] = 999999999;
	D[0][0] = m[0][0];	
	for ai in range(1, al):
		for bi in range(max(1,ai-w), min(bl,ai+w)):
			D[ai][bi] = m[ai][bi] + \
				min(
				D[ai-1][bi],D[ai][bi-1],D[ai-1][bi-1]
				);

#	print D[al-1][bl-1];
	return D[al-1][bl-1];

def scalematch(a,b):
	al = len(a);
	bl = len(b);
	vals = [];
	while True:
		sum = 0;
		al = len(a);
		bl = len(b);
		for i in range(0, max(al,bl)):
			bx = i;
			ax = i;
			if ( bl < al ): bx = i * bl / al;
			elif (bl > al ): ax = i * al / bl;
			if ( a[ax] != b[bx] ): sum += 8;
		vals.append(sum);
		if (len(a) < 20): break;

		a.pop(len(a)-1);
		a.pop(0);


		if (a[0] > 0 or a[len(a)-1] > 0 ): break;
	vals.sort();
	return vals[0];

def mddtw(a, b, fn, w):
	asy = len(a);
	bsy = len(b);
	asx = len(a[0]);
	bsx = len(b[0]);

	m = [];
	D = [];
	for ai in range(0, asy):
		m.append([]);
		D.append([]);
		for bi in range(0, bsy):
			D[ai].append(9999999999);
			if (fn == 0):
				l1 = [];
				l2 = [];
				for x in range(0,asx): l1.append(a[ai][x]);
				for x in range(0,bsx): l2.append(b[bi][x]);
				m[ai].append(dtw(l1,l2, max(8, abs(len(l1)-len(l2))+4)));


			elif (fn == 1):
				
				sum = 0;
				for x in range(0, max(asx,bsx)):
					bx = x;
					ax = x;
					if ( bsx < asx ): bx = x * bsx / asx;
					elif ( bsx > asx ): ax = x * asx / bsx;
					
					if a[ai][ax] != b[bi][bx]: 
						if b[bi][bx] > a[ai][ax]:
							sum += 8;
						else: sum += 8;

				m[ai].append(sum);
			
			elif (fn == 2):
				l1 = [];
				l2 = [];
				for x in range(0,asx): l1.append(a[ai][x]);
				for x in range(0,bsx): l2.append(b[bi][x]);
				m[ai].append(scalematch(l1,l2));


			else: m[ai].append(0);
	
#	for ai in range(1, asy):
#		m[ai][0] = 999999999;
#	for bi in range(1, bsy):
#		m[0][bi] = 999999999;

	D[0][0] = m[0][0];


	for ai in range(1, asy):
		for bi in range(max(1,ai-w), min(bsy, ai+w )):
			D[ai][bi] = m[ai][bi] + min(
			D[ai-1][bi],D[ai][bi-1],D[ai-1][bi-1]
			);
	
	#matprint(D);
	return D[asy-1][bsy-1];


xseries = [];
yseries = [];

def analyze_fontfeature(data, idx, label):
	ywidth = len(data);
	xwidth = len(data[0]);

	yserie = [];
	for y in range(0,ywidth):
		count = 0;
		running = False;
		for x in range(0,xwidth):
			if ( data[y][x] > 190 ):
				if ( running == False ):
					running = True;
					count += 1;
			else:
				running = False;

		yserie.append(count);

	xserie = [];
	for x in range(0,xwidth):
		count = 0;
		running = False;
		for y in range(0,ywidth):
			if ( data[y][x] > 190 ):
				if ( running == False ):
					running = True;
					count += 1;
			else:
				running = False;

		xserie.append(count);
#	print chr(label), xserie, yserie;
	return ( xserie, yserie );
	


#############################################################
## Load IDX files

fi = open("img.idx", "rb");
fl = open("label.idx", "rb");

if (not fi or not fl): exit();

header = [];
lheader = [];

header.append(struct.unpack(">B", fi.read(1))[0]);
header.append(struct.unpack(">B", fi.read(1))[0]);
header.append(struct.unpack(">B", fi.read(1))[0]);
header.append(struct.unpack(">B", fi.read(1))[0]);
lheader.append(struct.unpack(">B", fl.read(1))[0]);
lheader.append(struct.unpack(">B", fl.read(1))[0]);
lheader.append(struct.unpack(">B", fl.read(1))[0]);
lheader.append(struct.unpack(">B", fl.read(1))[0]);

if ( header[2] != 8 or header[3] != 3 ): exit();

header.append(struct.unpack(">I", fi.read(4))[0]);
header.append(struct.unpack(">I", fi.read(4))[0]);
header.append(struct.unpack(">I", fi.read(4))[0]);
lheader.append(struct.unpack(">I", fl.read(4))[0]);

labels = [];
da = [];
icount = header[4];
xsize = header[5];
ysize = header[6];

for id in range(0,icount):
	lb = fl.read(1);
	labels.append(struct.unpack(">B", lb)[0]);

	da.append([]);
	for x in range(0,xsize):
		da[id].append([]);
		for y in range(0,ysize):
			b = fi.read(1);
			if b == "": 
				print "?!?!?!?!";
				exit();

			p = struct.unpack(">B", b)[0];
			da[id][x].append(p);
	
	ft = analyze_fontfeature(da[id], id, labels[id]);
	
	xseries.append(ft[0]);
	yseries.append(ft[1]);
	


#############################################################
## Load Image


def getDTWList(mg, getCount = 3):

	img = mg;

	imw = img.size[0];
	imh = img.size[1];

	imm = [];

	for y in range(0, img.size[1]):
		imm.append([]);
		for x in range(0, img.size[0]):
			if ( img.getpixel((x,y))[0] < 190 ):
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

	#print dlist;

	lastd = 0;

	guessstring = [];
	charidx = 0;
	for d in dlist:
		nim1 = img.crop((lastd,0,min(d+1,img.size[0]), img.size[1]));
		nim11 = nim1.crop(ImageOps.invert(nim1.convert("RGB")).getbbox());

		nim2 = nim11;
		if (nim11.size[0] < 24  or nim11.size[1] < 24):
#			exa = (28 - max(nim11.size[0], nim11.size[1]))/2;
			exa = (28 - (nim11.size[0]+nim11.size[1])/2)/2;
			nim2 = ImageOps.expand(nim11, border=exa, fill='white');
		
		if (nim11.size[0] < 24  or nim11.size[1] < 24):
#			exa = (28 - max(nim11.size[0], nim11.size[1]))/2;
			exa = (28 - (nim11.size[0]+nim11.size[1])/2)/2;
			nim2 = ImageOps.expand(nim11, border=exa, fill='white');
		
		if (nim11.size[0] < 24  or nim11.size[1] < 24):
#			exa = (28 - max(nim11.size[0], nim11.size[1]))/2;
			exa = (28 - (nim11.size[0]+nim11.size[1])/2)/2;
			nim2 = ImageOps.expand(nim11, border=exa, fill='white');

		sm = [];
		for y in range(0,nim2.size[1]):
			sm.append([]);
			for x in range(0, nim2.size[0]):
				if (nim2.getpixel((x,y))[0] > 190):
					sm[y].append(0);
				else: 
					sm[y].append(255);

		lastd = d;

		#print nim2.size;
		#matprint (sm);
		#print "";
		
		ft = analyze_fontfeature(sm, 0,0);
		xs = ft[0];
		ys = ft[1];
		#matprint(sm);

		capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

		fl = [];
		for id in range(0, icount):
			xd = (dtw(xs, xseries[id],max(abs(len(xs)-len(xseries[id])),8))+1);
			yd = (dtw(ys,yseries[id],max(abs(len(ys)-len(yseries[id])),8))+1);
			fl.append((chr(labels[id]), id,xd+yd,xd,yd));
		fl.sort(key=lambda a: a[2]);

		#matprint(da[fl[0][1]]);
		#print xseries[fl[0][1]]
		#print xs;
		#print yseries[fl[0][1]]
		#print ys;
		#print xd, yd;
		
		maxdt1 = 0;
		maxdt2 = 0;
		maxdt3 = 0;
		el = [];
		printcount = 0;
		for i in fl:
			exist = False;
			for e in el:
				if e[0] == i[0]: 
					exist = True;
					break;

			if exist == False and not (charidx > 0 and i[0] in capitals): 
				#print i;
				dt1 = mddtw(sm, da[i[1]], 0, 8);
				dt2 = mddtw(sm, da[i[1]], 1, 8);
				dt3 = mddtw(sm, da[i[1]], 2, 8);

				if ( dt1 > maxdt1 ): maxdt1 = dt1;
				if ( dt2 > maxdt2 ): maxdt2 = dt2;
				if ( dt3 > maxdt3 ): maxdt3 = dt3;
				#print "\t"+str(mddtw(sm, da[i[1]], 0, 100)),
				#print "\t"+str(mddtw(sm, da[i[1]], 1, 100)),
				#print "\t"+str(mddtw(sm, da[i[1]], 2, 100));
				el.append((i[0], dt1, dt2, dt3));
				printcount += 1;
				if ( printcount > 15 ): break;
		

		#print "";
		nel = [];
		for e in el:
			dt1 = 1.0*e[1]/maxdt1;
			dt2 = 1.0*e[2]/maxdt2;
			dt3 = 1.0*e[3]/maxdt3;
			dtd = math.pow(dt1, 2) + math.pow(dt2, 2) + math.pow(dt3,2);
			if ( dt1 < 0.9 and dt2 < 0.9 and dt3 < 0.9 ):
				nel.append((e[0], dtd, dt1, dt2, dt3));
#				if (len(nel) == 0 ):
#					nel.append((e[0], dtd, dt1, dt2, dt3));
#				elif (len(nel) == 1):
#					if not (nel[0][1] < 1.0 and dtd > 1.5):
#						nel.append((e[0], dtd, dt1, dt2, dt3));
#					else: break;
#				else:
#					nel.append((e[0], dtd, dt1, dt2, dt3));
					
		
		nel.sort(key=lambda a: a[1]);
		
		posc = [];
		for e in nel:
			#print e;
			if ( len(posc) < getCount ):
				posc.append(e[0]);
		guessstring.append(posc);
		charidx += 1;

	return guessstring;


		


#mg = Image.open("distributed.png");	
#mg = Image.open("Gaussian.png");	
#mg = Image.open("update.png");	
#mg = Image.open("forany_.png");	
#mg = Image.open("helloworld4.png");	
#mg = Image.open("multivariate.png");	
#mg = Image.open("finitely.png");	
#mg = Image.open("Kernels.png");	
#if (len( sys.argv) > 1 ):
#	mg = Image.open(sys.argv[1]);

#res = getDTWList(mg);
#print res;

