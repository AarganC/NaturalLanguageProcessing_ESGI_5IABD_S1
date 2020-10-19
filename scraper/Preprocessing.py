import time
import spacy
import os
import glob
import re
import errno
import en_core_web_sm

# nlp_en = spacy.load('en_core_web_md')
nlp_en = en_core_web_sm.load()

def openText(folder,name):
    with open(os.path.join('Company_folder_files_clean/'+folder+'/'+name+'.txt'), 'r', encoding='utf-8') as f:
        text = f.read()
        #print(text)
    return text

def open_text_from_path(path):
    with open(os.path.join(path), 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def open_all_files_in_folder(folder):
    files =[]
    for filename in glob.glob('Company_folder_files/'+folder+'/*.txt'):
        files.append(filename)
    return files

def cleaning(keywords=["Privacy","Cookies","Terms","Policy"]):
    files_with_nothing = open("files_with_nothing.txt", "w+")
    for keyword in keywords:
        files = open_all_files_in_folder(keyword)
        for file in files:
            text = open_text_from_path(file)
            text = re.sub('\n', ' ', text)
            doc = nlp_en(text)
            #key_word = ['Terms', 'terms', 'Privacy', 'privacy', 'policy', 'Policy', 'Cookies', 'Cookie', 'cookies',"Condition"]
            key_word = ["Privacy policy",
                            "Terms of Use",
                            "Terms of use",
                            "Terms and Conditions",
                            "Privacy Policy",
                            "PRIVACY POLICY",
                            "Privacy Policy",
                            "Privacy Contact",
                            "PERSONAL DATA",
                            "Privacy Notice",
                            "TERMS AND CONDITIONS",
                            "Cookie Policy",
                            "Cookies Policy",
                            "Cookie Notice",
                            "Privacy Statement",
                            "Data Privacy"]
            filename = file.replace('Company_folder_files','Company_folder_files_clean')
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            file = open(filename, "w+")
            print(filename)
            text2=''
            first_word = False
            for el in doc.sents:
                if any(word in str(el) for word in key_word):#if any(word in str(el) for word in key_word):
                    first_word = True
                if first_word:
                    text2+=str(el).replace('\n','').replace('\t','').rstrip().lstrip()
                    text2.replace('  ',' ')
                    text2+='\n'
            if(len(text2)<70):
                filename_n = filename + '\n'
                files_with_nothing.write(filename_n)
            if len(text) >0:
                print(len(text), len(text2), str(100 - round(len(text2)/len(text)*100,1))+"%")
            else:
                print(len(text), len(text2))
            file.write(text2)
            file.close()
    files_with_nothing.close()


file = openText("Terms","aib_Terms")
doc = nlp_en(file)
