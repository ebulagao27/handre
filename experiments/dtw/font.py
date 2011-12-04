import ImageFont, ImageDraw, ImageOps
from PIL import Image;
import struct;


def mkImage (f, s, r):
	img = Image.new("RGB", (28,28), "#FFFFFF");
	#draw = ImageDraw.Draw(image);

	minx = 100;
	miny = 100;
	maxx = 0;
	maxy = 0;
	t = Image.new('L', (100,100));
	for fontsize in range(1,9):
		font = ImageFont.truetype(f, 16+fontsize*5);
		t = Image.new('L', (500,500));
		d = ImageDraw.Draw(t);
		size = d.textsize(s, font=font);

		d.text((50,50), " "+s+" ", font=font, fill=255);

		t = t.rotate(r, expand=1);

		#xsum = 0;
		#ysum = 0;
		minx = 100000;
		miny = 100000;
		maxx = 0;
		maxy = 0;
		#pixcount = 0;
		for i in range (0,t.size[0]):
			for j in range (0, t.size[1]):
				if (t.getpixel((i,j)) > 100):
					if ( minx > i ): minx = i;
					if ( miny > j ): miny = j;
					if ( maxx < i ): maxx = i;
					if ( maxy < j ): maxy = j;

					t.putpixel((i,j), 255);

					#xsum += i;
					#ysum += j;
					#pixcount += 1;
		
		xwidth = maxx-minx;
		ywidth = maxy-miny;
#		print minx, maxx, miny, maxy
		if ( xwidth > 18 and xwidth < 28): break;
		if ( ywidth > 18 and ywidth < 28): break;
	
#	xavr = xsum / (pixcount);
#	yavr = ysum / (pixcount);

	midx = (minx + maxx)/2;
	midy = (miny + maxy)/2;

	print minx, maxx, miny, maxy, midx, midy

#	if ( pixcount == 0 ):
#		print "pixcount == 0 at ", f, s;

	#d.text((14-size[0]/2,14-size[1]/2), s, font=font, fill=255);
	#img.paste(t, (0,0,t.size[0],t.size[1]));
	img.paste(ImageOps.colorize(t,(0,0,0),(0,0,0)), (14-midx,14-midy),t);

	return img;
	#img.save("A.png", "png");
	#draw.text((10,10), "hi", font=font);

fontlist = ["dakota.ttf"];
#fontlist = ["christopher.ttf","star.ttf", "angelina.ttf", "note_this.ttf", "handsean.ttf", "harrison.ttf"];
#charlist = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
charlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
#rotatelist = [-6, -2, 0, 2]; 
rotatelist = [-16, -14, -12, -10, -8, -6, -4, -2, 0, 
									2, 4, 6, 8, 10, 12, 14, 16];

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
		print "Starting character "+ c;
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


