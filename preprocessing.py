from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer

def stemmed_words(doc):
    """"Extracts the token of the word stemmed (in italian), removing the italian stop word
    
    :param doc: string. Document to tokenize and to stem
    :return: the token extracted from the text stemmed
    """
    analyzer = CountVectorizer().build_analyzer()
    return (ItalianStemmer().stem(w) for w in analyzer(doc) if w not in stopwords.words('italian'))

def clean_text(doc): 
    """"Removes the number from the text
    
    :param doc: string. Document to preprocess
    :return: doc: string. The document cleaned
    """
    doc =  re.sub(r'\d+', '', doc)
    return doc

def preprocess_text(doc):
    """"Preprocess the text 
    
    :param doc: string. Document to preprocess
    :return: The document preprocessed
    """
    doc = clean_text(doc)
    return stemmed_words(doc)

#decode the text if it is necessary
def decodeData(list):
    """"Decodes a list of texts extracted from files if necessary
    
    :param: list: list of str. List of text to decode
    :return: decodedData:list of str. List of text decoded
    """
    decodedData = []
    for item in list:
        try:
            decodedData.append(item.encode('latin1').decode('utf8'))
        except UnicodeDecodeError as e:
            decodedData.append(item)
    return decodedData
