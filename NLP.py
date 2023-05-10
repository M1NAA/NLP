import spacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from nltk.corpus import PlaintextCorpusReader
import streamlit as st
import nltk
from urllib import request 
from bs4 import BeautifulSoup as bs
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import heapq
#from nltk.stem.isri import ISRIStemmer
from nltk.corpus import PlaintextCorpusReader ,stopwords
#import pandas as pd




st.title("summarization with nlp")


with st.form("form1"):
    
   # option = st.selectbox('choose the topic you want to summarize',('English', 'Arabic')) #, 'tech'))
    
    
    path = r"C:\Users\Support\Documents\News Articles\English"
    texts = []
    for topics in PlaintextCorpusReader(path, '.*').fileids():
        file = open(path+"\\"+topics, "r", encoding="utf8")
        texts.append(file.read())
 
    topic = st.number_input('Enter the number of text you want to summarize from 1 to 510 :', min_value=1, max_value=510, value=1, step=1)
    article_text = texts[topic]
    
    

    

    submited = st.form_submit_button(label='summarize')
    if submited:
        if article_text is not None:
            # Removing Square Brackets and Extra Spaces
            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)
            
            # Removing special characters and digits
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            
            import nltk
            nltk.download('punkt')
            nltk.download('stopwords')
            sentence_list = sentences_tokens = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', article_text)
            
            
            stopwords = nltk.corpus.stopwords.words('english')
            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
                        
                        
            #word_frequencies 
            maximum_frequncy = max(word_frequencies.values())
            
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)  
                
                
           
            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]    


            import heapq
            summary_sentences = heapq.nlargest(int(len(sentence_scores)/2), sentence_scores, key=sentence_scores.get)
            final_summray = []
            if len(summary_sentences) <= 1:
                final_summray.append(' '.join(summary_sentences))
            else:
                for text in sentence_scores.keys():
                    if text in summary_sentences:
                        final_summray.append(text)
                final_summray = ' '.join(final_summray);



            st.success("the original text:-  ")
            st.text(".\n".join(article_text.split(". ")))
           
            
            
            st.success("summarized text:- ")
            st.text(".\n".join(final_summray.split(". ")))


