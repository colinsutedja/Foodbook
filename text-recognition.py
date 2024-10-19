#PHOTO OF TEXT INTO STRING
from PIL import Image
import pytesseract
import numpy as np
import cv2
import requests
import json


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
filename = 'pines_cropped2.jpg'
img = np.array(Image.open(filename))

'''
#Erosion
kernel = np.ones((3, 3), np.uint8) 
img_erosion = cv2.erode(img, kernel, iterations=1) 
'''

#read the img
text = pytesseract.image_to_string(img)

#Cleaning menu text
cleantext = ''
for c in text:
    if((c.isalpha() or c ==' ' or c=='\n') and not (c==',')):
        cleantext += c
cleantext = cleantext.split('\n')
cleantext = [elem.strip() for elem in cleantext]
menu_items = list(filter(lambda elem: len(elem)>3, cleantext))

print("----------------")
print("RAW READ TEXT:")
print("----------------")
print(text)

print("----------------")
print("CLEANED UP TEXT:")
print("----------------")
print(menu_items)

'''
#FIND SIMILAR STRINGS 1
import pandas as pd
import bs4 as bs
import urllib.request
import nltk
nltk.download('punkt')
import string
from gensim.models import Word2Vec

data1 = pd.read_csv('dataset/FOOD-DATA-GROUP1.csv', usecols=['food'])
data2 = pd.read_csv('dataset/FOOD-DATA-GROUP2.csv', usecols=['food'])
data3 = pd.read_csv('dataset/FOOD-DATA-GROUP3.csv', usecols=['food'])
data4 = pd.read_csv('dataset/FOOD-DATA-GROUP4.csv', usecols=['food'])
data5 = pd.read_csv('dataset/FOOD-DATA-GROUP5.csv', usecols=['food'])
food_names = pd.concat([data1, data2, data3, data4, data5], ignore_index=True)
food_names = list(food_names.get('food'))
print(food_names)
word2vec = Word2Vec(food_names, min_count=2)
print(word2vec.wv.most_similar('cream cheese'))
'''

#FIND SIMILAR STRINGS 2
from rapidfuzz import process, fuzz
import pandas as pd
data1 = pd.read_csv('dataset/FOOD-DATA-GROUP1.csv', usecols=['food'])
data2 = pd.read_csv('dataset/FOOD-DATA-GROUP2.csv', usecols=['food'])
data3 = pd.read_csv('dataset/FOOD-DATA-GROUP3.csv', usecols=['food'])
data4 = pd.read_csv('dataset/FOOD-DATA-GROUP4.csv', usecols=['food'])
data5 = pd.read_csv('dataset/FOOD-DATA-GROUP5.csv', usecols=['food'])
food_names = pd.concat([data1, data2, data3, data4, data5], ignore_index=True)
food_names = list(food_names.get('food'))

def find_best_match(menu_item, dataframe_column, n=5):
    matches = process.extract(menu_item, dataframe_column)
    matches = sorted(matches, key=lambda x: x[1])
    if max(matches, key=lambda x: x[1])[1] < 55:
        return
    top_n_matches = [tup[0] for tup in matches[-1:-n-1:-1]]
    return (menu_item, top_n_matches)
    
matched_pairs = list(filter(lambda x: x!= None,[find_best_match(item, food_names,n=3) for item in menu_items]))
matches_df = pd.DataFrame().assign(menu_item = [elem[0] for elem in matched_pairs])
matches_df = matches_df.assign(match = [elem[1] for elem in matched_pairs])


print(matches_df)
