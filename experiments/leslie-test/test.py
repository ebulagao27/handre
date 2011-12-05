import mnist, Image, sys, ImageOps
from pylab import imread, imshow, gray, mean
from numpy import array
from cvxopt import matrix
from scipy.misc import imsave
from sklearn import svm, metrics
from sklearn.cross_validation import LeaveOneOut
from sklearn.externals import joblib
import scipy
from numpy import vstack
from numpy import append
import os
import segmentword
import numpy
import math
from itertools import product

def getSVMList(image):

  # get the individual characters
  images = getSplitImageArray(image)
  #print len(images) 
  # get the classifier
  clf = joblib.load('classy.pkl')
  
  startIndex = ord('A')
  endIndex = ord('Z')

  rowTable = []
  
  for index in range(startIndex, endIndex+1):
    tuple = (chr(index), [])
    rowTable.append(tuple)
  
  startIndex = ord('a')
  endIndex = ord('z')

  for index in range(startIndex, endIndex+1):
    tuple = (chr(index), [])
    rowTable.append(tuple)

  predictions = clf.predict(images)
  # print map(chr, map(int, predictions))
  
  predictions_prob = clf.predict_log_proba(images)
  # print predictions_prob
  
  big_table = []

  for guess in predictions_prob:
    guess_table = []
    guess_table.extend(rowTable)
    
    i=0
    newRow = []
    for tp in guess_table:
      # for each tuple (<char>,<prob>)
      tp = (tp[0], guess[i])
      newRow.append((tp[0], guess[i]))
      i += 1
    
    big_table.append(newRow)
  
  return_table = []

  for row in big_table:
    candidates = []
    row.sort(key=lambda r: r[1], reverse=True)
    for i in range(2):
      candidates.append(row[i][0])
    return_table.append([candidates])

  # print return_table
  return return_table
  # print big_table[0]
  

def getSplitImageArray(image):
   
  # image array
  globalImageArray = []
  
  # counter
  i = 0

  # given the image object, we get an array of each individual character image
  characterImagesArray = segmentword.getCharImages(image)
  
  for characterImage in characterImagesArray:
    
    # change mode to RGB
    if characterImage.mode != 'RGB':
      characterImage = characterImage.convert('RGB')
   
    # make it white on black
    characterImage = ImageOps.invert(characterImage)

    # get dimensions of raw image
    width, height = characterImage.size
    
    # remove borders from image
    bbox = characterImage.getbbox()

    threshold = 1

    left = max(bbox[0]-threshold, 0)
    top = max(bbox[1]-threshold, 0)
    right = min(bbox[2]+threshold, width)
    bottom = min(bbox[3]+threshold, height)
    
    bbox = (left, top, right, bottom)
    croppedCharacterImage = characterImage.crop(bbox)
    
    # resize image  
    thumbnail = croppedCharacterImage.copy()
    thumbnail.thumbnail((28,28))
    
    # place the resized image in the middle of a 28x28 container
    thumbnail_w, thumbnail_h = thumbnail.size
    image_container = Image.new('RGB', (28,28), 'black')
    image_container.paste(thumbnail, (max(0,(28-thumbnail_w)/2),max(0,(28-thumbnail_h)/2)))
    thumbnail = image_container

    # create pixel array
    pixels = thumbnail.load()
    pixel_w, pixel_h = thumbnail.size
    pixel_array = []
    
    for y in range(pixel_h):
      for x in range(pixel_w):
        pixel = pixels[x, y]
        pixel_array.append(pixel[0])
    
    # save image array
    image_array = numpy.asarray(pixel_array).reshape((pixel_h,pixel_w))
    scipy.misc.imsave('./segmented'+str(i)+'_normalized.png', image_array)
    
    # add image_arrayi
    globalImageArray.append(array(numpy.asarray(pixel_array)))
    
    # increment counter
    i += 1
    #print 'i='+str(i)

  return globalImageArray

def getDTWList(image):
  return getSVMList(image)


def foo(*seqs):
  return (x for x in product(*seqs) if len(x) == len(set(x)))

# pick word
wordImage = Image.open("multivariate.png")

# run
svmlist = getSVMList(wordImage.copy())
dtwlist = getSVMList(wordImage.copy())

#print 'svmlist='+str(svmlist)
#print 'dtwlist='+str(dtwlist)

def permutations(list):
  orig = "";
  for cl in list:
    orig += cl[0];

  wordlist = [orig];

  print orig;
  
  for ci in range(0, len(list)):
    for word in wordlist:
      for ct in list[ci]:
        cs = word[:ci]+ct+word[ci+1:];
        if not cs in wordlist: 
          wordlist.append(cs);
          #print cs;
  return wordlist;
        
    

combined_list = []
combined_list2 = []
if len(svmlist) == len(dtwlist):
  for i in range(len(svmlist)):
    # for each char in the word
    svm_candidates = svmlist[i][0]
    dtw_candidates = dtwlist[i][0]
    
    #intersection_candidates = filter(lambda x: x in svm_candidates, dtw_candidates)[0]
    #union_candidates = svm_candidates+filter(lambda x: x not in svm_candidates, dtw_candidates)[0]
    
    
    intersection_candidates = map(chr,list(set(map(ord,svm_candidates)) & set(map(ord,dtw_candidates))))
    union_candidates = map(chr, list(set(map(ord,svm_candidates)) | set(map(ord,dtw_candidates))))
    
    if len(intersection_candidates) == 0:
      intersection_candidates = [svm_candidates[0], dtw_candidates[0]] 
    print svm_candidates

    combined_list.append(intersection_candidates)
    combined_list2.append(union_candidates)
  
  print combined_list
  print combined_list2
  possibles = permutations(combined_list);
  print len(possibles)
