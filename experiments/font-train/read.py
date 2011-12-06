import mnist
import Image
import os
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave

alphabets = ['a', 'b', 'c', 'A']


# read all the training data and labels
for i in alphabets:
  
  print 'Reading char=' + str(i) + ', ord=' + str(ord(i))
  images, labels = mnist.read([ord(i)])
  
  for j in range(0, images.size[0]):
    img_matrix_1d = images[j,:]
    img_matrix = matrix(img_matrix_1d, (28,28)).trans()
    img_array = array(img_matrix)
    savePath = './raw/training/'+str(ord(i))+'/'
    if not os.path.exists(savePath):
      os.makedirs(savePath)
    imsave(savePath + str(j)+'.png', img_array)

