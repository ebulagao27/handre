import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics
from sklearn.cross_validation import LeaveOneOut
import prepare_data
import scipy
import os
# train the digits 0
alphabets  = ['a', 'd', 'e', 'c', 'u', 's', 'o', 'f', 't']

alphabets_ord = map(ord, alphabets)
images, labels = mnist.read(alphabets_ord, './../../data/', 'font-christopher.idx', 'label-christopher.idx')
images = array(images)
labels = array(labels).reshape(1, len(labels))[0]
n_samples = len(images)

# read the training data and labelsi
sys.stdout.write('Reading in training data and labels')
x_train = images[:n_samples]
y_train = labels[:n_samples]
#print y_train
sys.stdout.write(' ... Done!\n')

if not os.path.exists("./img"):
  os.makedirs("./img")


i=0
for data in x_train:
  scipy.misc.imsave('./img/x_train' + str(i) + '.png', data.reshape(28,28))
  i=i+1

# read the test data and labels
sys.stdout.write('Reading in testing data and labels')
#x_test = images[n_samples/2:]
#y_test = labels[n_samples/2:]
x_test, y_test = prepare_data.readCSV()
x_test = array(x_test)
y_test = array(y_test)
#print x_test
print 'x_test.size=' + str(len(x_test))
print 'y_test=' + str(y_test)
print type(y_test)
sys.stdout.write(' ... Done!\n')

i=0
for data in x_test:
  scipy.misc.imsave('./img/x_test' + str(i) + '.png', data.reshape(28,28))
  i = i +1
# create classifier
classifier = svm.SVC(C=1.0, kernel='linear', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=True, tol=0.001)

# train the classifier
sys.stdout.write('Training the classifier')
classifier.fit(x_train, y_train)
sys.stdout.write(' ... Done!\n')

# test the classifier
sys.stdout.write("Performing prediction on test set")
prediction = classifier.predict(x_test);
sys.stdout.write(" ... Done!\n")

print '--------------------------------------'
print 'actual       =' + str(map(chr,map(int,y_test)))
print 'prediction   =' + str(map(chr,map(int,prediction)))
print '--------------------------------------'

predict_prob = classifier.predict_proba(x_test)
print predict_prob

# report
print 'Classification report for classifier [%s]\n%s' % (classifier, metrics.classification_report(y_test, prediction))
print 'Confusion matrix:\n%s' % (metrics.confusion_matrix(y_test, prediction))

