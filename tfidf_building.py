from preprocessing import *

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from util.object_handling import saveObject, loadObject

start = timeit.default_timer()
categories = ['ambiente', 'attualita', 'cultura-e-spettacolo', 'economia-e-lavoro', 'mondo', 'politica', 'scienze', 'sport', 'tecnologia']

#opening the train files
train_set=load_files("./articles/train", encoding="latin1", description=None, categories=categories, load_content=True, shuffle=False, random_state=42)
#opening the test files
test_set = load_files("./articles/test", encoding="latin1", description=None, categories=categories, load_content=True, shuffle=False, random_state=42)

#converting binaries to strings
mylist=train_set.data
trainingData = decodeData(mylist)

mylist = test_set.data
testData = decodeData(mylist)

#counting the word occurrences 

count_vect = CountVectorizer(analyzer=preprocess_text, min_df = 2, max_df = 100000000)

train_counts = count_vect.fit_transform(raw_documents=trainingData)#returns a Compressed Sparse Row matrix
test_counts = count_vect.transform(testData)#tokenization and word counting

#saveObject(count_vect, "count_vect")
#saveObject(train_counts, "train_counts")
#saveObject(test_counts, "test_counts")

# TF-IDF extraction 
tfidf_transformer = TfidfTransformer()# includes calculation of TFs (frequencies) and IDF
train_tfidf = tfidf_transformer.fit_transform(train_counts)
test_tfidf = tfidf_transformer.transform(test_counts)#feature extraction
saveObject(train_tfidf, "train_tfidf")
saveObject(test_tfidf, "test_tfidf")

stop = timeit.default_timer()
execution_time = stop - start
print("Program Executed in "+str(execution_time)) # It returns time in seconds