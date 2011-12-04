import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics
from sklearn.cross_validation import LeaveOneOut
from sklearn.externals import joblib
import prepare_data
import scipy
from numpy import vstack
from numpy import append
import os
# train the digits 0
alphabets  = [] #'a', 'd', 'e', 'c', 'u', 's', 'o', 'f', 't']
alphabets_ord = map(ord, alphabets)
ignoreList = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
ignoreList = map(ord, ignoreList)
images, labels = mnist.read(alphabets_ord, ignoreList = ignoreList)

images = array(images)
labels = array(labels).reshape(1, len(labels))[0]

fonts = ['comicsans', 'dakota', 'showhands', 'danielbd', 'danielbk', 'dandelion' ]
for font in fonts:
  font_images, font_labels = mnist.read(alphabets_ord, './../../data/', font + '_img.idx', font + '_label.idx', ignoreList=ignoreList)
  font_images = array(font_images)
  font_labels = array(font_labels).reshape(1, len(font_labels))[0]
  
  images = vstack((images, font_images))
  labels = append(labels, font_labels)

'''
images, labels = mnist.read(alphabets_ord, './../../data/', 'comicsans_img.idx', 'comicsans_label.idx')

images = array(images)
labels = array(labels).reshape(1, len(labels))[0]
# n_samples = len(images)

images2, labels2 = mnist.read(alphabets_ord)
images2 = array(images2)
labels2 = array(labels2).reshape(1, len(labels2))[0]

images3, labels3 = mnist.read(alphabets_ord, './../../data/', 'dakota_img.idx', 'dakota_label.idx')
images3 = array(images3)
labels3 = array(labels3).reshape(1, len(labels3))[0]

images = images2
labels = labels2
'''
n_samples = len(images)

print '-------------------------------'
print 'n_samples=' + str(len(images))
print '-------------------------------'
print n_samples

# read the training data and labelsi
sys.stdout.write('Reading in training data and labels')
x_train = images[:n_samples]
y_train = labels[:n_samples]
#print y_train
sys.stdout.write(' ... Done!\n')

if not os.path.exists("./img"):
  os.makedirs("./img")

printTrain = False

if printTrain:
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
classifier = svm.SVC(C=1, kernel='linear', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=True, tol=0.001)
#classifier = svm.LinearSVC() #SVC(C=100, kernel='rbf', degree=3, gamma=1e-3, coef0=0.0, shrinking=True, probability=True, tol=0.001)

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

joblib.dump(classifier, 'classy.pkl')
