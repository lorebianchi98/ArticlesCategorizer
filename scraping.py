import requests
import time
import re
import json
import math
import io
from bs4 import BeautifulSoup

categories = ['ambiente', 'attualita', 'cultura-e-spettacolo', 'economia-e-lavoro', 'mondo', 'politica', 'scienze', 'sport', 'tecnologia']

#find the link of numArticles articles for each category
def linkScraper(url, numArticles):
    """"Finds the links of numArticles articles for each category and stores them on links/links.json
    
    :param url: string. Base link of the webstite to use as starting point to scrape links
    :param numArticles: int. Number of articles to scrape for each category
    """
    urlCustom = url
    linkDictionary = {}
    numPage = math.ceil(int(numArticles / 12)) #for each page there are 12 articles, numPage will contain the number of page to explore
    lastPageArticles = numArticles - (numPage - 1) * 12
    numTotal = 0
    for category in categories:
        numScraped = 0
        linkList = []
        print("scraping category: " + category)
        for i in range(numPage):
            urlCustom = url + category + "/page/" + str(i + 1)
            print(urlCustom)
            try:
                page = requests.get(urlCustom)
            
                result = BeautifulSoup(page.text, "html.parser")
                
                h2s = result.findAll("h2", class_ = "news__title") #getting the tags which contain the links
                    
                for h2 in h2s:
                    if numScraped < numArticles:
                        a = h2.find("a")
                        link = a.attrs['href'] #getting the link from the attribute of the tag <a>
                        #print(str(numScraped) + " " + link)
                        numScraped = numScraped + 1
                        numTotal = numTotal + 1
                        linkList.append(link)
                
                print("Total scraped: " + str(numTotal) + " --- " + category + " scraped: " + str(numScraped))
            except requests.ConnectionError:
                print("Connection Error")
            time.sleep(5)
        linkDictionary[category] = linkList
    dictionarySaver(linkDictionary, "links/links.json") #saving the dictionary in json format


def getAllArticles(firstToScrape):
    """"Scrapes the articles saved in links/links.json, starting from the firstToScrape article.
        The 80% of the articles are saved on articles/train/CATEGORY folder, the 20% on articles/test/CATEGORY, in order to construct the training set and the test set
    
    :param firstToScrape: int. Number of the first article to scrape
    """
    numTotal = 0
    numTrainingArticles = (linkCounter() / len(categories)) * 0.8 #number of articles to save on the training set for each category
    print("training set count = " + str(numTrainingArticles))
    failedLinks = {}
    with open('links/links.json') as json_file:
        articlesDict = json.load(json_file)
    for category in articlesDict:
        numCategory = 0
        for link in articlesDict[category]:
            if numTotal >= firstToScrape:
                articleText = extractText(link)
                if articleText != "":
                    if (numCategory < numTrainingArticles):
                        saveArticle(articleText, numTotal, "train/" + category)
                    else:
                        saveArticle(articleText, numTotal, "test/" + category)
                #if the text of the article is empty an error occur and the link not scraped is saved on a log file
                else:
                    failedLinks[numTotal] = [category, link] #log of the articles to recover
                    print("Failed to scrape article number = " + str(numTotal) + ", category: " + category)
                    dictionarySaver(failedLinks, "log/log")
                
                time.sleep(1)
                    
            numCategory += 1
            numTotal += 1
            
    print("Scraping ended with success")


def extractText(url):
    """"Get the text from the page passed via URL, extracting text from h1, h2 and p tags
    
    :param url: string. Url of the article to scrape
    :return: totalText: string. Text of the scraped article
    """
    try:
        page = requests.get(url)
    
        result = BeautifulSoup(page.text, "html.parser")
        
        h1 = result.find("h1")
        h2s = result.findAll("h2", class_ = "")
        paragraphs = result.findAll("p", class_ = "")
            
        totalText = h1.text #inserts the title on the text
            
        i = 0
        for h2 in h2s: #inserts the subtitles in the text
            totalText = totalText + "\n" + h2.text 
            
        i = 0
        for paragraph in paragraphs: #inserts the paragraphs in the text
            if i < len(paragraphs) - 1: #the last paragraph is a meaningless footer, so it will not be added
                totalText = totalText + "\n" + paragraph.text
            i = i + 1
        
        return totalText
    except requests.ConnectionError:
        print("Connection error")
        return ""        

def dictionarySaver(dictionary, path):
    a_file = open(path, "w")
    json.dump(dictionary, a_file)
    a_file.close()
    

def linkCounter():
    """function to control if the number of link scraped is okay
    
    :return: numTotal: int. Number of links of articles saved
    """
    with open('links/links.json') as json_file:
        articlesDict = json.load(json_file)
        
    numTotal = 0
    for category in articlesDict:
        numCategory = 0
        for link in articlesDict[category]:
            numCategory += 1
            numTotal += 1
        print(category + ": " + str(numCategory))
    print("Total: " +  str(numTotal))
    return numTotal
    

def saveArticle(text, num, path):
    """function to save an article on a file in the appropriate directory
    
    :param: text: str. Text of the article
    :param: num: int. Number of the article
    :param: path: str. Dyrectory of the article
    """
    try:
        filePath = "articles/" + path + "/" + str(num)
        with io.open(filePath, "w", encoding="utf-8") as text_file:
            text_file.write(text)    
            text_file.close()
            print("Saved the article number = " + str(num) + ", directory: " + path)
    except Exception as e:
        print("Error occured saving the article number = " + str(num) + ", directory: " + path)
        print(e)

#script to extraxt the links of the articles and to scrape them
"""
base_url = 'https://www.open.online/c/'
linkScraper(base_url, 300)
getAllArticles(0)
"""