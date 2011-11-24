import mnist
import Image
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave

# read all the training data and labels
images, labels = mnist.read([0])

# get the first row of pixel dataq
img0_matrix_1d = images[0,:]
img0_matrix = matrix(img0_matrix_1d, (28,28))
img0_array = array(img0_matrix)

# save the image 
imsave('./raw/mnist_training_digit_4_data_0.png', img0_array)

