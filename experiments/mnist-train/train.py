import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics

# train the digits 0
digit = [0]

# read the training data and labelsi
sys.stdout.write('Reading in training data and labels')
train_images, train_labels = mnist.read(digit, "training", "./../../data")
sys.stdout.write(' ... Done!\n')

# read the test data and labels
sys.stdout.write('Reading in testing data and labels')
test_images, test_labels = mnist.read(digit, "testing", "./../../data")
sys.stdout.write(' ... Done!\n')

# convert to arrays
x_train = array(train_images)
y_train = array(train_labels)

# create classifier
classifier = svm.SVC()

# train the classifier
sys.stdout.write('Training the classifier')
classifier.fit(x_train, y_train)
sys.stdout.write(' ... Done!')
