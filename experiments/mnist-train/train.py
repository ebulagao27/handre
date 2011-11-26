import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics

# train the digits 0
digit = [1,2,3,4,5]

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
y_train = array(train_labels).reshape(1, len(train_labels))[0]

x_test = array(test_images)
y_test = array(test_labels).reshape(1, len(test_labels))[0]

# create classifier
classifier = svm.LinearSVC()

# train the classifier
sys.stdout.write('Training the classifier')
classifier.fit(x_train, y_train)
sys.stdout.write(' ... Done!\n')

# test the classifier
sys.stdout.write("Performing prediction on test set")
prediction = classifier.predict(x_test);
sys.stdout.write(" ... Done!\n")

# report
print 'Classification report for classifier [%s]\n%s' % (classifier, metrics.classification_report(y_test, prediction))
print 'Confusion matrix:\n%s' % (metrics.confusion_matrix(y_test, prediction))
