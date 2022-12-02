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
df = pd.DataFrame(columns=['source_url', 'access_datetime', 'content', 'word'])
for link in links:
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    for p in soup.find_all("p"):
        paragraph = p.get_text()
        text = paragraph
        for i in ['”', '“', '–', '«', '»']:
            text = text.replace(i, "")
        text = re.sub(r'[0-9]', '', text)
        for word in text.split():
            word = word.strip(string.punctuation)
            if word not in ['', 'ta']:
                df = df.append({'source_url': link, 'access_datetime': datetime.datetime.now(),
                                'content': paragraph, 'word': word}, ignore_index=True)

df['word_count'] = pd.Series(dtype='object')
for i in df.index:
    df['word_count'][i] = df['word'].value_counts()[df['word'][i]]

df.to_excel('dataset.xlsx')
df.to_csv('dataset.csv')