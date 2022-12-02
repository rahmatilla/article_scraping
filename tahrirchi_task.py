from bs4 import BeautifulSoup
import pandas as pd
import requests
import string
import re
import datetime

links = [
    'https://kun.uz/uz/news/2022/11/30/parda-ortidagi-xususiylashtirish-yirik-aktivlar-qanday-qilib-ofshor-kompaniyalarga-otib-ketmoqda',
    'https://kun.uz/uz/news/2022/12/01/ispaniya-bosh-vaziriga-bomba-solingan-maktub-yuborildi',
    'https://kun.uz/uz/news/2022/11/30/olmazorda-profilaktika-inspektori-oldirib-ketildi'
]
df = pd.DataFrame(columns=['source_url', 'access_datetime', 'content', 'word'])  # create dataframe with columns
for link in links:
    source = requests.get(link).text                                             # get web response in text format
    soup = BeautifulSoup(source, 'lxml')                                         # create beautiful soup object
    for p in soup.find_all("p"):                                                 # find all paragraph tags
        paragraph = p.get_text()                                                 # get text inside paragraph tag
        text = paragraph
        for i in ['”', '“', '–', '«', '»']:
            text = text.replace(i, "")                                # remove ['”', '“', '–', '«', '»'] symbols in text
        text = re.sub(r'[0-9]', '', text)                             # remove numbers
        for word in text.split():                                     # split text into words
            word = word.strip(string.punctuation)                     # remove other punctuations from word
            if word not in ['', 'ta']:
                df = df.append({'source_url': link, 'access_datetime': datetime.datetime.now(),
                                'content': paragraph, 'word': word}, ignore_index=True)   # add row to dataframe

df['word_count'] = pd.Series(dtype='object')                          # add new 'word_count' column to dataframe
for i in df.index:
    df['word_count'][i] = df['word'].value_counts()[df['word'][i]]    # count frequency of word

df.to_excel('dataset.xlsx')                                           # save dataframe in excel and csv format
df.to_csv('dataset.csv')
