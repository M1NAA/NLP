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
# from nltk.stem.isri import ISRIStemmer
from nltk.corpus import PlaintextCorpusReader, stopwords

#nltk.download('wordnet')


# import pandas as pd


my_dict = {

    'English': 'English',
    'Arabic': 'Arabic',

}

st.title("summarization with nlp")

with st.form("form1"):
    option = st.selectbox('choose the topic you want to summarize', ('English', 'Arabic'))  # , 'tech'))

    path = 'C:/Users/mosaa/Downloads/News Articles/' + my_dict[option]
    texts = []
    for topics in PlaintextCorpusReader(path, '.*').fileids():
        file = open(path + "\\" + topics, "r", encoding="utf8")
        texts.append(file.read())

    topic = st.number_input('Enter the number of text you want to summarize from 1 to 200 :', min_value=0,
                            max_value=153, value=0, step=1)
    texts = texts[topic]

    submited = st.form_submit_button(label='summarize')
    if submited:
        if texts is not None:
            def preprocess_text(text):
                # Remove URLs and HTML tags
                text = re.sub(r'http\S+', '', text)
                text = re.sub(r'<.*?>', '', text)
                text = re.sub(r'،', '', text)
                text = text.replace("\"", "")

                # Tokenize text
                tokens = text.lower()
                tokens = text.split()

                # Remove punctuation
                exclude = set(string.punctuation) - set('.')
                tokens = [ch for ch in tokens if ch not in exclude]

                # Remove stop words
                # stop_words = stopwords.words('english')
                # filtered_tokens = [token for token in tokens if token not in stop_words]

                stop_words = stopwords.words('arabic')
                filtered_tokens = [token for token in tokens if token not in stop_words]

                # Lemmatize tokens
                lemmatizer = WordNetLemmatizer()
                lemmas = [lemmatizer.lemmatize(token) for token in filtered_tokens]

                # Join lemmas back into a single string
                preprocessed_text = ' '.join(lemmas)

                sentences_tokens = nltk.sent_tokenize(preprocessed_text)

                return lemmas, sentences_tokens


            words_tokens, sentences_tokens = preprocess_text(texts)

            word_frequencies = {}
            for word in words_tokens:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

            number_of_tokens = len(word_frequencies)
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word] / number_of_tokens)

            sentences_scores = {}
            wordsCounter = 0.0
            for sentence in sentences_tokens:
                for word in nltk.word_tokenize(sentence):
                    if word in word_frequencies.keys():
                        wordsCounter += 1;

                        if sentence not in sentences_scores.keys():
                            sentences_scores[sentence] = word_frequencies[word]
                        else:
                            sentences_scores[sentence] += word_frequencies[word]
                sentences_scores[sentence] = sentences_scores[sentence] / wordsCounter
                wordsCounter = 0

            Summary = heapq.nlargest(int(len(sentences_tokens) / 2), sentences_scores, key=sentences_scores.get)
            final_summray = []
            if len(Summary) <= 1:
                final_summray.append(' '.join(Summary))
            else:
                for text in sentences_scores.keys():
                    if text in Summary:
                        final_summray.append(text)

                final_summray = ' \n'.join(final_summray)

            st.success("the original text:-  ")
            st.text(texts)

            st.success("summarized text:- ")
            st.text(final_summray)










