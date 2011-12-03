def cropbbox(imagewidth,imageheight, thumbwidth,thumbheight):
    """ cropbbox(imagewidth,imageheight, thumbwidth,thumbheight)

        Compute a centered image crop area for making thumbnail images.
          imagewidth,imageheight are source image dimensions
          thumbwidth,thumbheight are thumbnail image dimensions

        Returns bounding box pixel coordinates of the cropping area 
        in this order (left, upper, right, and lower).
    """
    # determine scale factor
    fx = float(imagewidth)/thumbwidth
    fy = float(imageheight)/thumbheight
    f = fx if fx < fy else fy

    # calculate size of crop area
    cropheight,cropwidth = int(thumbheight*f),int(thumbwidth*f)

    # center the crop area on the source image
    dx = (imagewidth-cropwidth)/2
    dy = (imageheight-cropheight)/2

    # return bounding box of crop area
    return dx,dy, cropwidth+dx,cropheight+dy

if __name__=='__main__':

    print "==="
    bbox = cropbbox(1024,768, 128,128)
    print "cropbbox(1024,768, 128,128):", bbox

    print "==="
    bbox = cropbbox(1024,768, 128,128)
    print "cropbbox(1024,768, 128,128):", bbox

    print "==="
    bbox = cropbbox(1024,1024, 96,128)
    print "cropbbox(1024,1024, 96,128):", bbox

    print "==="
    bbox = cropbbox(1024,1024, 128,96)
    print "cropbbox(1024,1024, 128,96):", bbox