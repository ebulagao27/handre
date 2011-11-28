import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics

# train the digits 0
alphabets  = ['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
alphabets_ord = map(ord, alphabets)
images, labels = mnist.read(alphabets_ord)
images = array(images)
labels = array(labels).reshape(1, len(labels))[0]
n_samples = len(images)

# read the training data and labelsi
sys.stdout.write('Reading in training data and labels')
x_train = images[:n_samples/2]
y_train = labels[:n_samples/2]
sys.stdout.write(' ... Done!\n')

# read the test data and labels
sys.stdout.write('Reading in testing data and labels')
x_test = images[n_samples/2:]
y_test = labels[n_samples/2:]
sys.stdout.write(' ... Done!\n')

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
