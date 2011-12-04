import os, struct
from array import array
from cvxopt.base import matrix

def read(digits, path = "./../../data/", data="alphabets-font-images.idx", label="alphabets-font-labels.idx", ignoreList = []):
    """
    Python function for importing the MNIST data set.
    """

    fname_img = os.path.join(path, data)#'alphabets-font-images.idx')
    fname_lbl = os.path.join(path, label)#'alphabets-font-labels.idx')

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = array("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = array("B", fimg.read())
    fimg.close()

    #print '(^_^)'
    #print 'ignoreList='+str(ignoreList)
    #print ('----')
    
    ind = [ k for k in xrange(size) if ((not lbl[k] in ignoreList) and  (lbl[k] in digits or digits == [])) ]
    images =  matrix(0, (len(ind), rows*cols))
    labels = matrix(0, (len(ind), 1))
    for i in xrange(len(ind)):
        images[i, :] = img[ ind[i]*rows*cols : (ind[i]+1)*rows*cols ]
        labels[i] = lbl[ind[i]]

    return images, labels
