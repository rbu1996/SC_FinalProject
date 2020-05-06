from django.shortcuts import render
from django.http import HttpResponse

import itertools
import re
from collections import Counter, defaultdict
from typing import Dict, List, NamedTuple

import numpy as np
from numpy.linalg import norm
import math
import argparse
import json

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from .datacore import alldata

class Document(NamedTuple):
    newsID: int
    title: List[str]
    author: List[str]
    content: List[str]
    link: str
    orititle: str

    def sections(self):
        return [self.title, self.author, self.content]

    def __repr__(self):
        return (f"title: {self.title}\n" +
            f"  author: {self.author}\n" +
            f"  content: {self.content}")

def read_stopwords(file):
    with open(file) as f:
        return set([x.strip() for x in f.readlines()])

def read_docs(file, key_type=0, limit=None):
    key_types = [
        ['title', 'content'],
        ['headline', 'short_description'],
    ]
    keys = key_types[key_type]
    docs = []
    
    cnt = 0
    with open(file) as f:
        for line in f:
            cnt += 1
            if limit and cnt > limit:
                break
            line = json.loads(line.strip())
            
            words_list = []
            for key in keys:
                words_list.append([ word.lower() for word in word_tokenize(line[key]) ])
            docs.append(Document(line['newsID'], words_list[0], [], words_list[1], line['link'], line['title']))
    return docs

def stem_doc(doc: Document):
    return Document(doc.newsID, *[[stemmer.stem(word) for word in sec]
        for sec in doc.sections()])

def stem_docs(docs: List[Document]):
    return [stem_doc(doc) for doc in docs]

def remove_stopwords_doc(doc: Document):
    return Document(doc.newsID, *[[word for word in sec if word not in stopwords]
        for sec in doc.sections()]+[doc.link, doc.orititle])

def remove_stopwords(docs: List[Document]):
    return [remove_stopwords_doc(doc) for doc in docs]

class TermWeights(NamedTuple):
    title: float
    author: float
    content: float

def compute_doc_freqs(docs: List[Document]):
    '''
    Computes document frequency, i.e. how many documents contain a specific word
    '''
    freq = Counter()
    for doc in docs:
        words = set()
        for sec in doc.sections():
            for word in sec:
                words.add(word)
        for word in words:
            freq[word] += 1
    return freq

def compute_tf(doc: Document, doc_freqs: Dict[str, int], weights: list, n_docs):
    vec = defaultdict(float)
    for word in doc.title:
        vec[word] += weights.title
    for word in doc.author:
        vec[word] += weights.author
    for word in doc.content:
        vec[word] += weights.content
    return dict(vec)  # convert back to a regular dict

def compute_tfidf(doc, doc_freqs, weights, n_docs):
    vec = defaultdict(float)
    tf = compute_tf(doc, doc_freqs, weights, n_docs)
    for word in tf:
        if doc_freqs[word] == 0: continue
        # vec[word] = (1 + math.log(tf[word])) * math.log(N/doc_freqs[word])
        vec[word] = tf[word] * math.log(n_docs/doc_freqs[word])
    return dict(vec)


def dictdot(x: Dict[str, float], y: Dict[str, float]):
    '''
    Computes the dot product of vectors x and y, represented as sparse dictionaries.
    '''
    keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
    return sum(x.get(key, 0) * y.get(key, 0) for key in keys)

def cosine_sim(x, y):
    '''
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    '''
    num = dictdot(x, y)
    if num == 0:
        return 0
    return num / (norm(list(x.values())) * norm(list(y.values())))

def gen_vector(docs, term, stem, removestop, term_weights):
    processed_docs = process_docs(docs, stem, removestop)

    doc_freqs = compute_doc_freqs(processed_docs)
    n_docs = len(docs)
    doc_vectors = [compute_tfidf(doc, doc_freqs, term_weights, n_docs) for doc in processed_docs]
    return doc_vectors, doc_freqs, n_docs


def prepare_data():
    X = read_docs('polls/MainData.json')
    return X

def process_docs(docs, stem, removestop):
    processed_docs = docs
    if removestop:
        processed_docs = remove_stopwords(processed_docs)
    if stem:
        processed_docs = stem_docs(processed_docs)

    return processed_docs


def search(doc_vectors, query_vec, sim):
    results_with_score = [(doc_id , sim(query_vec, doc_vec))
                    for doc_id, doc_vec in enumerate(doc_vectors)]
    results_with_score = sorted(results_with_score, key=lambda x: -x[1])
#     print(results_with_score)
#     results = [x[0] for x in results_with_score]
    return results_with_score

def search_engine(query, data_vec, doc_freq, n_docs):
    query_words = [ word.lower() for word in word_tokenize(query) ]
    query_doc = Document(-1, [], [], query_words, "", "")
    query_doc = process_docs([query_doc], False, True)[0]
    query_vec = compute_tfidf(query_doc, doc_freq, TermWeights(title=3, author=1, content=1), n_docs)
    result  = search(data_vec, query_vec, cosine_sim)
    return result
    
def similar_docs(doc_id, data_vec, doc_freq, n_docs):
    # doc = alldata[doc_id]
    # query_doc = Document(doc['newsID'], doc['title'], doc['author'], doc['content'], doc['link'], doc['title'])
    
    # query_doc = process_docs([query_doc], False, True)[0]
    # query_vec = compute_tfidf(query_doc, doc_freq, TermWeights(title=3, author=1, content=1), n_docs)
    query_vec = data_vec[doc_id]
    result  = search(data_vec, query_vec, cosine_sim)
    return result

stopwords = read_stopwords('polls/common_words')

stemmer = SnowballStemmer('english')

term = 'tfidf'
sim = 'cosine'
data = prepare_data()
data_vec, doc_freq, n_docs = gen_vector(data, term, False, True, TermWeights(title=3, author=1, content=1))

def get_query(request):
    return render(request, 'index.html')

def show_result(request):
    query = request.GET["q"]  # name="q"
    res = ""

    items = search_engine(query, data_vec, doc_freq, n_docs)
    
    docs = [alldata[items[i][0]] for i in range(10)]
    return render(request, 'results.html', {
        'docs': docs,
        'query': query
    })


def show_news(request, news_id):
    items = similar_docs(int(news_id), data_vec, doc_freq, n_docs)[1:]

    docs = [alldata[items[i][0]] for i in range(7)]
    
    return render(request, 'news.html', {
        'doc': alldata[int(news_id)],
        'sim_docs': docs
    })
