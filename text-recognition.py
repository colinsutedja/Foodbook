#PHOTO OF TEXT INTO STRING
from PIL import Image
import pytesseract
import numpy as np
import cv2
import requests
import json


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
filename = 'sample_menu.jpg'
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
    if(c.isalpha() or c ==' ' or c=='\n'):
        cleantext += c
cleantext = cleantext.split('\n')

'''
#Spoonacular API cleaning menu text
SpoonUrl = 'https://api.spoonacular.com/food/detect'
SpoonKey = 'd2c7c2b8a5894cb59ac576f384ec1ec0'
text = 'I like to eat delicious tacos. Only cheeseburger with cheddar are better than that. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good, too!'
headers= {'Content-Type': 'application/json'}
data = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post("https://api.spoonacular.com/food/detect?apiKey="+SpoonKey+"&text="+text, data=json.dumps(data), headers=headers)
if(response.status_code == 200):
    print(response.json())
else:
    print(response.status_code)
'''
print("----------------")
print("RAW READ TEXT:")
print("----------------")
print(text)

print("----------------")
print("CLEANED UP TEXT:")
print("----------------")
print(cleantext)

'''
#FIND SIMILAR STRINGS
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