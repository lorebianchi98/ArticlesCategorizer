from sklearn.datasets import load_files
import timeit
from sklearn import metrics
import numpy as np

from util.object_handling import saveObject, loadObject
from preprocessing import *

def testClassifier(classifier, tfidf_test, fileName, test_set):
    """"Test the accuracy of a classifier on the test set
    
    :param classifier: Classifier. Classifier to test
    :param tfidf_test: scipy.sparse.csr.csr_matrix. The tfidf calculated from the test set
    :param fileName: str. Name of the file to save the classifier test
    :param 
    """
    print("Testing " + fileName)
    predicted = classifier.predict(tfidf_test)#prediction
    #Extracting statistics and metrics
    accuracy=np.mean(predicted == test_set.target)#accuracy extraction
    fileText = "Accuracy on test set:\n"
    fileText += str(accuracy)
    fileText += "\nMetrics per class on test set:\n"
    fileText +=  metrics.classification_report(test_set.target, predicted, target_names=test_set.target_names) #metrics extractions (precision    recall  f1-score   support)
    fileText += "\nConfusion matrix:\n"   
    labels = [ 'am', 'ac', 'c ', 'ec', 'm ', 'p ', 'sc', 'sp', 't ']
    fileText += "    am  ac c  ec m  p  sc sp t\n"
    confusion_matrix = metrics.confusion_matrix(test_set.target, predicted) 
    #for row, row_index in enumerate(confusion_matrix):
    #    fileText += label[row_index] + row    
    i = 0    
    for row in confusion_matrix:
        fileText += labels[i] + " " + str(row) + '\n'
        i += 1
    print(fileText)
    
    f = open("dumped_objects/classifier_evaluations/" + fileName + ".txt", "w")
    f.write(fileText)
    f.close()
    
    print("End of test " + fileName)

categories = ['ambiente', 'attualita', 'cultura-e-spettacolo', 'economia-e-lavoro', 'mondo', 'politica', 'scienze', 'sport', 'tecnologia']
start = timeit.default_timer()
test_set = load_files("./articles/test", encoding="latin1", description=None, categories=categories, load_content=True, shuffle=False, random_state=42)
test_tfidf = loadObject("test_tfidf")

#loading all the classifiers
clf_mul = loadObject("classifiers/multinomialNB_classifier")
clf_svm = loadObject("classifiers/svm_classifier")
clf_dt = loadObject("classifiers/decisionTree_classifier")
clf_rf = loadObject("classifiers/randomForest_classifier")
clf_kn = loadObject("classifiers/kNeighbors_classifier")


testClassifier(clf_mul, test_tfidf, "multinomialNB_classifier", test_set)
testClassifier(clf_svm, test_tfidf, "svm_classifier", test_set)
testClassifier(clf_dt, test_tfidf, "decisionTree_classifier", test_set)
testClassifier(clf_rf, test_tfidf, "randomForest_classifier", test_set)
testClassifier(clf_kn, test_tfidf, "kNeighbors_classifier", test_set)

stop = timeit.default_timer()
execution_time = stop - start
print("Program Executed in "+str(execution_time)) # It returns time in seconds