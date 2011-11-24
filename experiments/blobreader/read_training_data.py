import mnist
import Image
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave

# read all the training data and labels

# images, labels = mnist.read([0])

# get the first row of pixel dataq
#img0_matrix_1d = images[0,:]
#img0_matrix = matrix(img0_matrix_1d, (28,28))
#img0_array = array(img0_matrix)

# save the image 
#imsave('./raw/mnist_training_digit_4_data_0.png', img0_array)

# go through all possible digits
for i in range(0,10):
  
  print 'Reading digit=' + str(i)
  images, labels = mnist.read([i])
  
  for j in range(0, images.size[0]):
    img_matrix_1d = images[j,:]
    img_matrix = matrix(img_matrix_1d, (28,28))
    img_array = array(img_matrix)
    imsave('./raw/training/'+str(i)+'/'+str(j)+'.png', img_array)

