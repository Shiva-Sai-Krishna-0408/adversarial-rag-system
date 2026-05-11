from pypdf import PdfReader
import re

def clean_text(text):

    clean=[]
    temp=[]
    counter=0

    for w in text.split():
        if len(w) > 1:
            if temp:
                clean.extend(temp)
                temp.clear()
            clean.append(w)
            counter = 0
        else:
            counter += 1
            temp.append(w)
            if counter > 5:
                temp.clear()
    clean_data = ' '.join(clean)
    clean_1 = re.sub('\d+/\d+/\d+,\s\d+:\d+\s[AP]M','',clean_data)
    clean_2 = re.sub(r'https://\S+','',clean_1)
    clean_2 = clean_2.replace('Legal - iCloud - Apple','')
    clean_3 = re.sub(r'\d+/\d+','',clean_2)

    return clean_3