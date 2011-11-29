from sklearn import datasets
from sklearn import svm
from sklearn import cross_validation

iris = datasets.load_iris()
n_samples = iris.data.shape[0]

classifier = svm.SVC(kernel='linear')

cv = cross_validation.ShuffleSplit(n_samples, n_iterations=3, test_fraction=0.3, random_state=0)

print cross_validation.cross_val_score(classifier, iris.data, iris.target, cv=10)
