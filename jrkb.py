import re
import lxml.html
import requests
from selenium import webdriver
import collections
import pandas as pd
#import matplotlib.pyplot as plt

jobtext = ""
TAG_RE = re.compile(r'<[^>]+>')
keyword = input('Welcome to Joel\'s Resume Keyword Builder!\n\nTo find words that you could add to your resume,\nJRKB takes your keyword and searches for\nrelated words from job postings on Indeed.com.\n\nWhat keyword(s) would you like to search with?\nThis could be a job title, technology, skill, etc: ')
html  = requests.get('https://www.indeed.com/jobs?as_and='+ keyword + '&as_phr&as_any&as_not&as_ttl&as_cmp&jt=all&st&as_src&salary&radius=25&l&fromage=any&limit=50&sort&psf=advsrch&from=advancedsearch&advn=8750053495747110li')
doc = lxml.html.fromstring(html.content)
urls = doc.xpath("//a[contains(@class, 'jobtitle')]/@href")
print("Okay, now we're going to use the web browser.")
#print('Links:', (urls))
browser = webdriver.Chrome()
for i in urls:
    urlparttwo = str(i)
    url = 'https://www.indeed.com' + urlparttwo
    browser.get(url)
    innerHTML = browser.execute_script('return document.querySelector("#jobDescriptionText").innerHTML')
    jobtext = jobtext + TAG_RE.sub('', innerHTML)
browser.quit()
#print(jobtext)
a = jobtext
# using code from https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
# Stopwords
stopwords = set(line.strip() for line in open('stopwords.txt'))
stopwords = stopwords.union(set(['mr','mrs','one','two','said']))
# Instantiate a dictionary, and for every word in the file, 
# Add to the dictionary if it doesn't exist. If it does, increase the count.
wordcount = {}
# To eliminate duplicates, remember to split by punctuation, and use case demiliters.
for word in a.lower().split():
    word = word.replace(".","")
    word = word.replace(",","")
    word = word.replace(":","")
    word = word.replace("\"","")
    word = word.replace("!","")
    word = word.replace("â€œ","")
    word = word.replace("â€˜","")
    word = word.replace("*","")
    if word not in stopwords:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
# Print most common word
n_print = int(input("How many related words would you like to see (type a number): "))
print("\nOK.\n".format(n_print))
word_counter = collections.Counter(wordcount)
for word, count in word_counter.most_common(n_print):
    print(word, ": ", count)
# Close the file

# Create a data frame of the most common words 
# Draw a bar chart
lst = word_counter.most_common(n_print)
#df = pd.DataFrame(lst, columns = ['Word', 'Count'])
#df.plot.bar(x='Word',y='Count')