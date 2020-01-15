import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from functools import reduce
import time
import os
import errno
session = requests.Session()

def loop_data(keyword,data):
    for index, row in data.iterrows():
        print(row['Website'], row[keyword])
        if '.pdf' in row[keyword]:
            if 'www.' in row[keyword]:
                scrapping_pdf(row[keyword],keyword)
            else:
                scrapping_pdf(row["Website"] + row[keyword],keyword)
        elif 'www.' in row[keyword]:
            scrapping(row[keyword],keyword)
        else:
            scrapping(row["Website"]+row[keyword],keyword)


def scrapping(website,keyword):
    try:
        html = session.get("http://" + website,timeout=3)
        soup = BeautifulSoup(html.text, "html5lib")
        body_element = soup.body
        string_body = str(body_element)
        list_script = list(body_element.find_all('script'))
        list_noscript = list(body_element.find_all('noscript'))
        list_style = list(body_element.find_all('style'))
        list_footer = list(body_element.find_all('footer'))
        list_suppression = list_script +list_noscript +list_style +list_footer

        for el in list_suppression:
            string_body =string_body.replace(str(el),"")
        soup2 = BeautifulSoup(string_body, "html5lib")
        #print((str(soup2.get_text()).strip().replace('\n',' ')))
        body_text_after = str(soup2.get_text()).strip().replace('\n\n','\n')

        folder = "Company_folder_files"
        company_name = website.replace("www.", "") \
            .replace(".com", " ") \
            .replace('.co', ' ') \
            .replace('.ca', ' ') \
            .replace('.de', ' ') \
            .replace('.it', ' ') \
            .replace('.in', '').split(" ")[0]
        name_of_file = company_name+"_"+keyword
        filename = folder+"/"+keyword+"/"+name_of_file+".txt"

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        file = open(filename, "w+")
        file.write(body_text_after)
        file.close()

    except:
        print('NAN')

def scrapping_pdf(website,keyword) :
    try:
        html = session.get("http://" + website, timeout=30)
        folder="Company_folder_files"
        #name_of_file = website.replace("/","_").replace("www.","").replace(".com"," ")
        company_name = website.replace("www.", "")\
                                .replace(".com", " ")\
                                .replace('.co',' ')\
                                .replace('.ca',' ') \
                                .replace('.de', ' ') \
                                .replace('.it', ' ') \
                                .replace('.in','').split(" ")[0]
        name_of_file = str(company_name.replace('.pdf',''))+"_"+keyword
        filename =folder+"/"+keyword+"/"+name_of_file+".pdf"


        print('\n',filename,'\n')
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


        open(filename, 'wb').write(html.content)
    except:
        print('NAN')



# Initialisation
concat_data = pd.read_csv('Web-concat_clean.csv')

'''for i in range(2, 11):
    data2 = pd.read_csv('CompaniesWebsiteKeyWordPath ' + str(i) + '.csv')
    concat_data = pd.concat([concat_data, data2])'''

# Compartimentation
concat_data.fillna("NAN", inplace=True)
concat_data['Website'] = concat_data['Website'].apply(lambda x: "www." + x if "www." not in x else x)
data_terms = concat_data[concat_data['Terms'] != "NAN"]
data_privacy = concat_data[concat_data['Privacy'] != "NAN"]
data_policy = concat_data[concat_data['Policy'] != "NAN"]
data_cookies = concat_data[concat_data['Cookies'] != "NAN"]


data_terms['Terms'] = data_terms['Terms'].apply(lambda x: x.split("//")[1] if "//" in x else x)
data_privacy['Privacy'] = data_privacy['Privacy'].apply(lambda x: x.split("//")[1] if "//" in x else x)
data_policy['Policy'] = data_policy['Policy'].apply(lambda x: x.split("//")[1] if "//" in x else x)
data_cookies['Cookies'] = data_cookies['Cookies'].apply(lambda x: x.split("//")[1] if "//" in x else x)

#data_terms['Website'] = data_terms['Website'].apply(lambda x: "www." + x if "www." not in x else x)

#loop_data('Privacy',data_privacy)
#loop_data('Terms',data_terms)
loop_data('Policy',data_policy)
loop_data('Cookies',data_cookies)
'''for index, row in data_terms.iterrows():
    print(row['Website'], row['Terms'])
    if '.pdf' in row['Terms']:
        if 'www.' in row['Terms']:
            scrapping_pdf(row['Terms'],'Terms')
        else:
            scrapping_pdf(row["Website"]+row['Terms'],'Terms')'''
    #elif 'www.' in row['Terms']:
        #scrapping(row['Terms'])
    #else:
        #scrapping(row["Website"]+row['Terms'])


