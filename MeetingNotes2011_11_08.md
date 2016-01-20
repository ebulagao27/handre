# Goals #
In summary, our project should aim to achieve the following:
  * Perform segmentation of a string into its individual characters
  * Perform recognization/inference of each character by using SVMs
  * Incorporate some form a `prior' in order to improve the inference
    * For example, dictionary matching of words
  * Incorporate one or more of the following extensions
    * Conditional Random Fields as a type of prior
    * Robust Learning
    * Semi-supervised Learning
    * Transductive SVMs


# Optimization Problem #
This can be generalized into the equation:

http://people.csail.mit.edu/culim/projects/machine_learning/equation.PNG

http://people.csail.mit.edu/culim/projects/machine_learning/thetak.PNG models the character.

Loss function measures how well `x' matches the model.

Equations used can be either SVM or Logisitic Regression.

SVM:

http://people.csail.mit.edu/culim/projects/machine_learning/equation2.PNG

Logistic Regression:

http://people.csail.mit.edu/culim/projects/machine_learning/equation3.PNG


# Segmentation #
Perform some form of heuristic to segment the characters in a string.
  * Fall-back strategy would be to hand-label the strings.
  * Otherwise, will be understaking **change-point detection**