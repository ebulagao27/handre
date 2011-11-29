import mnist, Image, sys
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from pprint import pprint
from scipy.misc import imsave
from sklearn.metrics import classification_report, precision_score, recall_score
from sklearn.cross_validation import LeaveOneOut, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC, LinearSVC

# train the digits 0
alphabets  = ['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
alphabets_ord = map(ord, alphabets)
images, labels = mnist.read(alphabets_ord)
images = array(images)
labels = array(labels).reshape(1, len(labels))[0]
n_samples = len(images)

# read the training data and labelsi
sys.stdout.write('Reading in training data and labels')
X = images
y = labels
sys.stdout.write(' ... Done!\n')

# split the data into two equal parts respecting label proprtions
train, test = iter(StratifiedKFold(y, 2)).next()

#################################################

# set the tuning parameters
tuned_parameters = [{ 'kernel':['rbf'], 
                      'gamma' : [1e-3, 1e-4], 
                      'C' : [1, 10, 100, 1000]
                    },
                    { 'kernel':['linear'],
                      'C' : [1, 10, 100, 1000]
                    }
                    ]
scores = [
          ('precision', precision_score),
          ('recall', recall_score)
         ]

for score_name, score_func in scores:
  clf = GridSearchCV(SVC(C=1), tuned_parameters, score_func=score_func)
  clf.fit(X[train], y[train], cv=StratifiedKFold(y[train], 5))
  y_true, y_pred = y[test], clf.predict(X[test])

  print "Classification report for the best estimator: "
  print clf.best_estimator
  print "Tuned for '%s with optimal value: %0.3f" % (score_name, score_func(y_true, y_pred))
  print classification_report(y_true, y_pred)
  print "Grid scores:"
  pprint(clf.grid_scores_)
  print
  

