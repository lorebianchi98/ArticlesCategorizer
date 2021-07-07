from preprocessing import *

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import timeit

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from util.object_handling import saveObject, loadObject
import numpy as np

def findPerfectK(tfidf_train, tfidf_test, targetTrain, targetTest):
    """"find the best parameter k for the K-NN classifier, testing the classifier on the training set and returning the k with the best accuracy

    :param tfidf_train: scipy.sparse.csr.csr_matrix. Tfidf of the training set.
    :param tfidf_test: scipy.sparse.csr.csr_matrix. Tfidf of the test set.
    :param targetTrain: numpy.ndarray. Target array of the training set
    :param targetTest: numpy.ndarray. Target array of the test set
    :return: perfectK: int. The k with the higher accuracy
    """
    perfectK = 1
    maxAccuracy = 0
    for i in range(1, 100):
        classifier = KNeighborsClassifier(n_neighbors = i).fit(tfidf_train, targetTrain)
        predicted = classifier.predict(tfidf_test)#prediction
        accuracy=np.mean(predicted == targetTest)#accuracy extraction
        print("With " + str(i) + " neighbors accuracy of " + str(accuracy))
        if (accuracy > maxAccuracy):
            maxAccuracy = accuracy
            perfectK = i
    print ("Best k is " + str(perfectK) + " with an accuracy of " + str(maxAccuracy))
    return perfectK


start = timeit.default_timer()
categories = ['ambiente', 'attualita', 'cultura-e-spettacolo', 'economia-e-lavoro', 'mondo', 'politica', 'scienze', 'sport', 'tecnologia']

#opening the train files

train_set=load_files("./articles/train", encoding="latin1", description=None, categories=categories, load_content=True, shuffle=False, random_state=42)
test_set = load_files("./articles/test", encoding="latin1", description=None, categories=categories, load_content=True, shuffle=False, random_state=42)

train_tfidf = loadObject("train_tfidf")
test_tfidf = loadObject("test_tfidf")

#the classifiers are built using the tfidf extracted from the training set, and they are stored on files
clf_mul = MultinomialNB().fit(train_tfidf, train_set.target)
saveObject(clf_mul, "classifiers/multinomialNB_classifier")

clf_svm = SVC().fit(train_tfidf, train_set.target)
saveObject(clf_svm, "classifiers/svm_classifier")

clf_dt = DecisionTreeClassifier().fit(train_tfidf, train_set.target)
saveObject(clf_dt, "classifiers/decisionTree_classifier")

clf_rf = RandomForestClassifier().fit(train_tfidf, train_set.target)
saveObject(clf_rf, "classifiers/randomForest_classifier")

k = findPerfectK(train_tfidf, test_tfidf, train_set.target, test_set.target)
clf_kn = KNeighborsClassifier(n_neighbors = k).fit(train_tfidf, train_set.target)
saveObject(clf_kn, "classifiers/kNeighbors_classifier")

stop = timeit.default_timer()
execution_time = stop - start
print("Program Executed in "+str(execution_time)) # It returns time in seconds